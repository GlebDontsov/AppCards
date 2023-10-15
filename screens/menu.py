import json
import random
import sys
import threading

from kivy.uix.label import Label
from kivymd.uix.button import MDFillRoundFlatButton, MDIconButton, MDFlatButton
from kivymd.uix.screen import Screen
from kivymd.uix.boxlayout import MDBoxLayout
from utils.util import set_screen, change_word, voice


class ScreenMenu(Screen):
    def __init__(self, sm, **kwargs):
        with open('cache/words.json', 'r') as f:
            words = json.loads(f.read())
        key = random.choice(list(words))
        super(ScreenMenu, self).__init__(**kwargs)

        box = MDBoxLayout(orientation='vertical',
                          size_hint=(0.9, 0.9),
                          pos_hint={'center_x': 0.5, 'center_y': 0.5},
                          spacing=8)

        word = MDFlatButton(text=f"{words[key]['word']}",
                            font_size='24sp',
                            size_hint=(1, 0.2),
                            md_bg_color_disabled='red',
                            ripple_alpha=0.15,
                            ripple_color=[1, 1, 1, 1],
                            on_press=lambda x: threading.Thread(target=voice, args=(x.text,)).start())

        translation = Label(text=f"{words[key]['translation']}",
                            color='black',
                            font_size='24sp',
                            size_hint=(1, 0.1))

        box.add_widget(word)
        box.add_widget(translation)

        box.add_widget(MDIconButton(icon='arrow-right',
                                    pos_hint={'center_x': 0.90},
                                    ripple_alpha=0.15,
                                    on_press=lambda x: change_word(word, translation, words)))

        box.add_widget(MDFillRoundFlatButton(text='Тренироваться',
                                             font_size='30sp',
                                             size_hint=(1, 0.3),
                                             ripple_alpha=0.15,
                                             on_press=lambda x: set_screen('sets', sm)))

        box.add_widget(MDFillRoundFlatButton(text='Переводчик',
                                             font_size='30sp',
                                             size_hint=(1, 0.3),
                                             ripple_alpha=0.15,
                                             on_press=lambda x: set_screen('translator', sm)))

        box.add_widget(MDFillRoundFlatButton(text='Избранное',
                                             font_size='30sp',
                                             size_hint=(1, 0.3),
                                             ripple_alpha=0.15,
                                             on_press=lambda x: set_screen('star', sm)))

        box.add_widget(MDFillRoundFlatButton(text='Создать набор',
                                             font_size='30sp',
                                             size_hint=(1, 0.3),
                                             ripple_alpha=0.15,
                                             on_press=lambda x: set_screen('create_sets', sm)))

        box.add_widget(MDFillRoundFlatButton(text='Выйти',
                                             font_size='30sp',
                                             size_hint=(1, 0.3),
                                             ripple_alpha=0.15,
                                             on_press=lambda x: sys.exit()))

        self.add_widget(box)
