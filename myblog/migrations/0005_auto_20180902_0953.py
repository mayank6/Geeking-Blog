# Generated by Django 2.0.7 on 2018-09-02 04:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myblog', '0004_auto_20180901_2316'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='tag',
            field=models.ManyToManyField(blank=True, related_name='posttag', to='myblog.Tag'),
        ),
    ]