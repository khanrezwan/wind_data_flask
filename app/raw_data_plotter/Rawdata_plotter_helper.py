import calendar
import datetime
from dateutil import rrule

# app specific import
from .. import db
from ..models import RawData

dict_keys = ["query", "date", "sensor_id", "time_stamp"]  # Update this list if key in dictionary_builder changes

class Rawdata_plotter_helper(object):
    """
    Helper functions for querries on rawdata
    returns query object
    """

    @staticmethod
    def dictionary_builder(query, date=None, sensor_id=None, time_stamp=None):
        return {
            "query": query,
            "date": date,
            "sensor_id": sensor_id,
            "time_stamp": time_stamp
        }



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
            query_distinct_time_stamps = RawData.query.with_entities(RawData.time_stamp.distinct().label('time_stamp')).filter(
                RawData.yearmonthdate_stamp == str(date.year) + str(date.month) + str(date.day),
                RawData.fk_sensor_id == sensor_id)
            time_stamp_list = list()

            for item in query_distinct_time_stamps.all():
                time_stamp_list.append(item.time_stamp)
            # print query.count()
            # return query
            return Rawdata_plotter_helper.dictionary_builder(query, date=date, sensor_id=sensor_id,
                                                             time_stamp=time_stamp_list)
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
            # return query
            return Rawdata_plotter_helper.dictionary_builder(query, date=date, sensor_id=sensor_id)
        else:
            raise TypeError('date must be of type datetime.datetime')
        pass

    @staticmethod
    def get_Data_Date_Range_24Hr(startDate, endDate, sensor_id):
        if isinstance(startDate, datetime.datetime) and isinstance(endDate, datetime.datetime):
            if endDate >= startDate:
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
                time_stamp_list = list()
                for item in query_distinct_time_stamps.all():

                    query_list.append(RawData.query.with_entities(db.func.avg(RawData.ch_min).label('ch_min'),
                                                                  db.func.avg(RawData.ch_max).label('ch_max'),
                                                                  db.func.avg(RawData.ch_avg).label('ch_avg'),
                                                                  RawData.time_stamp.label('time_stamp')).filter(

                        RawData.yearmonthdate_stamp >= start_date_param,
                        RawData.yearmonthdate_stamp <= end_date_param,
                        RawData.fk_sensor_id == sensor_id,
                        RawData.time_stamp == item.time_stamp))
                    time_stamp_list.append(item.time_stamp)

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
                # return query_list
                return Rawdata_plotter_helper.dictionary_builder(query_list, date=(startDate, endDate),
                                                                 sensor_id=sensor_id, time_stamp=time_stamp_list)
            else:
                raise ValueError('End date must be greater than or equal to start date')
        else:
            raise TypeError('date must be of type datetime.datetime')
        pass

    @staticmethod
    def get_Data_Date_Range_Single_Point(startDate, endDate, sensor_id):
        if isinstance(startDate, datetime.datetime) and isinstance(endDate, datetime.datetime):
            if endDate >= startDate:
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
                # return query
                return Rawdata_plotter_helper.dictionary_builder(query, date=(startDate, endDate), sensor_id=sensor_id)
            else:
                raise ValueError('End date must be greater than or equal to start date')
        else:
            raise TypeError('date must be of type datetime.datetime')
        pass

    @staticmethod
    def get_Data_Date_Range_Single_Point_for_each_Date(startDate, endDate, sensor_id):
        if isinstance(startDate, datetime.datetime) and isinstance(endDate, datetime.datetime):
            if endDate >= startDate:
                try:
                    sensor_id = int(sensor_id)
                except ValueError:
                    raise ValueError('sensor_id must be an integer')
                query_list = list()
                date_list = list()
                for dt in rrule.rrule(rrule.DAILY, dtstart=startDate,until=endDate):
                    res = Rawdata_plotter_helper.get_Data_Date_Single_Point(dt, sensor_id)
                    query = res['query']
                    query_list.append(query)
                    date_list.append(dt)
               #test code start
                    print 'count ', query.count()
                    print 'ch_max ', query.first().ch_max
                    print 'ch_min ', query.first().ch_min
                    print 'ch_avg ', query.first().ch_avg
                #test code end
                # return query_list, date_list
                return Rawdata_plotter_helper.dictionary_builder(query_list, date=date_list, sensor_id=sensor_id)
            else:
                raise ValueError('End date must be greater than or equal to start date')
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
            res = Rawdata_plotter_helper.get_Data_Date_Range_Single_Point(start_date, end_date, sensor_id)
            query = res['query']
           #test code start
            print 'count ', query.count()
            print 'ch_max ', query.first().ch_max
            print 'ch_min ', query.first().ch_min
            print 'ch_avg ', query.first().ch_avg
            #test code end
            return Rawdata_plotter_helper.dictionary_builder(query, date=date, sensor_id=sensor_id)
        else:
            raise TypeError('date must be of type datetime.datetime')
        pass

    @staticmethod
    def get_Data_Month_Range_Single_Point(startDate, endDate, sensor_id):  # single data point for all month
        if isinstance(startDate, datetime.datetime) and isinstance(endDate, datetime.datetime):
            if endDate >= startDate:
                try:
                    sensor_id = int(sensor_id)
                except ValueError:
                    raise ValueError('sensor_id must be an integer')
                (weekday_of_first_day_month, end_date_of_month) = calendar.monthrange(endDate.year, endDate.month)
                startDate = datetime.datetime(startDate.year, startDate.month, 1)
                endDate = datetime.datetime(endDate.year, endDate.month, end_date_of_month)
                res = Rawdata_plotter_helper.get_Data_Date_Range_Single_Point(startDate, endDate, sensor_id)
                query = res['query']
                #test code start
                print 'count ', query.count()
                print 'ch_max ', query.first().ch_max
                print 'ch_min ', query.first().ch_min
                print 'ch_avg ', query.first().ch_avg
                #test code end
                # return query
                return Rawdata_plotter_helper.dictionary_builder(query, date=(startDate, endDate), sensor_id=sensor_id)
            else:
                raise ValueError('End date must be greater than or equal to start date')
        else:
            raise TypeError('date must be of type datetime.datetime')

        pass

    pass

    @staticmethod
    def get_Data_Month_Range_Single_Point_for_each_Month(startDate, endDate, sensor_id):  # single data point for each month
        if isinstance(startDate, datetime.datetime) and isinstance(endDate, datetime.datetime):
            if endDate >= startDate:
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
                    res = Rawdata_plotter_helper.get_Data_Month_Single_Point(dt, sensor_id)
                    query = res["query"]
                    query_list.append(query)
                    month_list.append(dt)

                # return query_list, month_list
                return Rawdata_plotter_helper.dictionary_builder(query_list, date=month_list, sensor_id=sensor_id)
            else:
                raise ValueError('End date must be greater than or equal to start date')
        else:
            raise TypeError('date must be of type datetime.datetime')

        pass

    # Todo-Rezwan Add Monthly 24 Hr view and Monthly 24 Hr view for a range

    @staticmethod
    def get_Data_Month_24Hr(date, sensor_id):
        if isinstance(date, datetime.datetime):
            try:
                sensor_id = int(sensor_id)
            except ValueError:
                raise ValueError('sensor_id must be an integer')

            (weekday_of_first_day_month, end_date_month) = calendar.monthrange(date.year, date.month)

            start_date = datetime.datetime(date.year, date.month, 1)
            # print type(start_date)
            end_date = datetime.datetime(date.year, date.month, end_date_month)
            res = Rawdata_plotter_helper.get_Data_Date_Range_24Hr(start_date, end_date, sensor_id)
            # print res
            query = res['query']
           # #test code start
           #  print 'count ', query.count()
           #  print 'ch_max ', query.first().ch_max
           #  print 'ch_min ', query.first().ch_min
           #  print 'ch_avg ', query.first().ch_avg
           #  #test code end]
            return res
        else:
            raise TypeError('date must be of type datetime.datetime')
        pass

    @staticmethod
    def get_Data_Month_Range_Single_Point_for_each_Day(startDate, endDate, sensor_id):

        # Todo call where startdate is 1st day stardate month and end date is last day of endday monthRawdata_plotter_helper.get_Data_Date_Range_Single_Point_for_each_Date()

        pass

    @staticmethod
    def get_Data_Month_Single_Point_for_each_Day(date, sensor_id):
        # Todo call where date is 1st day stardate month and end date is last day of date month Rawdata_plotter_helper.get_Data_Date_Range_Single_Point_for_each_Date()
        if isinstance(date, datetime.datetime):
            try:
                sensor_id = int(sensor_id)
            except ValueError:
                raise ValueError('sensor_id must be an integer')

            (weekday_of_first_day_month, end_date_month) = calendar.monthrange(date.year, date.month)

            start_date = datetime.datetime(date.year, date.month, 1)
            # print type(start_date)
            end_date = datetime.datetime(date.year, date.month, end_date_month)

            res = Rawdata_plotter_helper.get_Data_Date_Range_Single_Point_for_each_Date(start_date, end_date, sensor_id)
            # print res
            query = res['query']
           # #test code start
           #  print 'count ', query.count()
           #  print 'ch_max ', query.first().ch_max
           #  print 'ch_min ', query.first().ch_min
           #  print 'ch_avg ', query.first().ch_avg
           #  #test code end]
            return res
        else:
            raise TypeError('date must be of type datetime.datetime')
        pass
        pass

    @staticmethod
    def get_Data_Month_Range_24Hr(startDate, endDate, sensor_id):
        if isinstance(startDate, datetime.datetime) and isinstance(endDate, datetime.datetime):
            if endDate >= startDate:
                try:
                    sensor_id = int(sensor_id)
                except ValueError:
                    raise ValueError('sensor_id must be an integer')
                (weekday_of_first_day_month, end_date_month) = calendar.monthrange(endDate.year, endDate.month)

                start_date = datetime.datetime(startDate.year, startDate.month, 1)
                # print type(start_date)
                end_date = datetime.datetime(endDate.year, endDate.month, end_date_month)
                return Rawdata_plotter_helper.get_Data_Date_Range_24Hr(start_date, end_date, sensor_id)
            else:
                raise ValueError('End date must be greater than or equal to start date')
        else:
            raise TypeError('date must be of type datetime.datetime')

        pass

    pass

