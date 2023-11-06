import uuid

from slugify import slugify


# Будь осторожен с циклическими импортами
def generate_slug(text):
    """Генерирует уникальное значение для поля slug на основе переданного текста"""
    return slugify(f'{text}-{uuid.uuid4()}')
