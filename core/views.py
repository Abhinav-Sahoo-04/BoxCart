from django.shortcuts import render
from store.models import Product
def home(request):
    product=Product.objects.all().filter(is_available=True)
    context={
        "product":product,
        "title":"Homepage",
    }
    return render(request,'home.html',context)