import pygame
from kivy.app import App
from kivy.uix.screenmanager import Screen, ScreenManager
from kivy.properties import StringProperty, NumericProperty, BooleanProperty
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
VICTORY_SOUND = "assets/sounds/victory.mp3"
GAME_OVER_SOUND = "assets/sounds/gameover.mp3"
OPENING_SOUND = "assets/sounds/opening.mp3"

# Questions categorized by level
questions = {
    "asia": [
        {"image": "images/Indonesia.png", "answer": "Indonesia", "choices": ["Indonesia", "Malaysia", "Thailand", "Singapore"]},
        {"image": "images/Jepang.png", "answer": "Jepang", "choices": ["Vietnam", "Filiphina", "Thailand", "Jepang"]},
        {"image": "images/Korea Selatan.png", "answer": "Korea Selatan", "choices": ["Timor Leste", "Palestina", "Malaysia", "Korea Selatan"]},
        {"image": "images/lebanon.png", "answer": "Lebanon", "choices": ["Lebanon", "Malaysia", "Thailand", "Singapore"]},
        {"image": "images/laos.png", "answer": "Laos", "choices": ["Vietnam", "Filiphina", "Thailand", "Laos"]},
        {"image": "images/jordan.png", "answer": "Jordan", "choices": ["Timor Leste", "Jordan", "Malaysia", "Korea Selatan"]},
        {"image": "images/irak.png", "answer": "Irak", "choices": ["Irak", "Malaysia", "Thailand", "Singapore"]},
        {"image": "images/iran.png", "answer": "Iran", "choices": ["Vietnam", "Filiphina", "Iran", "Jepang"]},
        {"image": "images/mesir.png", "answer": "Mesir", "choices": ["Mesir", "Malaysia", "Thailand", "Singapore"]},
        {"image": "images/timorleste.png", "answer": "Timor Leste", "choices": ["Vietnam", "Timor Leste", "Thailand", "Jepang"]},
        {"image": "images/kamboja.png", "answer": "Kamboja", "choices": ["Kamboja", "Palestina", "Malaysia", "Korea Selatan"]},
        {"image": "images/brunai.png", "answer": "Brunai", "choices": ["Brunai", "Malaysia", "Thailand", "Singapore"]},
        {"image": "images/Afganistan.png", "answer": "Afganistan", "choices": ["Vietnam", "Filiphina", "Thailand", "Afganistan"]}
    ],
    "europe": [
        {"image": "images/Jerman.png", "answer": "Jerman", "choices": ["Jerman", "Jamaika", "Sudan", "India"]},
        {"image": "images/Portugal.png", "answer": "Portugal", "choices": ["Jerman", "Spanyol", "Inggris", "Portugal"]},
        {"image": "images/Belanda.png", "answer": "Belanda", "choices": ["Qatar", "Belanda", "China", "Malaysia"]},
        {"image": "images/italia.png", "answer": "Italia", "choices": ["Italia", "Jamaika", "Sudan", "India"]},
        {"image": "images/irlandia.png", "answer": "Irlandia", "choices": ["Italia", "Irlandia", "Inggris", "Portugal"]},
        {"image": "images/yunani.png", "answer": "Yunani", "choices": ["Yunani", "Jamaika", "Sudan", "India"]},
        {"image": "images/finlandia.png", "answer": "Finlandia", "choices": ["Finlandia", "Spanyol", "Inggris", "Portugal"]},
        {"image": "images/denmark.png", "answer": "Denmark", "choices": ["Denmark", "Jamaika", "Sudan", "India"]},
        {"image": "images/ceko.png", "answer": "Ceko", "choices": ["Ceko", "Spanyol", "Inggris", "Portugal"]},
        {"image": "images/kroasia.png", "answer": "Kroasia", "choices": ["Kroasia", "Jamaika", "Sudan", "India"]},
        {"image": "images/belgia.png", "answer": "Belgia", "choices": ["Belgia", "Spanyol", "Inggris", "Portugal"]},
        {"image": "images/austria.png", "answer": "Austria", "choices": ["Austria", "Jamaika", "Sudan", "India"]}
    ],
    "amerikaselatan": [
        {"image": "images/Argentina.png", "answer": "Argentina", "choices": ["Argentina", "Haiti", "Afrika", "Inggris"]},
        {"image": "images/Bolivia.png", "answer": "Bolivia", "choices": ["Bolivia", "Haiti", "Afrika", "Inggris"]},
        {"image": "images/Brazil.png", "answer": "Brazil", "choices": ["Brazil", "Haiti", "Afrika", "Inggris"]},
        {"image": "images/Chile.png", "answer": "Chile", "choices": ["Chile", "Haiti", "Afrika", "Inggris"]},
        {"image": "images/Colombia.png", "answer": "Colombia", "choices": ["Colombia", "Haiti", "Afrika", "Inggris"]},
        {"image": "images/Ecuador.png", "answer": "Ecuador", "choices": ["Ecuador", "Haiti", "Afrika", "Inggris"]},
        {"image": "images/Paraguay.png", "answer": "Paraguay", "choices": ["Paraguay", "Haiti", "Afrika", "Inggris"]},
        {"image": "images/Peru.png", "answer": "Peru", "choices": ["Peru", "Haiti", "Afrika", "Inggris"]},
        {"image": "images/Suriname.png", "answer": "Suriname", "choices": ["Suriname", "Haiti", "Afrika", "Inggris"]},
        {"image": "images/Uruguay.png", "answer": "Uruguay", "choices": ["Uruguay", "Haiti", "Afrika", "Inggris"]},
        {"image": "images/Venezuela.png", "answer": "Venezuela", "choices": ["Venezuela", "Haiti", "Afrika", "Inggris"]}
    ]
}

class StartScreen(Screen):
    def on_enter(self):
        self.play_opening_sound()

    def go_to_level_screen(self):
        self.manager.current = 'level'

    def play_opening_sound(self):
        pygame.mixer.music.load(OPENING_SOUND)
        pygame.mixer.music.play(-1)

    def stop_opening_sound(self):
        pygame.mixer.music.stop()

class LevelScreen(Screen):
    def select_level(self, level):
        game_screen = self.manager.get_screen('game')
        game_screen.selected_level = level
        game_screen.load_questions()
        self.manager.current = 'game'
        game_screen.start_timer()

class GameWidget(Screen):
    image_source = StringProperty("")
    timer = NumericProperty(0)
    selected_level = StringProperty("asia")

    def __init__(self, **kwargs):
        super(GameWidget, self).__init__(**kwargs)
        self.score = 0
        self.question_count = 0
        self.current_question = None
        self.timer_event = None

    def start_timer(self):
        self.timer = 0
        if self.timer_event:
            self.timer_event.cancel()
        self.timer_event = Clock.schedule_interval(self.update_timer, 1)

    def update_timer(self, dt):
        self.timer += 1
        self.ids.timer_label.text = f"Time: {self.timer}s"

    def load_questions(self):
        self.questions = questions[self.selected_level]
        self.load_question()

    def load_question(self):
        if self.question_count  >= 10:
            self.end_game()
        else:
            self.current_question = random.choice(self.questions)
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
        sm.add_widget(StartScreen(name='start'))
        sm.add_widget(LevelScreen(name='level'))
        sm.add_widget(GameWidget(name='game'))
        sm.add_widget(ResultScreen(name='result'))
        return sm

if __name__ == '__main__':
    TebakGambarApp().run()
