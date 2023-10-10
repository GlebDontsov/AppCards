# AppCards

Это приложение предназначено для изучения английского языка через использование карточек со словами, возможностью перевода текста с русского на английский и с английского на русский, а также озвучкой слов. В приложении доступно около 50 наборов и более 5000 слов для изучения.

## Основные функции приложения:

- Изучение слов по карточкам: Приложение предоставляет наборы карточек со словами на английском языке. Вы можете перелистывать карточки, изучая новые слова и их значения.
-  Перевод текста: Приложение позволяет переводить текст с русского на английский и с английского на русский.
-  Озвучка слов: Приложение предоставляет возможность озвучивания слов. Вы можете прослушать произношение слов на английском языке, чтобы улучшить свои навыки произношения.
-  Наборы и словари: Приложение содержит около 50 различных наборов слов для изучения. Вы можете выбрать набор, который наиболее соответствует вашим потребностям и интересам.
-  Словарь: Где вы можете изучить новые слова и их произношение.

## Локальный запуск приложения

Для локального развертывания данного приложения следуйте следующим шагам:

1. Установите все зависимости из файла requirements.txt. Это можно сделать с помощью команды:
```
pip install -r requirements.txt`
```
2. Раскомментируйте первые 10 строк в файлах `utils/translate_eng_to_ru.py` и `utils/translate_ru_to_eng.py`. Эти строки отвечают за загрузку моделей перевода. Запустите код этих файлов, чтобы загрузить соответствующие модели.
   
3. Запустите файл main.py, чтобы запустить приложение. Вы можете сделать это с помощью следующей команды:
```
python3 -m main.py
```
Теперь приложение будет запущено локально и будет готово к использованию.



