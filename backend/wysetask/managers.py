from django.contrib.auth.base_user import BaseUserManager

class UserManager(BaseUserManager):
    use_in_migrations=True

    def create_user(self,email,password=None,**extra_fields):
        if not email:
            raise ValueError('Email is required')
        #normalize will convert to identical emails which are in diffrenet cases(lowercase , uppercase) in a similar case so that they can be compared 
        email=self.normalize_email(email)
        user=self.model(email=email,**extra_fields)
        #hash our password with set password
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self,email,password,**extra_fields):
        extra_fields.setdefault('is_staff',True)
        extra_fields.setdefault('is_superuser',True)
        extra_fields.setdefault('is_active',True)

        if(extra_fields.get('is_staff') is not True):
            raise ValueError('superuser must have is staff true ')
        #at the end of create_superuser function we simply return create user we just chaneg the required fields in this function
        return self.create_user(email,password,**extra_fields)