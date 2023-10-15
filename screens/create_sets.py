import os
import json

from screens.sets import ScreenSets
from utils.util import set_screen

from kivy.uix.label import Label
from kivymd.uix.button import MDFillRoundFlatButton, MDIconButton
from kivymd.uix.screen import Screen
from kivymd.uix.textfield import MDTextField
from kivymd.uix.stacklayout import MDStackLayout


class ScreenCreateSets(Screen):
    def __init__(self, sm, **kwargs):
        self.sm = sm
        self.dict_card = {}
        self.card_number = 1
        super(ScreenCreateSets, self).__init__(**kwargs)

        box = MDStackLayout(adaptive_height=True,
                            size_hint=(0.9, 0.9),
                            pos_hint={'center_x': 0.5, 'center_y': 0.5},
                            spacing=5
                            )

        self.set_name = MDTextField(size_hint=(1, 0.1),
                                    max_text_length=28,
                                    hint_text="Название набора")

        self.cards = Label(text=f'Карточка №: {self.card_number}',
                           size_hint=(1, 0.2),
                           color=[0, 0, 0, 1],
                           font_size='16sp')

        self.card = MDTextField(size_hint=(1, 0.35),
                                max_text_length=28,
                                hint_text="Видимая сторона карточки")

        self.card2 = MDTextField(size_hint=(1, 0.35),
                                 max_text_length=28,
                                 hint_text="Обратная сторона карточки")

        box.add_widget(self.set_name)
        box.add_widget(self.cards)
        box.add_widget(self.card)
        box.add_widget(Label(size_hint=(1, 0.1)))
        box.add_widget(self.card2)
        box.add_widget(Label(size_hint=(1, 0.1)))

        box.add_widget(MDIconButton(icon='arrow-left',
                                    size_hint=(0.5, 0.1),
                                    line_color='0099ff',
                                    ripple_alpha=0.15,
                                    on_press=lambda x: self.button_back()))

        box.add_widget(MDIconButton(icon='arrow-right',
                                    size_hint=(0.5, 0.1),
                                    line_color='0099ff',
                                    ripple_alpha=0.15,
                                    on_press=lambda x: self.button_next()))

        box.add_widget(MDFillRoundFlatButton(text='Назад',
                                             font_size='15sp',
                                             size_hint=(0.5, 0.1),
                                             ripple_alpha=0.15,
                                             on_press=lambda x: self.button_cancel()))

        box.add_widget(MDFillRoundFlatButton(text='Сохранить',
                                             font_size='15sp',
                                             md_bg_color='#32CD32',
                                             size_hint=(0.5, 0.1),
                                             ripple_alpha=0.15,
                                             on_press=lambda x: self.button_save()))

        self.add_widget(box)

    def button_back(self):
        if len(self.card.text) <= 28 and len(self.card2.text) <= 28:
            if self.card_number not in self.dict_card and self.card.text and self.card2.text:
                self.dict_card[self.card_number] = {'card': self.card.text, 'card2': self.card2.text}
            if self.card_number > 1:
                self.card_number -= 1
                self.cards.text = f'Карточка №: {self.card_number}'
                self.card.text = self.dict_card[self.card_number]['card']
                self.card2.text = self.dict_card[self.card_number]['card2']
        else:
            pass

    def button_next(self):
        if len(self.card.text) <= 28 and len(self.card2.text) <= 28:
            if self.card_number + 1 in self.dict_card:
                self.card_number += 1
                self.cards.text = f'Карточка №: {self.card_number}'
                self.card.text = self.dict_card[self.card_number]['card']
                self.card2.text = self.dict_card[self.card_number]['card2']
            elif self.card.text and self.card2.text:
                self.dict_card[self.card_number] = {'card': self.card.text, 'card2': self.card2.text}
                self.card.text = ''
                self.card2.text = ''
                self.card_number += 1
                self.cards.text = f'Карточка №: {self.card_number}'
        else:
            pass

    def button_save(self):
        if len(self.card.text) <= 28 and len(self.card2.text) <= 28 and len(self.set_name.text) <= 28:
            if not os.path.exists(f'cache/sets/{self.set_name.text}.json'):
                if self.card_number not in self.dict_card and self.card.text and self.card2.text:
                    self.dict_card[self.card_number] = {'card': self.card.text, 'card2': self.card2.text}
                if self.dict_card and self.set_name.text:
                    with open(f'cache/sets/{self.set_name.text}.json', 'w') as f:
                        f.write(json.dumps(self.dict_card))
                    ScreenSets.update_sets(self.sm.get_screen('sets'), self.set_name.text)
                    self.button_cancel()
            else:
                self.set_name.hint_text = 'Набор уже существует'
                self.set_name.error = True

        else:
            pass

    def button_cancel(self):
        set_screen('menu', self.sm)
        self.dict_card.clear()
        self.card_number = 1
        self.card.text = ''
        self.card2.text = ''
        self.set_name.text = ''
        self.set_name.hint_text = 'Название набора'
        self.cards.text = f'Карточка №: {self.card_number}'
