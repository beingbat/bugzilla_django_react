from django.db import models

class Project(models.Model):
  name = models.CharField(
    max_length=50,
    verbose_name="Project Name",
    )

  description = models.TextField(
    max_length=250,
    verbose_name="Project Description",
    )

  def __str__(self):
    return self.name
