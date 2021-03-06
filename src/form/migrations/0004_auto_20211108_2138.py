# Generated by Django 3.2.8 on 2021-11-09 00:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('form', '0003_poll'),
    ]

    operations = [
        migrations.AlterField(
            model_name='answer',
            name='result_agricultura',
            field=models.FloatField(default=0, null=True),
        ),
        migrations.AlterField(
            model_name='answer',
            name='result_ambiente',
            field=models.FloatField(default=0, null=True),
        ),
        migrations.AlterField(
            model_name='answer',
            name='result_bancoCentral',
            field=models.FloatField(default=0, null=True),
        ),
        migrations.AlterField(
            model_name='answer',
            name='result_desenvolvimento',
            field=models.FloatField(default=0, null=True),
        ),
        migrations.AlterField(
            model_name='answer',
            name='result_economia',
            field=models.FloatField(default=0, null=True),
        ),
        migrations.AlterField(
            model_name='answer',
            name='result_educacao',
            field=models.FloatField(default=0, null=True),
        ),
        migrations.AlterField(
            model_name='answer',
            name='result_infraestrutura',
            field=models.FloatField(default=0, null=True),
        ),
        migrations.AlterField(
            model_name='answer',
            name='result_saude',
            field=models.FloatField(default=0, null=True),
        ),
        migrations.AlterField(
            model_name='poll',
            name='against',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='poll',
            name='pros',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='poll',
            name='votes',
            field=models.JSONField(default={'votes': []}),
        ),
    ]
