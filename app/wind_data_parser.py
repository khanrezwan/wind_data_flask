__author__ = 'rezwan'
import os
import time
from app import db
from .models import File, RawData, Sensor, Logger, Site

#
# [5] Using SqlAlchemy version 0.8.4 read this tut http://www.blog.pythonlibrary.org/2012/07/01/a-simple-sqlalchemy-0-7-0-8-tutorial/
# http://docs.sqlalchemy.org/en/rel_0_8/orm/relationships.html#relationship-patterns
# [6] Regular expression to extract data from filename. import re then re.match('regex','input_string')
# re.match('regex','input_string').group(1) is serial 2 is year in order
# (?P<serial>\d\d\d\d)(?P<year>(?:19|20)\d\d)(?P<month>0[1-9]|1[012])(?P<day>0[1-9]|[12][0-9]|3[01])(?P<FileNo>\d*)(?P<extension>\.txt$)
# Following Reg ex ignores txt extension subject of testing
# (?P<serial>\d\d\d\d)(?P<year>(?:19|20)\d\d)(?P<month>0[1-9]|1[012])(?P<day>0[1-9]|[12][0-9]|3[01])(?P<FileNo>\d*)
#  http://www.pythoncentral.io/sqlalchemy-association-tables/
# Many to One supports cascade delete without sqllite Pragma foreign_key = ON support
#  matplotlib in virtualenv sudo apt-get build-dep python-matplotlib

#######################################################################################################################


