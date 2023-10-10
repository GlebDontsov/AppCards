import shutil
import os

from utils.util import set_screen, create_screen_update, create_screen_train

from kivymd.uix.button import MDFillRoundFlatButton
from kivymd.uix.screen import Screen
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.list import OneLineAvatarIconListItem, IconLeftWidget, IconRightWidget
from kivymd.uix.scrollview import MDScrollView
from kivymd.uix.list import MDList


class ScreenSets(Screen):
    def __init__(self, sm, **kwargs):
        self.sm = sm
        super(ScreenSets, self).__init__(**kwargs)

        box = MDBoxLayout(orientation='vertical',
                          size_hint=(0.95, 0.95),
                          pos_hint={'center_x': 0.5, 'center_y': 0.5},
                          spacing=8)

        box.add_widget(MDFillRoundFlatButton(text='Назад',
                                             font_size='15sp',
                                             size_hint=(1, 0.1),
                                             ripple_alpha=0.15,
                                             on_press=lambda x: set_screen('menu', self.sm)))

        self.list_view = MDList(size_hint=(0.93, 1))

        directory = 'cache/sets'

        for filename in os.listdir(directory):
            file_name = os.path.join(directory, filename)[11:-5]

            self.line = OneLineAvatarIconListItem(text=f'{file_name}',
                                                  on_press=lambda x: create_screen_train(x, 'sets', self.sm))

            self.button_feather = IconRightWidget(icon='feather',
                                                  text=f'{file_name}',
                                                  ripple_alpha=0.15,
                                                  on_press=lambda x: create_screen_update(x, 'sets', self.sm))

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
        path = f'cache/sets/{x.text}.json'
        os.remove(path)

    def add_to_star(self, x):
        self.list_view.remove_widget(x.ids['container'])
        list_view = self.list_view.children
        self.scroll = MDScrollView(list_view)
        source_path = f'cache/sets/{x.text}.json'
        destination_path = 'cache/star'
        shutil.move(source_path, destination_path)
        from AppCards.screens.stars import ScreenStar
        ScreenStar.update_star(self.sm.get_screen('star'), x.text)

    def update_sets(self, text, screen=None, operation='add'):
        if operation == 'update' and screen:
            self.list_view.remove_widget(screen.ids['container'])
            list_view = self.list_view.children
            self.scroll = MDScrollView(list_view)

        self.line = OneLineAvatarIconListItem(text=f'{text}',
                                              on_press=lambda x: create_screen_train(x, 'sets', self.sm))

        self.button_feather = IconRightWidget(icon='feather',
                                              text=f'{text}',
                                              ripple_alpha=0.15,
                                              on_press=lambda x: create_screen_update(x, 'sets', self.sm))

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
