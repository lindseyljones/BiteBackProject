import os
import django
import biteback
from django.core.management import call_command
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'biteback.settings')
django.setup()

from mainApp.models import Restaurant
from biteback import settings
import googlemaps
import time

def store_results(places):
    if "results" in places:
            print(len(places["results"]))
            for place in places["results"]:
                
                my_restaurant = Restaurant()
                my_restaurant.name = place["name"]
                my_restaurant.rating = place["rating"]
                if(place.get('opening_hours') == None):
                    my_restaurant.open_now = False
                else:
                    my_restaurant.open_now = place.get('opening_hours').get('open_now');

                my_restaurant.id = place["place_id"]
                my_restaurant.num_of_ratings = place["user_ratings_total"]
                my_restaurant.save()


def popRestaurants():
    api_key = settings.GOOGLE_PLACES_API_KEY
    try:
        gmaps = googlemaps.Client(key=api_key)
        places = gmaps.places(location=(38.0335529, -78.5079772), query="restaurants")
        next_page_token = places["next_page_token"]
        store_results(places=places)
        time.sleep(3)
        places = gmaps.places(page_token=next_page_token)
        next_page_token = places["next_page_token"]
        store_results(places=places)
        time.sleep(3)
        places = gmaps.places(page_token=next_page_token)
        print(len(places["results"]))
        store_results(places=places)
    except Exception as e:
        print(e)

if __name__ == "__main__":
    try:
        restaurants = Restaurant.objects.order_by("name")
    except Exception as e:
        print("No restaurants in database, populating now...")
        popRestaurants()

    if len(Restaurant.objects.all()) <= 59:
        popRestaurants()
    
    print(len(Restaurant.objects.all()))