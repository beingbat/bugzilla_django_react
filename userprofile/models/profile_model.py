from django.urls import reverse
from utilities.constants import USER_TYPES, MANAGER, DEVELOPER

from django.db import models
from django.contrib.auth.models import User
from project.models import Project


class Profile(models.Model):

    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    designation = models.CharField(
        max_length=10,
        choices=USER_TYPES + ((MANAGER, "Manager"),),
        default=DEVELOPER,
    )

    project = models.ForeignKey(
        Project,
        on_delete=models.DO_NOTHING,
        related_name="assigned_project",
        blank=True,
        null=True,
    )

    def __str__(self):
        return self.user.username

    def get_absolute_url(self):
        return reverse("user-detail", args=[str(self.user.pk)])
