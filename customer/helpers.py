import requests
from django.conf import settings

GOOGLE_KEY = settings.GOOGLE_MAPS_API_KEY

def get_distance_and_eta(user_lat, user_lon, doctors):
    """
    doctors: list of dicts [{'id':1,'lat':..,'lon':..,'name':..}]
    Returns list of doctors with road distance and ETA
    """
    # Prepare destinations string
    destinations = "|".join([f"{d['latitude']},{d['longitude']}" for d in doctors])
    origin = f"{user_lat},{user_lon}"

    url = (
        f"https://maps.googleapis.com/maps/api/distancematrix/json"
        f"?origins={origin}&destinations={destinations}"
        f"&key={GOOGLE_KEY}"
        f"&mode=driving"  # driving, walking, bicycling
    )

    res = requests.get(url).json()
    results = []

    if res.get("status") == "OK":
        elements = res["rows"][0]["elements"]
        for idx, element in enumerate(elements):
            if element.get("status") == "OK":
                doctor_info = doctors[idx].copy()
                doctor_info["distance_text"] = element["distance"]["text"]       # e.g., "3.5 km"
                doctor_info["distance_value"] = element["distance"]["value"]     # in meters
                doctor_info["duration_text"] = element["duration"]["text"]       # e.g., "7 mins"
                doctor_info["duration_value"] = element["duration"]["value"]     # in seconds
                results.append(doctor_info)

    # Sort doctors by ETA (duration_value)
    results.sort(key=lambda x: x["duration_value"])
    return results
