from django import template
from django.template import TemplateSyntaxError
import string

register = template.Library()

@register.filter(name='censor')
def censor(value):
    if not isinstance(value, str):
        raise TemplateSyntaxError("Censor filter can only be applied to strings.")

    censored_words = ["редиска"]  # Список нецензурных слов
    punctuation = string.punctuation  # Получаем все символы пунктуации

    words = value.split()
    new_words = []

    for word in words:
        # Убираем знаки препинания из слова
        clean_word = ''.join(char for char in word if char not in punctuation)
        # Проверяем, содержит ли слово какое-либо из запрещенных слов в любом регистре
        if clean_word.lower() in censored_words:
            # Оставляем первую букву видимой, остальные заменяем на звездочки
            if len(clean_word) > 1:
                censored_word = clean_word[0] + '*' * (len(clean_word) - 1)
            else:
                censored_word = '*'
            # Восстанавливаем знаки препинания в слове
            censored_word = ''.join(char if char in punctuation else '' for char in word[:-len(clean_word)]) + censored_word
            new_words.append(censored_word)
        else:
            new_words.append(word)
    return ' '.join(new_words)
