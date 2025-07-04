from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.admin.sites import site
from django.shortcuts import render
from rentalapp.models import usertable, booking_table
from rental_business.models import buss_vehicle
import json
from django.db.models import Sum, Count, FloatField
from django.db.models.functions import Cast, ExtractDay
from django.utils import timezone
from django.utils.dateparse import parse_date
import csv
from django.http import HttpResponse
from django.db.models import F, ExpressionWrapper, fields

@staff_member_required
def dashboard_view(request):
    # Stats
    stats = {
        'total_users': usertable.objects.count(),
        'total_vehicles': buss_vehicle.objects.count(),
        'total_bookings': booking_table.objects.count(),
        'total_revenue': booking_table.objects.annotate(
            amount_float=Cast('amount', FloatField())
        ).aggregate(total=Sum('amount_float'))['total'] or 0,
    }

    # Bookings per month (last 6 months)
    now = timezone.now()
    months = [(now - timezone.timedelta(days=30*i)).strftime('%b %Y') for i in reversed(range(6))]
    bookings_per_month = [
        booking_table.objects.filter(
            booking_date__year=(now - timezone.timedelta(days=30*i)).year,
            booking_date__month=(now - timezone.timedelta(days=30*i)).month
        ).count() for i in reversed(range(6))
    ]
    bookings_data = {
        'labels': months,
        'values': bookings_per_month,
    }

    # Vehicle Popularity (Top 5)
    vehicle_counts = booking_table.objects.values('vehicle_id__buss_vehicle_model').annotate(
        count=Count('id')
    ).order_by('-count')[:5]
    vehicle_popularity = {
        'labels': [v['vehicle_id__buss_vehicle_model'] for v in vehicle_counts],
        'values': [v['count'] for v in vehicle_counts],
    }

    # User Registrations Over Time (last 6 months)
    user_registrations = [
        usertable.objects.filter(
            created_at__year=(now - timezone.timedelta(days=30*i)).year,
            created_at__month=(now - timezone.timedelta(days=30*i)).month
        ).count() for i in reversed(range(6))
    ]
    user_registrations_data = {
        'labels': months,
        'values': user_registrations,
    }

    # Revenue Over Time (last 6 months)
    revenue_per_month = [
        booking_table.objects.filter(
            booking_date__year=(now - timezone.timedelta(days=30*i)).year,
            booking_date__month=(now - timezone.timedelta(days=30*i)).month
        ).annotate(
            amount_float=Cast('amount', FloatField())
        ).aggregate(total=Sum('amount_float'))['total'] or 0
        for i in reversed(range(6))
    ]
    revenue_data = {
        'labels': months,
        'values': revenue_per_month,
    }

    # Booking Status Distribution
    status_counts = booking_table.objects.values('status').annotate(count=Count('id'))
    booking_status_data = {
        'labels': [s['status'].capitalize() for s in status_counts],
        'values': [s['count'] for s in status_counts],
    }

    # Vehicle Type Distribution
    type_counts = buss_vehicle.objects.values('buss_vehicle_type').annotate(count=Count('id'))
    vehicle_type_data = {
        'labels': [t['buss_vehicle_type'] for t in type_counts],
        'values': [t['count'] for t in type_counts],
    }

    context = site.each_context(request)
    context['stats'] = stats
    context['bookings_data'] = json.dumps(bookings_data)
    context['vehicle_popularity'] = json.dumps(vehicle_popularity)
    context['user_registrations_data'] = json.dumps(user_registrations_data)
    context['revenue_data'] = json.dumps(revenue_data)
    context['booking_status_data'] = json.dumps(booking_status_data)
    context['vehicle_type_data'] = json.dumps(vehicle_type_data)
    return render(request, 'dashboard/overview.html', context)

# @staff_member_required
# def bookings_analysis(request):
#     # Example: Daily bookings for the last 30 days
#     now = timezone.now()
#     days = [(now - timezone.timedelta(days=i)).strftime('%d %b') for i in reversed(range(30))]
#     daily_bookings = [
#         booking_table.objects.filter(
#             booking_date__date=(now - timezone.timedelta(days=i)).date()
#         ).count() for i in reversed(range(30))
#     ]
#     bookings_trend = {
#         'labels': days,
#         'values': daily_bookings,
#     }
#     context = site.each_context(request)
#     context['bookings_trend'] = json.dumps(bookings_trend)
#     return render(request, 'dashboard/bookings_analysis.html', context)

