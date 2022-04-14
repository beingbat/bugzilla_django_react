from django.urls import reverse

from utilities import constants

from django.db import models
from django.contrib.auth.models import User
from project.models.project import Project


class Profile(models.Model):

    user = models.OneToOneField(
        User, on_delete=models.CASCADE, primary_key=True)
    designation = models.CharField(max_length=10,
                                   choices=constants.USER_TYPES +
                                   ((constants.MANAGER, 'Manager'),),
                                   default=constants.DEVELOPER
                                   )

    project = models.ForeignKey(Project,
                                on_delete=models.DO_NOTHING,
                                related_name='assigned_project',
                                blank=True,
                                null=True)

    def __str__(self):
        return self.user.username

    def get_absolute_url(self):
        return reverse('user-detail', args=[str(self.user.pk)])
