from django.shortcuts import render,redirect
import folium
import geocoder
from django.http import HttpResponse
from .models import Search
from .forms import SearchForm

def index(request):
    if request.method == 'POST':
        form = SearchForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/')
    else:
        form= SearchForm()
    address = Search.objects.all().last()
    location = geocoder.osm(address)
    latitude = location.lat
    longitude = location.lng
    country = location.country
    if latitude==None or longitude==None:
        address.delete()
        return HttpResponse("Place unavailable")
    # Creating a map object
    map = folium.Map(location=[8,25],zoom_start=3)
    folium.Marker([latitude,longitude],tooltip="More info",popup=country).add_to(map)
    #HTML representation of map object
    map = map._repr_html_()
    context={
        "map":map,
        "form":form,
        }
    return render(request, 'main/index.html',context)
