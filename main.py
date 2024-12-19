import threading
import pygame
from kivy.app import App
from kivy.uix.screenmanager import Screen, ScreenManager
from kivy.properties import StringProperty, NumericProperty
from kivy.lang import Builder
from kivy.clock import Clock
import random
from kivy.core.audio import SoundLoader
from kivy.animation import Animation
from kivy.core.window import Window
from kivy.properties import BooleanProperty
Window.size = (360, 640)

# Load the KV file
Builder.load_file('tebakgambar.kv')

# Initialize Pygame Mixer
pygame.mixer.init()

# Load sounds
CORRECT_SOUND = "assets/sounds/benar.mp3"
WRONG_SOUND = "assets/sounds/salah.mp3"
VICTORY_SOUND = "assets/sounds/victory.mp3"  # Suara kemenangan
GAME_OVER_SOUND = "assets/sounds/gameover.mp3"  # Suara game over
OPENING_SOUND = "assets/sounds/opening.mp3"  # Suara opening

questions = [
    {"image": "images/Indonesia.png", "answer": "Indonesia", "choices": ["Indonesia", "Malaysia", "Thailand", "Singapore"]},
    {"image": "images/Jepang.png", "answer": "Jepang", "choices": ["Vietnam", "Filiphina", "Thailand", "Jepang"]},
    {"image": "images/Australia.png", "answer": "Australia", "choices": ["Australia", "Haiti", "Afrika", "Inggris"]},
    {"image": "images/Jerman.png", "answer": "Jerman", "choices": ["Jerman", "Jamaika", "Sudan", "India"]},
    {"image": "images/Argentina.png", "answer": "Argentina", "choices": ["Spain", "Argentina", "Peru", "Kroasia"]},
    {"image": "images/Amerika.png", "answer": "Amerika", "choices": ["Brazil", "Belanda", "Amerika", "United States"]},
    {"image": "images/Korea Utara.png", "answer": "Korea Utara", "choices": ["Singapura", "Indonesia", "Korea Utara", "Malaysia"]},
    {"image": "images/Korea Selatan.png", "answer": "Korea Selatan", "choices": ["Timor Leste", "Palestina", "Malaysia", "Korea Selatan"]},
    {"image": "images/Portugal.png", "answer": "Portugal", "choices": ["Jerman", "Spanyol", "Inggris", "Portugal"]},
    {"image": "images/Belanda.png", "answer": "Belanda", "choices": ["Qatar", "Belanda", "China", "Malaysia"]},
    {"image": "images/Saudi Arabia.png", "answer": "Saudi Arabia", "choices": ["Indonesia", "Malaysia", "Saudi Arabia", "Singapore"]},
]

class LoginScreen(Screen):
    is_sign_up = BooleanProperty(False)  # Declare the 'is_sign_up' as a BooleanProperty

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def toggle_sign_up(self):
        """Switch between login and sign-up forms."""
        self.is_sign_up = not self.is_sign_up
        self.ids.login_error.text = ""
        self.ids.username.text = ""
        self.ids.password.text = ""
        self.ids.confirm_password.text = ""  # Clear confirm password
        if self.is_sign_up:
            self.ids.submit_button.text = "Sign Up"
            self.ids.switch_button.text = "Already have an account? Log in"
        else:
            self.ids.submit_button.text = "Login"
            self.ids.switch_button.text = "Don't have an account? Sign up"

    def submit(self):
        """Handle login or sign-up based on the form mode."""
        username_input = self.ids.username.text
        password_input = self.ids.password.text
        if self.is_sign_up:
            # Check if passwords match for sign-up
            confirm_password_input = self.ids.confirm_password.text
            if password_input == confirm_password_input:
                # Proceed with sign-up (mock example)
                self.manager.current = 'start'  # Transition to the start screen after successful registration
            else:
                self.ids.login_error.text = "Passwords do not match."
        else:
            # Login validation (hardcoded for testing)
            if username_input == "admin" and password_input == "1234":
                self.manager.current = 'start'  # Transition to the start screen after successful login
            else:
                self.ids.login_error.text = "Invalid Username or Password"
    
    def clear_error(self):
        self.ids.login_error.text = ""

