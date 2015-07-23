from datetime import datetime

from flask import render_template, session, redirect, url_for, request, flash, g, make_response, send_file, jsonify

from flask import current_app as app

import os
import json

import pygal

# App specific imports

from . import raw_data_plotter
from .forms import *

from .. import db
from ..models import *

Json_date_obj_pattern = '%Y-%m-%dT%H:%M:%S.%fZ'

def jsonify_date(obj):
    """
    JSON serializer for datetime objects not serializable by default json code
    :param obj:
    :return:
    """
    if isinstance(obj, datetime.datetime):
        serial = obj.isoformat()
        return serial
    raise TypeError("Type not serializable")


@raw_data_plotter.route('/getLoggers', methods=['Get'])
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


@raw_data_plotter.route('/getAvailableDates/<int:sensor_id>', methods=['Get'])
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
                'min_date': jsonify_date(date.first().min),
                'max_date': jsonify_date(date.first().max)

            })


@raw_data_plotter.route('/getPlotDataDate24Hr', methods=['Get'])
def get_Plot_Data_Date_24Hr():

    print request.query_string

    sensor_id = int(request.args.get('sensor_id'))
    date = request.args.get('date')
    date = '2015-05-1T20:34:05.787Z'
    try:
        date = datetime.datetime.strptime(date, Json_date_obj_pattern)
    except:
        return make_response(jsonify({'error': 'Not a Java Script Date object'}), 404)

    data_list = RawData.query.filter(RawData.yearmonthdate_stamp == str(date.year) + str(date.month) + str(date.day),
                                     RawData.fk_sensor_id == sensor_id)

    if data_list.count() == 0:
        return make_response(jsonify({'error': 'No Raw Data object found'}), 404)

    # RawData.query.with_entities(db.func.min(RawData.date_time).label('date')).filter(RawData.fk_sensor_id == sensor_id).first()
    else:
        return jsonify(
            {

                'dataList': [{'data': data.serialize()} for data in data_list.all()],
                'success': True
            })


@raw_data_plotter.route('/getPlotDataDateSinglePoint', methods=['Get'])
def get_Plot_Data_Date_Single_Point():

    sensor_id = request.args.get('sensor_id')
    date = request.args.get('date')
    date = '2015-05-1T20:34:05.787Z'

    sensor_id = 1
    try:
        date = datetime.datetime.strptime(date, Json_date_obj_pattern)
    except:
        return make_response(jsonify({'error': 'Not a Java Script Date object'}), 404)

    channel_data = RawData.query.with_entities(db.func.avg(RawData.ch_min).label('ch_min'),
                                               db.func.avg(RawData.ch_max).label('ch_max'),
                                               db.func.avg(RawData.ch_avg).label('ch_avg'))\
        .filter(
        RawData.yearmonthdate_stamp == str(date.year) + str(date.month) + str(date.day),
        RawData.fk_sensor_id == sensor_id)

    if (channel_data.first().ch_avg is None) or (channel_data.first().ch_max is None) or (channel_data.first().ch_min is None):
        return make_response(jsonify({'error': 'No data available for that date'}), 404)

    else:

        return jsonify({
            'ch_avg': "{0:.2f}".format(channel_data.first().ch_avg),
            'ch_max': "{0:.2f}".format(channel_data.first().ch_max),
            'ch_min': "{0:.2f}".format(channel_data.first().ch_min),
            'date': jsonify_date(date),
            'success': True
        })


@raw_data_plotter.route('/getPlotDataDateRange24Hr', methods=['Get'])
def get_Plot_Data_Date_Range_24Hr():
    return jsonify({

        'success': True,
    })


@raw_data_plotter.route('/getPlotDataDateRangeSinglePoint', methods=['Get'])
def get_Plot_Data_Date_Range_Single_Point():
    return jsonify({
        'success': True,
    })


@raw_data_plotter.route('/getPlotDataMonth24Hr', methods=['Get'])
def get_Plot_Data_Month_24Hr():
    return jsonify({
        'success': True,
    })


@raw_data_plotter.route('/getPlotDataMonthSinglePoint', methods=['Get'])
def get_Plot_Data_Month_Single_Point():
    return jsonify({
        'success': True,
    })



@raw_data_plotter.route('/', methods=['Get', 'Post'])
def query_test():
    form = RawDataForm()
    loggers = Logger.query.all()
    print loggers
    form.loggers.query = loggers
    # flash(str(request.args.get('month')))
    sensors = Sensor.query.all()
    print sensors
    form.sensors.query = sensors
    if request.method == 'POST' and form.validate_on_submit():
        sensor_id = form.sensors.data.id
        print 'logger id ', form.loggers.data.id
        month = int(form.month.data)
        print 'month ', month
        res = Sensor.query.filter(RawData.fk_sensor_id == sensor_id, RawData.month_stamp == month)
        print res.count()
        flash('Count ' + str(res.count()))
        return render_template('raw_data_plotter/query_tester.html', form=form)
    return render_template('raw_data_plotter/query_tester.html', form=form)
    pass


@raw_data_plotter.route('/test')
def ajs_test_1():

    return render_template('raw_data_plotter/query_tester.html')
    pass


@raw_data_plotter.route('/test_ret/<name>', methods=['Get'])
def ajs_test(name):  # Working Fine Testing Angular JS

    try:
        name = str(name)
    except ValueError:
        print 'Something'
    print name
    return jsonify({
        'success': True,
        'todoList': name
    })
    pass

@raw_data_plotter.route('/pygltest')
def pygl_test():
    bar_chart = pygal.Bar()
    bar_chart.title = "Remarquable sequences"
    bar_chart.x_labels = map(str, range(11))
    bar_chart.add('Fibonacci', [0, 1, 1, 2, 3, 5, 8, 13, 21, 34, 55])
    bar_chart.add('Padovan', [1, 1, 1, 2, 2, 3, 4, 5, 7, 9, 12])
    chart = bar_chart.render(is_unicode=True)

    results = RawData.query.filter(RawData.month_stamp == 5).distinct()
    #results = RawData.query.filter(datetime.datetime.strptime(RawData.date_time, '%Y-%m-%d %H:%M:%S.%f').month == endingdate.month).count()
    print type(results)
    print results.count()
    count = 0
    for res in results:
        if res.date_time.month == 5:
            # print res.filename
            count += 1
    print 'count ', count

    # return make_response(chart)
    return render_template('raw_data_plotter/index.html', chart=chart)
