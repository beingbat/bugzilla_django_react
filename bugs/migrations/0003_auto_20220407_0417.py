# Generated by Django 2.2.24 on 2022-04-07 04:17

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('bugs', '0002_auto_20220404_0940'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bug',
            name='project',
            field=models.ForeignKey(editable=False, on_delete=django.db.models.deletion.CASCADE, to='project.Project', verbose_name='Found In Project'),
        ),
        migrations.AlterField(
            model_name='bug',
            name='status',
            field=models.CharField(choices=[('start', 'New'), ('in_progress', 'In Progress'), ('completed', 'Resolved')], default='start', max_length=20, verbose_name='Bug/Feature Status'),
        ),
    ]
