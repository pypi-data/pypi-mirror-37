""" File for loading data from Dynamo Tables """

from copy import deepcopy
import boto3
from botocore.exceptions import ClientError


class Pynamo(object):
    """ Class for adding methods on top of boto3 dynamo client/session """

    def __init__(self, boto_session=None, table_prefix="", raise_exception=False, **kwargs):

        if boto_session:
            self.session = boto_session
        else:
            self.session = boto3.session.Session(**kwargs)
        self.client = self.session.client('dynamodb')
        self.raise_exception = raise_exception
        self.__table_prefix = table_prefix
        self.__default_response = {
            'status': 200,
            'error_msg': None,
            'data': []
        }

    def scan(self, table_name, **kwargs):
        """ Load in generic table """
        response = deepcopy(self.__default_response)
        kwargs['TableName'] = '%s%s' % (self.__table_prefix, table_name)
        while True:
            try:
                table_response = self.client.scan(**kwargs)
                response['data'].extend(self._dyno_dic(table_response.get('Items', [])))
                if not table_response.get('LastEvaluatedKey', None):
                    break
                else:
                    kwargs['ExclusiveStartKey'] = table_response['LastEvaluatedKey']
            except ClientError as error:
                return self.__return(self.__client_error(error, response, table_name))
        return self.__return(response)

    def get_item(self, table_name, key, **kwargs):
        """ Get Item from Dynamo Table """
        response = deepcopy(self.__default_response)
        kwargs['TableName'] = '%s%s' % (self.__table_prefix, table_name)
        kwargs['Key'] = self._dic_dyno(key)

        try:
            table_response = self.client.get_item(**kwargs)
        except ClientError as error:
            return self.__return(self.__client_error(error, response, table_name))

        response['data'] = self._dyno_dic([table_response.get('Item', None)])[0]
        if not response['data']:
            response['status'] = 404
            response['error_msg'] = "%s could not be found in %s." % (key, kwargs['TableName'])
        return self.__return(response)

    def put_item(self, table_name, item, overwrite=False, **kwargs):
        """ Put Item into Dynamo Table """
        response = deepcopy(self.__default_response)
        kwargs['TableName'] = '%s%s' % (self.__table_prefix, table_name)
        for key, value in item.items():
            if value == "":
                item[key] = None
        kwargs['Item'] = self._dic_dyno(item)

        # Check to make sure not overwriting same entry
        if not overwrite:
            try:
                keys = self.table_keys(table_name)
            except ClientError as error:
                return self.__return(self.__client_error(error, response, table_name))
            if keys["RANGE"]:
                condition = "NOT (attribute_exists(#name_hash) AND attribute_exists(#name_range))"
                expression_names = {"#name_hash": keys["HASH"], "#name_range": keys["RANGE"]}
            else:
                condition = "attribute_not_exists(#name_hash)"
                expression_names = {"#name_hash": keys["HASH"]}

            kwargs["ConditionExpression"] = condition
            kwargs["ExpressionAttributeNames"] = expression_names

        try:
            self.client.put_item(**kwargs)
        except ClientError as error:
            return self.__return(self.__client_error(error, response, table_name))
        response['data'] = item
        return self.__return(response)

    def delete_item(self, table_name, key, **kwargs):
        """ Delete Item from Dynamo Table """
        response = deepcopy(self.__default_response)
        kwargs['TableName'] = '%s%s' % (self.__table_prefix, table_name)
        kwargs['Key'] = self._dic_dyno(key)
        try:
            table_response = self.client.delete_item(**kwargs)
        except ClientError as error:
            return self.__return(self.__client_error(error, response, table_name))
        response['data'] = table_response
        return self.__return(response)

    def update_item(self, table_name, key, attribute_updates, **kwargs):
        """ Update Item in Dynamo Table """
        response = deepcopy(self.__default_response)
        kwargs['TableName'] = '%s%s' % (self.__table_prefix, table_name)
        kwargs['Key'] = self._dic_dyno(key)

        new_attributes = {}
        for up_key, up_value in attribute_updates.items():
            new_attributes[up_key] = {}
            new_attributes[up_key]['Action'] = up_value['Action']
            new_attributes[up_key]['Value'] = self._dic_dyno(up_value['Value'], first=False)
        kwargs['AttributeUpdates'] = new_attributes

        try:
            table_response = self.client.update_item(**kwargs)
        except (ValueError, ClientError) as error:
            return self.__return(self.__client_error(error, response, table_name))
        response['data'] = table_response
        return self.__return(response)

    def rewrite_item(self, table_name, original_key, new_item):
        response = deepcopy(self.__default_response)

        # Get table keys
        try:
            keys = self.table_keys(table_name)
            get_response = self.get_item(table_name, original_key)
            if get_response['status'] != 200:
                return self.__return(get_response)
        except (ValueError, ClientError) as error:
            return self.__return(self.__client_error(error, response, table_name))

        # Check if keys changed
        same_key = True
        for key in [x for x in keys.values() if x]:
            if key not in original_key.keys():
                response['error_msg'] = "%s is a key for table %s, but is not in original_key" % (key, table_name)
                response['status'] = 400
                return self.__return(response)
            if key not in new_item.keys():
                response['error'] = "%s is a key for table %s, but is not in new_item" % (key, table_name)
                response['status'] = 400
                return self.__return(response)
            same_key = same_key and original_key[key] == new_item[key]

        # Key not changed
        if same_key:
            return self.__return(self.put_item(table_name, new_item))

        # Key changed
        put_table_response = self.put_item(table_name, new_item, overwrite=False)

        # Delete old entry
        if put_table_response['status'] == 200:
            del_table_response = self.delete_item(table_name, original_key)
            if del_table_response['status'] != 200:
                return self.__return(del_table_response)

        return self.__return(put_table_response)

    def table_keys(self, table_name):
        key_schema = self.client.describe_table(TableName=table_name)['Table']['KeySchema']
        return {
            "HASH": next((x["AttributeName"] for x in key_schema if x['KeyType'] == "HASH"), None),
            "RANGE": next((x["AttributeName"] for x in key_schema if x['KeyType'] == "RANGE"), None)
        }

    def table_key_values(self, table_name):
        keys = self.table_keys(table_name)
        response = self.scan(table_name, AttributesToGet=[x for x in keys.values() if x])
        return self.__return(response)

    def __return(self, response):
        if self.raise_exception and response['status'] != 200:
            raise Exception(response['error_msg'])
        return response

    # def update_item_list(self, table_name, key, attribute, elements, add):
    #     """ Add/Remove Element from Item List in Dynamo Table """
    #     #get current table item
    #     response = deepcopy(self.__default_response)
    #     get_response = self.get_item(
    #         table_name,
    #         key,
    #         AttributesToGet=['AccountNumber', attribute, 'Status']
    #     )
    #     if not get_response.get('data', None):
    #         return get_response

    #     current_attribute = get_response['data'][attribute]
    #     if not isinstance(current_attribute, list):
    #         response['status'] = 400,
    #         response['error_msg'] = 'Selected attribute is not a list'
    #         return response

    #     attribute_updates = {attribute: {'Action': 'PUT'}}
    #     if add:
    #         attribute_updates[attribute]['Value'] = [
    #             x for x in current_attribute if x not in elements
    #         ] + elements
    #     else:
    #         attribute_updates[attribute]['Value'] = [
    #             x for x in current_attribute if x not in elements
    #         ]

    #     return self.update_item(table_name, key, attribute_updates)


