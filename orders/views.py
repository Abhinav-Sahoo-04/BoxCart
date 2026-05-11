from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from django.shortcuts import redirect, render
from django.http import HttpResponse,JsonResponse
import datetime
import json
from cart.models import CartItem
from orders.forms import OrderedForm
from orders.models import Order, OrderProduct, Payment
from store.models import Product
# Create your views here.
def place_order(request,total=0,qunatity=0):
    current_user=request.user

    # Check if the cart item count is <0 if yes then redirect to the store
    cart_item=CartItem.objects.filter(user=current_user)
    if cart_item.count() <= 0:
        return redirect('store')
    
    total=0
    tax=0
    if request.method=='POST':
        form=OrderedForm(request.POST)
        for item in cart_item:
            total+=(item.product.price*item.quantity)
            qunatity+=item.quantity
        tax=(5*total)/100
        grand_total=tax+total
        if form.is_valid():
            data=Order()
            data.user=current_user
            data.first_name=form.cleaned_data['first_name']
            data.last_name=form.cleaned_data['last_name']
            data.phone=form.cleaned_data['phone']
            data.email=form.cleaned_data['email']
            data.address_line_1=form.cleaned_data['address_line_1']
            data.address_line_2=form.cleaned_data['address_line_2']
            data.country=form.cleaned_data['country']
            data.state=form.cleaned_data['state']
            data.city=form.cleaned_data['city']
            data.order_note=form.cleaned_data['order_note']
            data.order_total=grand_total
            data.tax=tax
            data.ip=request.META.get('REMOTE_ADDR')
            data.save()
            # Generating the order numbber
            yr=int(datetime.date.today().strftime('%Y'))
            dt=int(datetime.date.today().strftime('%d'))
            mt=int(datetime.date.today().strftime('%m'))
            date=datetime.date(yr,mt,dt)
            current_date=date.strftime("%Y%m%d")
            order_number=current_date+str(data.id)
            data.order_number=order_number
            data.save()
            
            order=Order.objects.get(user=current_user,is_ordered=False,order_number=order_number)
            context={
                'title':"Payment",
                'order':order,
                'cart_item':cart_item,
                'tax': tax,
                'total':total,
                'grand_total':grand_total,

            }
            return render(request,'orders/payment.html',context)
        else:
            return redirect('checkout')

def payment(request):

    #Transaction details are stored in the Payment product
    data=json.loads(request.body)
    print(data)

    order=Order.objects.get(user=request.user,is_ordered=False,order_number=data['orderID'])

    payment=Payment(
        user=request.user,
        payment_id=data['transID'],
        payment_method=data['payment_method'],
        amount_paid=order.order_total,
        status=data['status'],
    )
    payment.save()

    order.payment=payment
    order.is_ordered=True
    order.save()

    # Storing the data in the OrderProduct Model

    cart_items=CartItem.objects.filter(user=request.user)
    for item in cart_items:
        orderproduct=OrderProduct()
        orderproduct.order_id=order.id
        orderproduct.payment=payment
        orderproduct.user_id=request.user.id
        orderproduct.product_id=item.product.id
        orderproduct.quantity=item.quantity
        orderproduct.product_price=item.product.price
        orderproduct.ordered=True
        orderproduct.save()
        cart_item=CartItem.objects.get(id=item.id)
        product_variation=cart_item.variation.all()
        orderproduct=OrderProduct.objects.get(id=orderproduct.id)
        orderproduct.variation.set(product_variation)
        orderproduct.save()


        # Reduce the quantity of sold Product
        product=Product.objects.get(id=item.product_id)
        product.stock-=item.quantity
        product.save()


    #Clear the Cart 
    CartItem.objects.filter(user=request.user).delete()

    #Send the order email
    mail_subject="Thankyou for your order !"
    message=render_to_string('orders/order_recieved_email.html',{
        "user":request.user,
        "order":order,
            })
    to_mail=request.user.email
    send_mail=EmailMessage(mail_subject,message,to=[to_mail])
    send_mail.send()

    #send JsonResponse to the user
    data={
        'Order_ID':order.order_number,
        'Trans_ID':payment.payment_id, 
    }
    return JsonResponse(data)

    # return render(request,'orders/payment.html')


def order_complete(request):
    orderID=request.GET.get('order_number')
    payment_id=request.GET.get('payment_id')
    order=Order.objects.get(order_number=orderID,is_ordered=True)
    orderproduct=OrderProduct.objects.filter(order_id=order.id)
    payment=Payment.objects.get(payment_id=payment_id)

    subtotal=0
    for i in orderproduct:
        subtotal+=i.product_price*i.quantity
    

    context={
        'orderID':orderID,
        'transID':payment_id,
        'order':order,
        'orderproduct':orderproduct,
        'payment':payment,
        'subtotal':subtotal,
    }
    return render(request,'orders/order_complete.html',context)