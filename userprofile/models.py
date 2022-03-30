from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse

USER_TYPES = (
  ('dev', 'Developer'),
  ('qae', 'Quality Assurance Engineer'),
)


class Profile(models.Model):

  user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
  designation = models.CharField(max_length=3, choices = USER_TYPES+(('man', 'Manager'),), default='dev')

  def __str__(self):
    return self.user.username

  def get_absolute_url(self):
        return reverse('user-detail', args=[str(self.user.pk)])
