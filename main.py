from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout
from kivy.core.window import Window
from kivy.animation import Animation
import random

class TicTacToe(App):
    def build(self):
        Window.fullscreen = 'auto'
        self.current_player = 'X'
        self.board = [['' for _ in range(3)] for _ in range(3)]
        self.vs_computer = False  # Initially, it's player vs player
        self.difficulty = 'Easy'  # Default difficulty is Easy
        
        self.layout = BoxLayout(orientation='vertical', padding=30, spacing=20)
        self.grid = GridLayout(cols=3, spacing=20)
        self.status_label = Label(text=f"Player {self.current_player}'s turn", font_size=32, bold=True, size_hint=(1, 0.15), color=(1,1,1,1))
        
        self.buttons = [[self.create_button() for _ in range(3)] for _ in range(3)]
        
        for row in self.buttons:
            for button in row:
                self.grid.add_widget(button)
        
        self.reset_button = Button(text='New Game', font_size=32, size_hint=(1, 0.2), background_color=(0, 0.8, 0, 1), bold=True)
        self.reset_button.bind(on_press=self.reset_game)
        
        self.mode_button = Button(text='Play vs Computer', font_size=32, size_hint=(1, 0.2), background_color=(0, 0, 1, 1), bold=True)
        self.mode_button.bind(on_press=self.toggle_mode)
        
        self.difficulty_button = Button(text=f'Difficulty: {self.difficulty}', font_size=32, size_hint=(1, 0.2), background_color=(0, 1, 1, 1), bold=True)
        self.difficulty_button.bind(on_press=self.toggle_difficulty)
        
        self.developer_label = Label(text='Developed by Zunaiyed', font_size=20, size_hint=(1, 0.07), bold=True, color=(1, 1, 1, 0.7))
        
        self.layout.add_widget(self.developer_label)
        self.layout.add_widget(self.status_label)
        self.layout.add_widget(self.grid)
        self.layout.add_widget(self.mode_button)
        self.layout.add_widget(self.difficulty_button)
        self.layout.add_widget(self.reset_button)
        
        return self.layout
    
    def create_button(self):
        button = Button(font_size=52, background_color=(0.3, 0.3, 0.3, 1),
                        color=(1, 1, 1, 1), size_hint=(1, 1),
                        background_normal='', bold=True)
        button.bind(on_press=self.make_move)
        return button

    def make_move(self, instance):
        if self.vs_computer and self.current_player == 'O':
            return  # If it's computer's turn, don't let the player move.

        # Check if the game is already over
        if self.check_winner('X') or self.check_winner('O') or all(all(cell != '' for cell in row) for row in self.board):
            return  # Do nothing if the game has ended
        
        for i in range(3):
            for j in range(3):
                if self.buttons[i][j] == instance and self.board[i][j] == '':
                    self.board[i][j] = self.current_player
                    instance.text = self.current_player
                    instance.background_color = (1, 0.2, 0.2, 1) if self.current_player == 'X' else (0.2, 0.2, 1, 1)

                    anim = Animation(size_hint=(1.15, 1.15), duration=0.1) + Animation(size_hint=(1, 1), duration=0.1)
                    anim.start(instance)

                    if self.check_winner(self.current_player):
                        self.status_label.text = f'Player {self.current_player} Wins!'
                        self.highlight_winner(self.current_player)
                        return
                    elif all(all(cell != '' for cell in row) for row in self.board):
                        self.status_label.text = 'It\'s a Draw!'
                        return
                    else:
                        self.current_player = 'O' if self.current_player == 'X' else 'X'
                        self.status_label.text = f"Player {self.current_player}'s turn"
                        
                        if self.vs_computer and self.current_player == 'O':
                            self.computer_move()
                    return

    def toggle_mode(self, instance):
        self.vs_computer = not self.vs_computer
        if self.vs_computer:
            self.mode_button.text = 'Play vs Player'
            self.status_label.text = "Player X's turn"
            self.difficulty_button.disabled = False  # Enable difficulty button when playing against the computer
        else:
            self.mode_button.text = 'Play vs Computer'
            self.status_label.text = "Player X's turn"
            self.difficulty_button.disabled = True  # Disable difficulty button when playing against human

    def toggle_difficulty(self, instance):
        if self.vs_computer:
            self.difficulty = 'Hard' if self.difficulty == 'Easy' else 'Easy'
            self.difficulty_button.text = f'Difficulty: {self.difficulty}'

    def computer_move(self):
        if self.difficulty == 'Easy':
            empty_cells = [(i, j) for i in range(3) for j in range(3) if self.board[i][j] == '']
            if empty_cells:
                i, j = random.choice(empty_cells)  # Random move for Easy difficulty
                self.board[i][j] = 'O'
                self.buttons[i][j].text = 'O'
                self.buttons[i][j].background_color = (0.2, 0.2, 1, 1)
        else:
            self.minimax_computer_move()

        if self.check_winner('O'):
            self.status_label.text = 'Computer Wins!'
            self.highlight_winner('O')
            return
        elif all(all(cell != '' for cell in row) for row in self.board):
            self.status_label.text = 'It\'s a Draw!'
            return
        else:
            self.current_player = 'X'
            self.status_label.text = "Player X's turn"

    def minimax_computer_move(self):
        best_score = float('-inf')
        best_move = None
        
        for i in range(3):
            for j in range(3):
                if self.board[i][j] == '':
                    self.board[i][j] = 'O'
                    score = self.minimax(self.board, 0, False)
                    self.board[i][j] = ''
                    if score > best_score:
                        best_score = score
                        best_move = (i, j)

        i, j = best_move
        self.board[i][j] = 'O'
        self.buttons[i][j].text = 'O'
        self.buttons[i][j].background_color = (0.2, 0.2, 1, 1)

    def minimax(self, board, depth, is_maximizing):
        if self.check_winner('O'):
            return 1  # Computer wins
        elif self.check_winner('X'):
            return -1  # Player wins
        elif all(all(cell != '' for cell in row) for row in board):
            return 0  # Draw

        if is_maximizing:
            best_score = float('-inf')
            for i in range(3):
                for j in range(3):
                    if board[i][j] == '':
                        board[i][j] = 'O'
                        score = self.minimax(board, depth + 1, False)
                        board[i][j] = ''
                        best_score = max(score, best_score)
            return best_score
        else:
            best_score = float('inf')
            for i in range(3):
                for j in range(3):
                    if board[i][j] == '':
                        board[i][j] = 'X'
                        score = self.minimax(board, depth + 1, True)
                        board[i][j] = ''
                        best_score = min(score, best_score)
            return best_score

    def check_winner(self, player):
        for row in self.board:
            if all(cell == player for cell in row):
                return True
        for col in range(3):
            if all(self.board[row][col] == player for row in range(3)):
                return True
        if all(self.board[i][i] == player for i in range(3)) or all(self.board[i][2 - i] == player for i in range(3)):
            return True
        return False

    def highlight_winner(self, player):
        # Highlight winning cells with green
        for i in range(3):
            for j in range(3):
                if self.board[i][j] == player:
                    self.buttons[i][j].background_color = (0, 1, 0, 1)

    def reset_game(self, instance):
        self.current_player = 'X'
        self.board = [['' for _ in range(3)] for _ in range(3)]
        self.status_label.text = f"Player {self.current_player}'s turn"
        
        for i in range(3):
            for j in range(3):
                self.buttons[i][j].text = ''
                self.buttons[i][j].background_color = (0.3, 0.3, 0.3, 1)

if __name__ == '__main__':
    TicTacToe().run()
