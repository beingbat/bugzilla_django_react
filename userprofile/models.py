from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.urls import reverse

USER_TYPES = (
  ('dev', 'Developer'),
  ('qae', 'Quality Assurance Engineer'),
)


class Profile(models.Model):


  USERS_TYPES = (
    ('dev', 'Developer'),
    ('qae', 'Quality Assurance Engineer'),
    ('man', 'Manager'),
  )

  user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
  designation = models.CharField(max_length=3, choices = USERS_TYPES, default='dev')

  def __str__(self):
    return self.user.username

  def get_absolute_url(self):
        return reverse('user-detail', args=[str(self.user.pk)])



# @receiver(post_save, sender=User)
# def create_user_profile(sender, instance, created, **kwargs):
#   if created:
#     Profile.objects.create(user=instance)

# @receiver(post_save, sender=User)
# def save_user_profile(sender, instance, **kwargs):
#   instance.profile.save()



