# Generated by Django 5.1.2 on 2024-12-10 10:53

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('matches', '0003_team_match_ticket'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ticket',
            name='match_instance',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='tickets', to='matches.match'),
        ),
    ]