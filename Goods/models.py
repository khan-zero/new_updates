from django.db import models
from django.contrib.auth.models import User
from random import sample
import string

class GenereteCode(models.Model):
    
    generate_code = models.CharField(max_length=255, blank=True, unique=True)
    
    
    def save(self, *args, **kwargs):
        if not self.id:
            self.generate_code = "".join(sample(string.ascii_letters, 20))
        super(GenereteCode, self).save(*args, **kwargs)
        
        
    class Meta:
        abstract = True

class Banner(GenereteCode):
    title1 = models.CharField(max_length=255)
    title2 = models.CharField(max_length=255)
    title3 = models.CharField(max_length=255)
    title4 = models.CharField(max_length=255)
    title5 = models.CharField(max_length=255)

    sub_title1 = models.CharField(max_length=255, blank=True, null=True)
    sub_title2 = models.CharField(max_length=255, blank=True, null=True)
    sub_title3 = models.CharField(max_length=255, blank=True, null=True)

    img1 = models.ImageField(upload_to='images/banners/'),
    img2 = models.ImageField(upload_to='images/banners/'),

    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.title


class Category(GenereteCode):

    name = models.CharField(max_length=255)
    img = models.ImageField(upload_to='images/category/')
    body = models.TextField()

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.id:
            self.generate_code = "".join(sample(string.ascii_letters, 20))
        super(Category, self).save(*args, **kwargs)

class Product(GenereteCode):
    name:str = models.CharField(max_length=255)
    quantity:int = models.PositiveIntegerField(default=1)
    price:float = models.DecimalField(max_digits=8, decimal_places=2)
    category:Category = models.ForeignKey(Category, on_delete=models.CASCADE)
    description:str = models.TextField()
    

    def __str__(self):
        return self.name

class ProductImg(GenereteCode):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    img = models.ImageField(upload_to='product-img')

    def __str__(self):
        return self.product.name
        
class ProductEnter(GenereteCode):
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True)
    quantity = models.IntegerField()
    old_quantity = models.IntegerField()
    date = models.DateTimeField(auto_now_add=True)
    description = models.TextField()

    def save(self, *args, **kwargs):
        if not self.pk:
            #  agar object yangi bolsa saqlashdan oldin eski quantityni avtomatik o'rnatish
            self.old_quantity = self.product.quantity
            self.product.quantity += self.quantity
        else:
            # update
            original = ProductEnter.objects.get(pk=self.pk)
            self.product.quantity -= original.quantity
            self.product.quantity += self.quantity

        self.product.save()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Entry for {self.product.name} on {self.date}"
           
        

class Cart(GenereteCode):
    author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    is_active = models.BooleanField(default=True)
    shopping_date = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return self.author.username

class CartProduct(GenereteCode):
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True)
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return self.product.name

class Order(GenereteCode):
    cart = models.ForeignKey(Cart, on_delete=models.SET_NULL, null=True)
    full_name = models.CharField(max_length=255)
    email = models.EmailField(blank=True, null=True)
    phone = models.CharField(max_length=13)
    address = models.CharField(max_length=255)
    status = models.SmallIntegerField(
        choices=(
            (1, 'Tayyorlanmoqda'),
            (2, 'Yo`lda'),
            (3, 'Yetib borgan'),
            (4, 'Qabul qilingan'),
            (5, 'Qaytarilgan'),
        )
    )

    def __str__(self):
        return self.full_name


class NavbarTop(GenereteCode):
    logo_img = models.ImageField(upload_to='images/logo/')
    info_icon_img = models.ImageField(upload_to='images/icon/')
    info_text = models.CharField(max_length=255)
    call_canter = models.CharField(max_length=20)
    email_address = models.EmailField()

    verbose_name = 'NavbarTop'
    verbose_name_plural = 'NavbarTop'

class Footer(GenereteCode):
    call_center = models.CharField(max_length=255)
    location = models.TextField()
    img = models.ImageField()

    class Meta:
        verbose_name = 'Footer'



class FooterImages(GenereteCode):
    name = models.CharField(max_length=255)
    img = models.ImageField(upload_to='images/footer/')

    class Meta:
        verbose_name = 'FooterImage'
        verbose_name_plural = 'FooterImages'