@staff_member_required
def bookings_analysis(request):
    now = timezone.now()
    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')
    if start_date and end_date:
        start = parse_date(start_date)
        end = parse_date(end_date)
        days = [(start + timezone.timedelta(days=i)).strftime('%d %b')
                for i in range((end - start).days + 1)]
        daily_bookings = [
            booking_table.objects.filter(
                booking_date__date=(start + timezone.timedelta(days=i))
            ).count() for i in range((end - start).days + 1)
        ]
        filter_qs = booking_table.objects.filter(booking_date__date__range=[start_date, end_date])
    else:
        days = [(now - timezone.timedelta(days=i)).strftime('%d %b') for i in reversed(range(30))]
        daily_bookings = [
            booking_table.objects.filter(
                booking_date__date=(now - timezone.timedelta(days=i)).date()
            ).count() for i in reversed(range(30))
        ]
        filter_qs = booking_table.objects.all()
    bookings_trend = {
        'labels': days,
        'values': daily_bookings,
    }
    # Bookings by Payment Method
    payment_counts = filter_qs.values('payment_method').annotate(count=Count('id'))
    bookings_by_payment = {
        'labels': [p['payment_method'].capitalize() for p in payment_counts],
        'values': [p['count'] for p in payment_counts],
    }
    # Bookings by Status Over Time (stacked bar)
    status_choices = [c[0] for c in booking_table._meta.get_field('status').choices]
    status_data = {status: [] for status in status_choices}
    for i, day in enumerate(days):
        date_obj = (start + timezone.timedelta(days=i)) if (start_date and end_date) else (now - timezone.timedelta(days=(29-i)))
        for status in status_choices:
            count = filter_qs.filter(booking_date__date=date_obj, status=status).count()
            status_data[status].append(count)
    bookings_by_status = {
        'labels': days,
        'datasets': [
            {'label': status.capitalize(), 'data': status_data[status]} for status in status_choices
        ]
    }
    # Top 5 Users by Bookings
    user_counts = filter_qs.values('login_id__emailid').annotate(count=Count('id')).order_by('-count')[:5]
    top_users = {
        'labels': [u['login_id__emailid'] for u in user_counts],
        'values': [u['count'] for u in user_counts],
    }
    # Bookings by City/Location (if available)
    if hasattr(filter_qs.first(), 'vehicle_id') and hasattr(filter_qs.first().vehicle_id, 'buss_vehicle_location'):
        city_counts = filter_qs.values('vehicle_id__buss_vehicle_location').annotate(count=Count('id')).order_by('-count')[:10]
        bookings_by_city = {
            'labels': [c['vehicle_id__buss_vehicle_location'] or 'Unknown' for c in city_counts],
            'values': [c['count'] for c in city_counts],
        }
    else:
        bookings_by_city = {'labels': [], 'values': []}
    # Average Booking Duration by Vehicle (Top 10)
    duration_qs = filter_qs.annotate(
        duration_days=ExtractDay(F('from_to') - F('from_duration'))
    ).values('vehicle_id__buss_vehicle_model').annotate(
        avg_duration=ExpressionWrapper(
            Sum('duration_days') / Cast(Count('id'), output_field=fields.FloatField()),
            output_field=fields.FloatField()
        )
    ).order_by('-avg_duration')[:10]
    avg_booking_duration = {
        'labels': [d['vehicle_id__buss_vehicle_model'] for d in duration_qs],
        'values': [round(d['avg_duration'], 2) if d['avg_duration'] is not None else 0 for d in duration_qs],
    }
    context = site.each_context(request)
    context['bookings_trend'] = json.dumps(bookings_trend)
    context['bookings_by_payment'] = json.dumps(bookings_by_payment)
    context['bookings_by_status'] = json.dumps(bookings_by_status)
    context['top_users'] = json.dumps(top_users)
    context['bookings_by_city'] = json.dumps(bookings_by_city)
    context['avg_booking_duration'] = json.dumps(avg_booking_duration)
    return render(request, 'dashboard/bookings_analysis.html', context)

