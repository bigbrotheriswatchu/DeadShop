from django.db import models
from django.urls import reverse

from django.db.models.signals import post_save


class Collection(models.Model):
    collection_name =   models.CharField(max_length=50, db_index=True)
    description     =   models.TextField(max_length=300)
    image           =   models.ImageField(upload_to='image', blank=True)
    slug            =   models.SlugField(max_length=250, unique=True)


    class Meta:
        verbose_name = 'Коллекция'
        verbose_name_plural = 'Коллекции'

    #def get_absolute_url(self):
        #return reverse('card:list_by_category', args=[self.slug])

    def __str__(self):
        return self.collection_name


class Tshirt(models.Model):
    collection      =   models.ForeignKey(Collection, on_delete=models.CASCADE, verbose_name="Категория")
    name            =   models.CharField(max_length=50, blank=True, null=True)
    price           =   models.DecimalField(max_digits=10, decimal_places=2, default=1500)
    shirt_image     =   models.ImageField(upload_to='image', blank=True)
    size            =   models.CharField(max_length=10)
    composition     =   models.CharField(max_length=50)
    is_active       =   models.BooleanField(default=True)

    class Meta:
        verbose_name = 'Майка'
        verbose_name_plural = 'Майки'

    #def get_absolute_url(self):
        #return reverse('shop:list_by_category', args=[self.slug])

    def __str__(self):
        return "%s" % self.name

    def __int__(self):
        return self.price




class Status(models.Model):
    name = models.CharField(max_length=24, blank=True, null=True, default=None)
    is_active = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True, auto_now=False)
    updated = models.DateTimeField(auto_now_add=False, auto_now=True)

    def __str__(self):
        return "Статус %s" % self.name


    class Meta:
        verbose_name = 'Статус заказа'
        verbose_name_plural = 'Статусы заказа'


class Order(models.Model):
    total_price = models.DecimalField(max_digits=10, decimal_places=2, default=0)#total price for all products in order
    customer_name = models.CharField(max_length=64, blank=True, null=True, default=None)
    customer_email = models.EmailField(blank=True, null=True, default=None)
    customer_phone = models.CharField(max_length=48, blank=True, null=True, default=None)
    customer_address = models.CharField(max_length=128, blank=True, null=True, default=None)
    comments = models.TextField(blank=True, null=True, default=None)
    status = models.ForeignKey(Status, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True, auto_now=False)
    updated = models.DateTimeField(auto_now_add=False, auto_now=True)

    def __str__(self):
        return self.status.name

    class Meta:
        verbose_name = 'Заказ'
        verbose_name_plural = 'Заказы'

    def save(self, *args, **kwargs):

        super(Order, self).save(*args, **kwargs)


class ProductInOrder(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, blank=True, null=True, default=None)
    t_shirt = models.ForeignKey(Tshirt, blank=True, null=True, default=None, on_delete=models.CASCADE)
    nmb = models.IntegerField(default=1)
    price_per_item = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    total_price = models.DecimalField(max_digits=10, decimal_places=2, default=0)#price*nmb
    is_active = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True, auto_now=False)
    updated = models.DateTimeField(auto_now_add=False, auto_now=True)

    def __str__(self):
        return self.t_shirt

    class Meta:
        verbose_name = 'Товар в заказе'
        verbose_name_plural = 'Товары в заказе'

    if hasattr(t_shirt, 'price'):
        def save(self, *args, **kwargs):
            price_per_item = self.t_shirt.price
            self.price_per_item = price_per_item
            self.total_price = self.nmb * price_per_item

            super(ProductInOrder, self).save(*args, **kwargs)


def product_in_order_post_save(sender, instance, created, **kwargs):
    order = instance.order
    all_products_in_order = ProductInOrder.objects.filter(order=order, is_active=True)

    order_total_price = 0
    for item in all_products_in_order:
        order_total_price += item.total_price

    instance.order.total_price = order_total_price
    instance.order.save(force_update=True)


post_save.connect(product_in_order_post_save, sender=ProductInOrder)


class ProductInBasket(models.Model):
    session_key = models.CharField(max_length=128, blank=True, null=True, default=None)
    order = models.ForeignKey(Order, blank=True, null=True, default=None, on_delete=models.CASCADE)
    t_shirt = models.ForeignKey(Tshirt, blank=True, null=True, default=None, on_delete=models.CASCADE)
    nmb = models.IntegerField(default=1)
    price_per_item = models.DecimalField(max_digits=10, decimal_places=2, default=1500)
    total_price = models.DecimalField(max_digits=10, decimal_places=2, default=0)#price*nmb
    is_active = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True, auto_now=False)
    updated = models.DateTimeField(auto_now_add=False, auto_now=True)


    def __str__(self):
        return self.t_shirt.name

    class Meta:
        verbose_name = 'Товар в корзине'
        verbose_name_plural = 'Товары в корзине'

    def save(self, *args, **kwargs):
        price_per_item = self.t_shirt.price
        self.price_per_item = price_per_item
        self.total_price = int(self.nmb) * price_per_item

        super(ProductInBasket, self).save(*args, **kwargs)