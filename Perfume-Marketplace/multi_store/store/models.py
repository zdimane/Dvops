from django.db import models
from django.utils import timezone
from django.core.validators import MinValueValidator, MaxValueValidator


# Create your models here.
# Brand Model
class Brand(models.Model):
    brand_name = models.CharField(max_length=50, default="")
    image = models.ImageField(upload_to="images/")
    category = models.CharField(max_length=50, default="")

    @staticmethod
    def get_all_brands():
        return Brand.objects.all()
    # Category Model
class Category(models.Model):
    id= models.IntegerField(primary_key=True)
    class Type1(models.IntegerChoices):
        woody = 1
        floral = 2
        oriental = 3
        fresh = 4
        celebrity_scents = 5

    type1 = models.IntegerField(choices = Type1.choices, null=True)
    class Type2(models.IntegerChoices):
        fresh_floral = 1
        fruity_floral = 2
        oriental_floral = 3
        classic_oriental = 4
        woody_oriental = 5
        fresh_water = 6
        fresh_citrus = 7
        fresh_green = 8
        woody_mossy = 9
        woody_smokey = 10
        celebrity_scents = 11
        fresh_oriental = 12
    type2 = models.IntegerField(choices = Type2.choices,  null=True)


    @staticmethod
    def get_all_category():
        return Category.objects.all()
    
    @staticmethod
    def get_category_type():
        t = set()
        cat = Category.objects.all()
        for c in cat:
            x = c.get_type1_display()
            t.add(x)
        return t
    
    @staticmethod
    def get_category_type2(cat):
        return cat.get_type2_display()

    @staticmethod
    def get_cat_num(category):
        cat_ty = []
        cat = Category.objects.all()
        for c in cat:
            if (c.get_type1_display() == category):
                cat_ty.append(c.id)
        return cat_ty
    # Customer Model
class Customer(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.EmailField()
    phone = models.CharField(max_length=10)
    gender = models.CharField(max_length=10, default="")
    password = models.CharField(max_length=150)

    def register(self):
        self.save()
    def customer_info(id):
        return Customer.objects.get(id = id)
        
    def checkk(user, flag):
        if (flag == "email"):
            try:
                return Customer.objects.get(email = user)
            except:
                return None
        elif (flag == "phone"):
            try:
                return Customer.objects.get(phone = user)
            except:
                return None
    def info(email):
       return Customer.objects.get(email=email) 
    # Product Model
class Product(models.Model):
    name = models.CharField(max_length=50)
    price = models.IntegerField(default=0)
    description = models.CharField(max_length=2000, blank=True)
    image = models.ImageField(upload_to="images/")
    category = models.ForeignKey(Category, db_column='type2', on_delete=models.CASCADE)
    rating = models.IntegerField(default=1, validators=[MinValueValidator(0),MaxValueValidator(5)])
    brand = models.CharField(max_length=50, default="")
    gender = models.CharField(max_length=50, default="")
    size = models.CharField(max_length=50, default="")
    
    @staticmethod
    def get_product_by_id(id):
        return Product.objects.filter(id__in = id)
    
    @staticmethod
    def get_product(id):
        return Product.objects.filter(id = id)

    @staticmethod
    def get_all_products():
        return Product.objects.all()

    @staticmethod
    def get_spf_products(category_id):
        if (category_id):
            return Product.objects.filter(category = category_id)
        else:
            return Product.objects.all()
    
    @staticmethod
    def get_brands():
        return Product.objects.values("brand").distinct()

    @staticmethod
    def gen_filter(g, prds):
        if (g == "Male"):
            return prds.filter(gender = g)
        elif (g == "Female"):
            g = "women"
            return prds.filter(gender = g)

    @staticmethod
    def sorting(s, prds):
        if (s == "Low To High"):
            return prds.order_by('price')
        elif (s == "High To Low"):
            return prds.order_by('-price')
    @staticmethod
    def typee(fil, prds):
        return prds.filter(category__in = fil)
    @staticmethod
    def brandfilter(brand, prds):
        return prds.filter(brand__in = brand)
# Order Model
class Order(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    price = models.IntegerField(default=500) 
    adress = models.CharField(max_length=50, default="", blank=True)
    phone = models.CharField(max_length=10, default="", blank=True)
    date = models.DateField(default=timezone.now())
    status = models.TextField(max_length=50, default="received")
    rating = models.IntegerField(default=0, validators=[MinValueValidator(0),MaxValueValidator(5)])

    @staticmethod
    def place_order(self):
        self.save()
    
    @staticmethod
    def get_order_by_id(id):
        return Order.objects.get(id = id)

    @staticmethod
    def status_update(id, stat):
        o = Order.objects.get(id = id)
        o.status = stat
        o.save()
    
    @staticmethod
    def rating_update(id, rate):
        o = Order.objects.get(id = id)
        o.rating = rate
        o.save()
    
    @staticmethod
    def by_customer(customer):
        return Order.objects.filter(customer = customer).order_by("date").reverse()
    
    @staticmethod
    def get_all_orders():
        return Order.objects.all()
    
    @staticmethod
    def total(o):
        return (int(o.quantity) * int(o.price))

# Rate Model  
class Rate(models.Model):
    rating = models.IntegerField(default=1, validators=[MinValueValidator(0),MaxValueValidator(5)])
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    order = models.ForeignKey(Order, on_delete=models.CASCADE)

    def place_order(self):
        self.save()
    
    @staticmethod
    def check_order_id(id):
        return Rate.objects.filter(order = id)  


