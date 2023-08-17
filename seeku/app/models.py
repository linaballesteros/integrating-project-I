from django.db import models
from datetime import date

# Create your models here.
CATEGORY_CHOICES=(('PH', 'Phone'), ('KY', 'Keys'), ('NB', 'NoteBooks'), ('HP', 'Headphones'), ('WB', 'Water-Bottle'), ('CD', 'Cards'),)
BLOCK_CHOICES = [
    ('Block 1', 'Block 1'),
    ('Block 2', 'Block 2'),
    ('Block 3', 'Block 3'),
    # ... continue with other blocks ...
    ('Block 39', 'Block 39'),
]


class Object(models.Model):
    title = models.CharField(max_length=100)
    description = models.CharField(max_length=100)
    image = models.ImageField(upload_to="product")
    url = models.URLField(blank=True)
    place_found = models.CharField(max_length=100, default='Block 1')
    date_found = models.DateField(default=date.today)  #set default to today's date

    def __str__(self):
        return self.title


    
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