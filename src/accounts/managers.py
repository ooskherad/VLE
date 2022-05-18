from django.contrib.auth.base_user import BaseUserManager


class UserManager(BaseUserManager):
    def create_user(self, **kwargs):
        if not kwargs.get('mobile'):
            raise ValueError('Users must have a mobile')

        if not kwargs.get('mobile'):
            raise ValueError('Users must have a password')

        user = self.model(mobile=kwargs.get('mobile'))
        user.set_password(kwargs.get('password'))
        user.save(using=self._db)
        return user

    def create_superuser(self, mobile, password=None):
        user = self.create_user(mobile=mobile, password=password)
        user.is_admin = True
        user.save(using=self._db)
        return user
