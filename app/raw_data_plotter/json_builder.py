__author__ = 'rezwan'

from flask import jsonify
import datetime
#app specific imports
from .. import db

# ToDo-Rezwan make all routes return x,y data in following json format {"xy_list":[{"xy":{"x":1,"y":1}},{"xy":{"x":2,"y":6}},{"xy":{"x":4,"y":9}}]}

class JsonBuilder(object):
    """
    1. This class will return json data and http response code
    2. it will receive query or query list and build json dict as following
    3. {"xy_list":[{"xy":{"x":1,"y":1}},{"xy":{"x":2,"y":6}},{"xy":{"x":4,"y":9}}]}
    4. sample json object:

        {"xy_list":[
            "y_label": "Sensor1 : Sensor desciption",
            "x_label": "date" / "Timestamp"/ "Month",
            " y_unit": "m/s" / "volt"
            "xy":
            {
                "x":
                {
                    "ch_max": 8.11,
                    "ch_min": 5.2,
                    "ch_avg": 7.0
                },
                "y": "2015-05-1T20:34:05.787Z" / "00:00" / "January"
            }
            },
            ...
            "success":  True
            ]
        }
    """
    @staticmethod
    def json_response_single_data(query,date, sensor_id):
        JsonBuilder.datetime_validator(date)

        pass

    @staticmethod
    def json_response_list(query_list, date_list, sensor_id):
        pass

    @staticmethod
    def json_timestamp_response_list(query_list, date_list, sensor_id):
        pass

    @staticmethod
    def datetime_validator(date):
        if isinstance(date,list()):
            for dt in date:
                if not isinstance(dt, datetime.datetime):
                    raise TypeError('date must be of type datetime.datetime')
        else:
            if not isinstance(date,datetime.datetime):
                raise TypeError('date must be of type datetime.datetime')

    @staticmethod
    def serialize_data(data_obj):
        """
        This was supposed to be inside RawData model but due to queries with entities we may recive a tuple hence here
        :param data_obj:
        :return:
        """
        return {
            "ch_max": "{0:.2f}".format(data_obj.ch_max),
            "ch_min": "{0:.2f}".format(data_obj.ch_min),
            "ch_Avg": "{0:.2f}".format(data_obj.ch_avg)
        }

    @staticmethod
    def serialize_date(obj):
        """
        JSON serializer for datetime objects not serializable by default json code
        :param obj: a datetime.datetime object
        :return:
        """
        if isinstance(obj, datetime.datetime):
            serial = obj.isoformat()
            return serial
        raise TypeError("Type not serializable")
    pass