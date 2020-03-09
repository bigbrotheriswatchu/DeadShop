from django.db import models
from django.urls import reverse


class Collection(models.Model):
    collection_name =   models.CharField(max_length=50, db_index=True)
    description     =   models.TextField(max_length=300)
    image           =   models.ImageField(upload_to='image', blank=True)
    slug            =   models.SlugField(max_length=250, unique=True)

    def get_absolute_url(self):
        return reverse('card:list_by_category', args=[self.slug])

    def __str__(self):
        return self.collection_name


class Tshirt(models.Model):
    collection      =   models.ForeignKey(Collection, on_delete=models.CASCADE, verbose_name="Категория")
    name            =   models.CharField(max_length=50)
    shirt_image     =   models.ImageField(upload_to='image', blank=True)
    size            =   models.CharField(max_length=10)
    composition     =   models.CharField(max_length=50)

