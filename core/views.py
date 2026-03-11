from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages
from django.db.models import Sum, Count
from django.utils import timezone
from datetime import date, timedelta
from farmers.models import Farmer
from milk_collection.models import MilkCollection, Inventory
from payments.models import Payment, Customer
from .models import UserProfile, MilkRate

def login_view(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            return redirect('dashboard')
        else:
            messages.error(request, 'Invalid credentials. Please try again.')
    return render(request, 'core/login.html')

def logout_view(request):
    logout(request)
    return redirect('login')

@login_required
def dashboard(request):
    today = date.today()
    this_month_start = today.replace(day=1)
    
    total_farmers = Farmer.objects.filter(is_active=True).count()
    today_collections = MilkCollection.objects.filter(date=today)
    today_milk = today_collections.aggregate(Sum('quantity'))['quantity__sum'] or 0
    today_amount = today_collections.aggregate(Sum('total_amount'))['total_amount__sum'] or 0
    
    month_collections = MilkCollection.objects.filter(date__gte=this_month_start)
    month_milk = month_collections.aggregate(Sum('quantity'))['quantity__sum'] or 0
    month_amount = month_collections.aggregate(Sum('total_amount'))['total_amount__sum'] or 0
    
    pending_payments = Payment.objects.filter(status__in=['pending', 'partial'])
    pending_amount = pending_payments.aggregate(Sum('total_amount'))['total_amount__sum'] or 0
    
    total_customers = Customer.objects.filter(is_active=True).count()
    low_stock_items = Inventory.objects.filter(current_stock__lte=models_min_stock()).count() if False else 0
    
    # Last 7 days chart data
    chart_labels = []
    chart_data = []
    for i in range(6, -1, -1):
        d = today - timedelta(days=i)
        qty = MilkCollection.objects.filter(date=d).aggregate(Sum('quantity'))['quantity__sum'] or 0
        chart_labels.append(d.strftime('%d %b'))
        chart_data.append(float(qty))
    
    recent_collections = MilkCollection.objects.select_related('farmer').order_by('-date', '-created_at')[:10]
    
    context = {
        'total_farmers': total_farmers,
        'today_milk': today_milk,
        'today_amount': today_amount,
        'month_milk': month_milk,
        'month_amount': month_amount,
        'pending_amount': pending_amount,
        'total_customers': total_customers,
        'chart_labels': chart_labels,
        'chart_data': chart_data,
        'recent_collections': recent_collections,
        'today': today,
    }
    return render(request, 'core/dashboard.html', context)

@login_required
def profile(request):
    if request.method == 'POST':
        user = request.user
        user.first_name = request.POST.get('first_name', '')
        user.last_name = request.POST.get('last_name', '')
        user.email = request.POST.get('email', '')
        user.save()
        profile, _ = UserProfile.objects.get_or_create(user=user)
        profile.phone = request.POST.get('phone', '')
        profile.address = request.POST.get('address', '')
        profile.save()
        messages.success(request, 'Profile updated successfully!')
        return redirect('profile')
    profile, _ = UserProfile.objects.get_or_create(user=request.user)
    return render(request, 'core/profile.html', {'profile': profile})

@login_required
def change_password(request):
    if request.method == 'POST':
        old_password = request.POST.get('old_password')
        new_password = request.POST.get('new_password')
        user = authenticate(request, username=request.user.username, password=old_password)
        if user:
            user.set_password(new_password)
            user.save()
            messages.success(request, 'Password changed successfully! Please login again.')
            return redirect('login')
        else:
            messages.error(request, 'Old password is incorrect.')
    return render(request, 'core/change_password.html')

@login_required
def milk_rates(request):
    rates = MilkRate.objects.all()
    if request.method == 'POST':
        fat = request.POST.get('fat')
        snf = request.POST.get('snf')
        rate = request.POST.get('rate')
        effective_from = request.POST.get('effective_from')
        MilkRate.objects.create(fat=fat, snf=snf, rate_per_liter=rate, effective_from=effective_from)
        messages.success(request, 'Rate added successfully!')
        return redirect('milk_rates')
    return render(request, 'core/milk_rates.html', {'rates': rates})

@login_required
def user_management(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        role = request.POST.get('role')
        first_name = request.POST.get('first_name', '')
        last_name = request.POST.get('last_name', '')
        if not User.objects.filter(username=username).exists():
            user = User.objects.create_user(username=username, email=email, password=password, first_name=first_name, last_name=last_name)
            UserProfile.objects.create(user=user, role=role)
            messages.success(request, f'User {username} created!')
        else:
            messages.error(request, 'Username already exists.')
        return redirect('user_management')
    users = User.objects.select_related('profile').all()
    return render(request, 'core/user_management.html', {'users': users})
