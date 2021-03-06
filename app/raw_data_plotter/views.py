from datetime import datetime
from dateutil import rrule
from flask import render_template, request, make_response, jsonify

from flask.ext.login import login_required

# App specific imports

from . import raw_data_plotter
from .forms import *
from .Rawdata_plotter_helper import Rawdata_plotter_helper
from .. import db
from ..models import *
from .json_builder import JsonBuilder

Json_date_obj_pattern = '%Y-%m-%dT%H:%M:%S.%fZ'


@raw_data_plotter.route('/test')
# Testing Rawdata_plotter helper class
def class_tester():
    # query = Rawdata_plotter_helper.get_Data_Date_Single_Point(datetime.datetime(2015, 6, 22), 1)
    # query =Rawdata_plotter_helper.get_Data_Month_Range_24Hr(datetime.datetime(2015, 5, 1), datetime.datetime(2015, 6, 1), 1)
    query = Rawdata_plotter_helper.get_Data_Date_Range_Single_Point_for_each_Date(datetime.datetime(2015, 6, 1),
                                                                                  datetime.datetime(2015, 6, 30), 1)
    # query = Rawdata_plotter_helper.get_Data_Month_Range_Single_Point_for_each_Month(datetime.datetime(2015, 4, 1), datetime.datetime(2015, 7, 20), 1)
    # query = Rawdata_plotter_helper.get_Data_Date_24Hr(datetime.datetime(2015, 5, 1), 1)
    # JsonBuilder.json_response(query, Xlabel=JsonBuilder.TIMESTAMP)
    (response, code) = JsonBuilder.json_response(query, Xlabel=JsonBuilder.DATE)
    return make_response(response, code)


def string_to_boolean(obj):
    if obj == 'true':
        return True
    elif obj == 'false':
        return False
    else:
        raise ValueError('Did not receive \'true\' or \'false\'')


@raw_data_plotter.route('/ngQueries', methods=['Get'])
@login_required
def get_ng_params():
    """
    This is the main route where angular JS will send query string
    :return: JSON data with response code
    """
    # print request.query_string
    try:
        sensor_id = int(request.args.get('sensor_id'))
    except TypeError:
        return make_response(jsonify({'error': 'sensor id must be an integer'}), 404)
    start_date = request.args.get('start_date')
    end_date = request.args.get('end_date')
    by_month = (request.args.get('by_month'))
    if by_month:
        by_month = string_to_boolean(by_month)
    by_date = (request.args.get('by_date'))
    if by_date:
        by_date = string_to_boolean(by_date)
    # by_range = (request.args.get('by_range'))
    by_timestamp = (request.args.get('by_timestamp'))
    if by_timestamp:
        by_timestamp = string_to_boolean(by_timestamp)
    show_individual_date_or_month = (request.args.get('show_individual_date_or_month'))
    if show_individual_date_or_month:
        show_individual_date_or_month = string_to_boolean(show_individual_date_or_month)
    response = jsonify({'error': 'Did not route to any cases'})
    code = 404
    try:
        start_date = datetime.datetime.strptime(start_date, Json_date_obj_pattern)  # There must be at least one Date
        if end_date:  # enddate may be None
            end_date = datetime.datetime.strptime(end_date, Json_date_obj_pattern)
    except ValueError:
        return make_response(jsonify({'error': 'Not a Java Script Date object'}), 404)

    # routing start

    if not end_date:
        if by_date is True:  # Routing Single date cases
            if by_timestamp is True:
                print 'routing get_Data_Date_24Hr'
                helper_dict = Rawdata_plotter_helper.get_Data_Date_24Hr(start_date, sensor_id)
                (response, code) = JsonBuilder.json_response(helper_dict, Xlabel=JsonBuilder.DATE)
            elif by_timestamp is False:
                print 'routing get_Data_Date_Single_Point'
                helper_dict = Rawdata_plotter_helper.get_Data_Date_Single_Point(start_date, sensor_id)
                (response, code) = JsonBuilder.json_response(helper_dict, Xlabel=JsonBuilder.DATE)
            else:
                return make_response(jsonify({'error': 'invalid choice combination'}), 404)
        elif by_month is True:  # Routing Single month cases
            if by_timestamp is False:
                if show_individual_date_or_month is True:
                    print 'routing get_Data_Month_Single_Point_for_each_Day'
                    helper_dict = Rawdata_plotter_helper.get_Data_Month_Single_Point_for_each_Day(start_date, sensor_id)
                    (response, code) = JsonBuilder.json_response(helper_dict, Xlabel=JsonBuilder.DATE)

                elif show_individual_date_or_month is False:
                    print 'routing get_Data_Month_Single_Point'
                    helper_dict = Rawdata_plotter_helper.get_Data_Month_Single_Point(start_date, sensor_id)
                    (response, code) = JsonBuilder.json_response(helper_dict, Xlabel=JsonBuilder.MONTH)
            elif by_timestamp is True:
                print 'routing get_Data_Month_24Hr'
                helper_dict = Rawdata_plotter_helper.get_Data_Month_24Hr(start_date, sensor_id)
                (response, code) = JsonBuilder.json_response(helper_dict, Xlabel=JsonBuilder.MONTH)

            else:
                return make_response(jsonify({'error': 'invalid choice combination'}), 404)
        else:
            return make_response(jsonify({'error': 'invalid choice combination'}), 404)

    elif start_date and end_date and (end_date >= start_date):
        if by_date is True:  # Routing date range cases
            if by_timestamp is False:
                if show_individual_date_or_month is True:
                    print 'routing get_Data_Date_Range_Single_Point_for_each_Date'
                    helper_dict = Rawdata_plotter_helper.get_Data_Date_Range_Single_Point_for_each_Date(start_date,
                                                                                                        end_date,
                                                                                                        sensor_id)
                    (response, code) = JsonBuilder.json_response(helper_dict, Xlabel=JsonBuilder.DATE)
                elif show_individual_date_or_month is False:
                    print 'routing get_Data_Date_Range_Single_Point'
                    helper_dict = Rawdata_plotter_helper.get_Data_Date_Range_Single_Point(start_date, end_date,
                                                                                          sensor_id)
                    (response, code) = JsonBuilder.json_response(helper_dict, Xlabel=JsonBuilder.DATE)
                else:
                    return make_response(jsonify({'error': 'invalid choice combination'}), 404)
            elif by_timestamp is True:
                print 'routing get_Data_Date_Range_24Hr'
                helper_dict = Rawdata_plotter_helper.get_Data_Date_Range_24Hr(start_date, end_date, sensor_id)
                (response, code) = JsonBuilder.json_response(helper_dict, Xlabel=JsonBuilder.DATE)
            else:
                return make_response(jsonify({'error': 'invalid choice combination'}), 404)
        elif by_month is True:  # Routing month range cases
            if by_timestamp is False:
                if show_individual_date_or_month is True:
                    print 'routing .get_Data_Month_Range_Single_Point_for_each_Month'
                    helper_dict = Rawdata_plotter_helper.get_Data_Month_Range_Single_Point_for_each_Month(start_date,
                                                                                                          end_date,
                                                                                                          sensor_id)
                    (response, code) = JsonBuilder.json_response(helper_dict, Xlabel=JsonBuilder.MONTH)
                elif show_individual_date_or_month is False:
                    print 'routing .get_Data_Month_Range_Single_Point'
                    helper_dict = Rawdata_plotter_helper.get_Data_Month_Range_Single_Point(start_date, end_date,
                                                                                           sensor_id)
                    (response, code) = JsonBuilder.json_response(helper_dict, Xlabel=JsonBuilder.MONTH)
                else:
                    return make_response(jsonify({'error': 'invalid choice combination'}), 404)
            elif by_timestamp is True:
                print 'routing get_Data_Month_Range_24Hr'
                helper_dict = Rawdata_plotter_helper.get_Data_Month_Range_24Hr(start_date, end_date, sensor_id)
                (response, code) = JsonBuilder.json_response(helper_dict, Xlabel=JsonBuilder.MONTH)
            else:
                return make_response(jsonify({'error': 'invalid choice combination'}), 404)

    else:
        return make_response(jsonify({'error': 'invalid choice combination'}), 404)
    return make_response(response, code)

    pass


