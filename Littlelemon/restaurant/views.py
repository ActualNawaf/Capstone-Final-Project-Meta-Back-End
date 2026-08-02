from django.http import HttpRequest, HttpResponse
from django.shortcuts import render
from django.core import serializers
from rest_framework import generics
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from datetime import datetime
from django.views.decorators.csrf import csrf_exempt
from .serializers import BookingSerializer, MenuSerializer
from .models import Booking, Menu
from .forms import BookingForm
from django.http import JsonResponse
import json
from datetime import date
# 
# API views
#
class MenuItemsView(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticated]
    
    queryset = Menu.objects.all()
    serializer_class = MenuSerializer

class SingleMenuItemView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Menu.objects.all()
    serializer_class = MenuSerializer
    
class BookingViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = BookingSerializer
    queryset = Booking.objects.all()
#
# Page views
#
def index(request: HttpRequest) -> HttpResponse:
    return render(request, 'index.html', {})

def about(request):
    return render(request, 'about.html')





def book(request):
    return render(request, 'book.html')


@csrf_exempt
def bookings(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            slot_val = int(data['reservation_slot'])
            
            exist = Booking.objects.filter(
                reservation_date=data['reservation_date'],
                reservation_slot=slot_val
            ).exists()
            
            if not exist:
                booking = Booking(
                    first_name=data['first_name'],
                    reservation_date=data['reservation_date'],
                    reservation_slot=slot_val
                )
                booking.save()
                return JsonResponse({'status': 1, 'message': 'Booking saved successfully'})
            else:
                return JsonResponse({'status': 0, 'message': 'Slot already booked'}, status=400)
                
        except Exception as e:
            print("POST ERROR:", str(e))
            return JsonResponse({'error': str(e)}, status=500)

    elif request.method == 'GET':
        date_param = request.GET.get('date')
        
        # 1. If JavaScript fetch API requests a specific date, return raw JSON
        if date_param:
            booking_data = Booking.objects.filter(reservation_date=date_param)
            serialized_data = serializers.serialize('json', booking_data)
            return HttpResponse(serialized_data, content_type='application/json')
            
        # 2. If a user opens /bookings/ directly in browser, render the HTML template page
        booking_data = Booking.objects.all()
        serialized_data = serializers.serialize('json', booking_data)
        return render(request, 'bookings.html', {'bookings': serialized_data})
    


# 1. Customer HTML View for /menu/
def menu(request):
    menu_data = Menu.objects.all()
    return render(request, 'menu.html', {'menu': menu_data})

# 2. Detail HTML View for /menu_item/<int:pk>
def display_menu_item(request, pk=None):
    if pk:
        menu_item = Menu.objects.get(pk=pk)
    else:
        menu_item = ""
    return render(request, 'menu_item.html', {'menu_item': menu_item})