@staff_member_required
def revenue_analysis(request):
    now = timezone.now()
    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')
    if start_date and end_date:
        start = parse_date(start_date)
        end = parse_date(end_date)
        days = [(start + timezone.timedelta(days=i)).strftime('%d %b')
                for i in range((end - start).days + 1)]
        daily_revenue = [
            booking_table.objects.filter(
                booking_date__date=(start + timezone.timedelta(days=i))
            ).annotate(
                amount_float=Cast('amount', FloatField())
            ).aggregate(total=Sum('amount_float'))['total'] or 0
            for i in range((end - start).days + 1)
        ]
        filter_qs = booking_table.objects.filter(booking_date__date__range=[start_date, end_date])
    else:
        days = [(now - timezone.timedelta(days=i)).strftime('%d %b') for i in reversed(range(30))]
        daily_revenue = [
            booking_table.objects.filter(
                booking_date__date=(now - timezone.timedelta(days=i)).date()
            ).annotate(
                amount_float=Cast('amount', FloatField())
            ).aggregate(total=Sum('amount_float'))['total'] or 0
            for i in reversed(range(30))
        ]
        filter_qs = booking_table.objects.all()
    revenue_trend = {
        'labels': days,
        'values': daily_revenue,
    }
    # Revenue by Vehicle Model (Top 10)
    vehicle_revenue = (
        filter_qs.values('vehicle_id__buss_vehicle_model')
        .annotate(total=Sum(Cast('amount', FloatField())))
        .order_by('-total')[:10]
    )
    revenue_by_vehicle = {
        'labels': [v['vehicle_id__buss_vehicle_model'] for v in vehicle_revenue],
        'values': [v['total'] for v in vehicle_revenue],
    }
    context = site.each_context(request)
    context['revenue_trend'] = json.dumps(revenue_trend)
    context['revenue_by_vehicle'] = json.dumps(revenue_by_vehicle)
    return render(request, 'dashboard/revenue_analysis.html', context)

@staff_member_required
def user_insights(request):
    # Example: Active vs. Inactive users
    total_users = usertable.objects.count()
    active_users = usertable.objects.filter(booking_table__isnull=False).distinct().count()
    inactive_users = total_users - active_users
    user_activity = {
        'labels': ['Active', 'Inactive'],
        'values': [active_users, inactive_users],
    }
    context = site.each_context(request)
    context['user_activity'] = json.dumps(user_activity)
    return render(request, 'dashboard/user_insights.html', context)

@staff_member_required
def bookings_export_csv(request):
    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')
    qs = booking_table.objects.all()
    if start_date and end_date:
        qs = qs.filter(booking_date__date__range=[start_date, end_date])
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="bookings.csv"'
    writer = csv.writer(response)
    writer.writerow(['ID', 'User', 'Vehicle', 'Date', 'Amount', 'Status'])
    for b in qs:
        writer.writerow([b.id, b.login_id.emailid, b.vehicle_id.buss_vehicle_model, b.booking_date, b.amount, b.status])
    return response

@staff_member_required
def revenue_export_csv(request):
    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')
    qs = booking_table.objects.all()
    if start_date and end_date:
        qs = qs.filter(booking_date__date__range=[start_date, end_date])
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="revenue.csv"'
    writer = csv.writer(response)
    writer.writerow(['ID', 'User', 'Vehicle', 'Date', 'Amount', 'Status'])
    for b in qs:
        writer.writerow([b.id, b.login_id.emailid, b.vehicle_id.buss_vehicle_model, b.booking_date, b.amount, b.status])
    return response

@staff_member_required
def bookings_by_city_analytics(request):
    now = timezone.now()
    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')
    if start_date and end_date:
        filter_qs = booking_table.objects.filter(booking_date__date__range=[start_date, end_date])
    else:
        filter_qs = booking_table.objects.all()
    if filter_qs.exists() and hasattr(filter_qs.first(), 'vehicle_id') and hasattr(filter_qs.first().vehicle_id, 'buss_vehicle_location'):
        city_counts = filter_qs.values('vehicle_id__buss_vehicle_location').annotate(count=Count('id')).order_by('-count')[:10]
        bookings_by_city = {
            'labels': [c['vehicle_id__buss_vehicle_location'] or 'Unknown' for c in city_counts],
            'values': [c['count'] for c in city_counts],
        }
    else:
        bookings_by_city = {'labels': [], 'values': []}
    context = site.each_context(request)
    context['bookings_by_city'] = json.dumps(bookings_by_city)
    return render(request, 'dashboard/bookings_by_city.html', context)

@staff_member_required
def bookings_by_city_export_csv(request):
    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')
    qs = booking_table.objects.all()
    if start_date and end_date:
        qs = qs.filter(booking_date__date__range=[start_date, end_date])
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="bookings_by_city.csv"'
    writer = csv.writer(response)
    writer.writerow(['City/Location', 'Bookings'])
    city_counts = qs.values('vehicle_id__buss_vehicle_location').annotate(count=Count('id')).order_by('-count')[:10]
    for c in city_counts:
        writer.writerow([c['vehicle_id__buss_vehicle_location'] or 'Unknown', c['count']])
    return response


