# Generated by Django 3.0.7 on 2020-06-20 08:03

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('referral', '0004_auto_20200618_2221'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='referrer',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='referred', to='referral.UserProfile'),
        ),
    ]