####################################################################################################

    def _dyno_dic(self, dyna_data, data_type=None, first=True):
        """ Convert dynamodb reponse to standard dictionary """
        data_keys = {
            "BOOL": bool,
            "S": str,
            "N": float,
            "B": str
        }

        if first:
            return [self._dyno_dic(x, data_type=None, first=False) for x in dyna_data]
        elif data_type == "NULL":
            return None
        elif isinstance(dyna_data, dict):
            return {str(k): self._dyno_dic(v[v.keys()[0]], data_type=v.keys()[0], first=False)
                    for (k, v) in dyna_data.items()}
        elif isinstance(dyna_data, list) and data_type != "SS" and data_type != "NS":
            return [self._dyno_dic(x[x.keys()[0]], data_type=x.keys()[0], first=False)
                    for x in dyna_data]
        elif data_type in data_keys:
            return data_keys[data_type](dyna_data)
        return str(dyna_data)

    def _dic_dyno(self, input_value, first=True):
        """ Convert standard dictionary to dynamodb """
        type_keys = {
            int: "N",
            float: "N",
            str: "S",
        }

        if first:
            return {str(k): self._dic_dyno(v, first=False) for (k, v) in input_value.items()}
        if isinstance(input_value, dict):
            return {"M": {k: self._dic_dyno(v, first=False) for (k, v) in input_value.items()}}
        elif isinstance(input_value, list):
            return {"L": [self._dic_dyno(x, first=False) for x in input_value]}
        elif input_value is None or input_value == "":
            return {"NULL": True}
        elif isinstance(input_value, bool):
            return {"BOOL": input_value}
        elif type(input_value) in type_keys:
            return {type_keys[type(input_value)]: str(input_value)}
        return {"S": str(input_value)}


    def __client_error(self, error, response, table_name=None):
        if "response" not in dir(error):
            response['status'] = 500
            response['error_msg'] = str(error)
        elif error.response['Error']['Code'] == 'ResourceNotFoundException':
            response['status'] = 404
            response['error_msg'] = "%s could not be found." % table_name
        elif error.response['Error']['Code'] == 'ExpiredTokenException':
            response['status'] = 403
            response['error_msg'] = "Token expired"
        elif error.response['Error']['Code'] in ['ConditionalCheckFailedException', 'ValidationException']:
            response['status'] = 403
            response['error_msg'] = str(error)
        else:
            response['status'] = 500
            response['error_msg'] = str(error)
        return response
