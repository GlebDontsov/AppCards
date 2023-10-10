import json
import random
import threading

from utils.util import back, voice

from kivy.uix.label import Label
from kivymd.uix.button import MDFillRoundFlatButton, MDIconButton, MDFlatButton
from kivymd.uix.screen import Screen
from kivymd.uix.stacklayout import MDStackLayout


class ScreenTrain(Screen):
    def __init__(self, sm, directory_name, file_name, **kwargs):
        with open(f'cache/{directory_name}/{file_name}.json', 'r') as f:
            self.sets_cards = json.loads(f.read())

        self.sm = sm
        self.back = directory_name
        self.dict_cards = dict(self.sets_cards)
        self.key = random.choice(list(self.dict_cards))

        self.num_card = len(self.dict_cards)
        self.ans_right = 0
        self.ans_wrong = 0
        self.flag = False

        super(ScreenTrain, self).__init__(**kwargs)

        box = MDStackLayout(size_hint=(0.9, 0.95),
                            pos_hint={'center_x': 0.5, 'center_y': 0.5},
                            spacing=8)

        self.text_dont_know = Label(text=f'{self.ans_right}',
                                    font_size='20sp',
                                    color='#FF0000',
                                    size_hint=(0.2, 0.072),
                                    halign='center')

        self.text_know = Label(text=f'{self.ans_wrong}',
                               font_size='20sp',
                               color='#00FF00',
                               size_hint=(0.2, 0.072),
                               halign='center')

        self.card = MDFlatButton(text=f'{self.dict_cards[self.key]["card"]}',
                                 halign="center",
                                 font_style='H3',
                                 size_hint=(1, 0.62),
                                 line_color='0099ff',
                                 line_width=1.5,
                                 ripple_alpha=0.15,
                                 on_press=lambda x: self.change_side(),
                                 )

        if len(self.dict_cards[self.key]['card']) < 13:
            self.card.font_size = '40sp'
        elif len(self.dict_cards[self.key]['card']) < 18:
            self.card.font_size = '30sp'
        else:
            self.card.font_size = '20sp'

        box.add_widget(MDFillRoundFlatButton(text='Назад',
                                             font_size='15sp',
                                             size_hint=(1, 0.09),
                                             on_press=lambda x: back(self.back, 'train', self.sm)))

        box.add_widget(self.text_dont_know)
        box.add_widget(self.text_know)

        box.add_widget(Label(text=f'{self.num_card}',
                             font_size='20sp',
                             color='black',
                             size_hint=(0.2, 0.072),
                             halign='center'))

        box.add_widget(MDIconButton(icon='microphone',
                                    size_hint=(0.4, 0.07),
                                    theme_icon_color="Custom",
                                    icon_color='0099ff',
                                    ripple_alpha=0.15,
                                    icon_size='30sp',
                                    on_press=lambda x: threading.Thread(target=voice, args=(
                                        self.dict_cards[self.key]['card'],)).start()))

        box.add_widget(self.card)

        box.add_widget(MDIconButton(icon='close-thick',
                                    size_hint=(0.5, 0.07),
                                    theme_icon_color="Custom",
                                    icon_color='#FF0000',
                                    ripple_alpha=0.15,
                                    icon_size='40sp',
                                    on_press=lambda x: self.dont_know()
                                    ))

        box.add_widget(MDIconButton(icon='check-bold',
                                    size_hint=(0.5, 0.07),
                                    icon_size='40sp',
                                    theme_icon_color="Custom",
                                    icon_color='#32CD32',
                                    ripple_alpha=0.15,
                                    on_press=lambda x: self.know()))

        box.add_widget(MDFillRoundFlatButton(text='Сначало',
                                             font_size='15sp',
                                             size_hint=(1, 0.09),
                                             md_bg_color='#32CD32',
                                             on_press=lambda x: self.start_over()))

        self.add_widget(box)

    def change_side(self):
        if self.flag:
            if len(self.dict_cards[self.key]['card']) < 13:
                self.card.font_size = '40sp'
            elif len(self.dict_cards[self.key]['card']) < 18:
                self.card.font_size = '30sp'
            else:
                self.card.font_size = '20sp'
            self.card.text = self.dict_cards[self.key]['card']
            self.flag = False
        else:
            if len(self.dict_cards[self.key]['card2']) < 13:
                self.card.font_size = '40sp'
            elif len(self.dict_cards[self.key]['card2']) < 18:
                self.card.font_size = '30sp'
            elif len(self.dict_cards[self.key]['card2']) < 22:
                self.card.font_size = '25sp'
            else:
                self.card.font_size = '20sp'
            self.card.text = self.dict_cards[self.key]['card2']
            self.flag = True

    def know(self):
        if self.ans_right + self.ans_wrong < self.num_card:
            self.ans_right += 1
            self.text_know.text = f'{self.ans_right}'
        self.change_card()

    def dont_know(self):
        if self.ans_right + self.ans_wrong < self.num_card:
            self.ans_wrong += 1
            self.text_dont_know.text = f'{self.ans_wrong}'
            self.change_card()

    def change_card(self):
        if len(self.dict_cards) != 1:
            del self.dict_cards[self.key]
            self.key = random.choice(list(self.dict_cards))
            self.card.text = self.dict_cards[self.key]['card']
            self.flag = False

    def start_over(self):
        self.dict_cards = dict(self.sets_cards)
        self.ans_right = 0
        self.ans_wrong = 0
        self.text_know.text = f'{self.ans_right}'
        self.text_dont_know.text = f'{self.ans_wrong}'
        self.key = random.choice(list(self.dict_cards))
        self.card.text = self.dict_cards[self.key]['card']
        self.flag = False
