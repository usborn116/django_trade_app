# Generated by Django 5.0 on 2023-12-21 22:57

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='League',
            fields=[
                ('name', models.CharField(max_length=50)),
                ('year', models.IntegerField()),
                ('id', models.IntegerField(primary_key=True, serialize=False)),
            ],
        ),
        migrations.CreateModel(
            name='Player',
            fields=[
                ('name', models.CharField(max_length=50)),
                ('id', models.IntegerField(primary_key=True, serialize=False)),
                ('position', models.CharField(max_length=10)),
                ('league', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='trade_app.league')),
            ],
        ),
        migrations.CreateModel(
            name='Team',
            fields=[
                ('name', models.CharField(max_length=50)),
                ('id', models.IntegerField(primary_key=True, serialize=False)),
                ('league', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='trade_app.league')),
            ],
        ),
        migrations.CreateModel(
            name='StatCard',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('pts', models.FloatField()),
                ('blk', models.FloatField()),
                ('stl', models.FloatField()),
                ('ast', models.FloatField()),
                ('oreb', models.FloatField()),
                ('dreb', models.FloatField()),
                ('to', models.FloatField()),
                ('fga', models.FloatField()),
                ('fgm', models.FloatField()),
                ('ftm', models.FloatField()),
                ('fta', models.FloatField()),
                ('m3p', models.FloatField(verbose_name='3PTM')),
                ('a3p', models.FloatField(verbose_name='3PTA')),
                ('afg', models.FloatField(verbose_name='AFG%')),
                ('ato', models.FloatField(verbose_name='A/TO')),
                ('ft_per', models.FloatField(verbose_name='FT%')),
                ('league', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='trade_app.league')),
                ('player', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='trade_app.player')),
                ('team', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='trade_app.team')),
            ],
        ),
        migrations.AddField(
            model_name='player',
            name='team',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='trade_app.team'),
        ),
    ]