class Parser(object):
    # CONST_class_names is a dictionary of type of objects and their attributes
    CONST_class_names = dict()
    Logger_list = list()
    Current_Logger = 0
    Site_list = list()
    Current_Site = 0
    Sensor_list = list()

    def __init__(self, file_list=list(), rawDataDirectory='Tester'):
        if not isinstance(file_list, list):
            raise TypeError("Expecting a list")
        if not isinstance(rawDataDirectory, str):
            raise TypeError("Expecting a string")
        self.file_list = file_list
        # self.base_dir = os.path.abspath(os.path.dirname(__file__))

        # self.rawDataDirectory = os.path.join(self.base_dir, rawDataDirectory)  # raw data file directory
        self.rawDataDirectory = rawDataDirectory # pass flask upload files config
        if self.file_list.__len__() == 0:
            for Files in os.listdir(self.rawDataDirectory):  # Iterate for all txt files in the directory
                if Files.endswith('.txt'):  # process files with .txt extension

                    self.file_list[self.file_list.__len__():] = [Files]  # insert it into the file list
            self.file_list.sort()  # Sort the file
        pass

    @staticmethod
    def init_static_vars():
        # Base.metadata.create_all(bind=engine)  # Create Table. if not exists
        Parser.Logger_list = db.session.query(Logger).all()  # Load existing loggers from loggers table
        # print Parser.Logger_list
        Parser.Site_list = db.session.query(Site).all()  # Load existing loggers from loggers table
        # print Parser.Site_list
        Parser.Current_Logger = 0
        Parser.Current_Site = 0
        Parser.CONST_class_names = {'Logger Information': 3, 'Site Information': 9, 'Sensor Information': 9}
        pass

    def parse(self):
        notprcoeesed_count = 0
        new_files_count = 0
        start_time = time.time()
        for filename in self.file_list:  # Loop through all txt files

            # fileopen = os.getcwd() + '/' + self.rawDataDirectory + '/' + filename  # open one file
            fileopen = os.path.join(self.rawDataDirectory, filename)
            # fileopen = self.rawDataDirectory + '/' + filename
            print 'processing ', filename
            f = File(filename)  # create an object of database file model
            if f.insert():  # if insertion in db is successful i.e. not processed before hand
                # File_list.append(f)
                new_files_count += 1
                inputFile = open(fileopen, mode='r') # open the file to read
                # lines to read variable initialized.
                # This variable is used track number of lines to be read in order to populate db model object
                lines_to_read = 0
                line = inputFile.readline()  # read a line
                classname = ''  # initialize the variable. it will hold db model class name to be created
                while line: # loop through the line. starts as string. becomes a list. reverts to string at the end of loop
                    line = line.strip('\r\n')  # Remove end tags. still a string
                    #print line
                    if line.startswith('-'):  # check if the line starts with '-'. Denotes start of a class object in the file
                        #print 'Create Class'
                        line = line.strip('-') # remove all occurrence of '-' to get the section / class name

                        if line in Parser.CONST_class_names:  # if the stripped line belongs to pre-defined class dictionary
                            lines_to_read = Parser.CONST_class_names.get(line)  # get succeeding number of lines for the attributes
                            classname = line  # get name of the class.
                            # print "lines to read " + str(lines_to_read) +" class name " + str(classname)
                        else:
                            lines_to_read = 0  # Not an object do not read subsequent lines. Should not be here.

                    else:
                        line = line.split('\t')  # Split the line along the tabs (field separator). line becomes a python list
                        #print line
                        if (line.__len__() == 1) and (line[0] == ''):  # Gap between object. blank line
                            # print 'Object gap'
                            pass  # do nothing. Ignore

                        elif (line.__len__() > 1) and (line.__len__() <= 2): # if there is two fields then it's an class object
                            # print 'Object start read next few lines' + str(line)
                            if lines_to_read > 0:
                                paramlist = list()  # create an empty list to append attributes
                                for i in range(0, lines_to_read):   # Loop for number of attribute for the particular class
                                    paramlist.insert(i, line[1]) # there are two fields line[0] is the name and line[1] is value
                                    line = inputFile.readline()  # read next lin. line is string
                                    line = line.strip('\r\n')  # remove end tags. line is string

                                    line = line.split('\t')  # split the line. line is python list

                                # print paramlist
                                Parser.object_factory(classname, paramlist, f)  # create an object

                        elif (line.__len__() > 2) and (line[0] != 'Date & Time Stamp'):  # getting raw data. ignore header
                            # print line, line.__len__(), Sensor_list.__len__()
                            RawData.assigndata(line, Parser.Sensor_list, f)  # process rawdata.

                        else:
                            # print 'only here for raw data header'
                            # print Sensor_list
                            pass

                        # print line, line.__len__()
                    line = inputFile.readline()  # read next line to continue the loop. line is string
                # print 'Logger list = ' + str(Logger_list.__len__()) + ' Site list = ' + str(Site_list.__len__()) + ' Sensor List =' \
                #       + str(Sensor_list.__len__())

                inputFile.close()  # end of file. close the file

                db.session.commit()  # commit db changes
            else:  # file has been processed before.
                notprcoeesed_count += 1

        db.session.commit()   # commit db changes
        return {'Time Taken': str(time.time()-start_time) + ' seconds', 'New Files Processed': new_files_count,
                'Files Already in Database': notprcoeesed_count}

    def cleanup(self):

        del Parser.Logger_list[:]  # clear list

        del Parser.Site_list[:]

        Parser.Current_Logger = 0
        Parser.Current_Site = 0
        # Parser.CONST_class_names = {'Logger Information': 3, 'Site Information': 9, 'Sensor Information': 9}
        for one_file in self.file_list:
            # path =
            try:
                os.remove(os.path.join(self.rawDataDirectory, one_file))
            except os.error:
                pass
            finally:
                pass
        del self.file_list[:]

        self.rawDataDirectory = ''

    @staticmethod
    def contains(List, Filter):
        """
            A downloaded helper function to searching a list of objects
             http://stackoverflow.com/questions/598398/searching-a-list-of-objects-in-python
        :param List: list to search
        :param Filter: lambda function with filter criteria
        :return: True if found. False if not
        """

        for x in List:
            if Filter(x):
                return True
        return False

    @staticmethod
    def object_factory(Classname, params, fileobj):
        """

        Creates object of a specific class
        :param Classname: Name of the class parsed from file
        :param params: Attributes of the object parsed from file
        :return: None
        """
        if not isinstance(Classname, str):
            raise TypeError("Expecting a string")
        if not isinstance(params, list):
            raise TypeError("Expecting a list")
        if not isinstance(fileobj, File):
            raise TypeError("Expecting a File from models.py")
        if Classname == 'Logger Information':
            # if the parameter number matches the predefined dictionary
            if params.__len__() == Parser.CONST_class_names.get(Classname):
                templogger = Logger(*params)  # create object of logger class
                if Parser.contains(Parser.Logger_list, lambda x: x.serial == templogger.serial):  # If already in database
                    # print 'Already in Logger list'
                    # mark it as current logger
                    Parser.Current_Logger = filter(lambda x: x.serial == templogger.serial, Parser.Logger_list).pop()
                    # complete the db logger to file relationship. This logger owns the current file
                    Parser.Current_Logger.files.extend([fileobj])
                # Populate the empty Sensor List from database, where current lgger id is the foreign key in sensors tables
                    Parser.Sensor_list = db.session.query(Sensor).filter(Sensor.fk_logger_id == Parser.Current_Logger.id).all()

                else:  # if not in database create new logger

                    if not templogger.insert():  # insert into database
                        raise Exception("Logger Database Insertion error")
                    del Parser.Sensor_list[:]  # empty the Sensor list. As new logger will have it's own set of sensors
                    Parser.Logger_list[Parser.Logger_list.__len__():] = [templogger]  # insert the logger into the in memory global list

                    Parser.Current_Logger = templogger  # Mark the newly inserted logger as current logger
                    # complete the db logger to file relationship. This logger owns the current file
                    Parser.Current_Logger.files.extend([fileobj])
                    # print current_Logger

        elif Classname == 'Site Information':
            # if the parameter number matches the predefined dictionary
            if params.__len__() == Parser.CONST_class_names.get(Classname):
                tempsite = Site(*params)  # create object of site class

                if Parser.contains(Parser.Site_list, lambda x: x._id == tempsite._id):   # If already in database
                    # print 'Already in Site list'
                    Parser.Current_Site = tempsite   # mark it as current Site
                    pass
                else:
                    # print tempsite

                    if not tempsite.insert():  # insert into database
                        raise Exception("Site Database Insertion error")
                    # del Logger_list[:]
                    Parser.Current_Site = tempsite
                    Parser.Current_Site.logger = Parser.Current_Logger
                    Parser.Site_list[Parser.Site_list.__len__():] = [tempsite]

        elif Classname == 'Sensor Information':
            if params.__len__() == Parser.CONST_class_names.get(Classname):
                if params[2] != 'No SCM Installed':
                    tempsensor = Sensor(*params)

                    if Parser.contains(Parser.Sensor_list, (lambda x: x.fk_logger_id == Parser.Current_Logger.id) and (lambda x: x.channel == tempsensor.channel)):
                        # print 'Already in Sensor list'
                        pass
                    else:
                        # print Sensor_list
                        if not tempsensor.insert():  # insert into database
                            raise Exception("Sensor Database Insertion error")

                        Parser.Sensor_list.append(tempsensor)
                        Parser.Current_Logger.sensors.extend(Parser.Sensor_list)
        else:
            print 'What r u doing here?'

# if __name__ == '__main__':
#     P = Parser(rawDataDirectory='May')
#     P.init_static_vars()
#     P.parse()
#
#     pass
