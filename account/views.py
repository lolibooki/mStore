from django.shortcuts import render
from .forms import UserRegistrationForm
from django.contrib.auth.decorators import login_required
from shop.models import Product, Transaction
from django.core.paginator import Paginator, EmptyPage,PageNotAnInteger
from django.http import HttpResponse, HttpResponseRedirect



def register(request):
    if request.method == 'POST':
        user_form = UserRegistrationForm(request.POST)
        if user_form.is_valid():
            new_user = user_form.save(commit=False)
            new_user.set_password(user_form.cleaned_data['password'])
            new_user.save()
        return render(request,
                      'account/register_done.html',
                      {'new_user': new_user})
    else :
        user_form = UserRegistrationForm()
    return render(request,
                  'account/register.html',
                  {'user_form': user_form})


@login_required
def dashboard(request):
    transactions = Transaction.undone.all()
    trans_paginator = Paginator(transactions,5)
    trans_page = request.GET.get('trans_page')

    products = Product.objects.all()[:10]
#   product_paginator = Paginator(products, 8)
#   product_page = request.GET.get('product_page')
    try:
        transactions = trans_paginator.page(trans_page)
    except PageNotAnInteger:
        # If page is not an integer deliver the first page
        transactions = trans_paginator.page(1)
    except EmptyPage:
        if request.is_ajax():
            # If the request is AJAX and the page is out of range
            # return an empty page
            return HttpResponse('')
        # If page is out of range deliver last page of results
            transactions = trans_paginator.page(trans_paginator.num_pages)
    if request.is_ajax():
        return render(request,
                      'account/trans_ajax.html',
                      {'section': 'dashboard',
                       'products': products,
                       'transactions':transactions})
    return render(request,
                  'account/dashboard.html',
                  {'section': 'dashboard',
                   'products': products ,
                   'transactions': transactions})


