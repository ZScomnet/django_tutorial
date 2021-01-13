from django.db import models
from django.contrib.auth.models import (BaseUserManager, AbstractBaseUser)

# email == 인증한 이메일
# token == kakao or google?
# ID == 로그인 할 떄 쓰는 ID
# name == 닉네임
# password == 로그인 할 떄 쓰는 password
class UserManager(BaseUserManager):
    def create_user(self, email, name, password=None):
        if not email:
            raise ValueError('Users must have an email address')

        user = self.model(
            email=self.normalize_email(email),
            name=name,
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, name, password):
        user = self.create_user(
            email=email,
            password=password,
            name=name,
        )
        user.is_admin = True
        user.save(using=self._db)
        return user


class User(AbstractBaseUser):
    email = models.EmailField(
        verbose_name='email',
        max_length=255,
        unique=True,
    )
    name = models.CharField(
    	verbose_name='name',
    	max_length=100,
    	unique=True,
    )
    ID = models.CharField(
    	verbose_name='ID',
    	max_length=100,
    	unique=True
    )
    token = models.CharField(
    	verbose_name='token',
    	max_length=100,
    	unique=False,
    )

    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name']

    def __str__(self):
        return self.name

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True

    @property
    def is_staff(self):
        return self.is_admin

# Create your models here.
