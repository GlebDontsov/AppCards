import shutil
import os
import sys
import json
import random
import uuid
import threading

from kivy.uix.label import Label
from kivymd.uix.screenmanager import ScreenManager
from kivymd.uix.button import MDFillRoundFlatButton, MDIconButton, MDFlatButton
from kivymd.uix.screen import Screen
from kivymd.uix.textfield import MDTextField
from kivymd.uix.stacklayout import MDStackLayout
from kivymd.app import MDApp
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.list import OneLineAvatarIconListItem, IconLeftWidget, IconRightWidget
from kivymd.uix.scrollview import MDScrollView
from kivymd.uix.list import MDList
from gtts import gTTS
from playsound import playsound


class ScreenMenu(Screen):
    def __init__(self, **kwargs):
        with open('words.json', 'r') as f:
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
                            on_press=lambda x: threading.Thread(target=Methods.voice, args=(x.text,)).start())

        translation = Label(text=f"{words[key]['translation']}",
                            color='black',
                            font_size='24sp',
                            size_hint=(1, 0.2))

        box.add_widget(word)
        box.add_widget(translation)

        box.add_widget(MDIconButton(icon='arrow-right',
                                    pos_hint={'center_x': 0.90},
                                    ripple_alpha=0.15,
                                    on_press=lambda x: change_word()))

        box.add_widget(MDFillRoundFlatButton(text='Тренироваться',
                                             font_size='30sp',
                                             size_hint=(1, 0.3),
                                             ripple_alpha=0.15,
                                             on_press=lambda x: Methods.set_screen('sets')))

        box.add_widget(MDFillRoundFlatButton(text='Избранное',
                                             font_size='30sp',
                                             size_hint=(1, 0.3),
                                             ripple_alpha=0.15,
                                             on_press=lambda x: Methods.set_screen('star')))

        box.add_widget(MDFillRoundFlatButton(text='Создать набор',
                                             font_size='30sp',
                                             size_hint=(1, 0.3),
                                             ripple_alpha=0.15,
                                             on_press=lambda x: Methods.set_screen('create_sets')))

        box.add_widget(MDFillRoundFlatButton(text='Выйти',
                                             font_size='30sp',
                                             size_hint=(1, 0.3),
                                             ripple_alpha=0.15,
                                             on_press=lambda x: sys.exit()))

        self.add_widget(box)

        def change_word():
            key = random.choice(list(words))
            word.text = f"{words[key]['word']}"
            translation.text = f"{words[key]['translation']}"


class ScreenSets(Screen):
    def __init__(self, **kwargs):
        super(ScreenSets, self).__init__(**kwargs)

        box = MDBoxLayout(orientation='vertical',
                          size_hint=(0.95, 0.95),
                          pos_hint={'center_x': 0.5, 'center_y': 0.5},
                          spacing=8)

        box.add_widget(MDFillRoundFlatButton(text='Назад',
                                             font_size='15sp',
                                             size_hint=(1, 0.1),
                                             ripple_alpha=0.15,
                                             on_press=lambda x: Methods.set_screen('menu')))

        self.list_view = MDList(size_hint=(0.93, 1))

        directory = 'sets'
        for filename in os.listdir(directory):
            file_name = os.path.join(directory, filename)[5:-5]

            self.line = OneLineAvatarIconListItem(text=f'{file_name}',
                                                  on_press=lambda x: Methods.create_screen_train(x, 'sets'))

            self.button_feather = IconRightWidget(icon='feather',
                                                  text=f'{file_name}',
                                                  ripple_alpha=0.15,
                                                  on_press=lambda x: Methods.create_screen_update(x, 'sets'))

            self.button_star = IconLeftWidget(icon="star-outline",
                                              text=f'{file_name}',
                                              ripple_alpha=0.15,
                                              on_press=lambda x: self.add_to_star(x))

            self.button_delete = IconRightWidget(icon='delete',
                                                 text=f'{file_name}',
                                                 ripple_alpha=0.15,
                                                 on_press=lambda x: self.delete_set(x))

            self.button_feather.ids['container'] = self.line
            self.button_star.ids['container'] = self.line
            self.button_delete.ids['container'] = self.line

            self.line.add_widget(self.button_feather)
            self.line.add_widget(self.button_star)
            self.line.add_widget(self.button_delete)
            self.list_view.add_widget(self.line)

        self.scroll = MDScrollView(self.list_view)
        box.add_widget(self.scroll)
        self.add_widget(box)

    def delete_set(self, x):
        self.list_view.remove_widget(x.ids['container'])
        list_view = self.list_view.children
        self.scroll = MDScrollView(list_view)
        path = f'sets/{x.text}.json'
        os.remove(path)

    def add_to_star(self, x):
        self.list_view.remove_widget(x.ids['container'])
        list_view = self.list_view.children
        self.scroll = MDScrollView(list_view)
        source_path = f'sets/{x.text}.json'
        destination_path = "star"
        shutil.move(source_path, destination_path)
        ScreenStar.update_star(sm.get_screen('star'), x.text)

    def update_sets(self, text, screen=None, operation='add'):
        if operation == 'update' and screen:
            self.list_view.remove_widget(screen.ids['container'])
            list_view = self.list_view.children
            self.scroll = MDScrollView(list_view)

        self.line = OneLineAvatarIconListItem(text=f'{text}',
                                              on_press=lambda x: Methods.create_screen_train(x, 'sets'))

        self.button_feather = IconRightWidget(icon='feather',
                                              text=f'{text}',
                                              ripple_alpha=0.15,
                                              on_press=lambda x: Methods.create_screen_update(x, 'sets'))

        self.button_star = IconLeftWidget(icon="star-outline",
                                          text=f'{text}',
                                          ripple_alpha=0.15,
                                          on_press=lambda x: self.add_to_star(x))

        self.button_delete = IconRightWidget(icon='delete',
                                             text=f'{text}',
                                             ripple_alpha=0.15,
                                             on_press=lambda x: self.delete_set(x))

        self.button_feather.ids['container'] = self.line
        self.button_star.ids['container'] = self.line
        self.button_delete.ids['container'] = self.line

        self.line.add_widget(self.button_feather)
        self.line.add_widget(self.button_star)
        self.line.add_widget(self.button_delete)
        self.list_view.add_widget(self.line)


