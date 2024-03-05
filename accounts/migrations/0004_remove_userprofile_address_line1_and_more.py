# Generated by Django 4.2.7 on 2024-02-24 12:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0003_alter_userprofile_cover_photo_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='userprofile',
            name='address_line1',
        ),
        migrations.RemoveField(
            model_name='userprofile',
            name='address_line2',
        ),
        migrations.AddField(
            model_name='userprofile',
            name='address',
            field=models.CharField(blank=True, max_length=250, null=True),
        ),
        migrations.AlterField(
            model_name='user',
            name='role',
            field=models.PositiveSmallIntegerField(blank=True, choices=[(1, 'Vendor'), (2, 'Customer')], null=True),
        ),
    ]