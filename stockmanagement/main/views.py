from django.shortcuts import render,redirect
from django.core.paginator import Paginator , EmptyPage ,PageNotAnInteger
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
from .models import *
from django.contrib import messages
from django.db.models import Q
from django.http import JsonResponse,FileResponse
import json
from .forms import *
from datetime import datetime
from.decorators import shop_acounts,authentcateduser
from.filters import SaleFilter
from django.db.models import Avg,Sum,Count
from django.db.models import Q

import io
from reportlab.pdfgen import canvas
from reportlab.lib.units import inch
from reportlab.lib.pagesizes import letter
# Create your views here.

@login_required(login_url="login_process")
@shop_acounts
def home(request):
    products  = Product.objects.all()
    
    order_value = Product.objects.aggregate(Sum('purchacing_price'))
    selling_value = Product.objects.aggregate(Sum('price'))
    product_count = Product.objects.all().count
    dist_count = Branch.objects.all().count

    page = request.GET.get('page')
    paginator = Paginator(products, 100)
    try:
        products  = paginator.page(page)        
    except PageNotAnInteger:
        products  = paginator.page(1)
    except EmptyPage:
        products  = paginator.page(paginator.num_pages)
    context = {
        'products':products,
        'product_count':product_count,
        'dist_count':dist_count,
        'order_value':order_value,
        'selling_value':selling_value,
        
    }
    return render(request,'index.html',context)


@login_required(login_url="login_process")
@shop_acounts
def all_cat(request):
    cats = Category.objects.all()

    context = {
        "cats":cats
    }
    return render (request,'all_cats.html',context)


@login_required(login_url="login_process")
@shop_acounts
def all_type(request):
    types = Type.objects.all()
    context = {
        "types":types
    }
    return render (request,'all_type.html',context)



@login_required(login_url="login_process")
@shop_acounts
def all_dist(request):
    dist = Branch.objects.all()
    context = {
        "dist":dist
    }
    return render (request,'all_dist.html',context)


@login_required(login_url="login_process")
@shop_acounts
def add_dist(request):
    if request.method == 'POST':
        form = DistAddForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request,f"You have successfuly added a product ")
            return redirect('all_dist')
        else:
            messages.error(request,f"form is not valid ")
    else:
        form = DistAddForm 
    return render(request,'add_dist.html',{'form':form })


@login_required(login_url="login_process")
@shop_acounts
def history(request):
    history = StockHistory.objects.all().order_by('-id')

    page = request.GET.get('page')
    paginator = Paginator(history, 10)
    try:
        history = paginator.page(page)        
    except PageNotAnInteger:
        history = paginator.page(1)
    except EmptyPage:
        history = paginator.page(paginator.num_pages)

    context = {
        "history":history

    }
    
    return render (request,'history.html',context)


@login_required(login_url="login_process")
@shop_acounts
def create_product(request):
    if request.method == 'POST':
        form = ProductAddForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request,f"You have successfuly added a product ")
            return redirect('product_list')
        else:
            messages.error(request,f"form is not valid ")
    else:
        form = ProductAddForm 
    return render(request,'add.html',{'form':form })


@login_required(login_url="login_process")
@shop_acounts
def deleteRoom(request,pk):
    room = Product.objects.get(id=pk)
    if request.method == "POST":
        room.delete()
        return redirect ('home')
    return render(request,'delete.html',{'obj':room})




@login_required(login_url="login_process")
@shop_acounts
def add_cat(request):
    if request.method == 'POST':
        form = CatAddForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request,f"You have successfuly added a category")
            return redirect('all_cat')
        else:
            messages.error(request,f"form is not valid ")
    else:
        form = CatAddForm 
    return render(request,'add_cat.html',{'form':form })


@login_required(login_url="login_process")
@shop_acounts
def add_type(request):
    if request.method == 'POST':
        form = TypeAddForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request,f"You have successfuly added a type ")
            return redirect('all_type')
        else:
            messages.error(request,f"form is not valid ")
    else:
        form = TypeAddForm
    return render(request,'add_type.html',{'form':form })



