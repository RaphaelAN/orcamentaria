# Generated by Django 3.0.8 on 2020-07-31 14:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('budgeter', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='transaction',
            name='title',
            field=models.CharField(default='test', max_length=200),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='user',
            name='budget_start_day',
            field=models.IntegerField(choices=[(1, '1'), (2, '2'), (3, '3'), (4, '4'), (5, '5'), (6, '6'), (7, '7'), (8, '8'), (9, '9'), (10, '10'), (11, '11'), (12, '12'), (13, '13'), (14, '14'), (15, '15'), (16, '16'), (17, '17'), (18, '18'), (19, '19'), (20, '20'), (21, '21'), (22, '22'), (23, '23'), (24, '24'), (25, '25'), (26, '26'), (27, '27'), (28, '28')], default=1),
        ),
    ]
