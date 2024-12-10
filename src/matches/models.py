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


class Team(models.Model):
    name = models.CharField(max_length=100)


class Match(models.Model):
    class Status(models.IntegerChoices):
        DRAFT = 0, 'Draft'
        PUBLISHED = 1, 'Published',

    team_a = models.ForeignKey(Team, on_delete=models.PROTECT, related_name='matches_as_team_a')
    team_b = models.ForeignKey(Team, on_delete=models.PROTECT, related_name='matches_as_team_b')

    seating_arrangement = models.ForeignKey(SeatingArrangment, on_delete=models.PROTECT)

    match_datetime = models.DateTimeField()
    status = models.IntegerField(choices=Status.choices, default=Status.DRAFT)


class Ticket(models.Model):
    match_instance = models.ForeignKey(Match, on_delete=models.PROTECT, related_name='tickets')
    seat = models.ForeignKey(Seat, on_delete=models.PROTECT)
    team = models.ForeignKey(Team, null=True, on_delete=models.SET_NULL)
    price = models.PositiveIntegerField()
