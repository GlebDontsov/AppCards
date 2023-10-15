import os

from colorama import init
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM

if not os.path.exists('../model/en-ru-local'):
    model_name = 'Helsinki-NLP/opus-mt-en-ru'

    tokenizer = AutoTokenizer.from_pretrained(model_name)
    model = AutoModelForSeq2SeqLM.from_pretrained(model_name)

    tokenizer.save_pretrained('../model/en-ru-local')
    model.save_pretrained('../model/en-ru-local')

init()
tokenizer = AutoTokenizer.from_pretrained('model/en-ru-local')
model = AutoModelForSeq2SeqLM.from_pretrained('model/en-ru-local')


def translate_phrase_to_ru(phrase: str) -> str:
    """
    Перевод фраз из файла, вывод перевода в терминал.
    Функция возвращает переведенную фразу.
    """
    inputs = tokenizer(phrase, return_tensors="pt")
    output = model.generate(**inputs, max_new_tokens=100)
    out_text = tokenizer.batch_decode(output, skip_special_tokens=True)

    if out_text[0] == "ПРАКТИЧЕСКИЕ ПРАКТИКИ":
        return "Change the translation language"
    return out_text[0]
