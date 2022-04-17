import json

import requests
from django.core import serializers
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render

from map.models import College, Entry

from .config import MAPBOX_API_KEY
from ratelimit.decorators import ratelimit

def index(request) -> HttpResponse:
    colleges = College.objects.all()

    serialized_objects = [{
        'name': college.name,
        'long': str(college.long),
        'lat': str(college.lat),
        'image': college.image,
        'entry': list(college.entry.all().values("first_name", "last_name"))
    } for college in colleges]

    context = {
        "colleges": json.dumps(serialized_objects)
    }

    print("context")
    return render(request, '../templates/index.html', context)


@ratelimit(key='ip', rate='50/h')
def process_entry(request):
    def is_ajax(req: request) -> bool:
        if request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest':
            return True
        else:
            return False

    if is_ajax(request) and request.method == "POST":
        entry = request.POST.dict()
        # First lets verify that the email is a valid one.
        # For this to be true the email must start with lastname(firstletter)

        entry["fname"] = entry["fname"].replace(" ", "")
        entry["lname"] = entry["lname"].replace(" ", "")
        entry["email"] = entry["email"].replace(" ", "")





        if not entry["fname"].isalpha():
            return JsonResponse("Number in Names", safe=False)

        if len(entry["email"]) <= 13:
            return JsonResponse("Invalid Email", safe=False)

        if Entry.objects.filter(email=entry["email"]).exists():
            return JsonResponse("Already Exists", safe=False)

        correct_email_prefix = entry["lname"].lower() + entry["fname"][0].lower()

        email_suffix = entry["email"][len(entry["email"]) - 13:len(entry["email"])].lower()

        is_email_valid = True if correct_email_prefix == entry["email"][0:len(
            correct_email_prefix)] and email_suffix == "my.sduhsd.net" else False

        if not is_email_valid:
            return JsonResponse("Invalid Email", safe=False)

        college_object = College.objects.filter(name=entry["college"]).first()
        if not college_object:
            formatted_name = entry["college"].replace(" ", "%20")
            formatted_api = f"https://api.mapbox.com/geocoding/v5/mapbox.places/{formatted_name}.json?access_token={MAPBOX_API_KEY}"

            data = requests.get(formatted_api).json()

            coordinates = data["features"][1]["geometry"]["coordinates"]

            longitude = coordinates[0]
            latitude = coordinates[1]

            college_name = entry["college"]
            college_source = requests.get(
                f"http://universities.hipolabs.com/search?name={college_name}&size=50").json()

            college_domain = college_source[0]["domains"][0]

            img_link = f"https://logo.clearbit.com/{college_domain}?size=25"

            new_college = College(name=college_name, long=longitude, lat=latitude, image=img_link)
            new_college.save()
            college_object = new_college

        new_entry = Entry(first_name=entry["fname"], last_name=entry["lname"], email=entry["email"],
                          college=college_object)
        new_entry.save()

        return JsonResponse("Success", safe=False)
    else:
        return HttpResponse("HTTP not accepted.")