class ScreenCreateSets(Screen):
    def __init__(self, **kwargs):
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
            if not os.path.exists(f'sets/{self.set_name.text}.json'):
                if self.card_number not in self.dict_card and self.card.text and self.card2.text:
                    self.dict_card[self.card_number] = {'card': self.card.text, 'card2': self.card2.text}
                if self.dict_card and self.set_name.text:
                    with open(f'sets/{self.set_name.text}.json', 'w') as f:
                        f.write(json.dumps(self.dict_card))
                    ScreenSets.update_sets(sm.get_screen('sets'), self.set_name.text)
                    self.button_cancel()
            else:
                self.set_name.hint_text = 'Набор уже существует'
                self.set_name.error = True

        else:
            pass

    def button_cancel(self):
        Methods.set_screen('menu')
        self.dict_card.clear()
        self.card_number = 1
        self.card.text = ''
        self.card2.text = ''
        self.set_name.text = ''
        self.set_name.hint_text = 'Название набора'
        self.cards.text = f'Карточка №: {self.card_number}'


class ScreenStar(Screen):
    def __init__(self, **kwargs):
        super(ScreenStar, self).__init__(**kwargs)

        box = MDBoxLayout(orientation='vertical',
                          size_hint=(0.95, 0.95),
                          pos_hint={'center_x': 0.5, 'center_y': 0.5},
                          spacing=8)

        box.add_widget(MDFillRoundFlatButton(text='Назад',
                                             font_size='15sp',
                                             size_hint=(1, 0.1),
                                             ripple_alpha=0.15,
                                             on_press=lambda x: Methods.set_screen('menu')))

        self.list_view = MDList(size_hint=(1, 1))

        directory = 'star'
        for filename in os.listdir(directory):
            file_name = os.path.join(directory, filename)[5:-5]

            self.line = OneLineAvatarIconListItem(
                text=f'{file_name}',
                on_press=lambda x: Methods.create_screen_train(x, 'star'))

            self.button_star = IconLeftWidget(icon="star",
                                              text=f'{file_name}',
                                              ripple_alpha=0.15,
                                              on_press=lambda x: self.delete_from_star(x))

            self.button_feather = IconRightWidget(icon='feather',
                                                  text=f'{file_name}',
                                                  ripple_alpha=0.15,
                                                  on_press=lambda x: Methods.create_screen_update(x, 'star'))

            self.button_star.ids['container'] = self.line
            self.button_feather.ids['container'] = self.line

            self.line.add_widget(self.button_feather)
            self.line.add_widget(self.button_star)
            self.list_view.add_widget(self.line)

        self.scroll = MDScrollView(self.list_view)
        box.add_widget(self.scroll)
        self.add_widget(box)

    def update_star(self, new_file, screen=None, operation='add'):
        if operation == 'update':
            self.list_view.remove_widget(screen.ids['container'])
            list_view = self.list_view.children
            self.scroll = MDScrollView(list_view)

        self.line = OneLineAvatarIconListItem(
            text=f'{new_file}',
            on_press=lambda x: Methods.create_screen_train(x, 'star'))

        self.button_star = IconLeftWidget(icon="star",
                                          text=f'{new_file}',
                                          ripple_alpha=0.15,
                                          on_press=lambda x: self.delete_from_star(x))

        self.button_feather = IconRightWidget(icon='feather',
                                              text=f'{new_file}',
                                              ripple_alpha=0.15,
                                              on_press=lambda x: Methods.create_screen_update(x, 'star'))

        self.button_star.ids['container'] = self.line
        self.button_feather.ids['container'] = self.line

        self.line.add_widget(self.button_feather)
        self.line.add_widget(self.button_star)
        self.list_view.add_widget(self.line)

    def delete_from_star(self, x):
        self.list_view.remove_widget(x.ids['container'])
        list_view = self.list_view.children
        self.scroll = MDScrollView(list_view)
        source_path = f'star/{x.text}.json'
        destination_path = "sets"
        shutil.move(source_path, destination_path)
        ScreenSets.update_sets(sm.get_screen('sets'), x.text)


