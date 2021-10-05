from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

# Create your models here.

class category(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class item(models.Model):
    namee = models.CharField(max_length=200)
    desc = models.TextField()
    img = models.ImageField(upload_to='productimage')
    cat_name = models.ForeignKey(category, on_delete=models.CASCADE)
    price = models.FloatField(max_length=5000)

    def __str__(self):
        return self.namee


class cart(models.Model):
    item_name = models.ForeignKey(item, on_delete=models.CASCADE)
    name = models.ForeignKey(User, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    price = models.FloatField()
    ordered = models.BooleanField(default=False)


    def __str__(self):
        return self.item_name.namee+ ' item quantity:-' + str(self.quantity)

    def itemno(self):
        ak = len(cart.objects.filter(name=self.user))
        return ak



class address(models.Model):
    name = models.ForeignKey(User, on_delete=models.CASCADE)
    address1 = models.CharField(max_length=200)
    address2 = models.CharField(max_length=200)
    zip_code = models.IntegerField()
    country = models.CharField(max_length=200)
    state = models.CharField(max_length=200)

    def __str__(self):
        return self.name.username + ' address: ' + self.address1


class order(models.Model):
    name = models.ForeignKey(User, on_delete=models.CASCADE)
    itemss = models.ForeignKey(item,on_delete=models.CASCADE,null=True)
    addressa = models.ForeignKey(address, on_delete=models.CASCADE)
    ordered = models.BooleanField(default=False)
    quantity = models.IntegerField(default=1)
    product_id = models.CharField(max_length=200)


    def __str__(self):
        return self.name.username

    def get_total(self):
        total = 0
        for order_item in self.items.all():
            total += order_item.get_final_price()
        return total


class troy(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    item_name = models.ForeignKey(item, on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)
    tried_complete = models.BooleanField(default=False)



    def __str__(self):
        return self.item_name.namee
