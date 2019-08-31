from inventory import Handler
import unittest


class FakeShopifyAPI:
    
    @classmethod
    def get_locations(cls):
        return [{'active': True,
  'address1': '1111 Spring Garden St.',
  'address2': '',
  'admin_graphql_api_id': 'gid://shopify/Location/48794762',
  'city': 'Philadelphia',
  'country': 'US',
  'country_code': 'US',
  'country_name': 'United States',
  'created_at': '2017-08-21T17:46:37-04:00',
  'id': 48794762,
  'legacy': False,
  'name': '1713 Spring Garden St.',
  'phone': '2026693489',
  'province': 'Pennsylvania',
  'province_code': 'PA',
  'updated_at': '2019-03-30T20:23:02-04:00',
  'zip': '19130'},
 {'active': True,
  'address1': '1234 South 3rd Street',
  'address2': '',
  'admin_graphql_api_id': 'gid://shopify/Location/31149424723',
  'city': 'Philadelphia',
  'country': 'US',
  'country_code': 'US',
  'country_name': 'United States',
  'created_at': '2019-08-07T19:39:54-04:00',
  'id': 31149424723,
  'legacy': False,
  'name': "Herman's",
  'phone': '',
  'province': 'PA',
  'province_code': 'PA',
  'updated_at': '2019-08-07T19:39:54-04:00',
  'zip': '19147'}]
    
    @classmethod
    def get_inventory_for_location(cls, location_id):
        return [{'location_id': 31149424723, 'available': 0, 'updated_at': '2019-08-10T17:43:20-04:00', 'admin_graphql_api_id': 'gid://shopify/InventoryLevel/30929059923?inventory_item_id=30583991205971', 'inventory_item_id': 30583991205971},
{'location_id': 31149424723, 'available': 7, 'updated_at': '2019-08-10T17:10:55-04:00', 'admin_graphql_api_id': 'gid://shopify/InventoryLevel/30929059923?inventory_item_id=30583983571027', 'inventory_item_id': 30583983571027}]
    
    @classmethod
    def get_products(cls):
        return [{'admin_graphql_api_id': 'gid://shopify/Product/3933732438099',
  'body_html': '<meta charset="utf-8">\n<p><strong>Base</strong><span>:\xa0Whole bean Tahitian vanilla ice cream</span><br><strong>Crunch:<span>\xa0</span></strong>Graham cracker crunch<br><strong>Swirl</strong><span>:\xa0Key lime curd</span></p>',
  'created_at': '2019-08-04T20:30:08-04:00',
  'handle': 'klp',
  'id': 3933732438099,
  'image': {'admin_graphql_api_id': 'gid://shopify/ProductImage/12031404179539',
   'alt': None,
   'created_at': '2019-08-04T20:31:04-04:00',
   'height': 1820,
   'id': 12031404179539,
   'position': 1,
   'product_id': 3933732438099,
   'src': 'https://cdn.shopify.com/s/files/1/2292/8709/products/8639E11D-B574-4ADD-8340-863192C8996D.JPG?v=1565038679',
   'updated_at': '2019-08-05T16:57:59-04:00',
   'variant_ids': [],
   'width': 1024},
  'images': [{'admin_graphql_api_id': 'gid://shopify/ProductImage/12031404179539',
    'alt': None,
    'created_at': '2019-08-04T20:31:04-04:00',
    'height': 1820,
    'id': 12031404179539,
    'position': 1,
    'product_id': 3933732438099,
    'src': 'https://cdn.shopify.com/s/files/1/2292/8709/products/8639E11D-B574-4ADD-8340-863192C8996D.JPG?v=1565038679',
    'updated_at': '2019-08-05T16:57:59-04:00',
    'variant_ids': [],
    'width': 1024}],
  'options': [{'id': 5137504600147,
    'name': 'Title',
    'position': 1,
    'product_id': 3933732438099,
    'values': ['Default Title']}],
  'product_type': 'Ice Cream',
  'published_at': None,
  'published_scope': 'web',
  'tags': 'Aug 7, Ice Cream',
  'template_suffix': None,
  'title': 'KLP',
  'updated_at': '2019-08-14T21:41:54-04:00',
  'variants': [{'admin_graphql_api_id': 'gid://shopify/ProductVariant/29438349475923',
    'barcode': '',
    'compare_at_price': None,
    'created_at': '2019-08-04T20:30:08-04:00',
    'fulfillment_service': 'manual',
    'grams': 907,
    'id': 29438349475923,
    'image_id': None,
    'inventory_item_id': 30583983571027,
    'inventory_management': 'shopify',
    'inventory_policy': 'deny',
    'inventory_quantity': 7,
    'old_inventory_quantity': 7,
    'option1': 'Default Title',
    'option2': None,
    'option3': None,
    'position': 1,
    'price': '12.00',
    'product_id': 3933732438099,
    'requires_shipping': True,
    'sku': '',
    'taxable': False,
    'title': 'Default Title',
    'updated_at': '2019-08-10T17:10:55-04:00',
    'weight': 2.0,
    'weight_unit': 'lb'}],
  'vendor': '1-900-ICE-CREAM'}]


class FakeHandler(Handler):
  api = FakeShopifyAPI


class TestHandler(unittest.TestCase):

    def test_content(self):
        x = FakeHandler.get_content()

        self.assertEqual(x[0][0], "Herman's")
        self.assertEqual(x[0][1], "KLP")
        self.assertEqual(x[0][2], 7)


if __name__ == '__main__':
    unittest.main()


