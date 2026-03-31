# uuid generates universally unique identifiers — imported but available for future use (e.g., primary keys)
import uuid

from datetime import datetime
from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _


# Create your models here.

# Concert maps to a database table storing information about a single concert event
class Concert(models.Model):
    concert_name = models.CharField(max_length=255)
    duration = models.IntegerField()
    city = models.CharField(max_length=255)
    date = models.DateField(default=datetime.now)

    # __str__ controls what is displayed when a Concert object is printed or shown in the Django admin
    def __str__(self):
        # Returns the concert name so the object is human-readable instead of showing "Concert object(1)"
        return self.concert_name


# ConcertAttending tracks whether a specific user is attending a specific concert
class ConcertAttending(models.Model):

    # AttendingChoices is an inner enum class that defines the valid values for the attending field
    # models.TextChoices makes Django enforce that only these values can be stored in the column
    class AttendingChoices(models.TextChoices):
        # NOTHING is the neutral/default state — stored as "-" in the database, displayed as "-"
        NOTHING = "-", _("-")
        # NOT_ATTENDING means the user has said they will not attend
        NOT_ATTENDING = "Not Attending", _("Not Attending")
        # ATTENDING means the user has confirmed they will attend
        ATTENDING = "Attending", _("Attending")

    # ForeignKey creates a many-to-one relationship: many attendance records can point to one Concert
    # null=True allows the database column to be NULL if no concert is linked
    # on_delete=models.CASCADE deletes this record automatically if the linked Concert is deleted
    # related_name="attendee" lets you do concert.attendee.all() to get all attendees for a concert
    concert = models.ForeignKey(
        Concert, null=True, on_delete=models.CASCADE, related_name="attendee"
    )
    # ForeignKey to Django's built-in User model — links this attendance record to a specific user
    # null=True allows the record to exist without a user (e.g., anonymous)
    # on_delete=models.CASCADE deletes this record if the linked User account is deleted
    user = models.ForeignKey(User, null=True, on_delete=models.CASCADE)
    # Stores the attendance status using the choices defined in AttendingChoices
    # max_length=100 sets the column size; choices restricts valid input to the enum values
    # default=AttendingChoices.NOTHING sets the initial value to "-" when no choice is made
    attending = models.CharField(
        max_length=100,
        choices=AttendingChoices.choices,
        default=AttendingChoices.NOTHING,
    )

    # Meta is an inner class that gives Django extra configuration options for this model
    class Meta:
        # unique_together enforces a database-level constraint: one user can only have one
        # attendance record per concert — prevents duplicate rows for the same (concert, user) pair
        unique_together = ['concert', 'user']

    # Returns the attending status string when the object is printed or shown in the admin
    def __str__(self):
        return self.attending


# Photo is a read-only model that maps to an existing table managed by the Pictures microservice
class Photo(models.Model):
    id = models.IntegerField(primary_key=True)
    pic_url = models.CharField(max_length=1000)
    event_country = models.CharField(max_length=255)
    event_state = models.CharField(max_length=255)
    event_city = models.CharField(max_length=255)
    event_date = models.DateField(default=datetime.now)

    # Meta gives Django extra configuration for this model
    class Meta:
        # managed=False tells Django NOT to create, modify, or delete this table via migrations
        # The table is owned and managed by the external Pictures microservice, not this Django app
        managed = False

    # Returns the photo URL when the object is printed or shown in the admin
    def __str__(self):
        return self.pic_url


# Song is a read-only model that maps to an existing table managed by the Songs microservice
class Song(models.Model):
    id = models.IntegerField(primary_key=True)
    title = models.CharField(max_length=255)
    lyrics = models.TextField()

    # Meta gives Django extra configuration for this model
    class Meta:
        # managed=False tells Django NOT to create, modify, or delete this table via migrations
        # The table is owned and managed by the external Songs microservice, not this Django app
        managed = False

    # Returns the song title when the object is printed or shown in the admin
    def __str__(self):
        return self.title