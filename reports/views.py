from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.db.models import Sum, Avg, Count
from django.db.models.functions import TruncMonth, TruncDate
from milk_collection.models import MilkCollection
from payments.models import Payment
from farmers.models import Farmer
from datetime import date, timedelta

@login_required
def daily_report(request):
    report_date = request.GET.get('date', str(date.today()))
    collections = MilkCollection.objects.filter(date=report_date).select_related('farmer')
    morning = collections.filter(shift='morning')
    evening = collections.filter(shift='evening')
    totals = {
        'morning_qty': morning.aggregate(Sum('quantity'))['quantity__sum'] or 0,
        'morning_amt': morning.aggregate(Sum('total_amount'))['total_amount__sum'] or 0,
        'evening_qty': evening.aggregate(Sum('quantity'))['quantity__sum'] or 0,
        'evening_amt': evening.aggregate(Sum('total_amount'))['total_amount__sum'] or 0,
    }
    totals['total_qty'] = totals['morning_qty'] + totals['evening_qty']
    totals['total_amt'] = totals['morning_amt'] + totals['evening_amt']
    return render(request, 'reports/daily.html', {'collections': collections, 'report_date': report_date, 'totals': totals})

@login_required
def monthly_report(request):
    today = date.today()
    year = int(request.GET.get('year', today.year))
    month = int(request.GET.get('month', today.month))
    from_date = date(year, month, 1)
    import calendar
    last_day = calendar.monthrange(year, month)[1]
    to_date = date(year, month, last_day)
    
    farmer_data = MilkCollection.objects.filter(date__gte=from_date, date__lte=to_date).values(
        'farmer__farmer_id', 'farmer__name'
    ).annotate(
        total_qty=Sum('quantity'),
        total_amt=Sum('total_amount'),
        avg_fat=Avg('fat'),
        avg_snf=Avg('snf'),
    ).order_by('farmer__farmer_id')
    
    grand_total = {'qty': sum(f['total_qty'] for f in farmer_data), 'amt': sum(f['total_amt'] for f in farmer_data)}
    
    months = [(i, date(2024, i, 1).strftime('%B')) for i in range(1, 13)]
    years = list(range(today.year - 2, today.year + 1))
    
    return render(request, 'reports/monthly.html', {
        'farmer_data': farmer_data, 'grand_total': grand_total,
        'year': year, 'month': month, 'months': months, 'years': years,
        'from_date': from_date, 'to_date': to_date
    })

@login_required
def payment_report(request):
    payments = Payment.objects.select_related('farmer').all().order_by('-created_at')
    total_due = payments.aggregate(Sum('total_amount'))['total_amount__sum'] or 0
    total_paid = payments.aggregate(Sum('paid_amount'))['paid_amount__sum'] or 0
    return render(request, 'reports/payments.html', {
        'payments': payments, 'total_due': total_due, 'total_paid': total_paid,
        'pending': total_due - total_paid
    })

@login_required
def fat_report(request):
    today = date.today()
    from_date = request.GET.get('from_date', str(today - timedelta(days=30)))
    to_date = request.GET.get('to_date', str(today))
    
    data = MilkCollection.objects.filter(date__gte=from_date, date__lte=to_date).values(
        'farmer__name', 'farmer__farmer_id'
    ).annotate(
        avg_fat=Avg('fat'), avg_snf=Avg('snf'), total_qty=Sum('quantity')
    ).order_by('-avg_fat')
    
    overall_fat = MilkCollection.objects.filter(date__gte=from_date, date__lte=to_date).aggregate(Avg('fat'))['fat__avg'] or 0
    
    return render(request, 'reports/fat.html', {
        'data': data, 'from_date': from_date, 'to_date': to_date, 'overall_fat': overall_fat
    })
