from django.db import models
from django.contrib.auth.models import User


class Question(models.Model):
    LEVELS = (
        (0, 'basic'),
        (1, 'medium'),
        (2, 'hard'),
        (3, 'extreme'),
    )
    TYPES = (
        (0, 'single'),
        (1, 'multi'),
    )
    qlevel = models.IntegerField(choices=LEVELS, db_index=True)
    qgroup = models.IntegerField(db_index=True)
    qtype = models.IntegerField(choices=TYPES)
    question = models.TextField()
    owner = models.ForeignKey(
        User, default=None, blank=True, null=True,
        on_delete=models.SET_NULL
    )
    class Meta:
        ordering = ['-qlevel', 'qgroup']

    def __str__(self):
        return 'level: {}, {}'.format(self.get_level_display, self.question)

    @property
    def no_answers(self):
        return ' {} ({})'.format(self.answers.count(), sum([1 for item in self.answers.all() if item.correct]))

    @classmethod
    def groupList(cls):
        output = []
        list = cls.objects.order_by('qlevel', 'qgroup').distinct('qlevel', 'qgroup')
        for item, item_name in cls.LEVELS:
            if list.filter(qlevel=item):
                output.append((item_name, list.filter(qlevel=item).values_list('qgroup', flat=True), item))
        return output

class Answer(models.Model):
    quiz = models.ForeignKey(Question, related_name="answers", on_delete=models.CASCADE)
    answer = models.CharField(max_length=256)
    correct = models.BooleanField(default=False)
