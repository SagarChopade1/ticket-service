import requests
from django.conf import settings


class DistanceMatrix:
    def __init__(self, api_key,url):
        self.api_key = api_key
        self.url=url
    
    def get_distance(self, source, destination):
        url = f"{self.url}?origins={source}&destinations={destination}&key={self.api_key}"
        try:
            response = requests.get(url)
            if response.ok:
                data = response.json()
                distance = data['rows'][0]['elements'][0]['distance']['value']
                return distance
        except Exception as e:
            return None
        
    
calculate_distance = DistanceMatrix(settings.GOOGLE_DISTANCE_MATRIX_KEY,settings.DISTANCE_MATRIC_CALCULATE_URL)

class DistancePriceCalculator:
    def get_price(self,distance_in_meter,transportation_type):
        pass