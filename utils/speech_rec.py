import speech_recognition as sr
from speech_recognition.exceptions import WaitTimeoutError


def recognize_speech(lang='ru'):
    # Создаем объект на основе библиотеки speech_recognition и вызываем метод для определения данных
    r = sr.Recognizer()
    with sr.Microphone() as source:
        # Устанавливаем паузу, чтобы прослушивание, началось лишь по прошествию 1 секунды
        r.pause_threshold = 1
        # используем adjust_for_ambient_noise для удаления посторонних шумов из аудио дорожки
        r.adjust_for_ambient_noise(source, duration=1)
        # Полученные данные записываем в переменную audio, пока мы получили лишь mp3 звук
        try:
            audio = r.listen(source, phrase_time_limit=5)
        except WaitTimeoutError:
            return 'Повторите еще раз, пожалуйста'

    # Распознаем данные из mp3 дорожки.
    try:
        word = r.recognize_google(audio, language=lang)
    except sr.UnknownValueError:
        word = 'Я вас не понял'

    return word