@raw_data_plotter.route('/getLoggers', methods=['Get'])
@login_required
def get_loggers():
    logger_list = Logger.query
    if logger_list.count() == 0:
        return make_response(jsonify({'error': 'No Logger in database'}), 404)
    else:
        return jsonify(
            {
                'success': True,
                'loggerList': [{'logger': logger.serialize()} for logger in logger_list.all()]
            })


@raw_data_plotter.route('/getSensors/<int:logger_id>', methods=['Get'])
@login_required
def get_sensors(logger_id):
    try:
        logger_id = int(logger_id)
    except ValueError:
        return make_response(jsonify({'error': 'Logger id must be an integer'}), 404)
    sensor_list = Sensor.query.filter(Sensor.fk_logger_id == logger_id)
    if sensor_list.count() == 0:
        return make_response(jsonify({'error': 'No Sensor found for the logger'}), 404)
    else:
        return jsonify(
            {
                'success': True,
                'sensorList': [{'sensor': sensor.serialize()} for sensor in sensor_list.all()]
            })


@raw_data_plotter.route('/getSensorDetails/<int:sensor_id>', methods=['Get'])
@login_required
def get_sensor_details(sensor_id):
    try:
        sensor_id = int(sensor_id)
    except ValueError:
        return make_response(jsonify({'error': 'Sensor id must be an integer'}), 404)

    query = Sensor.query.filter(Sensor.id == sensor_id)
    if query.count() == 0:
        return make_response(jsonify({'error': 'No Sensor found'}), 404)
    else:
        return jsonify(
            {
                'success': True,
                'sensor': query.first().serialize()
            })


@raw_data_plotter.route('/getAvailableDates/<int:sensor_id>', methods=['Get'])
@login_required
def get_sensors_available_dates(sensor_id):
    try:
        sensor_id = int(sensor_id)
    except ValueError:
        return make_response(jsonify({'error': 'sensor id must be an integer'}), 404)
    date = RawData.query.with_entities(db.func.min(RawData.date_time).label('min'),
                                       db.func.max(RawData.date_time).label('max'))\
        .filter(RawData.fk_sensor_id == sensor_id)
    # max_date = RawData.query.with_entities(db.func.max(RawData.date_time).label('date')).filter(RawData.fk_sensor_id == sensor_id).first()
    # min_date = db.session.query(db.func.min(RawData.date_time).label('min_date')).filter(RawData.fk_sensor_id == sensor_id).first() ## same effect
    if (date.first().min is None) or (date.first().max is None):
        return make_response(jsonify({'error': 'No dates found for the sensor'}), 404)
    else:
        return jsonify(
            {
                'success': True,
                'min_date': JsonBuilder.serialize_date(date.first().min),
                'max_date': JsonBuilder.serialize_date(date.first().max)

            })


@raw_data_plotter.route('/test_strings', methods=['Get'])
def testing_query():
    # print request.query_string
    date = (request.args.get('date'))
    if date:
        date = string_to_boolean(date)
    # print date
    return make_response(jsonify({'success': True}), 200)


@raw_data_plotter.route('/', methods=['Get'])
@login_required
def index():
    return render_template('raw_data_plotter/index.html')
