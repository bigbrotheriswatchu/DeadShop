from django.shortcuts import render, get_object_or_404
from shop.models import Collection, Tshirt, ProductInBasket

from django.http import JsonResponse


def index(request):
    collections = Collection.objects.all()
    return render(request, 'shop/index.html', context={'collections': collections})


def product(request, product_id):
    t_shirt = Tshirt.objects.get(id=product_id)

    session_key = request.session.session_key
    if not session_key:
        request.session.cycle_key()

    print(request.session.session_key)

    return render(request, 'shop/product.html', locals())


def list_of_tshirts_by_collection(request, collection_slug):

    t_shirt = Tshirt.objects.all()

    session_key = request.session.session_key
    if not session_key:
        request.session.cycle_key()

    print(request.session.session_key)

    if collection_slug:
        collection = get_object_or_404(Collection, slug__iexact=collection_slug)
        t_shirts = t_shirt.filter(collection=collection)

    template = 'shop/t_shirt_by_collection.html'
    context = {'t_shirts': t_shirts, 'collection': collection}
    return render(request, template, context, )


def basket_adding(request):
    return_dict = dict()
    session_key = request.session.session_key
    print(request.POST)
    data = request.POST
    product_id = data.get("t_shirt_id")
    t_shirt_name = data.get("t_shirt_name")
    nmb = data.get("nmb")
    print(nmb)

    new_product, created = ProductInBasket.objects.get_or_create(session_key=session_key, t_shirt_id=product_id, nmb=nmb)

    print(new_product)
    products_total_nmb = ProductInBasket.objects.filter(session_key=session_key, is_active=True).count()
    return_dict["products_total_nmb"] = products_total_nmb
    return JsonResponse(return_dict)