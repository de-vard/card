from rest_framework import serializers

from flashcard.models import FlashCard, Image


class ImageSerializer(serializers.ModelSerializer):
    """Сериализатор для изображений"""

    class Meta:
        model = Image
        fields = ('photo',)


class FlashCardSerializer(serializers.ModelSerializer):
    """Сериализатор для карточек, в котором описаны все необходимые поля."""

    set_image = ImageSerializer(source='image', read_only=True)

    class Meta:
        model = FlashCard
        fields = ('id', 'english_word', 'russian_word', 'transcription', 'set_image', 'image', 'sound', 'lesson')
