from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.db import models
from django.utils.timezone import now
from django_extensions.db.fields import AutoSlugField
from apps.account.managers import UserManager
from common.validators import mobile_length_validator, mobile_validator, email_regex_validator


class User(AbstractBaseUser, PermissionsMixin):
    """
    This class represents a User of the website
    The variables are self-commented.
    """
    first_name = models.CharField(max_length=30, blank=True, null=True)
    last_name = models.CharField(max_length=150, blank=True, null=True)
    gender = models.CharField('gender', max_length=1, choices=[('F', 'female'), ('M', 'male')], blank=True)
    email = models.EmailField(unique=True, validators=[email_regex_validator], blank=True, null=True)
    phone_number = models.CharField(max_length=15, unique=True, validators=[mobile_length_validator, mobile_validator],
                                    blank=True, null=True)
    bio = models.TextField(blank=True)
    website = models.CharField(max_length=100, null=True, blank=True)
    friends = models.ManyToManyField("User", blank=True)
    is_active = models.BooleanField(default=True)
    is_superuser = models.BooleanField('superuser', default=False)
    is_staff = models.BooleanField('staff', default=False)
    date_joined = models.DateTimeField(default=now)
    reg_type = models.CharField(verbose_name='registration type', choices=[('email', 'email'), ('sms', 'sms',)],
                                max_length=5)
    otp = models.PositiveIntegerField(blank=True, null=True)
    otp_create_time = models.DateTimeField(auto_now=True)
    pro_pic = models.ImageField(verbose_name='profile picture', upload_to='images', null=True, blank=True)
    username = models.CharField(max_length=100, unique=True)
    slug = AutoSlugField(populate_from=['username'], unique=True)

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = []
    objects = UserManager()

    class Meta:
        verbose_name = 'account'
        verbose_name_plural = 'users'
        app_label = 'account'

    def get_full_name(self):
        """
        Returns the first_name plus the last_name, with a space in between.
        """

        full_name = '%s %s' % (self.first_name, self.last_name)
        return full_name.strip()

    def get_short_name(self):
        """
        Returns the short name for the account.
        """
        return self.first_name

    def __str__(self):
        """
        override __str__()
        :return: account username
        """
        return self.username

    def save(self, *args, **kwargs):
        if self.reg_type == 'email':
            self.username = self.email
        else:
            self.username = self.phone_number
        super().save(*args, **kwargs)  # Call the "real" save() method.


class Following(models.Model):
    """
    This class represents relationship between Users of the website.
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    follower = models.ManyToManyField(User, related_name="follower")
    followed = models.ManyToManyField(User, related_name="followed")

    @classmethod
    def follow(cls, user, another_account):
        obj, create = cls.objects.get_or_create(user=user)
        obj.follower.add(another_account)
        print("followed")

    @classmethod
    def follow_back(cls, user, another_account):
        obj, create = cls.objects.get_or_create(user=user)
        obj.followed.add(another_account)
        print("followed")

    def __str__(self):
        return self.user.username


class FriendRequest(models.Model):
    """
    Request model
    """
    from_user = models.ForeignKey(User, related_name='from_user', on_delete=models.CASCADE)
    to_user = models.ForeignKey(User, related_name='to_user', on_delete=models.CASCADE)
