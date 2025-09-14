from django.db import models
from category.models import Category
from django.urls import reverse
from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator, MaxValueValidator


# Create your models here.
class Product(models.Model):
    product_name = models.CharField(max_length=200, unique=True)
    slug = models.SlugField(max_length=200, unique=True)
    product_description = models.TextField(max_length=500, blank=True)
    price = models.DecimalField(max_digits=6, decimal_places=2)
    image = models.ImageField(upload_to='photos/product')
    stock  = models.IntegerField()
    low_stock_threshold = models.IntegerField(default=5)
    is_avalible = models.BooleanField(default=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    created_date  = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now = True)


    def get_url(self):
        return reverse('product_detail',args=[self.category.slug,self.slug])

    def average_rating(self):
        reviews = ReviewRating.objects.filter(product=self, status=True).aggregate(average=models.Avg('rating'))
        avg = 0
        if reviews['average'] is not None:
            avg = float(reviews['average'])
        return avg

    def count_reviews(self):
        reviews = ReviewRating.objects.filter(product=self, status=True)
        count = reviews.count()
        return count

    def is_low_stock(self):
        return self.stock <= self.low_stock_threshold

    def is_out_of_stock(self):
        return self.stock <= 0

    def __str__(self):
        return self.product_name


class VariationManager(models.Manager):
    def weight(self):
        return super(VariationManager,self).filter(variation_category='weight',is_active=True)
    
    def volume(self):
        return super(VariationManager,self).filter(variation_category='volume',is_active=True)
    


variation_category_choice = (
    ('weight','weight'),
    ('volume','volume'),
) 

class Variation(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    variation_category = models.CharField(max_length=50,choices=variation_category_choice)
    variation_value = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)
    created_date = models.DateTimeField(auto_now=True)
    
    objects = VariationManager()
    
    def __str__(self):
        return self.variation_value


User = get_user_model()

class ReviewRating(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    subject = models.CharField(max_length=100, blank=True)
    review = models.TextField(max_length=500, blank=True)
    rating = models.FloatField(validators=[MinValueValidator(1), MaxValueValidator(5)])
    ip = models.CharField(max_length=20, blank=True)
    status = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.subject


class ProductGallery(models.Model):
    product = models.ForeignKey(Product, default=None, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='photos/products', max_length=255)

    def __str__(self):
        return self.product.product_name

    class Meta:
        verbose_name = 'productgallery'
        verbose_name_plural = 'product gallery'
