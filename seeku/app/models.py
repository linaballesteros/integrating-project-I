from django.db import models
from datetime import date

# Create your models here.
CATEGORY_CHOICES = [('Technology', 'Technology'),
    ('Keys', 'Keys'),
    ('Books', 'Books'),
    ('Water Bottles', 'Water Bottles'),
    ('Headphones', 'Headphones'),
    ('Lunchboxes', 'Lunchboxes'),
    ('Clothes', 'Clothes'),
    ('Accesories', 'Accesories'),]


HOUR_CHOICES = [('05:00-06:00', '05:00-06:00'),
    ('06:00-07:00', '06:00-07:00'),
    ('07:00-08:00', '07:00-08:00'),
    ('08:00-09:00', '08:00-09:00'),
    ('09:00-10:00', '09:00-10:00'),
    ('10:00-11:00', '10:00-11:00'),
    ('11:00-12:00', '11:00-12:00'),
    ('12:00-13:00', '12:00-13:00'),
    ('13:00-14:00', '13:00-14:00'),
    ('14:00-15:00', '14:00-15:00'),
    ('15:00-16:00', '15:00-16:00'),
    ('16:00-17:00', '16:00-17:00'),
    ('17:00-18:00', '17:00-18:00'),
    ('18:00-19:00', '18:00-19:00'),
    ('19:00-20:00', '19:00-20:00'),
    ('20:00-21:00', '20:00-21:00'),
    ('21:00-22:00', '21:00-22:00'),
    ('22:00-23:00', '22:00-23:00'),
    ('23:00-00:00', '23:00-00:00'),
    ]
COLOR_CHOICES = [
    ('Red', 'Red'),
    ('Blue', 'Blue'),
    ('Green', 'Green'),
    ('Yellow', 'Yellow'),
    ('Black', 'Black'),
    ('White', 'White'),
    ('Purple', 'Purple'),
    ('Orange', 'Orange'),
    ('Pink', 'Pink'),
    ('Brown', 'Brown'),
    ('Gray', 'Gray'),
    ('Teal', 'Teal'),
    ('Cyan', 'Cyan'),
    ('Magenta', 'Magenta'),
    ('Lime', 'Lime'),
    ('Indigo', 'Indigo'),
    ('Aqua', 'Aqua'),
    ('Gold', 'Gold'),
    ('Silver', 'Silver'),
    ('Maroon', 'Maroon'),
    ('Navy', 'Navy'),
    ('Olive', 'Olive'),
    ('Turquoise', 'Turquoise'),
    ('Violet', 'Violet'),
    ('Coral', 'Coral'),
    ('Slate', 'Slate'),
    ('Crimson', 'Crimson'),
    ('Fuchsia', 'Fuchsia'),
    ('Mint', 'Mint'),
    ('Salmon', 'Salmon'),
    ('Beige', 'Beige'),
    ('Tan', 'Tan'),
    ('Khaki', 'Khaki'),
    ('Lavender', 'Lavender'),
    ('Plum', 'Plum'),
    ('Steel Blue', 'Steel Blue'),
    ('Forest Green', 'Forest Green'),
    ('Midnight Blue', 'Midnight Blue'),
    ('Tomato', 'Tomato'),
    ('Dark Slate Gray', 'Dark Slate Gray'),
    ('Saddle Brown', 'Saddle Brown'),
]

CATEGORY_CHOICES = [
    ('Technology', 'Technology'),
    ('Keys', 'Keys'),
    ('Books', 'Books'),
    ('Water Bottles', 'Water Bottles'),
    ('Headphones', 'Headphones'),
    ('Lunchboxes', 'Lunchboxes'),
    ('Clothes', 'Clothes'),
    ('Accessories', 'Accessories'),
    # ... continue adding categories
]

BLOCK_CHOICES = [
    ('Block 1', 'Block 1'),
    ('Block 3', 'Block 3'),
    ('Block 4', 'Block 4'),
    ('Block 5', 'Block 5'),
    ('Block 6', 'Block 6'),
    ('Block 7', 'Block 7'),
    ('Block 8', 'Block 8'),
    ('Block 9', 'Block 9'),
    ('Block 10', 'Block 10'), 
    ('Block 12', 'Block 12'),
    ('Block 13', 'Block 13'),
    ('Block 14', 'Block 14'),
    ('Block 15', 'Block 15'),
    ('Block 16', 'Block 16'), 
    ('Block 17', 'Block 17'),
    ('Block 18', 'Block 18'),
    ('Block 19', 'Block 19'),
    ('Block 20', 'Block 20'),
    ('Block 21', 'Block 21'),
    ('Block 23', 'Block 23'),
    ('Block 26', 'Block 26'),
    ('Block 27', 'Block 27'),
    ('Block 28', 'Block 28'),
    ('Block 29', 'Block 29'),
    ('Block 30', 'Block 30'),
    ('Block 32', 'Block 32'), 
    ('Block 33', 'Block 33'),
    ('Block 34', 'Block 34'),
    ('Block 35', 'Block 35'),
    ('Block 37', 'Block 37'),
    ('Block 38', 'Block 38'),
    ('Block 39', 'Block 39'), 
    ('Argos Block', 'Argos Block'),
    ('Main Cafeteria', 'Main Cafeteria'),
    ('Cafeteria 2', 'Cafeteria 2'),
    ('North Parking Lot', 'North Parking Lot'),
    ('South Parking Lot', 'South Parking Lot'),
    ('Guayabos Parking Lot', 'Guayabos Parking Lot'),
    ('Synthetic fields - Main Cafeteria', 'Synthetic fields - Main Cafeteria'),
    ('Synthetic fields - North Parking Lot', 'Synthetic fields - North Parking Lot') ]


blocks_list = [
    "Block 1", "Block 2", "Block 3", "Block 4", "Block 5", "Block 6", "Block 7", "Block 8", "Block 9", "Block 10",
    "Block 12", "Block 13", "Block 14", "Block 15",
    "Block 16", "Block 17", "Block 18", "Block 19", "Block 20", "Block 21",
    "Block 23", "Block 26", "Block 27", "Block 28", "Block 29", "Block 30",
    "Block 32", "Block 33", "Block 34", "Block 35", "Block 37", "Block 38",
    "Block 39", "Argos Block", "Main Cafeteria", "Cafeteria 2", "North Parking Lot",
    "South Parking Lot", "Guayabos Parking Lot", "Synthetic fields - Main Cafeteria",
    "Synthetic fields - North Parking Lot"
]



class Object(models.Model):
    title = models.CharField(max_length=100)
    description = models.CharField(max_length=100)
    image = models.ImageField(upload_to="uploads/")
    

    
    url = models.URLField(blank=True)
    # place found, different lists
    place_found = models.CharField(max_length=100, default='Block 1', choices=BLOCK_CHOICES)

    date_found = models.DateField(default=date.today)  #set default to today's date
    hour_range = models.CharField(max_length=11, default='05:00-06:00', choices=HOUR_CHOICES)
    brands = models.CharField(max_length=100, default="Versage")
    color = models.CharField(max_length=100, default='Block 1', choices=COLOR_CHOICES)   
    category = models.CharField(max_length=100, default='Technology', choices=CATEGORY_CHOICES)   
    place_range = models.CharField(max_length=100)            


    
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