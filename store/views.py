from django.shortcuts import render,get_object_or_404
from .models import Category
from .models import Product
# Create your views here.
def store(request,category_slug=None):
    categories=None
    products=None
    title=None
    if category_slug!=None:
        categories=get_object_or_404(Category,slug=category_slug)
        products=Product.objects.filter(category=categories,is_available=True)
        product_conut=products.count()
        title=str(categories)+ ' items'

    else :
        products=Product.objects.all()
        product_conut=products.count()
        title="Store"
    context={
        "title":title,
        "product":products,
        "count":product_conut,
    }
    return render(request,'store/store.html',context)

def product_details(request,category_slug,product_slug):
    category_slug=category_slug.lower()
    category=get_object_or_404(Category,slug=category_slug)
    product=get_object_or_404(Product,slug=product_slug,category=category,is_available=True)
    print(product)
    context={
        'title':product.product_name,
        'product':product,
    }
    return render(request,"store/product_details.html",context)