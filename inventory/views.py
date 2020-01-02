from django.db.models import Sum, Count, F
from django.http import HttpResponse
from django.shortcuts import render
from django.template import loader

from inventory.forms import SearchForm
from inventory.models import Item, Container, ItemTag


def search(request):
    form = SearchForm(request.GET)
    if form.is_valid():
        context = {
            'items': Item.objects.annotate(total_count=Sum('quantity')),
            'containers': Container.objects,
            'results': form.get_results()
        }
        return render(request, 'search.html', context)


def index(request):
    restock_query = Item.objects.all().filter(quantity__lte=F('alert_quantity'))
    context = {
        'item_query': Item.objects.aggregate(item_count=Sum('quantity')),
        'containers': Container.objects,
        'restock_items': restock_query
    }
    print(context)
    return render(request, 'index.html', context)


def add(request):
    return render(request, 'add.html', {})


def item_detail(request, item_id):
    context = {'item': Item.objects.get(id=item_id)}
    return render(request, 'item_detail.html', context)


def container_detail(request, container_id):
    context = {'container': Container.objects.get(id=container_id)}
    return render(request, 'container_detail.html', context)


def tag_detail(request, tag_name):
    tag = ItemTag.objects.get(pk=tag_name)
    context = {'tag': tag}
    return render(request, 'tag_detail.html', context)