class StartScreen(Screen):
    def on_enter(self):
        self.play_opening_sound()

    def start_game(self):
        self.manager.current = 'game'
        self.manager.get_screen('game').start_timer()

    def play_opening_sound(self):
        pygame.mixer.music.load(OPENING_SOUND)
        pygame.mixer.music.play(-1)

    def stop_opening_sound(self):
        pygame.mixer.music.stop()
class GameWidget(Screen):
    image_source = StringProperty("")
    timer = NumericProperty(0)

    def __init__(self, **kwargs):
        super(GameWidget, self).__init__(**kwargs)
        self.score = 0
        self.question_count = 0
        self.current_question = None
        self.timer_event = None
        self.load_question()

    def start_timer(self):
        self.timer = 0
        if self.timer_event:
            self.timer_event.cancel()
        self.timer_event = Clock.schedule_interval(self.update_timer, 1)

    def update_timer(self, dt):
        self.timer += 1
        self.ids.timer_label.text = f"Time: {self.timer}s"

    def load_question(self):
        if self.question_count >= 10:
            self.end_game()
        else:
            self.current_question = random.choice(questions)
            self.image_source = self.current_question["image"]
            self.ids.score_label.text = f"Your Score: {self.score}"
            self.ids.answer_label.text = ""
            choices = self.current_question["choices"]
            random.shuffle(choices)
            self.ids.choice1.text = choices[0]
            self.ids.choice2.text = choices[1]
            self.ids.choice3.text = choices[2]
            self.ids.choice4.text = choices[3]

    def check_answer(self, answer):
        if answer == self.current_question["answer"]:
            self.score += 1
            message = "Benar!"
            self.play_sound(CORRECT_SOUND)
        else:
            message = "Salah!"
            self.play_sound(WRONG_SOUND)

        self.question_count += 1
        self.ids.answer_label.text = message
        self.ids.score_label.text = f"Your Score: {self.score}"
        self.load_question()

    def play_sound(self, sound_path):
        sound = pygame.mixer.Sound(sound_path)
        sound.play()

    def end_game(self):
        if self.timer_event:
            self.timer_event.cancel()
        self.manager.get_screen('result').ids.final_score_label.text = f"Your Final Score: {self.score}"
        self.manager.get_screen('result').ids.time_label.text = f"Time Taken: {self.timer} seconds"
        self.play_end_game_sound()
        self.manager.current = 'result'

    def play_end_game_sound(self):
        result_label = self.manager.get_screen('result').ids.result_label
        if self.score > 7:
            result_label.text = "Victory!"
            self.play_sound(VICTORY_SOUND)
            self.animate_victory(result_label)
        else:
            result_label.text = "Game Over!"
            self.play_sound(GAME_OVER_SOUND)
            self.animate_game_over(result_label)

    def animate_victory(self, result_label):
        initial_font_size = result_label.font_size
        anim = Animation(color=(1, 0.5, 0, 1), font_size=initial_font_size * 1.5, duration=1)
        anim += Animation(font_size=initial_font_size, duration=0.5)
        anim.repeat = True
        anim.start(result_label)

    def animate_game_over(self, result_label):
        initial_font_size = result_label.font_size
        anim = Animation(color=(1, 0, 0, 1), font_size=initial_font_size * 1.5, duration=1)
        anim += Animation(font_size=initial_font_size, duration=0.5)
        anim.repeat = True
        anim.start(result_label)

class ResultScreen(Screen):
    def display_result(self, score):
        result_label = self.ids.result_label
        final_score_label = self.ids.final_score_label

        if score > 7:
            result_label.text = "Victory!"
            self.play_sound(VICTORY_SOUND)
        else:
            result_label.text = "Game Over"
            self.play_sound(GAME_OVER_SOUND)

        final_score_label.text = f"Your Final Score: {score}"

    def play_sound(self, sound_file):
        pygame.mixer.music.load(f"assets/sounds/{sound_file}")
        pygame.mixer.music.play(0, 0.0)

    def reset_game(self):
        self.manager.get_screen('game').score = 0
        self.manager.get_screen('game').question_count = 0
        self.manager.get_screen('game').load_question()

class TebakGambarApp(App):
    def build(self):
        sm = ScreenManager()
        sm.add_widget(LoginScreen(name='login'))
        sm.add_widget(StartScreen(name='start'))
        sm.add_widget(GameWidget(name='game'))
        sm.add_widget(ResultScreen(name='result'))
        return sm

if __name__ == '__main__':
    TebakGambarApp().run()