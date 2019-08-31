from base64 import b64encode
import requests
from json import loads as parse_json
import os

class ShopifyAPI:
    token = os.environ['SHOPIFY_AUTH_TOKEN']

    headers = {
        'Authorization': 'Basic {token}'.format(
            token=b64encode(token.encode()).decode('ascii'))
    }

    shop_address = os.environ['SHOP_ADDRESS']
    api_base_url = f'https://{shop_address}.myshopify.com/admin/api/2019-07'

    @classmethod
    def _call_api(cls, api_string):
        return requests.get(
            url= api_string, 
            headers=cls.headers
        )

    @staticmethod
    def _decode_response(response):
        return parse_json(response._content.decode('utf-8'))

     
    @classmethod
    def get_locations(cls):
        response = cls._call_api(f"{cls.api_base_url}/locations.json") 
        return cls._decode_response(response)['locations']

    @classmethod
    def get_inventory_for_location(cls,location_id):
        response = cls._call_api(f"{cls.api_base_url}/locations/{location_id}/inventory_levels.json")
        return cls._decode_response(response)['inventory_levels']

    @classmethod
    def get_products(cls):
        # inventory item 1-1 correspondence with product variant, but IDs are different... thanks Shopify
        response = cls._call_api(f"{cls.api_base_url}/products.json")
        return cls._decode_response(response)['products']


class BusinessDetails:
    item_quantities = 'item_quantities'
    location_name = 'location_name'
    address = 'address'

    exclude_location_id_string = os.environ.get('EXCLUDE_LOCATION_IDS', '')
    exclude_location_ids = {int(exclude_location_id.strip()) for exclude_location_id in exclude_location_id_string.split(',')}


    def __init__(self):
        self.item_id_flavors_map = {}
        self.locations = {}
        self.items = {}

    def add_location(self, location):

        if location['id'] not in self.exclude_location_ids:

            if location['active']:
                self.locations[location['id']] = {
                self.location_name : location['name'], 
                self.address : location['address1'], 
                self.item_quantities : {}
                }

        return self

    def update_location_item_quantity(self, location, item, quantity):
        if location in self.locations:
            # being slick to aviod if/else or try/except
            self.locations[location][self.item_quantities][item] = quantity + self.locations[location][self.item_quantities].get(item,0)
            self.items[item] = None
        else:
            raise Exception('No such location')

    def is_item_available(self, item):
        return item in self.items

    def add_item_name(self,item, name):
        self.items[item] = name

    def get_item_name(self, item):
        return self.items.get(item, None)

    def get_business_details(self):
        details = []
        for location_id in self.locations:
            for item_id, quantity in self.locations[location_id].get(self.item_quantities, {}).items():
                details.append((self.locations[location_id][self.location_name], self.get_item_name(item_id), quantity))
        return details
    
    def get_locations(self):
        return self.locations

class Handler:

    api = ShopifyAPI

    @classmethod
    def _get_locations(cls, business_details):
        locations = cls.api.get_locations()

        locations_data = {}

        for loc in locations:
            business_details.add_location(loc)

    @classmethod
    def _add_item_quantities(cls, business_details):
        # modifies locations_data to include available flavors (stored via inventory_item_id)
        for location_id in business_details.get_locations():
            for level in cls.api.get_inventory_for_location(location_id):
                if level['available'] is not None and level['available'] > 0:
                    business_details.update_location_item_quantity(location=location_id, 
                                                                   item=level['inventory_item_id'],
                                                                   quantity=level['available'])

    @classmethod
    def _get_product_names(cls, business_details):
        # Assumes items have been filled out
        for product in cls.api.get_products():
            for variant in product['variants']:
                if business_details.is_item_available(variant['inventory_item_id']):
                    business_details.add_item_name(item=variant['inventory_item_id'],
                                                      name=product['title'])

    @classmethod
    def get_content(cls):
        business_details = BusinessDetails()
        cls._get_locations(business_details)
        cls._add_item_quantities(business_details)
        cls._get_product_names(business_details)
        return business_details.get_business_details()

