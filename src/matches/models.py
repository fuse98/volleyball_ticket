from django.db import models
from users.models import CustomUser


class Stadium(models.Model):
    title = models.CharField(max_length=100)
    address = models.TextField()
    lat = models.FloatField()
    long = models.FloatField()

    created_by = models.ForeignKey(CustomUser, on_delete=models.PROTECT)
    created_at = models.DateTimeField(auto_now_add=True)


class SeatingArrangment(models.Model):
    stadium = models.ForeignKey(Stadium, on_delete=models.PROTECT)


class Seat(models.Model):
    column = models.CharField(max_length=5)
    row = models.CharField(max_length=5)
    section = models.CharField(max_length=5, null=True, blank=True)

    # position for visual represntation
    pos_x = models.IntegerField()
    pos_y = models.IntegerField()

    seating_arrangment = models.ForeignKey(
        SeatingArrangment,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='seats',
    )

    def name(self):
        name = ''
        if self.section is not None:
            name += f'sec: {self.section}, '
        
        name += f'row: {self.row}, column: {self.column}'
        return name