class ScreenTrain(Screen):
    def __init__(self, directory_name, file_name, **kwargs):
        with open(f'{directory_name}/{file_name}.json', 'r') as f:
            self.sets_cards = json.loads(f.read())

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
                                             on_press=lambda x: Methods.back(self.back, 'train')))

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
                                    on_press=lambda x: threading.Thread(target=Methods.voice, args=(
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


class ScreenUpdate(Screen):
    def __init__(self, screen, directory, **kwargs):
        with open(f'{directory}/{screen.text}.json', 'r') as f:
            self.sets = json.loads(f.read())
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
                                 text=self.sets[self.keys[self.i]]['card'],
                                 multiline=True,
                                 required=True,
                                 max_text_length=28,
                                 hint_text="Обратная сторона карточки")

        box.add_widget(MDFillRoundFlatButton(text='Назад',
                                             font_size='15sp',
                                             size_hint=(1, 0.1),
                                             on_press=lambda x: Methods.back(self.directory, 'update')))

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
                os.rename(f'{self.directory}/{self.file_name}.json', f'{self.directory}/{self.set_name.text}.json')
                with open(f'{self.directory}/{self.set_name.text}.json', 'w') as f:
                    f.write(json.dumps(self.sets))
                if self.directory == 'sets':
                    ScreenSets.update_sets(sm.get_screen('sets'), self.set_name.text, self.screen, 'update')
                elif self.directory == 'star':
                    ScreenStar.update_star(sm.get_screen('star'), self.set_name.text, self.screen, 'update')
                Methods.back(self.directory, 'update')
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


class Methods:
    @staticmethod
    def set_screen(name_screen):
        sm.current = name_screen

    @staticmethod
    def create_screen_train(screen, directory):
        sm.add_widget(ScreenTrain(directory, screen.text, name='train'))
        sm.current = 'train'

    @staticmethod
    def create_screen_update(screen, directory):
        sm.add_widget(ScreenUpdate(screen, directory, name='update'))
        sm.current = 'update'

    @staticmethod
    def back(remove_screen, name_screen):
        sm.current = remove_screen
        sm.remove_widget(sm.get_screen(name_screen))

    @staticmethod
    def sets_update(sets):
        if sets == 'sets':
            sm.remove_widget(sm.get_screen('sets'))
            sm.add_widget(ScreenSets(name='sets'))
        elif sets == 'star':
            sm.remove_widget(sm.get_screen('star'))
            sm.add_widget(ScreenStar(name='star'))

    @staticmethod
    def voice(x):
        tts = gTTS(text=f'{x}', lang='en')
        tts.save("voice_word.mp3")
        playsound("voice_word.mp3")


class MainApp(MDApp):
    def build(self):
        sm.add_widget(ScreenMenu(name='menu'))
        sm.add_widget(ScreenSets(name='sets'))
        sm.add_widget(ScreenStar(name='star'))
        sm.add_widget(ScreenCreateSets(name='create_sets'))
        return sm


if __name__ == "__main__":
    sm = ScreenManager()
    MainApp().run()