@login_required(login_url="login_process")
@shop_acounts
def sales(request):
    sales = Sale.objects.all().order_by('-id')
    
    form = SaleSearch(request.POST or None)

    total = Sale.objects.aggregate(Sum('qty'))
    total_sales = 0
    
    for item in sales :
        total_sales += item.total()
    
    page = request.GET.get('page')
    paginator = Paginator(sales, 10)
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
    if request.method == "POST" or None:
        sales = Sale.objects.filter(
            date__range= [
                    form['start_date'].value(),
                    form['end_date'].value()
            ]
        )
        total = Sale.objects.filter(
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
                
            
            for line in range(lines):
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

    return render(request,'sales.html',context)

@login_required(login_url="login_process")
@shop_acounts
def product_list(request):
    q =  request.GET.get('q') 
    if q == None:
        products  = Product.objects.all()
    else:
        products = Product.objects.filter(Q(product_category__name__icontains=q)|
                                            Q(part_name__icontains=q)|
                                            Q(part_number__icontains=q)
                                             )
    page = request.GET.get('page')
    paginator = Paginator(products, 5)
    try:
        products  = paginator.page(page)        
    except PageNotAnInteger:
        products  = paginator.page(1)
    except EmptyPage:
        products  = paginator.page(paginator.num_pages)

    context = {
        "products":products,
    }
    return render(request,'products.html',context)


@login_required(login_url="login_process")
@shop_acounts
def delete_product(request,id):
    return render(request,'index.html')


@login_required(login_url="login_process")
@shop_acounts
def product_detail(request,pk):
	queryset = Product.objects.get(id=pk)
	context = {
		"title": queryset.part_name,
		"queryset": queryset,
	}
	return render(request, "product_detail.html", context)
    


@authentcateduser
def login_process(request):
    form = LoginForm(request.POST or None)
    msg = None
    if request.method == 'POST':
        if form.is_valid():
            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password")
            user=authenticate(request=request,username=username,password=password)  
            print(request.user)
            if user is not None:
                login(request=request,user=user)
                messages.success(request,f"You have successfuly logged in as {username} ")
                return redirect('home')
            else:
                msg =  'invalid credentials'
        else:
            form = LoginForm
    return render(request,'login.html',{'form':form, 'msg':msg})



def logout_process(request):
    logout(request)
    messages.success(request,"Logout Successfully")
    return render(request,'login.html')




@login_required(login_url="login_process")
@shop_acounts
def issue_items(request, pk):
    queryset = Product.objects.get(id=pk)

    form = IssueForm(request.POST or None, instance=queryset)
    if form.is_valid():
        instance = form.save(commit=False)
        print(instance.qyt)
        if instance.issue_quantity > instance.qyt :
            messages.error(request,"you Dont have this item in the where house")
            return redirect("product_detail", queryset.id)
        else:
            instance.qyt -= instance.issue_quantity
            instance.issue_by = str(request.user)
            instance.save()
            if Store.objects.filter(branch=instance.issued_to).exists():
                store = Store.objects.get(branch=instance.issued_to)
                if Storeitem.objects.filter(store=store,product=queryset).exists():
                    storeitem = Storeitem.objects.get(store=store,product=queryset)
                    storeitem.quantity = (storeitem.quantity  + instance.issue_quantity)
                    storeitem.save()
                    if storeitem.quantity <= 0:
                        storeitem.delete()
                else:
                    Storeitem.objects.create(store=store,product=queryset)
            else :
                Store.objects.create(branch=instance.issued_to)
                store = Store.objects.get(branch=instance.issued_to)
                storeitem = Storeitem.objects.create(store=store,product=queryset, quantity=instance.issue_quantity)
            
        
        StockHistory.objects.create(item_name = instance.part_name,receive_quantity = instance.issue_quantity,quantity = instance.qyt,receive_by = instance.issued_to,timestamp = datetime.now())  
        messages.success(request, "Successfully issued " + str(instance.issue_quantity) + " items to wherehouse you now have" + str(queryset.qyt)+ " items in store")
       
        return redirect('/product_detail/'+str(instance.id))
		# return HttpResponseRedirect(instance.get_absolute_url())

    context = {
		"queryset": queryset,
		"form": form,
	    }
    return render(request, "issueform.html", context)

def return_to_wherehouse(request,pk):
    item = Storeitem.objects.get(id=pk)
    number = item.quantity
    product_id = item.product.id
    queryset = Product.objects.get(id=product_id)
    form = RertunForm(request.POST or None, instance=item)
    if form.is_valid():
        instance = form.save(commit=False)
        instance.quantity = number- instance.quantity
        new_stock = queryset.qyt + instance.quantity
        form.save()
        p = StockHistory.objects.get()
        StockHistory.objects.create(item_name = instance.product.part_name,receive_quantity = instance.quantity,quantity = new_stock,receive_by = instance.product.issued_to,timestamp = datetime.now())  
        messages.success(request, "Successfully returned " + str(instance.quantity) + " items to wherehouse you now have" + str(queryset.qyt)+ " items in store")
        return redirect('/dist_detail/'+str(item.store.branch.id))
        
    context= {
        "form":form,
        }
    return render(request, "returnform.html",context)


@login_required(login_url="login_process")
@shop_acounts
def dist_detail(request,pk):
    store =""
    items = ""
    dist = Branch.objects.get(id=pk)
    try:
        store =  Store.objects.get(branch=dist)
        items = store.storeitem_set.all()
    except:
        pass
    
    
    context = {
        'dist':dist,
        'store':store,
        'items':items,
    }
    return render(request,'dist_detail.html',context)


@login_required(login_url="login_process")
@shop_acounts
def receive_items(request, pk):
    queryset = Product.objects.get(id=pk)
    form = ReceiveForm(request.POST or None, instance=queryset)
    if form.is_valid():
        instance = form.save(commit=False)
        instance.qyt += instance.receive_quantity
        instance.save()
        StockHistory.objects.create(item_name = instance.part_name,receive_quantity = instance.issue_quantity,quantity = instance.qyt,receive_by = 'receved',timestamp = datetime.now())  
        messages.success(request, "Received SUCCESSFULLY. You now have  " + str(instance.qyt) + " " + str(instance.part_name)+"s now in Store")
        return redirect('/product_detail/'+str(instance.id))
		# return HttpResponseRedirect(instance.get_absolute_url())
    context = {
			"title": 'Reaceive ' + str(queryset.part_name),
			"instance": queryset,
			"form": form,
			"username": 'Receive By: ' + str(request.user),
		}
    return render(request, "issueform.html", context)


@login_required(login_url="login_process")
@shop_acounts
def updateStore(request,id):
    data =  json.loads(request.body)
    productId =  data['productId']
    action =  data['action']

    print('Action:',action)
    print('productId:',productId)

    dist = Branch.objects.get(id=id)
    product = Product.objects.get(id=productId)
    order, created = Store.objects.get_or_create(customer=dist.name,complete = False)

    orderitem,created = Storeitem.objects.get_or_create(order=order,product=product)

    if action == "add":
        orderitem.quantity = (orderitem.quantity  + 1)
    elif action == "remove":
        orderitem.quantity = (orderitem.quantity  - 1)
    
    orderitem.save()

    if orderitem.quantity <= 0:
        orderitem.delete()

    return JsonResponse('item was added successfully',safe =  False)

