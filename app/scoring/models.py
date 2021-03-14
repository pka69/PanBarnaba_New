from django.db import models
from django.contrib.auth.models import User
# Create your models here.


class Score(models.Model):
    user = models.ForeignKey(User, related_name='scorings', on_delete=models.CASCADE)
    s_date = models.DateTimeField(auto_now_add=True)
    game = models.CharField(max_length=128, db_index=True)
    game_id = models.TextField(db_index=True)
    s_result = models.IntegerField(default=0)
    s_time = models.TimeField()

    class Meta:
        ordering = ['-s_result', 's_time']
        unique_together = (("user", "game", "game_id"),)

    def __str__(self):
        return '{} - {}/{} - {} : {:>d5.2} : {}'.format(
            self.user.username,
            self.game,
            self.game_id,
            self.s_date.strftime('%b %d %Y %H:%M:%S'),
            self.result,
            self.s_time.strftime('%H:%M:%S')
        )

    @classmethod
    def checkResultPosition(cls, game, game_id, s_result, s_time):
        results = cls.objects.filter(game=game).filter(game_id=game_id)
        output = []
        position = results.count() + 1
        for no, item in enumerate(results, 1):
            output.append([
                no,
                item.user.username[:25],
                item.s_result,
                item.s_time.strftime('%H:%M:%S')
            ])
            if (position > no) and (s_result >= item.s_result) and(s_time <= item.s_time):
                position = no
        return position, results.count(), output[:10]
