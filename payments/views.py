from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Sum
from farmers.models import Farmer
from milk_collection.models import MilkCollection
from .models import Payment, Customer, CustomerPayment
from datetime import date

@login_required
def payment_list(request):
    payments = Payment.objects.select_related('farmer').all()
    return render(request, 'payments/list.html', {'payments': payments})

@login_required
def generate_bill(request):
    farmers = Farmer.objects.filter(is_active=True)
    if request.method == 'POST':
        farmer_id = request.POST.get('farmer')
        from_date = request.POST.get('from_date')
        to_date = request.POST.get('to_date')
        period_type = request.POST.get('period_type', 'monthly')
        farmer = get_object_or_404(Farmer, pk=farmer_id)
        
        collections = MilkCollection.objects.filter(farmer=farmer, date__gte=from_date, date__lte=to_date)
        total_qty = collections.aggregate(Sum('quantity'))['quantity__sum'] or 0
        total_amt = collections.aggregate(Sum('total_amount'))['total_amount__sum'] or 0
        
        payment, created = Payment.objects.get_or_create(
            farmer=farmer, from_date=from_date, to_date=to_date,
            defaults={'total_quantity': total_qty, 'total_amount': total_amt, 'period_type': period_type}
        )
        if not created:
            payment.total_quantity = total_qty
            payment.total_amount = total_amt
            payment.save()
        
        messages.success(request, f'Bill generated for {farmer.name}!')
        return redirect('payment_detail', pk=payment.pk)
    return render(request, 'payments/generate.html', {'farmers': farmers, 'today': date.today()})

@login_required
def payment_detail(request, pk):
    payment = get_object_or_404(Payment, pk=pk)
    collections = MilkCollection.objects.filter(
        farmer=payment.farmer, date__gte=payment.from_date, date__lte=payment.to_date
    )
    return render(request, 'payments/detail.html', {'payment': payment, 'collections': collections})

@login_required
def mark_paid(request, pk):
    payment = get_object_or_404(Payment, pk=pk)
    if request.method == 'POST':
        paid = float(request.POST.get('paid_amount', 0))
        payment.paid_amount = paid
        payment.payment_date = date.today()
        if paid >= float(payment.total_amount):
            payment.status = 'paid'
        elif paid > 0:
            payment.status = 'partial'
        payment.save()
        messages.success(request, 'Payment updated!')
    return redirect('payment_list')

@login_required
def customer_list(request):
    customers = Customer.objects.all()
    return render(request, 'payments/customers.html', {'customers': customers})

@login_required
def customer_add(request):
    if request.method == 'POST':
        Customer.objects.create(
            name=request.POST.get('name'),
            phone=request.POST.get('phone'),
            address=request.POST.get('address'),
            milk_per_day=request.POST.get('milk_per_day'),
            rate_per_liter=request.POST.get('rate_per_liter'),
            joining_date=request.POST.get('joining_date'),
        )
        messages.success(request, 'Customer added!')
        return redirect('customer_list')
    return render(request, 'payments/customer_form.html', {'today': date.today()})
