from django.test import TestCase
from rest_framework.test import APITestCase
from apps.registercall.choices import CallTypes
from datetime import datetime
from apps.phonebill.functions import CallBill


class RegisterCallTestCase(APITestCase):
    """Class test over Call Resource"""

    fixtures = ['call.json']

    def setUp(self):
        super(RegisterCallTestCase, self).setUp()

        self.post_data_start = {
            "id_call": 78,
            "destination_call": "9993468278",
            "source_call": "99988526423",
            "timestamp_call": "2018-07-07 15:07:13",
            "type_call": 1
        }

        self.post_data_end = {
            "id_call": 78,
            "destination_call": "null",
            "source_call": "null",
            "timestamp_call": "2018-07-07 15:14:56",
            "type_call": 2
        }

    def create_call(self, type):
        """Make a post to create a call

        Arguments:
            **type (int):** the call type (1: Start, 2: End)

        Return:
            **response object:** the response of creation
        """

        if type == 1:
            data = self.post_data_start
        else:
            data = self.post_data_end
        return self.client.post('/registercall/', format='json', data=data)

    def test_create_call(self):
        """Test the API for create a new call

        Should return 201 CREATED
        """
        response = self.create_call(CallTypes.START)
        self.assertEquals(201, response.status_code)

        response = self.create_call(CallTypes.END)
        self.assertEquals(201, response.status_code)

    def test_get_calls(self):
        """Test the API for get all the calls

        Should return 200 OK and a list of calls
        """
        response = self.client.get('/registercall/', format='json')
        calls = response.json()
        self.assertEquals(200, response.status_code)
        self.assertTrue(len(calls) > 0)

    def test_get_call_detail(self):
        """Test the API for get a specific call

        Should return 200 OK
        """
        response = self.create_call(CallTypes.START)
        created_call = response.json()
        response = self.client.get("/registercall/{}/"
                                   .format(created_call['id']), format='json')
        self.assertEquals(200, response.status_code)

    def test_update_call(self):
        """Test the API for update a specific call

        Should return 200 OK
        """
        response = self.create_call(CallTypes.START)
        created_call = response.json()

        new_data = {
            "id_call": 99,
            "destination_call": "9993468278",
            "source_call": "99988526423",
            "timestamp_call": "2018-07-07 19:11:11",
            "type_call": 1
        }

        response = self.client.patch(
            "/registercall/{}/".format(created_call['id']), format='json', data=new_data
        )
        self.assertEquals(200, response.status_code)

    def test_update_partial_call(self):
        """Test the API for update a specific call

        Should return 200 OK
        """
        response = self.create_call(CallTypes.START)
        created_call = response.json()

        response = self.client.patch(
            "/registercall/{}/".format(created_call['id']), format='json',
            data={'timestamp_call': '2018-07-07 15:07:13'}
        )
        self.assertEquals(200, response.status_code)

    def test_delete_call(self):
        """Test the API for delete a specific call

        Should return 204 METHOD NO CONTENT
        """
        response = self.create_call(CallTypes.START)
        created_call = response.json()
        response = self.client.delete("/registercall/{}/"
                                      .format(created_call['id']), format='json')
        self.assertEquals(204, response.status_code)

    def test_no_data_call(self):
        """Test the API for create a new call with no data

        Should return 400 BAD REQUEST and a dict with the errors
        ::

            {
                'call': {
                    'call_id': ['This field is required'],
                    'timestamp': ['This field is required']
                }
            }
        """
        response = self.client.post('/registercall/', format='json', data={})
        self.assertEquals(400, response.status_code)
        self.assertEquals(
            {'type_call': ['This field is required.'],
             'timestamp_call': ['This field is required.'],
             'id_call': ['This field is required.'],
             'source_call': ['This field is required.'],
             'destination_call': ['This field is required.']},
            response.json()
        )

    def test_no_type_call(self):
        """Test the API for create a new call with no type

        Should return 400 BAD REQUEST and a dict with the error
        ::

            {
                'call': {
                    'type': ['This field cannot be null.']
                }
            }
        """
        del self.post_data_start['type_call']

        response = self.create_call(CallTypes.START)
        self.assertEquals(400, response.status_code)
        self.assertEquals(
            {'type_call': ['This field is required.']},
            response.json()
        )

    def teste_invalid_timestamp_call(self):
        """Test the API for create a new call with an invalid timestamp

        Should return 400 BAD REQUEST and a dict with the error
        ::

            {
                'error': "Datetime provided to 'timestamp_call' field doesn't appear to be
                a valid datetime string: <timestamp>."
            }
        """
        self.post_data_start['timestamp_call'] = "2018-99-99 00:00:00"
        response = self.create_call(CallTypes.START)

        self.assertEquals(400, response.status_code)
        self.assertEquals(
            {'timestamp_call':
             ['Datetime has wrong format. '
              'Use one of these formats instead: '
              'YYYY-MM-DDThh:mm[:ss[.uuuuuu]][+HH:MM|-HH:MM|Z].']},
            response.json()
        )

    def test_invalid_start_call(self):
        """Test the API for create a new start call without source and destination arguments

        Should return 400 BAD REQUEST and a dict with the errors
        ::

            {
                'call': {
                    'destination': ['This field is required'],
                    'source': ['This field is required']
                }
            }
        """
        del self.post_data_start['source_call']
        del self.post_data_start['destination_call']
        response = self.create_call(CallTypes.START)
        self.assertEquals(400, response.status_code)
        self.assertEquals(
            {'source_call': ['This field is required.'],
             'destination_call': ['This field is required.']},
            response.json()
        )


class PhoneBillTestCase(TestCase):
    """Class test over Bill Resource"""

    fixtures = ['bill.json']

    def setUp(self):
        super(PhoneBillTestCase, self).setUp()

        self.phone_bill = {
            "source_call": "99988526423",
            "period": "04/2019"
        }

    def create_phone_bill(self):
        """Make a post to create a Phone Bill

        Return:
            **response object:** the response of creation
        """

        data = self.phone_bill

        return self.client.post('/phonebill/', format='json', data=data)

    def test_create_phone_bill(self):
        """Test the API for create a new phone bill

        Should return 200 CREATED
        """
        response = self.create_phone_bill()
        self.assertEquals(200, response.status_code)

    def test_list_bill(self):
        """Test the API for get the list bill

        Should returno 200 OK
        """
        response = self.client.get('/phonebill/')
        self.assertEquals(200, response.status_code)


class BillCallRateTest(TestCase):
    """Class test over BillCall"""

    fixtures = ['call.json']

    def setUp(self):
        super(BillCallRateTest, self).setUp()

    def test_duration(self):
        """Test the duration of a call"""
        duration = CallBill._get_duration(0, 0)
        self.assertEquals("0h0m0s", duration)

        duration = CallBill._get_duration(datetime(2019, 1, 1, 21, 57, 13),
                                          datetime(2019, 1, 1, 22, 10, 56))
        self.assertEquals("0h13m43s", duration)

    def test_price(self):
        """Test the price of a call"""
        price = CallBill._get_price(0, 0)
        self.assertEquals("R$ 0.00", price)

        price = CallBill._get_price(datetime(2019, 1, 1, 21, 57, 13),
                                    datetime(2019, 1, 1, 22, 10, 56))
        self.assertEquals("R$ 0,54", price)

