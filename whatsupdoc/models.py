from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User


class Tickets(models.Model):
    NEW = 'New'
    IN_PROGESS = 'In Progress'
    DONE = 'Done'
    INVALID = 'Invalid'
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
        max_length=20,
        choices=TICKET_STATUS_CHOICES,
        default=NEW
    )
    created_by = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='created_by+'
    )
    assigned_by = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        default=None,
        null=True,
        blank=True,
        related_name='assigned_by+'
    )
    completed_by = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        default=None,
        null=True,
        related_name='completed_by+'
    )

    def __str__(self):
        return self.title
