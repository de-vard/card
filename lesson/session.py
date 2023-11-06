from django.conf import settings


class LessonSession:
    def __init__(self, request):
        """Инициализация сессию урока"""
        self.session = request.session  # текущий сеанс сохраняется
        if 'lesson' not in self.session:  # проверяем есть ли в сессии словарь со словами
            self.session['lesson'] = []  # добавляем словарь
        self.lesson = self.session['lesson']

    def add(self, word):
        """Добавить слово в сохраненные."""
        word_id = str(word.id)
        if word_id not in self.session['lesson']:  # проверяем на вхождение слова в сессию, если слово не входит
            self.session['lesson'].append(word_id)
            self.save()

    def save(self):
        # пометить сеанс как "измененный", чтобы обеспечить его сохранение
        self.session.modified = True

    def remove(self, word):
        """Удалить слово из урока."""
        word_id = str(word.id)
        if word_id in self.session['lesson']:
            self.session['lesson'].remove(word_id)
            self.save()

    def clear(self):
        # TODO: проверь нужен ли этот код, так как смылс очищать ссесию

        # удалить прогресс пользователя из сеанса
        del self.session[settings.LESSON_SESSION_ID]
        self.save()
