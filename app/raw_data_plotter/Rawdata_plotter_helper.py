import calendar
import datetime
from dateutil import rrule

# app specific import
from .. import db
from ..models import RawData

class Rawdata_plotter_helper(object):
    """
    Helper functions for querries on rawdata
    returns query object
    """
    @staticmethod
    def get_Data_Date_24Hr(date, sensor_id):
        if isinstance(date, datetime.datetime):
            try:
                sensor_id = int(sensor_id)
            except ValueError:
                raise ValueError('sensor_id must be an integer')
            query = RawData.query.filter(
                RawData.yearmonthdate_stamp == str(date.year) + str(date.month) + str(date.day),
                RawData.fk_sensor_id == sensor_id)
            # print query.count()
            return query
        else:
            raise TypeError('date must be of type datetime.datetime')
        pass

    @staticmethod
    def get_Data_Date_Single_Point(date, sensor_id):
        if isinstance(date, datetime.datetime):
            try:
                sensor_id = int(sensor_id)
            except ValueError:
                raise ValueError('sensor_id must be an integer')
            query = RawData.query.with_entities(db.func.avg(RawData.ch_min).label('ch_min'),
                                                db.func.avg(RawData.ch_max).label('ch_max'),
                                                db.func.avg(RawData.ch_avg).label('ch_avg')).\
                filter(RawData.yearmonthdate_stamp == str(date.year) + str(date.month) + str(date.day),
                       RawData.fk_sensor_id == sensor_id)
            print query.count()
            return query
        else:
            raise TypeError('date must be of type datetime.datetime')
        pass

    @staticmethod
    def get_Data_Date_Range_24Hr(startDate, endDate, sensor_id):
        if isinstance(startDate, datetime.datetime) and isinstance(endDate, datetime.datetime):
            try:
                sensor_id = int(sensor_id)
            except ValueError:
                raise ValueError('sensor_id must be an integer')
            start_date_param = str(startDate.year) + str(startDate.month) + str(startDate.day)
            end_date_param = str(endDate.year) + str(endDate.month) + str(endDate.day)

            query_distinct_time_stamps = RawData.query.with_entities(RawData.time_stamp.distinct().label('time_stamp')).filter(
                RawData.yearmonthdate_stamp >= start_date_param,
                RawData.yearmonthdate_stamp <= end_date_param,
                RawData.fk_sensor_id == sensor_id)
            query_list = list()
            for item in query_distinct_time_stamps.all():

                query_list.append(RawData.query.with_entities(db.func.avg(RawData.ch_min).label('ch_min'),
                                                              db.func.avg(RawData.ch_max).label('ch_max'),
                                                              db.func.avg(RawData.ch_avg).label('ch_avg'),
                                                              RawData.time_stamp.label('time_stamp')).filter(

                    RawData.yearmonthdate_stamp >= start_date_param,
                    RawData.yearmonthdate_stamp <= end_date_param,
                    RawData.fk_sensor_id == sensor_id,
                    RawData.time_stamp == item.time_stamp))
            # ToDo-Rezwan get average for a all dates date where time stamp == some particular time stamp
            # ToDo-Rezwan get a set of available time and run avg query
            # test code start
            for item in query_distinct_time_stamps.all():
                print item.time_stamp
            for res in query_list:
                print 'count ', res.count()
                print 'time', res.first().time_stamp
                print 'ch_max ', res.first().ch_max
                print 'ch_min ', res.first().ch_min
                print 'ch_avg ', res.first().ch_avg

            # test code end
            return query_list
        else:
            raise TypeError('date must be of type datetime.datetime')
        pass

    @staticmethod
    def get_Data_Date_Range_Single_Point(startDate, endDate, sensor_id):
        if isinstance(startDate, datetime.datetime) and isinstance(endDate, datetime.datetime):
            try:
                sensor_id = int(sensor_id)
            except ValueError:
                raise ValueError('sensor_id must be an integer')
            start_date_param = str(startDate.year) + str(startDate.month) + str(startDate.day)
            end_date_param = str(endDate.year) + str(endDate.month) + str(endDate.day)
            query = RawData.query.with_entities(db.func.avg(RawData.ch_min).label('ch_min'),
                                                db.func.avg(RawData.ch_max).label('ch_max'),
                                                db.func.avg(RawData.ch_avg).label('ch_avg')).\
                filter(
                RawData.yearmonthdate_stamp >= start_date_param,
                RawData.yearmonthdate_stamp <= end_date_param,
                RawData.fk_sensor_id == sensor_id)
           #test code start
            print 'count ', query.count()
            print 'ch_max ', query.first().ch_max
            print 'ch_min ', query.first().ch_min
            print 'ch_avg ', query.first().ch_avg
            #test code end
            return query
        else:
            raise TypeError('date must be of type datetime.datetime')
        pass

    @staticmethod
    def get_Data_Date_Range_Single_Point_for_each_Date(startDate, endDate, sensor_id):
        if isinstance(startDate, datetime.datetime) and isinstance(endDate, datetime.datetime):
            try:
                sensor_id = int(sensor_id)
            except ValueError:
                raise ValueError('sensor_id must be an integer')
            query_list = list()
            date_list = list()
            for dt in rrule.rrule(rrule.DAILY, dtstart=startDate,until=endDate):
                query = Rawdata_plotter_helper.get_Data_Date_Single_Point(dt,sensor_id)
                query_list.append(query)
                date_list.append(dt)
           #test code start
                print 'count ', query.count()
                print 'ch_max ', query.first().ch_max
                print 'ch_min ', query.first().ch_min
                print 'ch_avg ', query.first().ch_avg
            #test code end
            return query_list, date_list #ToDo dictionary or Tuple
        else:
            raise TypeError('date must be of type datetime.datetime')
        pass

    @staticmethod
    def get_Data_Month_Single_Point(date, sensor_id):
        if isinstance(date, datetime.datetime):
            try:
                sensor_id = int(sensor_id)
            except ValueError:
                raise ValueError('sensor_id must be an integer')

            (weekday_of_first_day_month, end_date_month) = calendar.monthrange(date.year, date.month)

            start_date = datetime.datetime(date.year, date.month, 1)
            print type(start_date)
            end_date = datetime.datetime(date.year, date.month, end_date_month)
            query = Rawdata_plotter_helper.get_Data_Date_Range_Single_Point(start_date, end_date, sensor_id)

           #test code start
            print 'count ', query.count()
            print 'ch_max ', query.first().ch_max
            print 'ch_min ', query.first().ch_min
            print 'ch_avg ', query.first().ch_avg
            #test code end
            return query
        else:
            raise TypeError('date must be of type datetime.datetime')
        pass

    @staticmethod
    def get_Data_Month_Range_Single_Point(startDate, endDate, sensor_id):  # single data point for all month
        if isinstance(startDate, datetime.datetime) and isinstance(endDate, datetime.datetime):
            try:
                sensor_id = int(sensor_id)
            except ValueError:
                raise ValueError('sensor_id must be an integer')
            (weekday_of_first_day_month, end_date_of_month) = calendar.monthrange(endDate.year, endDate.month)
            startDate = datetime.datetime(startDate.year, startDate.month, 1)
            endDate = datetime.datetime(endDate.year, endDate.month, end_date_of_month)
            query = Rawdata_plotter_helper.get_Data_Date_Range_Single_Point(startDate, endDate, sensor_id)

            #test code start
            print 'count ', query.count()
            print 'ch_max ', query.first().ch_max
            print 'ch_min ', query.first().ch_min
            print 'ch_avg ', query.first().ch_avg
            #test code end
            return query
        else:
            raise TypeError('date must be of type datetime.datetime')

        pass

    pass

    @staticmethod
    def get_Data_Month_Range_Single_Point_for_each_Month(startDate, endDate, sensor_id):  # single data point for each month
        if isinstance(startDate, datetime.datetime) and isinstance(endDate, datetime.datetime):
            try:
                sensor_id = int(sensor_id)
            except ValueError:
                raise ValueError('sensor_id must be an integer')
            startDate_query = datetime.datetime(startDate.year,startDate.month,1)
            # (weekday_of_first_day_month, end_Date_ofmonth) = calendar.monthrange(endDate.year, endDate.month)
            endDate_query = datetime.datetime(endDate.year, endDate.month, 1)
            # enddate_query = datetime.datetime(enddate.year,enddate.month)
            query_list = list()
            month_list = list()
            for dt in rrule.rrule(rrule.MONTHLY,dtstart=startDate_query,until=endDate_query):
                query_list.append(Rawdata_plotter_helper.get_Data_Month_Single_Point(dt,1))
                month_list.append(dt)


            return query_list, month_list  # Todo dictionary or tuple?
        else:
            raise TypeError('date must be of type datetime.datetime')

        pass

    pass