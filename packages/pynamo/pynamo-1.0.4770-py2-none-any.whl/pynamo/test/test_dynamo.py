"""we'll need a test sample"""

from copy import deepcopy

import boto3
from moto import mock_dynamodb2
from pynamo import Pynamo

TEST_ITEM = {
    "PrimaryKey": 'primary-key-1',
    "SecondaryKey": 'secondary-key-2',
    "data": {
        'datakey0': "",
        'datakey1': 1,
        'datakey2': 'hello',
        'datakey3': True,
        'datakey4': None,
        'datakey5': [
            1, True, 'hello'
        ]
    }
}

TEST_RETURN = {
    "PrimaryKey": 'primary-key-1',
    "SecondaryKey": 'secondary-key-2',
    "data": {
        'datakey0': None,
        'datakey1': 1,
        'datakey2': 'hello',
        'datakey3': True,
        'datakey4': None,
        'datakey5': [
            1, True, 'hello'
        ]
    }
}

TEST_KEY = {
    "PrimaryKey": 'primary-key-1',
    "SecondaryKey": 'secondary-key-2'
}

TEST_ATTRIBUTES = {
    "data": {
        "Value": {
            "datakey1": 2
        },
        "Action": "PUT"
    }
}

SESSION_INFO = {
    "region_name": 'us-east-1'
}

@mock_dynamodb2
def test_empty_scan():
    create_test_table()
    response = Pynamo(**SESSION_INFO).scan('test_table')
    assert response['status'] == 200 and response['data'] == [] and response['error_msg'] is None

@mock_dynamodb2
def test_put_scan():
    create_test_table()
    Pynamo(**SESSION_INFO).put_item('test_table', TEST_ITEM)
    scan_response = Pynamo(**SESSION_INFO).scan('test_table')
    assert scan_response['data'] == [TEST_RETURN]

@mock_dynamodb2
def test_put_get():
    create_test_table()
    Pynamo(**SESSION_INFO).put_item('test_table', TEST_ITEM)
    get_response = Pynamo(**SESSION_INFO).get_item('test_table', TEST_KEY)
    assert get_response['data'] == TEST_RETURN

@mock_dynamodb2
def test_put_delete():
    create_test_table()
    Pynamo(**SESSION_INFO).put_item('test_table', TEST_ITEM)
    Pynamo(**SESSION_INFO).delete_item('test_table', TEST_KEY)
    scan_response = Pynamo(**SESSION_INFO).scan('test_table')
    assert scan_response['status'] == 200 and scan_response['data'] == [] and scan_response['error_msg'] is None

@mock_dynamodb2
def test_put_update_get():
    create_test_table()
    Pynamo(**SESSION_INFO).put_item('test_table', TEST_ITEM)
    Pynamo(**SESSION_INFO).update_item('test_table', TEST_KEY, TEST_ATTRIBUTES)
    get_response = Pynamo(**SESSION_INFO).get_item('test_table', TEST_KEY)

    predicted_item = deepcopy(TEST_RETURN)
    predicted_item['data'] = {"datakey1": 2}
    assert get_response['data'] == predicted_item

@mock_dynamodb2
def test_error_no_table():
    create_test_table()
    error_codes = [403, 404, 500]
    pyn = Pynamo(**SESSION_INFO)
    if pyn.scan('bad-table')['status'] not in error_codes:
        assert False
    if pyn.get_item('bad-table', TEST_KEY)['status'] not in error_codes:
        assert False
    if pyn.put_item('bad-table', TEST_ITEM)['status'] not in error_codes:
        assert False
    if pyn.delete_item('bad-table', TEST_KEY)['status'] not in error_codes:
        assert False
    if pyn.update_item('bad-table', TEST_KEY, TEST_ATTRIBUTES)['status'] not in error_codes:
        assert False
    assert True 

@mock_dynamodb2
def test_existing_session():
    create_test_table()
    session = boto3.session.Session(**SESSION_INFO)
    response = Pynamo(boto_session=session).scan('test_table')
    assert response['status'] == 200 and response['data'] == [] and response['error_msg'] is None


def create_test_table():
    Pynamo(**SESSION_INFO).client.create_table(
        AttributeDefinitions=[
            {
                'AttributeName': 'PrimaryKey',
                'AttributeType': 'S'
            },
            {
                'AttributeName': 'SecondaryKey',
                'AttributeType': 'S'
            }
        ],
        TableName='test_table',
        KeySchema=[
            {
                'AttributeName': 'PrimaryKey',
                'KeyType': 'HASH'
            },
            {
                'AttributeName': 'SecondaryKey',
                'KeyType': 'RANGE'
            },
        ],
        ProvisionedThroughput={
            'ReadCapacityUnits': 10,
            'WriteCapacityUnits': 10
        }
    )
