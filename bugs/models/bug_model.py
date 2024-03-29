from django.db import models

from django.urls import reverse

from django.core.validators import FileExtensionValidator

import uuid
from django.utils.timezone import now

from project.models import Project
from userprofile.models import Profile
from utilities import *
import cloudinary


class Bug(models.Model):
    uuid = models.UUIDField(
        verbose_name="ID",
        default=uuid.uuid4,
        editable=False,
        unique=True,
        blank=False,
        null=False,
        primary_key=True,
    )
    project = models.ForeignKey(
        Project,
        blank=False,
        null=False,
        editable=False,
        verbose_name="Found In Project",
        on_delete=models.CASCADE,
    )
    title = models.CharField(
        max_length=100, verbose_name="Title", null=False, blank=False
    )
    description = models.TextField(
        verbose_name="Describe bug/feature in a paragraph",
        blank=True,
        null=True,
    )
    deadline = models.DateField(verbose_name="Bug Deadline", default=now, blank=True)
    type = models.CharField(
        max_length=20,
        verbose_name="Is it a Feature or Bug",
        choices=BUG_TYPE,
        null=False,
        blank=False,
        default=BUG_TYPE[0][0],
    )
    status = models.CharField(
        max_length=20,
        verbose_name="Bug/Feature Status",
        choices=BUG_STATUS,
        null=False,
        blank=False,
        default=NEW,
    )
    creator = models.ForeignKey(
        Profile,
        verbose_name="Creator of Bug/Feature",
        null=False,
        blank=False,
        limit_choices_to={"designation": QAENGINEER},
        on_delete=models.PROTECT,
        related_name="creator_qae",
    )
    assigned_to = models.ForeignKey(
        Profile,
        verbose_name="Developer Assigned To",
        on_delete=models.DO_NOTHING,
        blank=True,
        null=True,
        limit_choices_to={"designation": DEVELOPER},
        related_name="developer_assigned",
    )

    screenshot = cloudinary.models.CloudinaryField(
        "Image",
        null=True,
        blank=True,
        validators=[FileExtensionValidator(["png", "gif"])],
    )

    class Meta:
        unique_together = (("project", "title"),)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("detail-bug", kwargs={"pk": self.pk})
