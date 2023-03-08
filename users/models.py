from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.db import models


class UserManager(BaseUserManager):
    def create_user(self, email, password=None):
        """
        Creates and saves a User with the given email and password.
        """
        if not email:
            raise ValueError("Invalid Email")
        if not password:
            raise ValueError("Invalid password")

        user = self.model(
            email=self.normalize_email(email),

        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_staffuser(self, email, password):
        """
        Creates and saves a staff user with the given email and password.
        """
        user = self.create_user(
            email,
            password=password,
        )
        user.staff = True
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password):
        """
        Creates and saves a superuser with the given email and password.
        """
        user = self.create_user(
            email,
            password=password
        )
        user.staff = True
        user.admin = True
        user.save(using=self._db)
        return user


class User(AbstractBaseUser):
    user_type = models.ForeignKey("UserType", verbose_name="user type", on_delete=models.CASCADE, null=True)
    email = models.EmailField(max_length=255, unique=True)
    date_of_birth = models.DateField(blank=True, null=True)
    gender = models.CharField(max_length=20, verbose_name="gender")
    is_active = models.BooleanField(default=True)  # can login
    contact_number = models.CharField(max_length=50, blank=True)
    sms_notification_active = models.BooleanField(default=False)
    email_notification_active = models.BooleanField(default=False)
    user_image = models.ImageField(upload_to="images/users", blank=True)

    registration_date = models.DateTimeField(auto_now_add=True)
    staff = models.BooleanField(default=False)  # can login
    admin = models.BooleanField(default=False)  # can login

    USERNAME_FIELD = "email"
    objects = UserManager()

    def save(self, *args, **kwargs):
        # extra logic here
        super(User, self).save(*args, **kwargs)

    def __str__(self):  # __unicode__ on Python 2
        return self.email

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return True

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True

    @property
    def is_staff(self):
        "Is the user a member of staff?"
        return self.staff


class UserType(models.Model):
    user_type_name = models.CharField(max_length=20)
    has_additional_profile = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.id} - {self.user_type_name}"


class UserLog(models.Model):
    user_account = models.OneToOneField(User, on_delete=models.CASCADE, related_name="user_account_log")
    last_job_apply_date = models.DateField(verbose_name="last job apply date", null=True)

    def __str__(self):
        return f"{self.last_job_apply_date}"
