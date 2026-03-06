from django.shortcuts import render

# Create your views here.
def cart(request):
    context={
        "title":"Cart",
    }
    return render(request,'store/cart.html',context)