from django.db import models

# Create your models here.
CATEGORY_CHOICES=(('PH', 'Phone'), ('KY', 'Keys'), ('NB', 'NoteBooks'), ('HP', 'Headphones'), ('WB', 'Water-Bottle'), ('CD', 'Cards'),)


class Object(models.Model):
    title = models.CharField(max_length=100)
    description = models.CharField(max_length=100)
    image = models.ImageField(upload_to="product")
    url = models.URLField(blank=True)
    
    """discounted_price = models.FloatField()
    description = models.TextField()
    composition = models.TextField(default='')
    prodapp = models.TextField(default='')
    # brand = models.CharField(max_length=100)
    category = models.CharField(choices=CATEGORY_CHOICES, max_length=2)
    product_image = models.ImageField(upload_to='product')
    def __str__(self):
        return self.title
    """