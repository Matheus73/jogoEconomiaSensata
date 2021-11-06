# Generated by Django 3.2.8 on 2021-11-06 04:10

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='country',
            field=models.CharField(default=None, max_length=100),
        ),
        migrations.CreateModel(
            name='Bloc',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('leader1', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='leader1', to='user.user')),
                ('leader2', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='leader2', to='user.user')),
                ('leader3', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='leader3', to='user.user')),
                ('leader4', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='leader4', to='user.user')),
            ],
        ),
    ]
