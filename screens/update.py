import os
import json
import uuid

from utils.util import back
from AppCards.screens.stars import ScreenStar
from AppCards.screens.sets import ScreenSets

from kivy.uix.label import Label
from kivymd.uix.button import MDFillRoundFlatButton, MDIconButton
from kivymd.uix.screen import Screen
from kivymd.uix.textfield import MDTextField
from kivymd.uix.stacklayout import MDStackLayout


class ScreenUpdate(Screen):
    def __init__(self, sm, screen, directory, **kwargs):
        with open(f'cache/{directory}/{screen.text}.json', 'r') as f:
            self.sets = json.loads(f.read())
        self.sm = sm
        self.directory = directory
        self.screen = screen
        self.file_name = screen.text
        self.keys = list(self.sets.keys())
        self.card_number = len(self.sets)
        self.i = 0

        super(ScreenUpdate, self).__init__(**kwargs)

        box = MDStackLayout(adaptive_height=True,
                            size_hint=(0.9, 0.95),
                            pos_hint={'center_x': 0.5, 'center_y': 0.5},
                            spacing=5
                            )

        self.set_name = MDTextField(size_hint=(0.5, 0.1),
                                    text=self.file_name,
                                    required=True,
                                    max_text_length=28,
                                    hint_text="Название набора")

        self.cards = Label(text=f'Карточка №: {self.i + 1}',
                           size_hint=(0.5, 0.2),
                           color=[0, 0, 0, 1],
                           font_size='16sp')

        self.card = MDTextField(size_hint=(1, 0.3),
                                text=self.sets[self.keys[self.i]]['card'],
                                multiline=True,
                                required=True,
                                max_text_length=28,
                                hint_text="Видимая сторона карточки")

        self.card2 = MDTextField(size_hint=(1, 0.3),
                                 text=self.sets[self.keys[self.i]]['card2'],
                                 multiline=True,
                                 required=True,
                                 max_text_length=28,
                                 hint_text="Обратная сторона карточки")

        box.add_widget(MDFillRoundFlatButton(text='Назад',
                                             font_size='15sp',
                                             size_hint=(1, 0.1),
                                             on_press=lambda x: back(self.directory, 'update', self.sm)))

        box.add_widget(Label(text='Название набора: ',
                             size_hint=(0.5, 0.1),
                             color=[0, 0, 0, 1],
                             font_size='15sp'))

        box.add_widget(self.set_name)
        box.add_widget(self.cards)

        box.add_widget(MDIconButton(icon='minus',
                                    size_hint=(0.25, 0.2),
                                    icon_size='30sp',
                                    theme_icon_color="Custom",
                                    icon_color='#FF0000',
                                    ripple_alpha=0.15,
                                    on_press=lambda x: self.button_delete()
                                    ))

        box.add_widget(MDIconButton(icon='plus',
                                    size_hint=(0.25, 0.2),
                                    icon_size='30sp',
                                    theme_icon_color="Custom",
                                    icon_color='#32CD32',
                                    ripple_alpha=0.15,
                                    on_press=lambda x: self.button_plus()
                                    ))

        box.add_widget(self.card)
        box.add_widget(Label(size_hint=(1, 0.1)))
        box.add_widget(self.card2)

        box.add_widget(MDIconButton(icon='arrow-left',
                                    size_hint=(0.5, 0.1),
                                    icon_size='30sp',
                                    ripple_alpha=0.15,
                                    on_press=lambda x: self.button_back()))

        box.add_widget(MDIconButton(icon='arrow-right',
                                    size_hint=(0.5, 0.1),
                                    icon_size='30sp',
                                    ripple_alpha=0.15,
                                    on_press=lambda x: self.button_next()))

        box.add_widget(MDFillRoundFlatButton(text='Сохарнить',
                                             font_size='15sp',
                                             md_bg_color='#32CD32',
                                             size_hint=(1, 0.1),
                                             on_press=lambda x: self.button_save()))

        self.add_widget(box)

    def button_delete(self):
        if len(self.sets) == 1:
            self.card.text = ''
            self.card2.text = ''
            del self.sets[self.keys[self.i]]
            self.keys = []
            self.card_number = len(self.sets)
        elif self.sets:
            del self.sets[self.keys[self.i]]
            self.keys = list(self.sets.keys())
            self.card_number = len(self.sets)
            if self.i < len(self.keys):
                self.card.text = self.sets[self.keys[self.i]]["card"]
                self.card2.text = self.sets[self.keys[self.i]]["card2"]
                self.cards.text = f'Карточка №: {self.i + 1}'
            else:
                self.i -= 1
                self.card.text = self.sets[self.keys[self.i]]["card"]
                self.card2.text = self.sets[self.keys[self.i]]["card2"]
                self.cards.text = f'Карточка №: {self.i + 1}'

    def button_plus(self):
        if len(self.card.text) <= 28 and len(self.card2.text) <= 28:
            if self.card.text and self.card2.text:
                self.sets[str(uuid.uuid4())] = {'card': '', 'card2': ''}
                self.keys = list(self.sets.keys())
                self.card_number = len(self.sets)
                self.sets[self.keys[self.i]] = {'card': self.card.text, 'card2': self.card2.text}
                self.i = self.card_number - 1
                self.card.text = self.sets[self.keys[self.i]]["card"]
                self.card2.text = self.sets[self.keys[self.i]]["card2"]
                self.cards.text = f'Карточка №: {self.i + 1}'

    def button_save(self):
        if len(self.card.text) <= 28 and len(self.card2.text) <= 28 and len(self.set_name.text) <= 28:
            if self.card.text and self.card2.text:
                self.sets[self.keys[self.i]] = {'card': self.card.text, 'card2': self.card2.text}
            else:
                del self.sets[self.keys[self.i]]
            if self.sets and self.set_name.text:
                os.rename(f'cache/{self.directory}/{self.file_name}.json', f'cache/{self.directory}/{self.set_name.text}.json')
                with open(f'cache/{self.directory}/{self.set_name.text}.json', 'w') as f:
                    f.write(json.dumps(self.sets))
                if self.directory == 'sets':
                    ScreenSets.update_sets(self.sm.get_screen('sets'), self.set_name.text, self.screen, 'update')
                elif self.directory == 'star':
                    ScreenStar.update_star(self.sm.get_screen('star'), self.set_name.text, self.screen, 'update')
                back(self.directory, 'update', self.sm)
        else:
            pass

    def button_back(self):
        if len(self.card.text) <= 28 and len(self.card2.text) <= 28:
            if self.sets and self.card.text and self.card2.text:
                if self.card.text and self.card2.text:
                    self.sets[self.keys[self.i]] = {'card': self.card.text, 'card2': self.card2.text}
                if self.i > 0:
                    self.i -= 1
                    self.card.text = self.sets[self.keys[self.i]]["card"]
                    self.card2.text = self.sets[self.keys[self.i]]["card2"]
                    self.cards.text = f'Карточка №: {self.i + 1}'

    def button_next(self):
        if len(self.card.text) <= 28 and len(self.card2.text) <= 28:
            if self.sets and self.card.text and self.card2.text:
                if self.card.text and self.card2.text:
                    self.sets[self.keys[self.i]] = {'card': self.card.text, 'card2': self.card2.text}
                if self.i < self.card_number - 1:
                    self.i += 1
                    self.card.text = self.sets[self.keys[self.i]]["card"]
                    self.card2.text = self.sets[self.keys[self.i]]["card2"]
                    self.cards.text = f'Карточка №: {self.i + 1}'
