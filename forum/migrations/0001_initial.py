# Generated by Django 4.0 on 2022-01-26 18:32

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='Question',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Title', models.CharField(max_length=200)),
                ('Body', models.TextField()),
                ('Date_Asked', models.DateTimeField(default=django.utils.timezone.now)),
                ('Asked_By', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='auth.user')),
            ],
        ),
        migrations.CreateModel(
            name='Answer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Body', models.TextField()),
                ('Date_Answered', models.DateTimeField(default=django.utils.timezone.now)),
                ('Answered_By', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='auth.user')),
                ('Question_Answered', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='forum.question')),
            ],
        ),
    ]