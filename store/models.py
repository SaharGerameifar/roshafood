from django.db import models
from django.contrib.auth.models import User
from . import helper
from django.urls import reverse


class Category(models.Model):
    title = models.CharField(max_length=100, unique=True, verbose_name="عنوان")
    slug = models.SlugField(max_length=100, unique=True, allow_unicode=True, verbose_name="آدرس")
    parentCategory = models.ForeignKey('self', on_delete=models.SET_NULL, null=True, blank=True,
                                       verbose_name="سر دسته")

    class Meta:
        verbose_name_plural = 'دسته بندي ها'
        verbose_name = 'دسته بندي'

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('category', args=[self.slug])


class Product(models.Model):
    title = models.CharField(max_length=100, unique=True, verbose_name="عنوان")
    content = models.TextField(verbose_name="توضيحات")
    status = models.BooleanField(default=False, verbose_name="وضعيت")
    price = models.DecimalField(max_digits=11, decimal_places=0, default=0, verbose_name="قيمت")
    category = models.ManyToManyField(Category, blank=True, verbose_name="دسته بندي")
    pic = models.ImageField(upload_to='upload/product/images', default='upload/images/no-img.jpg', verbose_name="تصوير")
    recommended_product = models.ManyToManyField('self', blank=True,verbose_name="محصولات پيشنهادي")

    class Meta:
        ordering = ('-id',)
        verbose_name_plural = 'محصولات'
        verbose_name = 'محصول'

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('product-detail', args=[self.id])


class Order(models.Model):
    name = models.CharField(max_length=200, verbose_name="نام مشتري")
    family = models.CharField(max_length=200, verbose_name="نام خانوادگي مشتري")
    email = models.EmailField(max_length=200,null=True, verbose_name="ايميل مشتري")
    mobile = models.CharField(max_length=11, verbose_name="شماره تماس مشتري")
    address = models.TextField(max_length=500, blank=True, verbose_name="آدرس مشتري")
    authority = models.CharField(max_length=100, blank=True)
    refId = models.CharField(max_length=100, blank=True, verbose_name="كد پيگيري")
    order_date = models.DateTimeField(auto_now_add=True, verbose_name="تاريخ ثبت سفارش")
    random_order_id = models.IntegerField(default=helper.random_int, unique=True, verbose_name=" شماره سفارش")
    COMPLETED = 1
    CANCELED = 2
    INPROGRESS = 3
    CHECKING = 4
    PAYMENTTING = 5
    Order_statuses = (
        (COMPLETED, 'Completed'),
        (CANCELED, 'Canceled'),
        (INPROGRESS, 'In progress'),
        (CHECKING, 'Checking'),
        (PAYMENTTING, 'Paymentting'),
    )
    order_status = models.IntegerField(
        choices=Order_statuses,
        default=CHECKING,
    )
    amount = models.IntegerField(default=0, blank=True)


    class Meta:
        verbose_name_plural = 'سبدهاي خريد'
        verbose_name = 'سبد خريد'

    def __str__(self):
        return str(self.random_order_id)

    def get_total_cost(self):
        return sum(item.get_cost for item in self.items.all)


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items', verbose_name="نام سفارش")
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name="نام محصول")
    count = models.IntegerField(verbose_name="تعداد ")
    price = models.DecimalField(max_digits=11, decimal_places=0, default=0, verbose_name="قيمت ")

    class Meta:
        verbose_name_plural = 'جزئيات سبدهاي خريد'
        verbose_name = 'جزئيات سبد خريد'


    def __str__(self):
        return 'Create Time:%s Order id:%s Product:%s Name:%s Mobile:%s' % ( self.order.order_date, self.order, self.product, self.order.family, self.order.mobile)

    def get_cost(self):
        return self.price * self.count





    