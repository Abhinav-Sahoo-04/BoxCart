from django.shortcuts import redirect, render,get_object_or_404
from django.contrib import messages
from store.forms import ReviewForm
from .models import Category
from .models import Product,Variation,ReviewRating
from cart.views import _cart_id
from cart.models import CartItem
from django.db.models import Q 
from orders.models import OrderProduct
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
    try :
        orderproduct=OrderProduct.objects.filter(user=request.user,product_id=product.id).exists()
    except OrderProduct.DoesNotExist:
        orderproduct=None
    # print(variation)
    try:
        review= ReviewRating.objects.filter(product_id=product.id,status=True)
        review_count=review.count()
    except ReviewRating.DoesNotExist:
        review=None
        review_count=0

    
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
        'orderproduct':orderproduct,
        'review':review,
        'review_count':review_count,
    }
    return render(request,"store/product_details.html",context)

def search(request):
    keyword=request.GET.get('keyword')
    products=Product.objects.filter(Q(product_name__icontains=keyword)|Q(description__icontains=keyword))
    context={
        "product":products,
    }
    return render(request,'store/store.html',context)


def submit_review(request,product_id):
    url=request.META.get('HTTP_REFERER')
    if request.method=='POST':
        try:
            review=ReviewRating.objects.get(user__id=request.user.id,product__id=product_id)
            print(review)
            form=ReviewForm(request.POST,instance=review)
            form.save()
            messages.success(request,"Thank you ! Your review have been updated")
            return redirect(url)
        except ReviewRating.DoesNotExist:
            form=ReviewForm(request.POST)
            if form.is_valid():
                data=ReviewRating()
                data.subject=form.cleaned_data['subject']
                data.review=form.cleaned_data['review']
                data.rating=form.cleaned_data['rating']
                data.ip=request.META.get('REMOTE_ADDR')
                data.user_id=request.user.id
                data.product_id=product_id
                data.save()
                messages.success(request,"Thank you for your review !")
                return redirect(url)



