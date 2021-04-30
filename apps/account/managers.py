from django.contrib.auth.base_user import BaseUserManager


class UserManager(BaseUserManager):
    use_in_migrations = True

    def _create_user(self, email, password, reg_type, phone_number, **extra_fields):
        """
        Creates and saves a User with the given email or phone number and password.
        """
        if not reg_type and extra_fields.get('is_superuser') is True:
            user = self.model(**extra_fields)
            user.set_password(password)
            user.save(using=self._db)
            return user
        elif not reg_type:
            raise ValueError('choose one')
        elif reg_type == 'email' and not email:
            raise ValueError('The given email must be set')
        elif reg_type == 'sms' and not phone_number:
            raise ValueError('The given phone number must be set')
        elif reg_type == 'email' and email and extra_fields.get('is_superuser') is not True:
            email = self.normalize_email(email)
            user = self.model(username=email, **extra_fields)
            user.set_password(password)
            user.save(using=self._db)
            return user

        elif reg_type == 'sms' and phone_number:
            user = self.model(username=phone_number, **extra_fields)
            print(phone_number)
            user.set_password(password)
            user.save(using=self._db)
            print(user.username)
            return user

    def create_user(self, email, reg_type, phone_number, password=None, **extra_fields):
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, password, reg_type, phone_number, **extra_fields)

    def create_superuser(self, email=None, password=None, reg_type=None, phone_number=None, **extra_fields):
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_staff', True)

        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(email, password, reg_type, phone_number, **extra_fields)
