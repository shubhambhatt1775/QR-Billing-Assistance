from django.db import models

# Create your models here.
class author(models.Model):
    name = models.CharField(max_length=50)
    tagline = models.TextField()
    
class registration(models.Model):
    fname = models.CharField(max_length=50)
    lname = models.CharField(max_length=50,default="") 
    email = models.EmailField()
    mobile = models.CharField(max_length=10)
    password = models.CharField(max_length = 100)
    address = models.TextField()
    state = models.CharField(max_length = 50)
    city = models.CharField(max_length = 50)
    pincode = models.CharField(max_length = 7)

    def __str__(self):
        return f"{self.fname} {self.lname}"
        # return self.fname + " " + self.lname

class signin(models.Model):
    email = models.EmailField()
    password = models.CharField(max_length=100)

    def __str__(self):
        return self.email


class Customer(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)

    def __str__(self):
        return self.name

    
class Bill(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    amount = models.FloatField(default=0.00)
    bill_date = models.DateField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=(("Pending", "Pending"), ("Paid", "Paid")))
    items_summary = models.TextField(default="")

    def __str__(self):
        return f"Bill {self.id} - {self.customer.name}"


class Product(models.Model):
    Product_id = models.AutoField(primary_key=True)
    Product_name = models.CharField(max_length=50)
    Price = models.DecimalField(max_digits=10, decimal_places=2)
    Quantity = models.IntegerField()   # NEW FIELD
    GST_percentage = models.IntegerField()
    Preset_flag = models.BooleanField(default=False)

    def __str__(self):
        return self.Product_name


class Payment(models.Model):
    STATUS_CHOICES = [
        ('Paid', 'Paid'),
        ('Pending', 'Pending'),
        ('Failed', 'Failed'),
    ]
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    amount = models.FloatField()
    status = models.CharField(max_length=10, choices=STATUS_CHOICES)
    transaction_id = models.CharField(max_length=100, null=True, blank=True)
    date = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"{self.customer.name} - {self.status}"


class Sale(models.Model):
    bill = models.ForeignKey(Bill, on_delete=models.CASCADE, null=True, blank=True)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    product_name = models.CharField(max_length=200)
    quantity = models.IntegerField()
    total_amount = models.FloatField()
    date = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"Order {self.id} - {self.customer.name}"

# class Sale(models.Model):
#     customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
#     product_name = models.CharField(max_length=200)
#     quantity = models.IntegerField()
#     total_amount = models.FloatField()
#     date = models.DateField(auto_now_add=True)

#     def __str__(self):
#         return f"Order {self.id} - {self.customer.name}"


