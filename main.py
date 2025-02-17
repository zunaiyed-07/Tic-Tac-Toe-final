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
        Window.fullscreen = 'auto'  # Enable full-screen mode on all devices
        self.current_player = 'X'
        self.board = [['' for _ in range(3)] for _ in range(3)]
        self.vs_computer = False  # Default mode: Player vs Player
        self.difficulty = 'Easy'  # Default difficulty: Easy
        
        self.layout = BoxLayout(orientation='vertical', padding=20, spacing=10)
        self.grid = GridLayout(cols=3, spacing=10)
        self.status_label = Label(text=f"Player {self.current_player}'s turn", font_size=18, bold=True, size_hint=(1, 0.1))
        
        self.buttons = [[self.create_button() for _ in range(3)] for _ in range(3)]
        
        for row in self.buttons:
            for button in row:
                self.grid.add_widget(button)
        
        self.reset_button = Button(text='New Game', font_size=20, size_hint=(1, 0.15), background_color=(0, 1, 0, 1))
        self.reset_button.bind(on_press=self.reset_game)
        
        self.mode_button = Button(text='Play vs Computer', font_size=20, size_hint=(1, 0.15), background_color=(0, 0, 1, 1))
        self.mode_button.bind(on_press=self.toggle_mode)
        
        # Add difficulty button
        self.difficulty_button = Button(text=f'Difficulty: {self.difficulty}', font_size=20, size_hint=(1, 0.15), background_color=(0, 1, 1, 1))
        self.difficulty_button.bind(on_press=self.toggle_difficulty)
        
        self.developer_label = Label(text='Developed by Zunaiyed', font_size=14, size_hint=(1, 0.05), bold=True, color=(1, 1, 1, 0.7))
        
        self.layout.add_widget(self.developer_label)
        self.layout.add_widget(self.status_label)
        self.layout.add_widget(self.grid)
        self.layout.add_widget(self.mode_button)
        self.layout.add_widget(self.difficulty_button)  # Add difficulty button here
        self.layout.add_widget(self.reset_button)
        
        return self.layout
    
    def create_button(self):
        button = Button(font_size=32, background_color=(0.2, 0.2, 0.2, 1),
                        color=(1, 1, 1, 1), size_hint=(1, 1),
                        background_normal='', bold=True)
        button.bind(on_press=self.make_move)
        return button
    
    def make_move(self, button):
        for i in range(3):
            for j in range(3):
                if self.buttons[i][j] == button and self.board[i][j] == '':
                    self.board[i][j] = self.current_player
                    button.text = self.current_player
                    button.background_color = (1, 0, 0, 1) if self.current_player == 'X' else (0, 0, 1, 1)
                    
                    # Add animation when a button is clicked
                    anim = Animation(size_hint=(1.1, 1.1), duration=0.1) + Animation(size_hint=(1, 1), duration=0.1)
                    anim.start(button)
                    
                    if self.check_winner(self.current_player):
                        self.highlight_winner()
                        self.status_label.text = f'Player {self.current_player} Wins!'
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
    
    def toggle_difficulty(self, instance):
        if self.difficulty == 'Easy':
            self.difficulty = 'Hard'
        else:
            self.difficulty = 'Easy'
        self.difficulty_button.text = f'Difficulty: {self.difficulty}'
        self.reset_game(None)  # Reset game after changing difficulty

    def computer_move(self):
        if self.difficulty == 'Easy':
            self.easy_computer_move()
        else:
            self.hard_computer_move()

    def easy_computer_move(self):
        empty_cells = [(i, j) for i in range(3) for j in range(3) if self.board[i][j] == '']
        if empty_cells:
            i, j = random.choice(empty_cells)  # Random move
            self.make_move(self.buttons[i][j])

    def hard_computer_move(self):
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
        
        if best_move:
            i, j = best_move
            self.make_move(self.buttons[i][j])
    
    def minimax(self, board, depth, is_maximizing):
        if self.check_winner('O'):
            return 10 - depth
        if self.check_winner('X'):
            return depth - 10
        if all(all(cell != '' for cell in row) for row in board):
            return 0
        
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
    
    def reset_game(self, instance):
        self.current_player = 'X'
        self.board = [['' for _ in range(3)] for _ in range(3)]
        self.status_label.text = f"Player {self.current_player}'s turn"
        
        for i in range(3):
            for j in range(3):
                self.buttons[i][j].text = ''
                self.buttons[i][j].background_color = (0.2, 0.2, 0.2, 1)
    
    def toggle_mode(self, instance):
        self.vs_computer = not self.vs_computer
        mode_text = 'Play vs Human' if self.vs_computer else 'Play vs Computer'
        self.mode_button.text = mode_text
        self.reset_game(None)

    def highlight_winner(self):
        # Check the winning combination and highlight it
        for i in range(3):
            # Check rows
            if self.board[i][0] == self.board[i][1] == self.board[i][2] != '':
                self.buttons[i][0].background_color = (0, 1, 0, 1)
                self.buttons[i][1].background_color = (0, 1, 0, 1)
                self.buttons[i][2].background_color = (0, 1, 0, 1)
            # Check columns
            if self.board[0][i] == self.board[1][i] == self.board[2][i] != '':
                self.buttons[0][i].background_color = (0, 1, 0, 1)
                self.buttons[1][i].background_color = (0, 1, 0, 1)
                self.buttons[2][i].background_color = (0, 1, 0, 1)
        # Check diagonals
        if self.board[0][0] == self.board[1][1] == self.board[2][2] != '':
            self.buttons[0][0].background_color = (0, 1, 0, 1)
            self.buttons[1][1].background_color = (0, 1, 0, 1)
            self.buttons[2][2].background_color = (0, 1, 0, 1)
        if self.board[0][2] == self.board[1][1] == self.board[2][0] != '':
            self.buttons[0][2].background_color = (0, 1, 0, 1)
            self.buttons[1][1].background_color = (0, 1, 0, 1)
            self.buttons[2][0].background_color = (0, 1, 0, 1)

if __name__ == '__main__':
    TicTacToe().run()
