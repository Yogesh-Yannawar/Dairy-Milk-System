from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Sum, Q
from milk_collection.models import MilkCollection
from .models import Farmer
from datetime import date

@login_required
def farmer_list(request):
    q = request.GET.get('q', '')
    farmers = Farmer.objects.all()
    if q:
        farmers = farmers.filter(Q(name__icontains=q) | Q(farmer_id__icontains=q) | Q(phone__icontains=q))
    return render(request, 'farmers/list.html', {'farmers': farmers, 'q': q})

@login_required
def farmer_add(request):
    if request.method == 'POST':
        farmer_id = request.POST.get('farmer_id')
        if not Farmer.objects.filter(farmer_id=farmer_id).exists():
            Farmer.objects.create(
                farmer_id=farmer_id,
                name=request.POST.get('name'),
                address=request.POST.get('address'),
                phone=request.POST.get('phone'),
                email=request.POST.get('email', ''),
                bank_name=request.POST.get('bank_name', ''),
                account_number=request.POST.get('account_number', ''),
                ifsc_code=request.POST.get('ifsc_code', ''),
                joining_date=request.POST.get('joining_date'),
            )
            messages.success(request, 'Farmer added successfully!')
            return redirect('farmer_list')
        else:
            messages.error(request, 'Farmer ID already exists.')
    return render(request, 'farmers/form.html', {'title': 'Add Farmer'})

@login_required
def farmer_edit(request, pk):
    farmer = get_object_or_404(Farmer, pk=pk)
    if request.method == 'POST':
        farmer.name = request.POST.get('name')
        farmer.address = request.POST.get('address')
        farmer.phone = request.POST.get('phone')
        farmer.email = request.POST.get('email', '')
        farmer.bank_name = request.POST.get('bank_name', '')
        farmer.account_number = request.POST.get('account_number', '')
        farmer.ifsc_code = request.POST.get('ifsc_code', '')
        farmer.joining_date = request.POST.get('joining_date')
        farmer.is_active = 'is_active' in request.POST
        if 'photo' in request.FILES:
            farmer.photo = request.FILES['photo']
        farmer.save()
        messages.success(request, 'Farmer updated successfully!')
        return redirect('farmer_detail', pk=pk)
    return render(request, 'farmers/form.html', {'farmer': farmer, 'title': 'Edit Farmer'})

@login_required
def farmer_detail(request, pk):
    farmer = get_object_or_404(Farmer, pk=pk)
    collections = MilkCollection.objects.filter(farmer=farmer).order_by('-date')[:30]
    total_supply = MilkCollection.objects.filter(farmer=farmer).aggregate(Sum('quantity'))['quantity__sum'] or 0
    total_earnings = MilkCollection.objects.filter(farmer=farmer).aggregate(Sum('total_amount'))['total_amount__sum'] or 0
    
    # Monthly data for chart
    from django.db.models.functions import TruncMonth
    monthly = MilkCollection.objects.filter(farmer=farmer).annotate(
        month=TruncMonth('date')
    ).values('month').annotate(qty=Sum('quantity'), amt=Sum('total_amount')).order_by('-month')[:6]
    
    context = {
        'farmer': farmer,
        'collections': collections,
        'total_supply': total_supply,
        'total_earnings': total_earnings,
        'monthly': list(reversed(list(monthly))),
    }
    return render(request, 'farmers/detail.html', context)

@login_required
def farmer_delete(request, pk):
    farmer = get_object_or_404(Farmer, pk=pk)
    if request.method == 'POST':
        farmer.delete()
        messages.success(request, 'Farmer deleted successfully!')
        return redirect('farmer_list')
    return render(request, 'farmers/confirm_delete.html', {'farmer': farmer})
