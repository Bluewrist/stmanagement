from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class Category(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self) -> str:
        return self.name


class Type(models.Model):
    name = models.CharField(max_length=100)   

    def __str__(self) -> str:
        return self.name


class Branch(User):
    name = models.CharField(max_length=100)
    is_dist = models.BooleanField(default=True) 

    def __str__(self) -> str:
        return self.name


class Product(models.Model):
    part_number = models.CharField(max_length=12,unique=True)
    part_name = models.CharField(max_length=200)    
    price =  models.IntegerField(default= 0)
    part_detail =  models.TextField(max_length=1000,default='')
    product_category =  models.ForeignKey(Category,on_delete = models.CASCADE)
    car_type =  models.ForeignKey(Type,on_delete = models.CASCADE,null=True,blank=True)
    issued_to = models.ForeignKey(Branch,on_delete = models.CASCADE,null=True,blank=True)
    reorder_level = models.IntegerField(default=1)
    is_used = models.BooleanField(default=False)
    date =  models.DateTimeField(auto_now_add=True)
    purchacing_price = models.IntegerField(default=1)
    qyt = models.IntegerField(default=1)
    receive_quantity = models.IntegerField(default='0', blank=True, null=True)
    issue_quantity = models.IntegerField(default=1)
    last_updates= models.DateTimeField(auto_now_add=False,auto_now=True)
    expory_to_csv = models.BooleanField(default=False)


    def __str__(self) -> str:
        return self.part_name
    
    @property
    def total_order_value_per_item(self):
        total = self.qyt * self.purchacing_price
        return total 
    
    @property
    def total_selling_value_per_item(self):
        total = self.qyt * self.price
        return total 
    


class StockHistory(models.Model):
	category = models.ForeignKey(Category, on_delete=models.CASCADE, blank=True, null=True)
	item_name = models.CharField(max_length=50, blank=True, null=True)
	quantity = models.IntegerField(default='0', blank=True, null=True)
	receive_quantity = models.IntegerField(default='0', blank=True, null=True)
	receive_by = models.CharField(max_length=50, blank=True, null=True)
	issue_quantity = models.IntegerField(default='0', blank=True, null=True)
	issue_to = models.CharField(max_length=50, blank=True, null=True)
	timestamp = models.DateTimeField(auto_now_add=False, auto_now=False, null=True)


class Store(models.Model):
    branch = models.ForeignKey(Branch,on_delete=models.CASCADE)
    date_orderd =  models.DateTimeField(auto_now_add=True)
    transaction_id =  models.CharField(max_length=200,null=True)

    def __str__(self) -> str:
        return self.branch.name


    @property
    def get_store_total(self):
        storeitems = self.storeitem_set.all()
        total = sum([item.get_total for item in storeitems])
        return total 

    @property
    def get_store_items(self):
        storeitems = self.storeitem_set.all()
        total = sum([item.quantity for item in storeitems])
        return total


    @property
    def grand_total(self):
        total = self.get_store_total 
        return total
    

class Storeitem(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE,blank=True, null=True)
    store = models.ForeignKey(Store, on_delete= models.CASCADE)
    quantity = models.IntegerField(default=0)
    date_orderd =  models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.product.part_name

    @property
    def get_total(self):
        total = self.product.price * self.quantity
        return total
    
class Sale(models.Model):
    product = models.ForeignKey(Storeitem,on_delete=models.DO_NOTHING)
    store = models.ForeignKey(Store,on_delete=models.DO_NOTHING)
    qty = models.IntegerField(default=1)
    date =  models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.product.product.part_name 
    
    def total(self):
        total = self.product.product.price * self.qty
        return total
    

    