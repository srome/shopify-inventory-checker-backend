from base64 import b64encode
import requests
from json import loads as parse_json
import os
import datetime

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
        response = cls._call_api(f"{cls.api_base_url}/locations/{location_id}/inventory_levels.json?limit=250")
        return cls._decode_response(response)['inventory_levels']

    @classmethod
    def get_products(cls):
        # inventory item 1-1 correspondence with product variant, but IDs are different... thanks Shopify
        return cls._make_list_of_products(f"{cls.api_base_url}/products.json?limit=250")

    @classmethod
    def _make_list_of_products(cls, url):
        counter = 0
        products = []
        has_next = False
        while True:
            response = cls._call_api(url)
            products += cls._decode_response(response)['products']
            if 'LINK' in response.headers:
                has_next = "next" in response.headers['LINK'].split(';')[1]
                url = response.headers['LINK'].split(';')[0][1:-1]
            else:
                break

            if not has_next:
                break

        return products

class BusinessDetails:
    item_quantities = 'item_quantities'
    location_name = 'location_name'
    address = 'address'

    exclude_location_id_string = os.environ.get('EXCLUDE_LOCATION_IDS', '')
    exclude_location_ids = {
        int(exclude_location_id.strip())
        for exclude_location_id
        in exclude_location_id_string.split(',')
    } if exclude_location_id_string else []


    def __init__(self):
        self.item_id_flavors_map = {}
        self.locations = {}
        self.items = {}
        self.images = {}
        self.available_items = set()

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

    def does_item_exist(self, item):
        return item in self.items

    def add_item_name(self,item, name):
        self.items[item] = name

    def get_item_name(self, item):
        return self.items.get(item, None)

    def add_item_image(self, item, image):
        self.images[item] = image

    def get_item_image(self, item):
        return self.images.get(item, '')

    def add_available_tag(self, item):
        self.available_items.add(item)

    def item_has_availability_tag(self, item):
        # Additional check based on tags
        return item in self.available_items

    def _get_item_quantities_for_location(self, location_id):
        return self.locations[location_id].get(self.item_quantities, {}).items()

    def _build_item_detail(self, output_object, location_id, item_id, quantity):
        location_name = self.locations[location_id][self.location_name]

        # only do it if item hasn't been filtered
        if self.item_has_availability_tag(item_id):
            data = {
                'productName': self.get_item_name(item_id),
                'quantity': quantity,
                'image': self.get_item_image(item_id)
            }
            output_object[location_name] = output_object.get(location_name, []) + [data]

        return output_object

    def get_business_details(self):
        output_object = {}

        data = [
            self._build_item_detail(output_object, location_id, item_id, quantity)
            for location_id in self.locations
            for item_id, quantity in self._get_item_quantities_for_location(location_id)
        ]

        # Sort for consistency
        for key, value in output_object.items():
            output_object[key] = sorted(value, key = lambda x : x['productName'])


        return output_object
    
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
        today = datetime.datetime.now()
        for location_id in business_details.get_locations():
            for level in cls.api.get_inventory_for_location(location_id):
                # we filter later using the Available tag
                business_details.update_location_item_quantity(location=location_id, 
                                                                   item=level['inventory_item_id'],
                                                                   quantity=level['available'])

    @classmethod
    def _get_product_names(cls, business_details):
        # Assumes items have been filled out
        for product in cls.api.get_products():
            for variant in product['variants']:
                if business_details.does_item_exist(variant['inventory_item_id']):
                    # Check for available tag
                    tags = [x.strip() for x in product['tags'].split(',')]

                    if "Available" in tags:
                        business_details.add_available_tag(variant['inventory_item_id'])

                        business_details.add_item_name(
                            item=variant['inventory_item_id'],
                            name=product['title']
                        )
                        business_details.add_item_image(
                            item=variant['inventory_item_id'],
                            image=product['image']['src']
                        )

    @classmethod
    def get_content(cls):
        business_details = BusinessDetails()
        cls._get_locations(business_details)
        cls._add_item_quantities(business_details)
        cls._get_product_names(business_details)
        return business_details.get_business_details()

