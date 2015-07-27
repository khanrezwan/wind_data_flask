__author__ = 'rezwan'

from flask import jsonify
import datetime
#app specific imports
from .. import db
from ..models import RawData, Sensor
from .Rawdata_plotter_helper import dict_keys
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
    def json_response(dictionary, Xlabel=MONTH):
        # ToDo-Rezwan merge 1st + 4th if  and  3rd + 5th if
        # ToDo-Rezwan make complete Json response rather than dicts
        if isinstance(dictionary, dict):
            dictionary_keys = dictionary.keys()
            for key in dict_keys:
                if key not in dictionary_keys:
                    raise KeyError('Not the expected dictionary')
        else:
            raise ValueError("the parameter dictionary must be a python dict")
        query = dictionary['query']
        sensor_id = dictionary['sensor_id']
        date = dictionary['date']
        time_stamp = dictionary['time_stamp']

        print "Plot type ", Xlabel
        sensor, found = JsonBuilder.sensor_validator(sensor_id)
        print sensor, ' ', found
        JsonBuilder.datetime_validator(date)
        if found:
            if isinstance(query, list) and isinstance(date, list) and time_stamp is None:
                # get_Data_Date_Range_Single_Point_for_each_Date(startDate, endDate, sensor_id)
                # get_Data_Month_Range_Single_Point_for_each_Month
                query_list = list()
                for q in query:
                    query_list.append(q.first())
                print 'in first if'
                return ([{'X': JsonBuilder.serialize_date(itemX) , 'Y' : JsonBuilder.serialize_data(itemY)} for itemX, itemY in zip(date, query_list)])
                pass
            elif query.count() > 1 and not(isinstance(date, list) or isinstance(date, tuple)) and isinstance(time_stamp,list):
                # get_Data_Date_24Hr(date, sensor_id)
                # get_Data_Month_24Hr(date, sensor_id) to b implemented
                print 'in 2nd if'
                return ([{'X': itemX , 'Y' : JsonBuilder.serialize_data(itemY)} for itemX, itemY in zip(time_stamp, query.all())])

                pass
            elif query.count() == 1 and not(isinstance(date, list) or isinstance(date, tuple)) and time_stamp is None:
                # get_Data_Date_Single_Point(date, sensor_id)
                # get_Data_Month_Single_Point
                print 'in 3rd if'
                return {
                    'X': JsonBuilder.serialize_date(date),
                    'Y': JsonBuilder.serialize_data(query.first())
                }
                pass
            elif isinstance(query, list) and isinstance(date, tuple) and isinstance(time_stamp, list):
                # get_Data_Date_Range_24Hr(startDate, endDate, sensor_id)
                # get_Data_Month_Range_24Hr(startDate, endDate, sensor_id) to b implemented
                print 'in 4th if'
                query_list = list()
                for q in query:
                    query_list.append(q.first())
                return ([{'X': itemX , 'Y' : JsonBuilder.serialize_data(itemY)} for itemX, itemY in zip(time_stamp, query_list)])
                pass
            elif query.count() == 1 and isinstance(date, tuple) and time_stamp is None:
                #get_Data_Date_Range_Single_Point(startDate, endDate, sensor_id)
                # get_Data_Month_Range_Single_Point
                print 'in 5th if'
                return {
                    'X': JsonBuilder.serialize_date(date),
                    'Y': JsonBuilder.serialize_data(query.first())
                }
                pass
            else:
                print 'WTF??'
                return 'Query got 0 result', 404
                pass
        else:
            return sensor, 404 #sensor is string and 404 is not found
        # if isinstance(query, list):
        #     print "Query list"
        #     if isinstance(date, list):
        #         print "Date is List"
        #         pass
        #     elif isinstance(date, tuple):
        #         print "Date is tuple"
        #         pass
        #     else:
        #         # should be a list
        #         print "Date single point " # get_Data_Date_Range_24Hr
        #         pass
        #
        #     pass
        # elif query.count() == 1:
        #     # Work with single point single for X and Y
        #     print "Query single point"
        #     if isinstance(date, list):
        #         print "Date is list"
        #     elif isinstance(date, tuple):
        #         print "Date is tuple"
        #     else:
        #          print " Date single point"
        #
        #     pass
        # elif query.count() > 1:
        #     if isinstance(date, list):
        #         print "Query multi point Date is list"
        #
        #     elif isinstance(date, tuple):
        #         print "Date is tuple"
        #
        #     else:
        #         print "Query multi point Date single point"
        #
        #     pass
        # else:
        #     print "No result in Query"
        #     pass

    @staticmethod
    def datetime_validator(date):
        if isinstance(date, list) or isinstance(date, tuple):
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
        # if not isinstance(data_obj.ch_avg, basestring) and not isinstance(data_obj.ch_max, basestring) and not isinstance(data_obj.ch_min, basestring):
        if data_obj.ch_avg and data_obj.ch_max and data_obj.ch_min:
            return {
                "ch_max": float("{0:.2f}".format(data_obj.ch_max)),
                "ch_min": float("{0:.2f}".format(data_obj.ch_min)),
                "ch_Avg": float("{0:.2f}".format(data_obj.ch_avg))
            }
        else:
            return {
                "ch_max": (data_obj.ch_max),
                "ch_min": (data_obj.ch_min),
                "ch_Avg": (data_obj.ch_avg)
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