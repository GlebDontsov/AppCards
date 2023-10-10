import threading
from utils.util import set_screen, voice
from utils.translate_eng_to_ru import translate_phrase_to_ru
from utils.translate_ru_to_eng import translate_phrase_to_eng
from utils.speech_rec import recognize_speech
from kivy.uix.label import Label
from kivymd.uix.button import MDFillRoundFlatButton, MDIconButton
from kivymd.uix.screen import Screen
from kivymd.uix.textfield import MDTextField
from kivymd.uix.stacklayout import MDStackLayout
from kivy.metrics import sp


class ScreenTranslator(Screen):
    def __init__(self, sm, **kwargs):
        self.sm = sm
        super(ScreenTranslator, self).__init__(**kwargs)

        box = MDStackLayout(adaptive_height=False,
                            size_hint=(0.9, 0.9),
                            pos_hint={'center_x': 0.5, 'center_y': 0.5},
                            spacing=5
                            )

        self.lang1 = Label(text=f'ru',
                           font_size='20sp',
                           color='black',
                           size_hint=(0.4, 0.1),
                           halign='center')

        self.lang2 = Label(text=f'eng',
                           font_size='20sp',
                           color='black',
                           size_hint=(0.4, 0.1),
                           halign='center')

        self.translator = MDTextField(size_hint=(1, None),
                                      mode="rectangle",
                                      multiline=True,
                                      max_height=10 * sp(18),
                                      line_height=sp(18),
                                      hint_text="Введите текст")

        self.translation = MDTextField(size_hint=(1, None),
                                       mode="rectangle",
                                       multiline=True,
                                       max_height=10 * sp(18),
                                       line_height=sp(18),
                                       hint_text="Перевод")

        box.add_widget(self.lang1)

        box.add_widget(MDIconButton(icon='arrow-right',
                                    ripple_alpha=0.15,
                                    size_hint=(0.2, 0.1),
                                    on_press=lambda x: self.change_language()))

        box.add_widget(self.lang2)
        box.add_widget(self.translator)
        box.add_widget(self.translation)

        box.add_widget(Label(size_hint=(1, 0.005)))

        box.add_widget(MDIconButton(icon='trash-can-outline',
                                    size_hint=(0.333, 0.1),
                                    theme_icon_color="Custom",
                                    icon_color='red',
                                    ripple_alpha=0.15,
                                    icon_size='30sp',
                                    on_press=lambda x: self.trow_away()))

        box.add_widget(MDIconButton(icon='volume-high',
                                    size_hint=(0.333, 0.1),
                                    theme_icon_color="Custom",
                                    icon_color='0099ff',
                                    ripple_alpha=0.15,
                                    icon_size='30sp',
                                    on_press=lambda x: threading.Thread(
                                        target=voice,
                                        args=(self.translation.text, self.lang2.text,)).start()))

        box.add_widget(MDIconButton(icon='microphone',
                                    size_hint=(0.333, 0.1),
                                    theme_icon_color="Custom",
                                    icon_color='0099ff',
                                    ripple_alpha=0.15,
                                    icon_size='30sp',
                                    on_press=lambda x: self.speech()))

        box.add_widget(MDFillRoundFlatButton(text='Назад',
                                             font_size='15sp',
                                             size_hint=(0.5, 0.1),
                                             ripple_alpha=0.15,
                                             on_press=lambda x: set_screen('menu', self.sm)))

        box.add_widget(MDFillRoundFlatButton(text='Перевести',
                                             font_size='15sp',
                                             md_bg_color='#32CD32',
                                             size_hint=(0.5, 0.1),
                                             on_press=lambda x: self.translate_text(self.translator.text,
                                                                                    self.lang1.text)))

        self.add_widget(box)

    def translate_text(self, text, lang):
        if 'eng' == lang and text:
            self.translation.text = translate_phrase_to_ru(text)
        elif 'ru' == lang and text:
            self.translation.text = translate_phrase_to_eng(text)

    def change_language(self):
        self.lang1.text, self.lang2.text = self.lang2.text, self.lang1.text

    def trow_away(self):
        self.translation.text = ''
        self.translator.text = ''

    def speech(self):
        words = recognize_speech()
        self.translator.text = words
