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
        """
        This dictionary is built by each query functions and sent Json builder class for JSON response
        :param query: Flask-SqlAlchemy object may be a list or single object.
        @:type query: db.query
        :param date:  maybe list, tuple or single object
        @:type date: datetime.datetime
        :param sensor_id: Sensor ID
        @:type sensor_id: int
        :param time_stamp: defaults to None. it is used by 24hr queries. sends a list of strings..e.g. ['00:00', '00:10'...
        :return: returns a dictionary using the parameters
        """
        return {
            "query": query,
            "date": date,
            "sensor_id": sensor_id,
            "time_stamp": time_stamp
        }



    @staticmethod
    def get_Data_Date_24Hr(date, sensor_id):
        """
        queries for 24hr data for a particular date for a particular sensor.
        :param date: Date
        @:type date: datetime.datetime
        :param sensor_id: Sensor ID
        @:type sensor_id: int
        :return: returns a dict of query result, date (single datetime.datetime object), sensor_id (integer)
        and list of HH:MM strings
        """
        if isinstance(date, datetime.datetime):  # check if param date is python datetime object
            try:
                sensor_id = int(sensor_id)  # check if sensor_id is an integer
            except ValueError:
                raise ValueError('sensor_id must be an integer') # if fails raise Value error
            query = RawData.query.filter(
                RawData.yearmonthdate_stamp == str(date.year) + str(date.month) + str(date.day),
                RawData.fk_sensor_id == sensor_id)  # get data for all available data of date for sensor_id
            query_distinct_time_stamps = RawData.query.with_entities(RawData.time_stamp.distinct().label('time_stamp')).filter(
                RawData.yearmonthdate_stamp == str(date.year) + str(date.month) + str(date.day),
                RawData.fk_sensor_id == sensor_id)  # get distinct time_stamp for that date. reason you may not have data for all time intevals
            time_stamp_list = list()

            for item in query_distinct_time_stamps.all():  # create a list of time_stamps from query
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
        """
        queries for avg value for a senspr on a particular date
        :param date: Date
        @:type date: datetime.datetime
        :param sensor_id: Sensor ID
        @:type sensor_id: int
        :return: returns a dict of query result (single sqlalchemy object with count one), date (single datetime.datetime object), sensor_id (integer)
        """
        if isinstance(date, datetime.datetime):
            try:
                sensor_id = int(sensor_id)
            except ValueError:
                raise ValueError('sensor_id must be an integer')
            # query for avg need to use with_entities and sqlalchemy built in db function db.func.avg
            query = RawData.query.with_entities(db.func.avg(RawData.ch_min).label('ch_min'),
                                                db.func.avg(RawData.ch_max).label('ch_max'),
                                                db.func.avg(RawData.ch_avg).label('ch_avg')).\
                filter(RawData.yearmonthdate_stamp == str(date.year) + str(date.month) + str(date.day),
                       RawData.fk_sensor_id == sensor_id)

            return Rawdata_plotter_helper.dictionary_builder(query, date=date, sensor_id=sensor_id)
        else:
            raise TypeError('date must be of type datetime.datetime')
        pass

    @staticmethod
    def get_Data_Date_Range_24Hr(startDate, endDate, sensor_id):
        """
        queries for 24hr time_stamp view for a range of dates
        :param startDate: Start date
        @:type startDate: datetime.datetime
        :param endDate: End date
        @:type endDate: datetime.datetime
        :param sensor_id: Sensor id from database table
        @:type sensor_id: int
        :return: returns a dict of query result ( list of sqlalchemy query object with count one),
        date (tuple of datetime.datetime object), sensor_id (integer) and list of HH:MM strings
        """
        if isinstance(startDate, datetime.datetime) and isinstance(endDate, datetime.datetime):  # validate dates
            if endDate >= startDate:
                try:
                    sensor_id = int(sensor_id) # validate sensor_id
                except ValueError:
                    raise ValueError('sensor_id must be an integer')
                start_date_param = str(startDate.year) + str(startDate.month) + str(startDate.day)
                end_date_param = str(endDate.year) + str(endDate.month) + str(endDate.day)
                # first find all the distinct time_stamp for the sensor_id between start_date and end_date
                query_distinct_time_stamps = RawData.query.with_entities(RawData.time_stamp.distinct().label('time_stamp')).filter(
                    RawData.yearmonthdate_stamp >= start_date_param,
                    RawData.yearmonthdate_stamp <= end_date_param,
                    RawData.fk_sensor_id == sensor_id)
                query_list = list()  # initialize empty list
                time_stamp_list = list()  # initialize empty list
                for item in query_distinct_time_stamps.all():
                    # now get average of all data for the sensor_id between date range for one time_stamp
                    # and append to query_list
                    query_list.append(RawData.query.with_entities(db.func.avg(RawData.ch_min).label('ch_min'),
                                                                  db.func.avg(RawData.ch_max).label('ch_max'),
                                                                  db.func.avg(RawData.ch_avg).label('ch_avg'),
                                                                  RawData.time_stamp.label('time_stamp')).filter(

                        RawData.yearmonthdate_stamp >= start_date_param,
                        RawData.yearmonthdate_stamp <= end_date_param,
                        RawData.fk_sensor_id == sensor_id,
                        RawData.time_stamp == item.time_stamp))
                    # append the one time_stamp to time_stamp_list
                    time_stamp_list.append(item.time_stamp)

                # test code start
                # for item in query_distinct_time_stamps.all():
                #     print item.time_stamp
                # for res in query_list:
                #     print 'count ', res.count()
                #     print 'time', res.first().time_stamp
                #     print 'ch_max ', res.first().ch_max
                #     print 'ch_min ', res.first().ch_min
                #     print 'ch_avg ', res.first().ch_avg

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
        """
        Queries for avg value between two dates
        :param startDate: Start date
        @:type startDate: datetime.datetime
        :param endDate: End date
        @:type endDate: datetime.datetime
        :param sensor_id: Sensor id from database table
        @:type sensor_id: int
        :return: returns a dict of query result ( sqlalchemy query object with count one),
        date (tuple of datetime.datetime object), sensor_id (integer)
        """
        if isinstance(startDate, datetime.datetime) and isinstance(endDate, datetime.datetime):
            if endDate >= startDate:
                try:
                    sensor_id = int(sensor_id)
                except ValueError:
                    raise ValueError('sensor_id must be an integer')
                # build strings for RawData.yearmonthdate_stamp field from startDate and end endDate
                start_date_param = str(startDate.year) + str(startDate.month) + str(startDate.day)
                end_date_param = str(endDate.year) + str(endDate.month) + str(endDate.day)
                # now get average of all data for the sensor_id between date range
                query = RawData.query.with_entities(db.func.avg(RawData.ch_min).label('ch_min'),
                                                    db.func.avg(RawData.ch_max).label('ch_max'),
                                                    db.func.avg(RawData.ch_avg).label('ch_avg')).\
                    filter(
                    RawData.yearmonthdate_stamp >= start_date_param,
                    RawData.yearmonthdate_stamp <= end_date_param,
                    RawData.fk_sensor_id == sensor_id)
               # #test code start
               #  print 'count ', query.count()
               #  print 'ch_max ', query.first().ch_max
               #  print 'ch_min ', query.first().ch_min
               #  print 'ch_avg ', query.first().ch_avg
               #  #test code end
               #  # return query
                return Rawdata_plotter_helper.dictionary_builder(query, date=(startDate, endDate), sensor_id=sensor_id)
            else:
                raise ValueError('End date must be greater than or equal to start date')
        else:
            raise TypeError('date must be of type datetime.datetime')
        pass

    @staticmethod
    def get_Data_Date_Range_Single_Point_for_each_Date(startDate, endDate, sensor_id):
        """
        Queries for avg value between two dates shows average for each date between range
        :param startDate: Start date
        @:type startDate: datetime.datetime
        :param endDate: End date
        @:type endDate: datetime.datetime
        :param sensor_id: Sensor id from database table
        @:type sensor_id: int
        :return: returns a dict of query result ( list of sqlalchemy query object each with count one),
        date (list of datetime.datetime object), sensor_id (integer)
        """
        if isinstance(startDate, datetime.datetime) and isinstance(endDate, datetime.datetime):  # validate dates data type
            if endDate >= startDate:  # validate dates value
                try:
                    sensor_id = int(sensor_id) # validate sensor data type
                except ValueError:
                    raise ValueError('sensor_id must be an integer')
                query_list = list()  # initilize empty list
                date_list = list() # initilize empty list
                # loop for each date between the date range using dateutil.rrule function
                for dt in rrule.rrule(rrule.DAILY, dtstart=startDate, until=endDate):
                    res = Rawdata_plotter_helper.get_Data_Date_Single_Point(dt, sensor_id)
                    query = res['query']
                    query_list.append(query)
                    date_list.append(dt)
               # #test code start
               #      print 'count ', query.count()
               #      print 'ch_max ', query.first().ch_max
               #      print 'ch_min ', query.first().ch_min
               #      print 'ch_avg ', query.first().ch_avg
               #  #test code end
               #  # return query_list, date_list
                return Rawdata_plotter_helper.dictionary_builder(query_list, date=date_list, sensor_id=sensor_id)
            else:
                raise ValueError('End date must be greater than or equal to start date')
        else:
            raise TypeError('date must be of type datetime.datetime')
        pass

    @staticmethod
    def get_Data_Month_Single_Point(date, sensor_id):
        """
        Queries for avg value for a single month
        :param date: Date
        @:type date: datetime.datetime
        :param sensor_id: Sensor id from database table
        @:type sensor_id: int
        :return: returns a dict of query result ( sqlalchemy query object with count one),
        date (datetime.datetime object), sensor_id (integer)
        """
        if isinstance(date, datetime.datetime):
            try:
                sensor_id = int(sensor_id)
            except ValueError:
                raise ValueError('sensor_id must be an integer')
            # get last day of a month
            (weekday_of_first_day_month, end_date_month) = calendar.monthrange(date.year, date.month)
            # build start date of a month
            start_date = datetime.datetime(date.year, date.month, 1)
            # build end end date of a month
            end_date = datetime.datetime(date.year, date.month, end_date_month)
            res = Rawdata_plotter_helper.get_Data_Date_Range_Single_Point(start_date, end_date, sensor_id)
            query = res['query'] # get result from the dictionary returned by the Rawdata_plotter_helper.get_Data_Date_Range_Single_Point function
           # #test code start
           #  print 'count ', query.count()
           #  print 'ch_max ', query.first().ch_max
           #  print 'ch_min ', query.first().ch_min
           #  print 'ch_avg ', query.first().ch_avg
           #  #test code end
            return Rawdata_plotter_helper.dictionary_builder(query, date=date, sensor_id=sensor_id)
        else:
            raise TypeError('date must be of type datetime.datetime')
        pass

    @staticmethod
    def get_Data_Month_Range_Single_Point(startDate, endDate, sensor_id):  # single data point for all month
        """
        Queries for avg value between months returns total average
        :param startDate: Start date
        @:type startDate: datetime.datetime
        :param endDate: End date
        @:type endDate: datetime.datetime
        :param sensor_id: Sensor id from database table
        @:type sensor_id: int
        :return: returns a dict of query result ( sqlalchemy query object with count one),
        date (tuple datetime.datetime object), sensor_id (integer)
        """
        if isinstance(startDate, datetime.datetime) and isinstance(endDate, datetime.datetime):
            if endDate >= startDate:
                try:
                    sensor_id = int(sensor_id)
                except ValueError:
                    raise ValueError('sensor_id must be an integer')
                # get last day of a month
                (weekday_of_first_day_month, end_date_of_month) = calendar.monthrange(endDate.year, endDate.month)
                # build start date of a month
                startDate = datetime.datetime(startDate.year, startDate.month, 1)
                # build end end date of a month
                endDate = datetime.datetime(endDate.year, endDate.month, end_date_of_month)
                res = Rawdata_plotter_helper.get_Data_Date_Range_Single_Point(startDate, endDate, sensor_id)
                query = res['query'] # get result from the dictionary returned by the Rawdata_plotter_helper.get_Data_Date_Range_Single_Point function
                # #test code start
                # print 'count ', query.count()
                # print 'ch_max ', query.first().ch_max
                # print 'ch_min ', query.first().ch_min
                # print 'ch_avg ', query.first().ch_avg
                # #test code end
                # # return query
                return Rawdata_plotter_helper.dictionary_builder(query, date=(startDate, endDate), sensor_id=sensor_id)
            else:
                raise ValueError('End date must be greater than or equal to start date')
        else:
            raise TypeError('date must be of type datetime.datetime')

        pass

    pass

    @staticmethod
    def get_Data_Month_Range_Single_Point_for_each_Month(startDate, endDate, sensor_id):  # single data point for each month
        """
        Queries for avg value between two months shows average for each month between range
        :param startDate: Start date
        @:type startDate: datetime.datetime
        :param endDate: End date
        @:type endDate: datetime.datetime
        :param sensor_id: Sensor id from database table
        @:type sensor_id: int
        :return: returns a dict of query result ( list of sqlalchemy query object each with count one),
        date (list of datetime.datetime object), sensor_id (integer)
        """
        if isinstance(startDate, datetime.datetime) and isinstance(endDate, datetime.datetime):
            if endDate >= startDate:
                try:
                    sensor_id = int(sensor_id)
                except ValueError:
                    raise ValueError('sensor_id must be an integer')
                startDate_query = datetime.datetime(startDate.year, startDate.month, 1)  # first day of month for startDate

                endDate_query = datetime.datetime(endDate.year, endDate.month, 1)  # first day of month for endtDate

                query_list = list()
                month_list = list()
                # loop for each month between the date range using dateutil.rrule function
                for dt in rrule.rrule(rrule.MONTHLY, dtstart=startDate_query, until=endDate_query):
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



    @staticmethod
    def get_Data_Month_24Hr(date, sensor_id):
        """
        queries for 24hr data for a particular month for a particular sensor.
        :param date: Date
        @:type date: datetime.datetime
        :param sensor_id: Sensor ID
        @:type sensor_id: int
        :return: returns a dict of same as Rawdata_plotter_helper.get_Data_Date_Range_24Hr(start_date, end_date, sensor_id)
        """
        if isinstance(date, datetime.datetime):
            try:
                sensor_id = int(sensor_id)
            except ValueError:
                raise ValueError('sensor_id must be an integer')

            (weekday_of_first_day_month, end_date_month) = calendar.monthrange(date.year, date.month)

            start_date = datetime.datetime(date.year, date.month, 1)

            end_date = datetime.datetime(date.year, date.month, end_date_month)
            res = Rawdata_plotter_helper.get_Data_Date_Range_24Hr(start_date, end_date, sensor_id)

            # query = res['query']
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
        raise NotImplementedError('Do we need this?')
        # Todo call where startdate is 1st day stardate month and end date is last day of endday monthRawdata_plotter_helper.get_Data_Date_Range_Single_Point_for_each_Date()
        # ToDo do we need this?
        pass

    @staticmethod
    def get_Data_Month_Single_Point_for_each_Day(date, sensor_id):
        """
        Queries for avg value for a month returns average for each date between start and end date of a month.
        :param date: Date
        @:type date: datetime.datetime
        :param sensor_id: Sensor ID
        @:type sensor_id: int
        :return: returns a dict of same as Rawdata_plotter_helper.get_Data_Date_Range_Single_Point_for_each_Date
        """

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
            # query = res['query']
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
        """
        queries for 24hr time_stamp view for a range of months
        :param startDate: Start date
        @:type startDate: datetime.datetime
        :param endDate: End date
        @:type endDate: datetime.datetime
        :param sensor_id: Sensor id from database table
        @:type sensor_id: int
        :return: returns a dict of query result ( list of sqlalchemy query object each with count one),
        date (tuple of datetime.datetime object), sensor_id (integer) and list of HH:MM strings
        """
        if isinstance(startDate, datetime.datetime) and isinstance(endDate, datetime.datetime):
            if endDate >= startDate:
                try:
                    sensor_id = int(sensor_id)
                except ValueError:
                    raise ValueError('sensor_id must be an integer')
                (weekday_of_first_day_month, end_date_month) = calendar.monthrange(endDate.year, endDate.month)

                start_date = datetime.datetime(startDate.year, startDate.month, 1)

                end_date = datetime.datetime(endDate.year, endDate.month, end_date_month)
                return Rawdata_plotter_helper.get_Data_Date_Range_24Hr(start_date, end_date, sensor_id)
            else:
                raise ValueError('End date must be greater than or equal to start date')
        else:
            raise TypeError('date must be of type datetime.datetime')

        pass

    pass

# todo add comparison functions