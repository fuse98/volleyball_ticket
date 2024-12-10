import secrets
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


class TicketFactor(models.Model):
    class Status(models.IntegerChoices):
        WAITING_FOR_PAYMENT = 0, 'Waiting for payment'
        PAYED = 1, 'Payed'
        CANCELED = 2, 'Canceled'

    # A human readable code for verifying tickets purchase
    verification_code = models.CharField(max_length=10, unique=True)
    amount = models.PositiveIntegerField()
    status = models.IntegerField(choices=Status.choices, default=Status.WAITING_FOR_PAYMENT)
    created_at = models.DateTimeField(auto_now_add=True)
    buyer = models.ForeignKey(CustomUser, on_delete=models.PROTECT)

    @classmethod
    def generate_unique_verification_code(cls):
        while True:
            code = secrets.randbelow(10**10)
            code_str = f"{code:010}"
            if not cls.objects.filter(verification_code=code_str).exists():
                return code_str


class Ticket(models.Model):
    class Status(models.IntegerChoices):
        AVAILABLE = 0, 'Available'
        RESERVED_FOR_PAYMENT = 1, 'Reserved for payment'
        SOLD = 2, 'Sold'

    match_instance = models.ForeignKey(Match, on_delete=models.PROTECT, related_name='tickets')
    seat = models.ForeignKey(Seat, on_delete=models.PROTECT)
    team = models.ForeignKey(Team, null=True, on_delete=models.SET_NULL)
    price = models.PositiveIntegerField()
    status = models.IntegerField(choices=Status.choices, default=Status.AVAILABLE)

    ticket_factor = models.ForeignKey(
        TicketFactor,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='tickets'
    )
