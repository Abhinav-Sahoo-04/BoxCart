from django.shortcuts import get_object_or_404, render,redirect
from django.core.exceptions import ObjectDoesNotExist
from cart.models import Cart, CartItem
from store.models import Product,Variation
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required

# Create your views here.
def cart(request,total=0,qunatity=0,cart_items=None):
    # cart = Cart.objects.get(cart_id=_cart_id(request))
    tax=0
    grand_total=0
    try:
        if request.user.is_authenticated:
            cart_items=CartItem.objects.filter(user=request.user,is_active=True)
        else:
            cart = Cart.objects.get(cart_id=_cart_id(request))
            cart_items=CartItem.objects.filter(cart=cart,is_active=True)
        for cart_item in cart_items:
            total+=(cart_item.product.price*cart_item.quantity)
            qunatity+=cart_item.quantity
        tax=(5*total)/100
        grand_total=tax+total
    except ObjectDoesNotExist:
        pass
    context={
        "title":"Cart",
        "cart_items":cart_items,
        "total":total,
        "quantity":qunatity,
        "tax":tax,
        "grand_total":grand_total,
    }   
    return render(request,'store/cart.html',context)
def remove_cart(request,product_id,cart_item_id):
    product=get_object_or_404(Product,id=product_id)
    try:
        if request.user.is_authenticated:
            cart_item=CartItem.objects.get(user=request.user,product=product,id=cart_item_id) 
        else:
            cart=Cart.objects.get(cart_id=_cart_id(request))
            cart_item=CartItem.objects.get(cart=cart,product=product,id=cart_item_id)
        if cart_item.quantity>1:
            cart_item.quantity-=1
            cart_item.save()
        else:
            cart_item.delete()
        return redirect('cart')
    except:
        pass
def _cart_id(request):
    cart=request.session.session_key
    if not cart:
        cart=request.session.create()
    return cart
def remove_cart_item(request,product_id,cart_item_id):
    product=get_object_or_404(Product,id=product_id)
    try:
        if request.user.is_authenticated:
            cart_item=CartItem.objects.get(product=product,user=request.user,id=cart_item_id)
        else:
            cart=Cart.objects.get(cart_id=_cart_id(request))    
            cart_item=CartItem.objects.get(cart=cart,product=product,id=cart_item_id)
        cart_item.delete()
    except:
        pass
    return redirect('cart')

def add_cart(request,product_id):
    current_user=request.user
    if current_user.is_authenticated:
        product=Product.objects.get(id=product_id)
        product_variation=[]
        if request.method=="POST":
            for item in request.POST:
                key=item
                value=request.POST[key]

                try:
                    variation=Variation.objects.get(product=product,variation_category__iexact=key,variation_value__iexact=value)
                    product_variation.append(variation)
                except:
                    pass


        is_cart_item_exist=CartItem.objects.filter(product=product,user=current_user).exists()
        if is_cart_item_exist:
            cart_item=CartItem.objects.filter(user=current_user,product=product)
            ex_var_list=[]
            id=[]
            for item in cart_item:
                existing_variation=item.variation.all()
                ex_var_list.append(list(existing_variation))
                id.append(item.id)
            print(product_variation)
            if product_variation in ex_var_list:
                index=ex_var_list.index(product_variation)
                item_id=id[index]
                cart_item_ex=CartItem.objects.get(id=item_id,product=product)
                cart_item_ex.quantity+=1
                cart_item_ex.save()
            else:
                item=CartItem.objects.create(product=product,quantity=1,user=current_user)
                if len(product_variation)>0:
                    item.variation.clear()
                    item.variation.add(*product_variation)
                item.save()

        else:
            cart_item=CartItem.objects.create(
                product=product,
                quantity=1,
                user=current_user,
            )
            if len(product_variation)>0:
                cart_item.variation.clear()
                cart_item.variation.add(*product_variation)
            cart_item.save()
        # return HttpResponse(cart_item.product)
        return redirect('cart')

    else:
        product=Product.objects.get(id=product_id)
        product_variation=[]
        if request.method=="POST":
            for item in request.POST:
                key=item
                value=request.POST[key]

                try:
                    variation=Variation.objects.get(product=product,variation_category__iexact=key,variation_value__iexact=value)
                    product_variation.append(variation)
                except:
                    pass

        try:
            cart=Cart.objects.get(cart_id=_cart_id(request))
        except Cart.DoesNotExist:
            cart=Cart.objects.create(
                cart_id=_cart_id(request),
            )
            cart.save()

        is_cart_item_exist=CartItem.objects.filter(product=product,cart=cart).exists()
        if is_cart_item_exist:
            cart_item=CartItem.objects.filter(cart=cart,product=product)
            ex_var_list=[]
            id=[]
            for item in cart_item:
                existing_variation=item.variation.all()
                ex_var_list.append(list(existing_variation))
                id.append(item.id)
            print(product_variation)
            if product_variation in ex_var_list:
                index=ex_var_list.index(product_variation)
                item_id=id[index]
                cart_item_ex=CartItem.objects.get(id=item_id,product=product)
                cart_item_ex.quantity+=1
                cart_item_ex.save()
            else:
                item=CartItem.objects.create(product=product,quantity=1,cart=cart)
                if len(product_variation)>0:
                    item.variation.clear()
                    item.variation.add(*product_variation)
                item.save()

        else:
            cart_item=CartItem.objects.create(
                product=product,
                quantity=1,
                cart=cart,
            )
            if len(product_variation)>0:
                cart_item.variation.clear()
                cart_item.variation.add(*product_variation)
            cart_item.save()
        # return HttpResponse(cart_item.product)
        return redirect('cart')

@login_required(login_url='login')
def checkout(request,total=0,qunatity=0,cart_items=None):
    tax=0
    grand_total=0
    try:
        if request.user.is_authenticated:
            cart_items=CartItem.objects.filter(user=request.user,is_active=True)
        else:
            cart = Cart.objects.get(cart_id=_cart_id(request))
            cart_items=CartItem.objects.filter(cart=cart,is_active=True)
        for cart_item in cart_items:
            total+=(cart_item.product.price*cart_item.quantity)
            qunatity+=cart_item.quantity
        tax=(5*total)/100
        grand_total=tax+total
    except ObjectDoesNotExist:
        pass
    context={
        "title":"Checkout",
        "cart_items":cart_items,
        "total":total,
        "quantity":qunatity,
        "tax":tax,
        "grand_total":grand_total,
    }   
    return render (request,'checkout.html',context)