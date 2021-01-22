from django.db import models
from django.contrib.auth.models import (BaseUserManager, AbstractBaseUser)

# email == 인증한 이메일
# account_info == kakao or google etc..
# ID == 로그인 할 떄 쓰는 ID
# name == 닉네임
# password == 로그인 할 떄 쓰는 password
# tel == 연락처
# access_token == 인증 계정 프로필 token
class UserManager(BaseUserManager):
    def create_user(self, email, username, password=None):
        if not email:
            raise ValueError('Users must have an email address')

        user = self.model(
            email=self.normalize_email(email),
            username=username,
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, username, password):
        user = self.create_user(
            email=email,
            password=password,
            username=username,
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
    username = models.CharField(
    	verbose_name='username',
    	max_length=100,
    	unique=True,
    )
    ID = models.CharField(
    	verbose_name='ID',
    	max_length=100,
    	unique=True
    )
    access_token = models.CharField(
    	verbose_name='access_token',
    	max_length=100,
    	unique=True,
    )
    account_info = models.CharField(
    	verbose_name='account_info',
    	max_length=50,
    	unique=False,
    )
    tel = models.CharField(
    	verbose_name='tel',
    	max_length=11,
    	unique=False,
    )
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.username

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True

    @property
    def is_staff(self):
        return self.is_admin

# Create your models here.
