from django.db import models
from django.utils.crypto import get_random_string
from django.utils import timezone
from bot.models import Customer
from django.core.urlresolvers import reverse


class Product(models.Model):
    name = models.CharField(max_length=200, unique=True)
    price = models.PositiveIntegerField()
    count = models.PositiveIntegerField()
    number = models.CharField(editable=False, default=get_random_string , unique=True, max_length=20)
    created = models.DateTimeField(auto_now_add=True)
    image = models.ImageField(upload_to='images/%Y/%m/%d', blank=True)

    class Meta:
        ordering = ('count',)

    def __str__(self):
        return self.name

    def delete_url(self):
        return reverse('shop:product_delete',args=[self.id])

    def edit_url(self):
        return reverse('shop:product_edit',args=[self.id])


class UndoneManager(models.Manager):
    def get_queryset(self):
        return super(UndoneManager, self).get_queryset().filter(done=False)


class Transaction(models.Model):
    total_price = models.DecimalField(max_digits=10, decimal_places=1)
    number = models.CharField(editable=False,default=get_random_string, unique=True,max_length=20)
    shopper = models.ForeignKey(Customer,related_name='transactions')
    created = models.DateTimeField(auto_now_add=True, db_index=True)
    accepted = models.BooleanField(default=False)
    done = models.BooleanField(default=False)

    def __str__(self):
        return str(self.number)

    def delete_url(self):
        return reverse('shop:transaction_delete',args=[self.id])

    def accept_url(self):
        return reverse('shop:transaction_accept',args=[self.id])

    def edit_url(self):
        return reverse('shop:transaction_edit',args=[self.id])

    objects = models.Manager()
    undone = UndoneManager()


class Purchase(models.Model):
    transaction = models.ForeignKey(Transaction,related_name='purchases_in', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, related_name='in_purchases', on_delete=models.CASCADE)
    product_count = models.PositiveIntegerField()
    total_price = models.DecimalField(max_digits=10, decimal_places=1)

    def save(self, *args, **kwargs):
        self.total_price = self.product_count * self.product.price
        super(Purchase, self).save(*args, **kwargs)

    class Meta:
        ordering = ('-product_count',)

    def __str__(self):
        return 'we have {} {} is in transaction {}'.format(self.product_count,self.product,self.transaction)

Transaction.add_to_class('product_in',
                         models.ManyToManyField(Product,
                                         through=Purchase,
                                         related_name='in_transaction')
                         )