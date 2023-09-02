from django.db import models
from category.models import Category
from django.urls import reverse


# Create your models here.
class Product(models.Model):
    product_name = models.CharField(max_length=200, unique=True)
    slug = models.SlugField(max_length=200, unique=True)
    product_description = models.TextField(max_length=500, blank=True)
    price = models.DecimalField(max_digits=6, decimal_places=2)
    image = models.ImageField(upload_to='photos/product')
    stock  = models.IntegerField()
    is_avalible = models.BooleanField(default=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    created_date  = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now = True)


    def get_url(self):
        return reverse('product_detail',args=[self.category.slug,self.slug])

    def __str__(self):
        return self.product_name
    
variation_category_choice = (
    ('option1','option1'),
    ('option2','option2'),
) 

class Variation(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    variation_category = models.CharField(max_length=50,choices=variation_category_choice)
    variation_value = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)
    created_date = models.DateTimeField(auto_now=True)
    
    def __unicode__(self):
        return self.product
