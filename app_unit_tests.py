import json
import unittest
import requests


class MyTestCase(unittest.TestCase):
    URL = "http://127.0.0.1:5000"

    def testWelcomeMessage(self):
        response = requests.get(self.URL + '/welcome')
        self.assertEqual(response.json(), "Welcome to Pizza House")

    def testOrderDetails(self):
        response = requests.get(self.URL + '/getorders')
        json_response = response.json()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(json_response[0]['_id']['$oid'], '634717c8f929cf3d1611208f')
        self.assertEqual(json_response[0]['orders'][0], 'Pizza1')
        self.assertEqual(json_response[0]['orders'][1], 'Pizza2')
        self.assertEqual(json_response[1]['_id']['$oid'], '63471f8e40efcf34b1e51232')
        self.assertEqual(json_response[1]['orders'][0], 'Pizza3')
        self.assertEqual(json_response[1]['orders'][1], 'Pizza4')

    def testOrderOfGivenOrderId(self):
        response = requests.get(self.URL + '/getorders/{orderid}'.format(orderid='634717c8f929cf3d1611208f'))
        json_response = response.json()
        self.assertEqual(len(json_response), 2)
        self.assertEqual(json_response['_id']['$oid'], '634717c8f929cf3d1611208f')
        self.assertEqual(json_response['orders'][0], 'Pizza1')
        self.assertEqual(json_response['orders'][1], 'Pizza2')

    '''def testOrderResponse(self):
        orders = {
            'orders': ['Pizza4', 'Pizza5']
        }
        response = requests.post(self.URL + '/order', data=json.dumps(orders),
                                 headers={'Content-Type': 'application/json'})

        json_response = response.json()
        self.assertEqual(json_response['status'], 200)
        '''

    def testOrderResponse(self):
        orders = {
            'orders': ['Pizza5', 'Pizza6']
        }
        response = requests.post(self.URL + '/order', data=json.dumps(orders),
                                 headers={'Content-Type': 'application/json'})

        self.assertEqual(response.json(), 'Order Placed!')


if __name__ == '__main__':
    unittest.main()
