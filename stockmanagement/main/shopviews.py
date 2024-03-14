from django.shortcuts import render,redirect
from .models import *
from django.http import FileResponse
from django.contrib import messages
from .forms import SaleForm
from datetime import datetime
from django.core.paginator import Paginator , EmptyPage ,PageNotAnInteger
from django.db.models import Avg,Sum,Count
from .forms import *

from django.db.models import Q

import io
from reportlab.pdfgen import canvas
from reportlab.lib.units import inch
from reportlab.lib.pagesizes import letter



def home(request):
    dist = ""
    store = ""
    items = ""
    sales = ""
    try:
        user = request.user.id
        dist = Branch.objects.get(id=user)
        store =  Store.objects.get(branch=dist)
        items = store.storeitem_set.all()
        sales = Sale.objects.filter(store=dist).count()
    except:
        pass
    context = {
        'dist':dist,
        'store':store,
        'items':items,
        'sales':sales
    }
    return render(request,'shop/home.html',context)

def product_list(request):
    user = request.user.id
    dist = Branch.objects.get(id=user)
    store =  Store.objects.get(branch=dist)
    items = store.storeitem_set.all()
    page = request.GET.get('page')
    paginator = Paginator(items, 1)
    try:
        items = paginator.page(page)        
    except PageNotAnInteger:
        items = paginator.page(1)
    except EmptyPage:
        items = paginator.page(paginator.num_pages)

   
    context = {
        'dist':dist,
        'store':store,
        'items':items,
    }
    return render(request,'shop/products.html',context)


def sales(request):
    user = request.user.id
    dist = Store.objects.get(branch=user)
    sales = Sale.objects.filter(store=dist).order_by('-id')
    form = SaleSearch(request.POST or None)
    total = Sale.objects.filter(store=dist).aggregate(Sum('qty'))
    total_sales = 0
    
    for item in sales :
        total_sales += item.total()

    page = request.GET.get('page')
    paginator = Paginator(sales, 30)
    try:
        sales = paginator.page(page)        
    except PageNotAnInteger:
        sales = paginator.page(1)
    except EmptyPage:
        sales = paginator.page(paginator.num_pages)
    context = {
        'sale':sales,
        'total_sales':total_sales,
        'total':total,
        'form':form,
    }
    if request.method == "POST" or None:
        sales = Sale.objects.filter(
            store=dist,
            date__range= [
                    form['start_date'].value(),
                    form['end_date'].value()
            ]
        )
        total = Sale.objects.filter(
                store=dist,
                date__range= [
                    form['start_date'].value(),
                    form['end_date'].value()
            ]
            ).aggregate(Sum('qty'))
        if form['print_pdf'].value() ==True:
            buf = io.BytesIO()
            c = canvas.Canvas(buf,pagesize=letter,bottomup=0)
            textob = c.beginText()
            textob.setTextOrigin(inch,inch)
            textob.setFont('Helvetica',14)
            # Add some of lines 
            print(sales)
            lines = []
            for sale in sales:
                lines.append(f'Part Name  :' + sale.product.product.part_name)
                lines.append(f'Branch  :' + sale.store.branch.name)
                lines.append(f'Part Number  :' + str(sale.product.product.part_number))
                lines.append(f'Quantity  :' + str(sale.qty)+ ' Units')
                lines.append(f'Price USD  :' + str(sale.product.product.price) + '.00')
                lines.append(f'Total  :' + str(sale.total()) + '.00')
                lines.append("=========================")
            
            for line in lines:
                textob.textLine(line)


            c.drawText(textob)
            c.showPage()
            c.save()
            buf.seek(0)

            return FileResponse(buf,as_attachment=True,filename='sales.pdf')

        total_sales = 0
    
        for item in sales :
            total_sales += item.total()
        
        page = request.GET.get('page')
        paginator = Paginator(sales, 20)
        try:
            sales = paginator.page(page)        
        except PageNotAnInteger:
            sales = paginator.page(1)
        except EmptyPage:
            sales = paginator.page(paginator.num_pages)
           
        context = {
                'sale':sales,
                'total':total,
                'total_sales':total_sales,
                'form':form,
    }

    return render(request,'shop/sales.html',context)

def make_sale(request,id):
    user = request.user.id
    dist = Branch.objects.get(id=user)
    store =  Store.objects.get(branch=dist)
    items = store.storeitem_set.all()
    product = Storeitem.objects.get(id=id)
    store_quantity = product.quantity
    if product.quantity == 0:
        messages.error(request,f"This item is not available in store")
        return redirect('shop_products')
    if request.method == 'POST':
        form = SaleForm(request.POST or None, instance=product)
        if form.is_valid():
            qyt = form.cleaned_data['qty']
            if qyt > product.quantity:
                messages.error(request, "Your quantity is higher than whats available in stock")
                return redirect('shop_products')
            else:
                Sale.objects.create(product=product,store=store,qty=qyt,date=datetime.now())
                form.save()
                product.quantity = store_quantity - qyt
                product.save()
                messages.success(request,f"You have successfuly made a sale ")
                return redirect('shop_products')
        else:
            messages.error(request,f"form is not valid ")
    else:
        form = SaleForm
    
    context = {
        'form':form,
    }

    return render(request,'shop/make_sale.html',context)
