import random
import sounddevice as sd
import time

from gtts import gTTS
from playsound import playsound
from utils.model_speakers import model_ru, model_en


def set_screen(name_screen, sm):
    sm.current = name_screen


def create_screen_train(screen, directory, sm):
    from screens.train import ScreenTrain
    sm.add_widget(ScreenTrain(sm, directory, screen.text, name='train'))
    sm.current = 'train'


def create_screen_update(screen, directory, sm):
    from screens.update import ScreenUpdate
    sm.add_widget(ScreenUpdate(sm, screen, directory, name='update'))
    sm.current = 'update'


def back(remove_screen, name_screen, sm):
    sm.current = remove_screen
    sm.remove_widget(sm.get_screen(name_screen))


def sets_update(sets, sm):
    if sets == 'sets':
        from screens.sets import ScreenSets
        sm.remove_widget(sm.get_screen('sets'))
        sm.add_widget(ScreenSets(sm, name='sets'))
    elif sets == 'star':
        from screens.stars import ScreenStar
        sm.remove_widget(sm.get_screen('star'))
        sm.add_widget(ScreenStar(sm, ame='star'))


def voice(x, lang='en'):
    if x:
        if lang == 'ru':
            tts = gTTS(text=f'{x}', lang='ru')
        else:
            tts = gTTS(text=f'{x}', lang='en')
        tts.save("cache/voice_word.mp3")
        playsound("cache/voice_word.mp3")


def change_word(word, translation, words):
    word_key = random.choice(list(words))
    word.text = f"{words[word_key]['word']}"
    translation.text = f"{words[word_key]['translation']}"


def speak(what, lang='en'):
    put_accent = True
    put_yo = True
    sample_rate = 48000

    if lang == 'ru':
        audio = model_ru.apply_tts(text=what + "..",
                                   speaker='aidar',
                                   sample_rate=sample_rate,
                                   put_accent=put_accent,
                                   put_yo=put_yo)
    else:
        audio = model_en.apply_tts(text=what + "..",
                                   speaker='en_116',
                                   sample_rate=sample_rate,
                                   put_accent=put_accent,
                                   put_yo=put_yo)

    sd.play(audio, sample_rate)
    time.sleep((len(audio) / sample_rate))
    sd.stop(ignore_errors=True)

