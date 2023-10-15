import torch

language_ru = 'ru'
model_id_ru = 'v3_1_ru'
model_ru, example_text_ru = torch.hub.load(repo_or_dir='snakers4/silero-models',
                                           model='silero_tts',
                                           language=language_ru,
                                           speaker=model_id_ru,
                                           trust_repo=True)

language_en = 'en'
model_id_en = 'v3_en'
model_en, example_text_en = torch.hub.load(repo_or_dir='snakers4/silero-models',
                                           model='silero_tts',
                                           language=language_en,
                                           speaker=model_id_en,
                                           trust_repo=True)
