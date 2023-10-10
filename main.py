from kivymd.uix.screenmanager import ScreenManager
from kivymd.app import MDApp


class MainApp(MDApp):
    def build(self):
        from screens.menu import ScreenMenu
        from screens.sets import ScreenSets
        from screens.stars import ScreenStar
        from screens.create_sets import ScreenCreateSets
        from screens.translator import ScreenTranslator

        sm.add_widget(ScreenMenu(sm, name='menu'))
        sm.add_widget(ScreenSets(sm, name='sets'))
        sm.add_widget(ScreenStar(sm, name='star'))
        sm.add_widget(ScreenCreateSets(sm, name='create_sets'))
        sm.add_widget(ScreenTranslator(sm, name='translator'))

        return sm


if __name__ == "__main__":
    sm = ScreenManager()
    MainApp().run()
