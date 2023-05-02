import requests
from django.conf import settings
import qrcode,io


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
    @classmethod
    def get_price(cls,distance_in_meter,transportation_type,currency):
        return distance_in_meter*len(transportation_type)


class QrCode:
    @classmethod
    def generate_qr_code(cls,ticket_id,source, destination, journey_start_time,journey_end_time, amount_paid,currency, passenger_name,transportation_type):
        data = {
            'id': ticket_id,
            'source':source,
            'destination': destination,
            'journey_start_time': journey_start_time.strftime("%d/%m/%Y %H:%M:%S"),
            "journey_end_time":journey_end_time.strftime("%d/%m/%Y %H:%M:%S"),
            'amount_paid': amount_paid,
            'currency': currency,
            'passenger_name': passenger_name,
            "transportation_type":transportation_type
        }
        qr = qrcode.QRCode(
            version=None,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=10,
            border=4,
        )
        qr.add_data(data)
        qr.make(fit=True)
        img = qr.make_image(fill_color="black", back_color="white")
        img_byte_arr = io.BytesIO()
        img.save(img_byte_arr)
        return img_byte_arr.getvalue()