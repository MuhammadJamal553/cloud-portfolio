import unittest
from unittest.mock import MagicMock
import lambda_function

class TestChallangeCounter(unittest.TestCase):
    def test_hanlder_simulated_response(self):
        mock_dynamo = MagicMock()
        lambda_function.boto3.resource = MagicMock(return_value=mock_dynamo)
        mock_table = MagicMock()
        # 1. Mock the AWS DynamoDB resource so it doesn't contact real AWS servers
        mock_dynamo.Table.return_value = mock_table
        # 2. Simulate DynamoDB returning an updated visitor count of 20
        mock_table.update_item.return_value = {
            'Attributes': {
                'visitor_count' : 20
            }
        }

        # 3. Invoke your function signature

        fake_event ={}
        fake_context={}
        response = lambda_function.lambda_handler(fake_event,fake_context)


        # 4. Assert that the function parses out the data count correctly
        self.assertEqual(response['statusCode'],200)
        self.assertIn('20', response['body'])