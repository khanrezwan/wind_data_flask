__author__ = 'rezwan'

from flask import jsonify
import datetime
#app specific imports
from .. import db
from ..models import RawData, Sensor
# ToDo-Rezwan make all routes return x,y data in following json format {"xy_list":[{"xy":{"x":1,"y":1}},{"xy":{"x":2,"y":6}},{"xy":{"x":4,"y":9}}]}
# ToDo-Rezwan use list comprehension to build json [{'X': itemX , 'Y' : itemY} for itemX, itemY in zip(xList,yList)]


class JsonBuilder(object):
    """
    1. This class will return json data and http response code
    2. it will receive query or query list and build json dict as following
    3. {"xy_list":[{"xy":{"x":1,"y":1}},{"xy":{"x":2,"y":6}},{"xy":{"x":4,"y":9}}]}
    4. sample json object:

        {"xy_list":[
            "y_label": "Channel 1 : Sensor desciption",
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

    DATE = 0
    MONTH = 1
    TIMESTAMP = 2

    @staticmethod
    def json_response(query, date, sensor_id, query_is_List=False, date_is_List=False, Xlabel=MONTH):
        print "Plot type ", Xlabel
        sensor, found =JsonBuilder.sensor_validator(sensor_id)
        print sensor, ' ', found
        JsonBuilder.datetime_validator(date)
        if isinstance(query,list):
            if isinstance(date,list):
                print "Query list Date List"
                pass
            else:
                # should be a list
                print "Query list Date single point " # get_Data_Date_Range_24Hr
                pass

            pass
        elif query.count() == 1:
            # Work with single point single for X and Y
            if not isinstance(date, list):
                print "Query single point Date single point"
            else:
                 print "Query single point Date list"

            pass
        elif query.count() > 1:
            if not isinstance(date, list):
                print "Query multi point Date single point"


            else:
                print "Query multi point Date list"

            pass
        else:
            print "No result in Query"
            pass

    # @staticmethod
    # def json_response_single_data(query,date, sensor_id):
    #     JsonBuilder.datetime_validator(date)
    #     (sensor, found) = JsonBuilder.sensor_validator(sensor_id)
    #     if found:  # sensor is model object of type Sensor
    #         dataList = list()
    #         dateList = list()
    #         idx = 0
    #         if isinstance(date, list()): # got a list so the json will be list
    #             if query.count != 0:
    #
    #                 for data in query.all():
    #                     if (data.ch_max is not None) or (data.ch_min is not None) or (data.ch_avg is not None):
    #                         dataList.append(data)
    #                         dateList.append(date[idx])
    #                         idx += 1
    #
    #
    #             else:
    #                 return "No Result", 404
    #                 pass
    #         else: # got single date so the Json for single data point
    #             if query.count() != 0:
    #                 data = query.first()
    #                 if (data.ch_max is not None) or (data.ch_min is not None) or (data.ch_avg is not None):
    #                     dataList.append(data)
    #                     dataList.append(date)
    #         jsonify(
    #             {
    #                 'success': True,
    #                 'YList': [{'Y': JsonBuilder.serialize_data(dataObj)} for dataObj in dataList],
    #                 'XList': [{'X': JsonBuilder.serialize_date(dateObj)} for dateObj in dateList],
    #                 'sensor': sensor.serialize()
    #
    #             })
    #         pass
    #     else:
    #         return sensor, 404  # sensor is string and 404 return not found
    #
    #     pass
    #
    # @staticmethod
    # def json_response_list(query_list, date_list, sensor_id):
    #     pass
    #
    # @staticmethod
    # def json_timestamp_response_list(query_list, date_list, sensor_id):
    #     pass

    @staticmethod
    def datetime_validator(date):
        if isinstance(date, list):
            for dt in date:
                if not isinstance(dt, datetime.datetime):
                    raise TypeError('date must be of type datetime.datetime')
        else:
            if not isinstance(date,datetime.datetime):
                raise TypeError('date must be of type datetime.datetime')

    @staticmethod
    def sensor_validator(sensor_id):
        """

        :param sensor_id: sensor id
        :return: tuple: (model object Sensor if there already in database and found = True) or,
                (string if not in database and found = False)
        """
        try:
            sensor_id = int(sensor_id)
        except ValueError:
            raise ValueError("sensor_id must be an integer")
        query = Sensor.query.filter(Sensor.id == sensor_id)
        if query.count() != 0:
            found = True
            return query.first(), found
        else:
            found = False
            return "Sensor not found", found


    @staticmethod
    def serialize_data(data_obj):
        """
        This was supposed to be inside RawData model but due to queries with entities we may receive a tuple hence here
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