from django.shortcuts import redirect, render,get_object_or_404
from .models import Category
from .models import Product,Variation
from cart.views import _cart_id
from cart.models import CartItem
from django.db.models import Q 
from django.core.paginator import EmptyPage,PageNotAnInteger,Paginator
# Create your views here.
def store(request,category_slug=None):
    categories=None
    products=None
    title=None
    page_interval=6
    if category_slug!=None:
        categories=get_object_or_404(Category,slug=category_slug)
        products=Product.objects.filter(category=categories,is_available=True)
        product_conut=products.count()
        if page_interval>=product_conut:
            page_numbers=1
        else:
            page_numbers=(product_conut//page_interval)+1
        print(page_numbers)
        title=str(categories)+ ' items'
        paginator=Paginator(products,page_interval)
        page=request.GET.get('page')
        paged_product=paginator.get_page(page)
    else :
        products=Product.objects.filter(is_available=True)
        product_conut=products.count()
        paginator=Paginator(products,page_interval)
        page=request.GET.get('page')
        paged_product=paginator.get_page(page)
        if page_interval>=product_conut:
            page_numbers=1
        else:
            page_numbers=(product_conut//page_interval)+1
        print(page_numbers)
        title="Store"
    context={
        "title":title,
        "product":paged_product,
        "count":product_conut,
        "page_numbers":range(1,page_numbers+1),
    }
    return render(request,'store/store.html',context)

def product_details(request,category_slug,product_slug):
    category_slug=category_slug.lower()
    category=get_object_or_404(Category,slug=category_slug)
    product=get_object_or_404(Product,slug=product_slug,category=category,is_available=True)
    in_cart=CartItem.objects.filter(cart__cart_id=_cart_id(request),product=product).exists()
    variation=Variation.objects.filter(product=product)
    print(variation)
    variation_colors=variation.filter(variation_category='color')
    variation_color=[i.variation_value for i in variation_colors]
    variation_sizes=variation.filter(variation_category='size')
    variation_size=[i.variation_value for i in variation_sizes]
    # print(variation_color,variation_size)
    context={
        'title':product.product_name,
        'product':product,
        "in_cart":in_cart,
        'variation_color':variation_color,
        "variation_size":variation_size,
    }
    return render(request,"store/product_details.html",context)

def search(request):
    keyword=request.GET.get('keyword')
    products=Product.objects.filter(Q(product_name__icontains=keyword)|Q(description__icontains=keyword))
    context={
        "product":products,
    }
    return render(request,'store/store.html',context)