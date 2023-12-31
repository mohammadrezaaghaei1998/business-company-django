from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User




class Brand(models.Model):
    name = models.CharField(max_length=200,null=True,blank=True)
    def __str__(self):
        return self.name


    
class Color(models.Model):
    name = models.CharField(max_length=200,null=True,blank=True)
    code = models.CharField(max_length=50,null=True,blank=True)    
    def __str__(self):
        return self.name




class Categories (models.Model):
    name = models.CharField(max_length=200,null=True,blank=True)
    image = models.ImageField(upload_to='product_images/img',null=True,blank=True)
    def __str__(self):
        return self.name
    

class Subfield(models.Model):
    name = models.CharField(max_length=255)
    category = models.ForeignKey(Categories, on_delete=models.CASCADE, null=True, blank=True)
    def __str__(self):
        return self.name
    


class Subfield_Item(models.Model):
    name = models.CharField(max_length=255)
    category = models.ForeignKey(Categories, on_delete=models.CASCADE, null=True, blank=True)
    subfield = models.ForeignKey(Subfield, on_delete=models.CASCADE, null=True, blank=True)


    def __str__(self):
        return self.name





class Product(models.Model):
    image = models.ImageField(upload_to='product_images/img',null=True,blank=True)
    name = models.CharField(max_length=200,null=True,blank=True)
    price = models.IntegerField(null=True,blank=True)
    information = models.TextField(null=True,blank=True)
    description = models.TextField(null=True,blank=True)
    created_date = models.DateTimeField(default=timezone.now)
    origin = models.CharField(max_length=255,null=True,blank=True)
    quantity = models.PositiveIntegerField(default=0,null=True,blank=True)
    quality = models.CharField(max_length=255,null=True,blank=True)


    subfield_item = models.ForeignKey(Subfield_Item,on_delete=models.CASCADE,null=True,blank=True)
    subfield = models.ForeignKey(Subfield,on_delete=models.CASCADE,null=True,blank=True)
    categories = models.ForeignKey(Categories,on_delete=models.CASCADE,null=True,blank=True)
    brand = models.ForeignKey(Brand,on_delete=models.CASCADE,null=True,blank=True)
    color = models.ForeignKey(Color,on_delete=models.CASCADE,null=True,blank=True)
    discount_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)

    
        
    def __str__(self):
        return self.name




class Images(models.Model):
    image = models.ImageField(upload_to='product_images/img',null=True,blank=True)
    product = models.ForeignKey(Product,on_delete=models.CASCADE)






class Contact(models.Model):
    name = models.CharField(max_length=255)
    email = models.EmailField()
    message = models.TextField()

    def __str__(self):
        return f"{self.name} - {self.email}"





class Collaboration(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=1)  
    product_name = models.CharField(max_length=255)
    quantity = models.PositiveIntegerField()
    quality = models.CharField(max_length=255)
    origin = models.CharField(max_length=255)
    description = models.TextField()
    product_images = models.ImageField(upload_to='collaboration_images/', default='default_image.jpg')
    whatsapp = models.CharField(max_length=15, default='')

    def __str__(self):
        return self.product_name

class CollaborationImage(models.Model):
    collaboration = models.ForeignKey(Collaboration, related_name='collaboration_images', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='collaboration_images/')




class UserInfo(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, default='10000000000')
    name = models.CharField(max_length=255, default='')
    surname = models.CharField(max_length=255, default='')
    email = models.EmailField(max_length=255, unique=True, default='')
    whatsapp = models.CharField(max_length=15, default='')
    country = models.CharField(max_length=255, default='')
    city = models.CharField(max_length=255, default='')
    company = models.CharField(max_length=255, blank=True, null=True, default='')

    def __str__(self):
        return self.email





class Investment(models.Model):
    name = models.CharField(max_length=100)
    profitability_percentage = models.DecimalField(max_digits=5, decimal_places=2)
    duration_staying_money = models.IntegerField(help_text='Duration in months')
    origin = models.CharField(max_length=50)
    description = models.TextField(blank=True, null=True)
    start_date = models.DateField()
    end_date = models.DateField(blank=True, null=True)
    amount_invested = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    is_active = models.BooleanField(default=True)
    image = models.ImageField(upload_to='investment_product/img',null=True,blank=True)

    def __str__(self):
        return self.name
    



class Favorite(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    investment = models.ForeignKey(Investment, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.user.username}'s favorite - {self.investment.name}"


    


class OrderProduct(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    email = models.EmailField()
    address = models.TextField()
    phone_number = models.CharField(max_length=20)

    def __str__(self):
        return f"Order for {self.product.name} by {self.user.username}"
    



class OrderInvestment(models.Model):
    investment = models.ForeignKey(Investment, on_delete=models.CASCADE, null=True, default=None)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    email = models.EmailField()
    address = models.TextField()
    phone_number = models.CharField(max_length=20)

    def __str__(self):
        return f"Order for {self.investment.name} by {self.user.username}"
    




class JobApplication(models.Model):
    name = models.CharField(max_length=255)
    email = models.EmailField()
    whatsapp_number = models.CharField(max_length=20, blank=True, null=True)
    country = models.CharField(max_length=255, blank=True, null=True)
    city = models.CharField(max_length=255, blank=True, null=True)
    cv = models.FileField(upload_to='cv/', blank=True, null=True)



    def __str__(self):
        return self.name





class Product_Assistance(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=1)
    product_name = models.CharField(max_length=255)
    quantity = models.PositiveIntegerField()
    quality = models.CharField(max_length=255)
    origin = models.CharField(max_length=255)
    description = models.TextField()
    product_images = models.ImageField(upload_to='product_assistance_images/', default='default_image.jpg')
    whatsapp = models.CharField(max_length=15, default='')

    def __str__(self):
        return self.product_name

class Product_AssistanceImage(models.Model):
    product_assistance = models.ForeignKey(Product_Assistance, related_name='product_assistance_images', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='product_assistance_images/')





class Branches(models.Model):
    name = models.CharField(max_length=255)
    country = models.CharField(max_length=255)
    city = models.CharField(max_length=255)
    email = models.EmailField(max_length=255, unique=True, default='')
    number = models.CharField(max_length=15, default='')
    address = models.CharField(max_length=255)