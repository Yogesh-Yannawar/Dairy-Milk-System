from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Sum
from farmers.models import Farmer
from .models import MilkCollection, Inventory, InventoryTransaction
from datetime import date

@login_required
def collection_list(request):
    filter_date = request.GET.get('date', str(date.today()))
    shift = request.GET.get('shift', '')
    collections = MilkCollection.objects.select_related('farmer').filter(date=filter_date)
    if shift:
        collections = collections.filter(shift=shift)
    total_qty = collections.aggregate(Sum('quantity'))['quantity__sum'] or 0
    total_amt = collections.aggregate(Sum('total_amount'))['total_amount__sum'] or 0
    context = {'collections': collections, 'filter_date': filter_date, 'shift': shift,
               'total_qty': total_qty, 'total_amt': total_amt}
    return render(request, 'milk/list.html', context)

@login_required
def collection_add(request):
    farmers = Farmer.objects.filter(is_active=True)
    if request.method == 'POST':
        farmer_id = request.POST.get('farmer')
        coll_date = request.POST.get('date')
        shift = request.POST.get('shift')
        farmer = get_object_or_404(Farmer, pk=farmer_id)
        if MilkCollection.objects.filter(farmer=farmer, date=coll_date, shift=shift).exists():
            messages.error(request, 'Entry already exists for this farmer, date and shift.')
        else:
            MilkCollection.objects.create(
                farmer=farmer,
                date=coll_date,
                shift=shift,
                quantity=request.POST.get('quantity'),
                fat=request.POST.get('fat'),
                snf=request.POST.get('snf'),
            )
            messages.success(request, 'Milk collection recorded!')
            return redirect('collection_list')
    return render(request, 'milk/form.html', {'farmers': farmers, 'title': 'Record Collection', 'today': date.today()})

@login_required
def collection_edit(request, pk):
    collection = get_object_or_404(MilkCollection, pk=pk)
    farmers = Farmer.objects.filter(is_active=True)
    if request.method == 'POST':
        collection.quantity = request.POST.get('quantity')
        collection.fat = request.POST.get('fat')
        collection.snf = request.POST.get('snf')
        collection.save()
        messages.success(request, 'Collection updated!')
        return redirect('collection_list')
    return render(request, 'milk/form.html', {'collection': collection, 'farmers': farmers, 'title': 'Edit Collection'})

@login_required
def collection_delete(request, pk):
    collection = get_object_or_404(MilkCollection, pk=pk)
    if request.method == 'POST':
        collection.delete()
        messages.success(request, 'Entry deleted.')
        return redirect('collection_list')
    return render(request, 'milk/confirm_delete.html', {'collection': collection})

@login_required
def inventory_list(request):
    items = Inventory.objects.all()
    return render(request, 'milk/inventory.html', {'items': items})

@login_required
def inventory_add(request):
    if request.method == 'POST':
        Inventory.objects.create(
            name=request.POST.get('name'),
            category=request.POST.get('category'),
            unit=request.POST.get('unit'),
            min_stock=request.POST.get('min_stock'),
            price_per_unit=request.POST.get('price_per_unit'),
        )
        messages.success(request, 'Item added!')
        return redirect('inventory_list')
    return render(request, 'milk/inventory_form.html')

@login_required
def stock_transaction(request, pk):
    item = get_object_or_404(Inventory, pk=pk)
    if request.method == 'POST':
        qty = float(request.POST.get('quantity'))
        t_type = request.POST.get('transaction_type')
        InventoryTransaction.objects.create(
            item=item, transaction_type=t_type, quantity=qty,
            date=date.today(), notes=request.POST.get('notes', '')
        )
        if t_type == 'in':
            item.current_stock += qty
        else:
            item.current_stock -= qty
        item.save()
        messages.success(request, 'Stock updated!')
        return redirect('inventory_list')
    return render(request, 'milk/stock_form.html', {'item': item})
