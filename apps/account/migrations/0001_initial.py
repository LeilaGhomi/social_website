# Generated by Django 3.1.6 on 2021-04-29 21:45

import apps.account.managers
import common.validators
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import django_extensions.db.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('first_name', models.CharField(blank=True, max_length=30, null=True)),
                ('last_name', models.CharField(blank=True, max_length=150, null=True)),
                ('gender', models.CharField(blank=True, choices=[('F', 'female'), ('M', 'male')], max_length=1, verbose_name='gender')),
                ('email', models.EmailField(blank=True, max_length=254, null=True, unique=True, validators=[common.validators.email_regex_validator])),
                ('phone_number', models.CharField(blank=True, max_length=15, null=True, unique=True, validators=[common.validators.mobile_length_validator, common.validators.mobile_validator])),
                ('bio', models.TextField(blank=True)),
                ('website', models.CharField(blank=True, max_length=100, null=True)),
                ('is_active', models.BooleanField(default=True)),
                ('is_superuser', models.BooleanField(default=False, verbose_name='superuser')),
                ('is_staff', models.BooleanField(default=False, verbose_name='staff')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now)),
                ('reg_type', models.CharField(choices=[('email', 'email'), ('sms', 'sms')], max_length=5, verbose_name='registration type')),
                ('otp', models.PositiveIntegerField(blank=True, null=True)),
                ('otp_create_time', models.DateTimeField(auto_now=True)),
                ('pro_pic', models.ImageField(blank=True, null=True, upload_to='images', verbose_name='profile picture')),
                ('username', models.CharField(max_length=100, unique=True)),
                ('slug', django_extensions.db.fields.AutoSlugField(blank=True, editable=False, populate_from=['username'], unique=True)),
                ('friends', models.ManyToManyField(blank=True, to=settings.AUTH_USER_MODEL)),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.Group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.Permission', verbose_name='user permissions')),
            ],
            options={
                'verbose_name': 'account',
                'verbose_name_plural': 'users',
            },
            managers=[
                ('objects', apps.account.managers.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name='FriendRequest',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('from_user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='from_user', to=settings.AUTH_USER_MODEL)),
                ('to_user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='to_user', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Following',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('followed', models.ManyToManyField(related_name='followed', to=settings.AUTH_USER_MODEL)),
                ('follower', models.ManyToManyField(related_name='follower', to=settings.AUTH_USER_MODEL)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
