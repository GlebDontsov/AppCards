import os.path

from colorama import init

from transformers import AutoTokenizer, AutoModelForSeq2SeqLM

if not os.path.exists('model/ru-en-local'):
    model_name = "Helsinki-NLP/opus-mt-ru-en"
    # Загружаем предобученную модель и токенизатор для задачи машинного перевода с русского на английский
    tokenizer = AutoTokenizer.from_pretrained(model_name)
    model = AutoModelForSeq2SeqLM.from_pretrained(model_name)

    # Сохраняем загруженный токенизатор и модель в локальной директории 'model/ru-en-local'
    tokenizer.save_pretrained('model/ru-en-local')
    model.save_pretrained('model/ru-en-local')

init()  # инициализируем colorama

# Загружаем сохраненный токенизатор и модель для задачи машинного перевода из локальной директории 'model/ru-en-local'
tokenizer = AutoTokenizer.from_pretrained('model/ru-en-local')
model = AutoModelForSeq2SeqLM.from_pretrained('model/ru-en-local')


def translate_phrase_to_eng(phrase: str) -> str:
    """
    Перевод фраз из файла, вывод перевода в терминал.
    Функция возвращает переведенную фразу.
    """
    inputs = tokenizer(phrase, return_tensors="pt")
    output = model.generate(**inputs, max_new_tokens=100)
    out_text = tokenizer.batch_decode(output, skip_special_tokens=True)

    if out_text[0] == "ПРАКТИЧЕСКИЕ ПРАКТИКИ":
        return "Измените язык перевода"

    return out_text[0]
