# Generated by Django 2.2.24 on 2022-04-04 09:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('userprofile', '0002_profile_project'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='designation',
            field=models.CharField(choices=[('developer', 'Developer'), ('qaengineer', 'Quality Assurance Engineer'), ('manager', 'Manager')], default='developer', max_length=10),
        ),
    ]
