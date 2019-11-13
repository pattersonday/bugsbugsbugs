from django.db import models
from django.utils import timezone


class Tickets(models.Model):
    NEW = 'N'
    IN_PROGESS = 'IP'
    DONE = 'D'
    INVALID = 'IN'
    TICKET_STATUS_CHOICES = [
        (NEW, 'New'),
        (IN_PROGESS, 'In_progress'),
        (DONE, 'Done'),
        (INVALID, 'Invalid'),
    ]
    title = models.CharField(max_length=100)
    post_date = models.DateTimeField(default=timezone.now)
    description = models.TextField()
    ticket_status = models.CharField(
        max_length=2,
        choices=TICKET_STATUS_CHOICES,
        default=NEW
        )

    def __str__(self):
        return self.title
