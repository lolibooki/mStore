from django.shortcuts import render
from .forms import AddProductForm, ProductEditForm
from .models import Product, Transaction
from django.contrib import messages
from django.core.urlresolvers import reverse
from django.contrib import messages
from django.shortcuts import get_object_or_404
from .forms import PurchaseEditForm
from bot.forms import CustomerEditForm
from django.utils.crypto import get_random_string
from django.db.models import Sum
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect


@login_required()
def product_delete(request, id):
    try:
        Product.objects.filter(id=id).delete()
        messages.success(request,'محصول با موفقیت حذف شد')
    except Product.DoesNotExist:
        messages.error(request,'مشکلی در حذف محصول پیش آمده، شاید قبلا آن را حدف کرده اید')

    return HttpResponseRedirect(reverse('shop:storage'))


@login_required()
def product_edit(request, id):
    product = get_object_or_404(Product, id=id)
    if request.method == 'POST':
        product_edit_form = ProductEditForm(instance=product, data=request.POST, files=request.FILES)
        if product_edit_form.is_valid():
            product_edit_form.save()
            messages.success(request, 'محصول با موفقیت ویرایش شد')
        else:
            messages.error(request, 'خطا در ویرایش محصول')
    else:
        product_edit_form = ProductEditForm()
    return render(request,
                  'product_edit.html',
                  {'product_edit_form':product_edit_form,
                   'product': product})


@login_required()
def storage(request):
    print(request)
    products = Product.objects.all()
    if request.method == 'POST':
        product_form = AddProductForm(request.POST,
                                      files=request.FILES)
        if product_form.is_valid():
            product_form.save()
            messages.success(request, 'محصول جدید اضافه شد')
        else:
            messages.error(request, 'خطا در ایجاد محصول')
    else:
        product_form = AddProductForm()
    return render(request,
                  'storage.html',
                  {'section':'storage',
                   'products':products,
                   'product_form':product_form})
# Create your views here.


@login_required()
def statistic(request):
    return render(request,
                  'statistic.html',
                  {'section':'statistic'})


@login_required()
def transaction_delete(request, id):
    try:
        Transaction.objects.filter(id = id).delete()
        messages.success(request,'سفارش با موفقیت لغو شد')
    except Transaction.DoesNotExist:
        messages.error(request,'مشکلی در لغو سفارش پیش آمد، شاید قبلا لغو کرده اید')

    return HttpResponseRedirect(reverse('dashboard'))


@login_required()
def transaction_accept(request, id):
    try:
        transaction = Transaction.objects.get(id = id)
        transaction.accepted = True
        transaction.save()
        messages.success(request, 'سفارش با موفقیت ثبت شد')
    except Transaction.DoesNotExist:
        messages.success(request, 'مشکلی در ثبت سفارش پیش آمد، شاید قبلا ثبت کرده اید')
    return HttpResponseRedirect(reverse('dashboard'))


@login_required()
def transaction_edit(request, id):
    transaction = get_object_or_404(Transaction,id=id, done=False)
    purchases = transaction.purchases_in.all()
    customer = transaction.shopper
    purchase_forms_dict = {}
    if request.method == 'POST':
        customer_edit_form = CustomerEditForm(instance=customer,data=request.POST, prefix='customer')
        if customer_edit_form.is_valid():
            customer_edit_form.save()
        for purchase in purchases:
            purchase_edit_form = PurchaseEditForm(instance=purchase ,data=request.POST, prefix=str(purchase.id))
            purchase_forms_dict[purchase] = purchase_edit_form
            if purchase_edit_form.is_valid():
                purchase_edit_form.save()
        transaction.total_price = transaction.purchases_in.aggregate(total_price=Sum('total_price'))['total_price']
        transaction.save()

    else:
        customer_edit_form = CustomerEditForm(prefix='customer')
        customer_edit_form.fields['address'].widget.attrs['placeholder'] = customer.address
        customer_edit_form.fields['mobile'].widget.attrs['value'] = customer.mobile
        customer_edit_form.fields['phone'].widget.attrs['value'] = customer.phone
        for purchase in purchases:
            purchase_edit_form = PurchaseEditForm(prefix=str(purchase.id))
            purchase_edit_form.fields['product_count'].widget.attrs['value'] = purchase.product_count
            purchase_forms_dict[purchase] = purchase_edit_form

    return render(request,
                  'transaction_edit.html',
                  {'customer_edit_form':customer_edit_form,
                   'transaction':transaction,
                   'purchase_forms_dict':purchase_forms_dict
                   })