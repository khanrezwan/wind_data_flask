__author__ = 'rezwan'

from flask import jsonify
import datetime
import calendar
#app specific imports
from .. import db
from ..models import RawData, Sensor
from .Rawdata_plotter_helper import dict_keys



class JsonBuilder(object):
    """
    1. This class will return json data and http response code
    2. it will receive query or query list and build json dict as following
    3. {"xy_list":[{"xy":{"x":1,"y":1}},{"xy":{"x":2,"y":6}},{"xy":{"x":4,"y":9}}]}
    4. sample json object:

        {"xy_list":[
            "y_label": "Channel 1 : Sensor desciption",
            "x_label": "date" / "Timestamp"/ "Month",

            "xy":
            {
                "Y":
                {
                    "ch_max": 8.11,
                    "ch_min": 5.2,
                    "ch_avg": 7.0
                },
                "X": "2015-05-1T20:34:05.787Z" / "00:00" / "January"
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
    def json_response(dictionary, Xlabel=DATE):
        # ToDo-Rezwan Add comment as the function is way too convoluted

        if isinstance(dictionary, dict):
            dictionary_keys = dictionary.keys()
            for key in dict_keys:
                if key not in dictionary_keys:
                    return jsonify({'error': 'Not the expected dictionary'}), 404
                    # raise KeyError('Not the expected dictionary')
        else:
            return jsonify({'error': 'Not a dictionary'}), 404
            # raise TypeError("the parameter dictionary must be a python dict")
        query = dictionary['query']
        sensor_id = dictionary['sensor_id']
        date = dictionary['date']
        time_stamp = dictionary['time_stamp']

        sensor, found = JsonBuilder.sensor_validator(sensor_id)
        # print sensor, ' ', found
        JsonBuilder.datetime_validator(date)
        if found:
            date_format = "%d-%b-%Y"
            y_label_text = 'Channel ' + str(sensor.channel)+': ' + sensor.description + ' @ height ' \
                           + str(sensor.height) + 'm'
            X_label_text = JsonBuilder.extract_x_label_text(Xlabel)
            if isinstance(query, list):
                if isinstance(date, list) and time_stamp is None:
                    # get_Data_Date_Range_Single_Point_for_each_Date(startDate, endDate, sensor_id)
                    # get_Data_Month_Range_Single_Point_for_each_Month
                    query_list = list()

                    for q in query:
                        query_list.append(q.first())
                    # print 'in first if'
                    if Xlabel == JsonBuilder.MONTH:
                        date_list = list()
                        for dt in date:
                            date_list.append(JsonBuilder.extract_month_from_date(dt))
                        plot_data = JsonBuilder.plot_dictionary_builder(query_list, date_list, keep_date_string=True)
                        return jsonify({'plot_data': plot_data,
                                        "y_label": y_label_text,
                                        "x_label": X_label_text,
                                        "success": True}), 200
                    else:
                        plot_data = JsonBuilder.plot_dictionary_builder(query_list, date)
                        return jsonify({'plot_data': plot_data,
                                        "y_label": y_label_text,
                                        "x_label": X_label_text,
                                        "success": True}), 200
                elif isinstance(date, tuple) and isinstance(time_stamp, list):
                    # get_Data_Date_Range_24Hr(startDate, endDate, sensor_id)
                    # get_Data_Month_Range_24Hr(startDate, endDate, sensor_id) to b implemented
                    # print 'in 4th if'
                    query_list = list()

                    date_from_to = 'From '
                    if Xlabel == JsonBuilder.MONTH:
                        count = 1
                        for item in date:
                            date_from_to += JsonBuilder.extract_month_from_date(item)
                            if count < date.__len__():
                                date_from_to += ' to ' #append to between two dates
                            count += 1
                        X_label_text += date_from_to
                    else:
                        count = 1
                        for item in date:
                            date_from_to += item.strftime(date_format)
                            if count < date.__len__():
                                date_from_to += ' to ' #append to between two dates
                            count += 1
                        X_label_text += date_from_to

                    for q in query:
                        query_list.append(q.first())

                    # return ([{'X': itemX , 'Y' : JsonBuilder.serialize_data(itemY)} for itemX, itemY in zip(time_stamp, query_list)])
                    plot_data = JsonBuilder.plot_dictionary_builder(query_list, time_stamp, keep_date_string=True)
                    return jsonify({'plot_data': plot_data,
                                    "y_label": y_label_text,
                                    "x_label": X_label_text,
                                    "success": True}), 200
                    pass
            elif not isinstance(query, list):
                if query.count() > 1 and not(isinstance(date, list) or isinstance(date, tuple)) and isinstance(time_stamp,list):
                    # get_Data_Date_24Hr(date, sensor_id)
                    # get_Data_Month_24Hr(date, sensor_id) to b implemented
                    # print 'in 2nd if'
                    if Xlabel == JsonBuilder.MONTH:
                        X_label_text += JsonBuilder.extract_month_from_date(date)
                    else:
                        X_label_text += date.strftime(date_format)
                    # return ([{'X': itemX , 'Y' : JsonBuilder.serialize_data(itemY)} for itemX, itemY in zip(time_stamp, query.all())])
                    plot_data = JsonBuilder.plot_dictionary_builder(query.all(), time_stamp, keep_date_string=True)
                    # X = list()
                    # Y =list()
                    # for data in plot_data:
                    #     X.append(data['X'])
                    #     Y.append(data['Y'])
                    # print X
                    # print Y
                    return jsonify({'plot_data': plot_data,
                                    "y_label": y_label_text,
                                    "x_label": X_label_text,
                                    "success": True}) ,200
                    pass
                elif query.count() == 1 and not(isinstance(date, list) or isinstance(date, tuple)) and time_stamp is None:
                    # get_Data_Date_Single_Point(date, sensor_id)
                    # get_Data_Month_Single_Point
                    # print 'in 3rd if'
                    data_list = list()
                    date_list = list()
                    (data_list.append(query.first()))

                    if Xlabel == JsonBuilder.MONTH:
                        X_label_text += JsonBuilder.extract_month_from_date(date)
                    else:
                        X_label_text += date.strftime(date_format)

                    if Xlabel == JsonBuilder.MONTH:
                        date_list.append(JsonBuilder.extract_month_from_date(date))
                        plot_data = JsonBuilder.plot_dictionary_builder(data_list, date_list, keep_date_string=True)
                        return jsonify({'plot_data': plot_data,
                                        "y_label": y_label_text,
                                        "x_label": X_label_text,
                                        "success": True}), 200
                    else:
                        date_list.append(date)
                        # return ([{'X': JsonBuilder.serialize_date(itemX), 'Y': JsonBuilder.serialize_data(itemY)} for itemX, itemY in zip(date_list, data_list) if (itemY.ch_max and itemY.ch_min and itemY.ch_avg)])
                        plot_data = JsonBuilder.plot_dictionary_builder(data_list, date_list)
                        return jsonify({'plot_data': plot_data,
                                        "y_label": y_label_text,
                                        "x_label": X_label_text,
                                        "success": True}), 200
                    pass
                elif query.count() == 1 and isinstance(date, tuple) and time_stamp is None:
                    #get_Data_Date_Range_Single_Point(startDate, endDate, sensor_id)
                    # get_Data_Month_Range_Single_Point
                    # print 'in 5th if'
                    data_list = list()
                    date_list = list()
                    (data_list.append(query.first()))
                    date_from_to = 'From '
                    if Xlabel == JsonBuilder.MONTH:
                        count = 1
                        for item in date:
                            date_from_to += JsonBuilder.extract_month_from_date(item)
                            if count < date.__len__():
                                date_from_to += ' to ' #append to between two dates
                            count += 1
                        date_list.append(date_from_to)
                    else:
                        count = 1
                        for item in date:
                            date_from_to += item.strftime(date_format)
                            if count < date.__len__():
                                date_from_to += ' to ' #append to between two dates
                            count += 1
                        date_list.append(date_from_to)

                    plot_data = JsonBuilder.plot_dictionary_builder(data_list, date_list, keep_date_string=True)

                    return jsonify({'plot_data': plot_data,
                                    "y_label": y_label_text,
                                    "x_label": X_label_text,
                                    "success": True}) ,200

                else:
                    # print 'WTF??'
                    return jsonify({'error': 'No Query result from database'}), 404
                    pass
            else:
                return jsonify({'error': 'query is an unexpected object'}), 404
        else:
            return jsonify({'error': 'Sensor not found in database'}), 404 #sensor is string and 404 is not found

    @staticmethod
    def plot_dictionary_builder(data_list, date_list, keep_date_string=False):
        if not keep_date_string:
            return ([{'X': JsonBuilder.serialize_date(itemX), 'Y': JsonBuilder.serialize_data(itemY)}
                     for itemX, itemY in zip(date_list, data_list)
                     if (itemY.ch_max and itemY.ch_min and itemY.ch_avg)])
        else:
            return ([{'X': itemX, 'Y': JsonBuilder.serialize_data(itemY)}
                     for itemX, itemY in zip(date_list, data_list)
                     if (itemY.ch_max and itemY.ch_min and itemY.ch_avg)])

    @staticmethod
    def extract_month_from_date(date):
        """

        :param date: datetime.datetime
        :return: string
        """
        if isinstance(date, datetime.datetime):
            return calendar.month_name[date.month]
        else:
            raise TypeError("date must be a datetime.datetime object")


    @staticmethod
    def extract_x_label_text(Xlabel):
        if Xlabel == JsonBuilder.DATE:
            return 'Date'
            pass
        elif Xlabel == JsonBuilder.MONTH:
            return 'Month '
            pass
        elif Xlabel == JsonBuilder.TIMESTAMP: # pass a string time_stamp not datetime
            return 'HH:MM'


    @staticmethod
    def datetime_validator(date):
        if isinstance(date, list) or isinstance(date, tuple):
            for dt in date:
                if not isinstance(dt, datetime.datetime):
                    return jsonify({'error': 'date must be of type datetime.datetime'}), 404
                    # raise TypeError('date must be of type datetime.datetime')

        else:
            if not isinstance(date, datetime.datetime):
                return jsonify({'error': 'date must be of type datetime.datetime'}), 404
                # raise TypeError('date must be of type datetime.datetime')

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
            return jsonify({'error': '"sensor_id must be an integer'}), 404
            # raise ValueError("sensor_id must be an integer")
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
                "ch_avg": float("{0:.2f}".format(data_obj.ch_avg))
            }
        else:  # for None
            return {
                "ch_max": (data_obj.ch_max),
                "ch_min": (data_obj.ch_min),
                "ch_avg": (data_obj.ch_avg)
            }

    @staticmethod
    def serialize_date(obj):
        """
        JSON serializer for datetime objects not serializable by default json code
        :param obj: a datetime.datetime object
        :return:
        """
        if isinstance(obj, datetime.datetime):
            serial = obj.strftime('%d/%b/%Y')
            return serial
        raise TypeError("Type not serializable")
    pass

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