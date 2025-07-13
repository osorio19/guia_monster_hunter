from django.db import models
from django.contrib.auth.models import  AbstractUser
from django.core.validators import FileExtensionValidator
from django.conf import settings

class User(AbstractUser):
    username=models.CharField(max_length=150, unique=True)
    email= models.EmailField(unique=True)
    phone_number=models.CharField(max_length=15, blank=True, null=True)
    address=models.CharField(max_length=255, blank=True, null=True)
    city= models.CharField(max_length=100, blank=True,null=True)
    country= models.CharField(max_length=100, blank=True, null=True)
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at= models.DateTimeField(auto_now=True)

    class Meta:
        db_table='users'
        verbose_name='usuario'
        verbose_name_plural='usuarios'

    def __str__(self):
        return f'{self.username} ({self.email})'

class Type (models.Model):
    name_type=models.CharField(max_length=50)
    description=models.TextField(max_length=250)

    class Meta:
        db_table='types'
        verbose_name='tipo de martillo'
        verbose_name_plural='tipos de martillos'

    def __str__(self):
        return f'{self.name_type} ({self.description})'

class Monster (models.Model):
    name_monster=models.CharField(max_length=100)
    race=models.CharField(max_length=60)

    class Meta:
        db_table='Monster'
        verbose_name='Monstruo'
        verbose_name_plural='Monstruos'

    def __str__(self):
        return f'{self.name_monster} ({self.race})'

class Material (models.Model):
    name_material=models.CharField(max_length=250)
    monster=models.ForeignKey(Monster, on_delete=models.CASCADE,blank=True, null=True)
    rarity=models.IntegerField(unique=False)
    
    class Meta:
        db_table='Material'
        verbose_name='Material'
        verbose_name_plural='Materiales'

    def __str__(self):
        return f'{self.name_material}'

class Hammer(models.Model):
    name_hammer=models.CharField(max_length=100)
    material=models.ForeignKey(Material, on_delete=models.CASCADE,blank=True, null=True)
    power=models.IntegerField(unique=False)
    edge=models.CharField(max_length=30)
    type=models.ForeignKey(Type,on_delete=models.SET_NULL, null=True)
    # rarity=models.IntegerField(unique=False)
    image=models.ImageField(
    verbose_name='imagen',
    upload_to='core/hammers',
    validators=[FileExtensionValidator(allowed_extensions=['jpg','jpeg','png','webp'])],
    blank=True,
    null=True
    )

    class Meta:
        db_table='Hammer'
        verbose_name='Martillo'
        verbose_name_plural='Martillos'

    def __str__(self):
        return f'{self.name_hammer} {self.power} {self.edge}'

class Review(models.Model):
    user=models.ForeignKey(
    settings.AUTH_USER_MODEL,
    on_delete=models.CASCADE,
    related_name='review'
    )
    hammer=models.ForeignKey(Hammer, on_delete=models.CASCADE)
    content=models.TextField(max_length=250)
    created_at=models.DateField(auto_now_add=True)

    class Meta:
        db_table='review'
        verbose_name='reseña'
        verbose_name_plural='reseñas'

    def __str__(self):
        return f'{self.user.username} ({self.content})'
# Create your models here.
