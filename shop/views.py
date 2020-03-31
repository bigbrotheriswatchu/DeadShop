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
    product_id = data.get("product_id")
    nmb = data.get("nmb")
    is_delete = data.get("is_delete")

    if is_delete == 'true':
        ProductInBasket.objects.filter(id=product_id).update(is_active=False)
    else:
        new_product, created = ProductInBasket.objects.get_or_create(session_key=session_key,
                                                                     t_shirt_id=product_id,
                                                                     is_active=True,
                                                                     defaults={"nmb": nmb})
        if not created:
            new_product.nmb += int(nmb)
            new_product.save(force_update=True)

    products_in_basket = ProductInBasket.objects.filter(session_key=session_key, is_active=True)



    products_total_nmb = products_in_basket.count()
    return_dict["products_total_nmb"] = products_total_nmb

    return_dict["products"] = list()
    for item in products_in_basket:
        total_price = 0
        total_price += item.total_price

        product_dict = dict()
        product_dict["name"] = item.t_shirt.name
        product_dict["id"] = item.id
        product_dict["price_per_item"] = item.price_per_item
        product_dict["nmb"] = item.nmb
        return_dict["products"].append(product_dict)
        print(return_dict)



    return JsonResponse(return_dict)


def checkout(request):
    session_key = request.session.session_key
    products_in_basket = ProductInBasket.objects.filter(session_key=session_key, is_active=True)
    return render(request, 'shop/checkout.html', locals())
