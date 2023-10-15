import shutil
import os

from utils.util import set_screen, create_screen_update, create_screen_train
from screens.sets import ScreenSets

from kivymd.uix.button import MDFillRoundFlatButton
from kivymd.uix.screen import Screen
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.list import OneLineAvatarIconListItem, IconLeftWidget, IconRightWidget
from kivymd.uix.scrollview import MDScrollView
from kivymd.uix.list import MDList


class ScreenStar(Screen):
    def __init__(self, sm, **kwargs):
        self.sm = sm
        super(ScreenStar, self).__init__(**kwargs)

        box = MDBoxLayout(orientation='vertical',
                          size_hint=(0.95, 0.95),
                          pos_hint={'center_x': 0.5, 'center_y': 0.5},
                          spacing=8)

        box.add_widget(MDFillRoundFlatButton(text='Назад',
                                             font_size='15sp',
                                             size_hint=(1, 0.1),
                                             ripple_alpha=0.15,
                                             on_press=lambda x: set_screen('menu', self.sm)))

        self.list_view = MDList(size_hint=(1, 1))

        directory = 'cache/star'
        for filename in os.listdir(directory):
            file_name = os.path.join(directory, filename)[5:-5]

            self.line = OneLineAvatarIconListItem(
                text=f'{file_name}',
                on_press=lambda x: create_screen_train(x, directory, self.sm))

            self.button_star = IconLeftWidget(icon='star',
                                              text=f'{file_name}',
                                              ripple_alpha=0.15,
                                              on_press=lambda x: self.delete_from_star(x))

            self.button_feather = IconRightWidget(icon='feather',
                                                  text=f'{file_name}',
                                                  ripple_alpha=0.15,
                                                  on_press=lambda x: create_screen_update(x, directory, self.sm))

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
            on_press=lambda x: create_screen_train(x, 'star', self.sm))

        self.button_star = IconLeftWidget(icon="star",
                                          text=f'{new_file}',
                                          ripple_alpha=0.15,
                                          on_press=lambda x: self.delete_from_star(x))

        self.button_feather = IconRightWidget(icon='feather',
                                              text=f'{new_file}',
                                              ripple_alpha=0.15,
                                              on_press=lambda x: create_screen_update(x, 'star', self.sm))

        self.button_star.ids['container'] = self.line
        self.button_feather.ids['container'] = self.line

        self.line.add_widget(self.button_feather)
        self.line.add_widget(self.button_star)
        self.list_view.add_widget(self.line)

    def delete_from_star(self, x):
        self.list_view.remove_widget(x.ids['container'])
        list_view = self.list_view.children
        self.scroll = MDScrollView(list_view)
        source_path = f'cache/star/{x.text}.json'
        destination_path = 'cache/sets'
        shutil.move(source_path, destination_path)
        ScreenSets.update_sets(self.sm.get_screen('sets'), x.text)
