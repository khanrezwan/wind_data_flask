import re
import datetime
from app import db
from sqlalchemy.engine import Engine
from sqlalchemy import event

############# Uncomment if using Sqlite##########################################################
# @event.listens_for(Engine, "connect")
# def set_sqlite_pragma(dbapi_connection, connection_record):
#     """
#      A function that listens to sqlite connection and turns on paragma foreign_key parameter to enforce cascade delete
#      and updates. passive delete will not work without this helper
#     :param dbapi_connection:
#     :param connection_record:
#     :return:
#     """
#
#     cursor = dbapi_connection.cursor()
#     cursor.execute("PRAGMA foreign_keys=ON")
#     cursor.close()
###################################################################################################



class SqlInterface(object):

    def search(self, *args):
        raise NotImplementedError("Implement")

    def insert(self, *args):
        raise NotImplementedError("Implement")

    def update(self, *args):
        raise NotImplementedError("Implement")

    def delete(self, *args):
        raise NotImplementedError("Implement")

    def batch_insert(self, *args):
        pass

###################################################################################################################
class RawData(db.Model):
    """
    sqlalchemy model for Rawdata
    It's an association table from many to many relationship between Sensor and File with additional data from the relation
    superclass : Base (sqlAlchemy)

    has foreign key from Sensor and File
    has many to many relationship with Sensor. backref('sensors_assoc') marks it as association
    has many to many relationship with File. backref('files_assoc') marks it as association
    """
    __tablename__ = 'rawdata'
    id = db.Column(db.Integer, primary_key=True)
    fk_filename = db.Column(db.String(256), db.ForeignKey("files.filename", ondelete="Cascade", onupdate="Cascade"), index=True)  # Foreign Key
    fk_sensor_id = db.Column(db.Integer, db.ForeignKey("sensors.id", ondelete="Cascade"), index=True)  # Foreign Key
    # Use date_time for MySQL/ Postgresql i.e. DBMS with built-in date time support.
    # datetime.datetime.strptime(RawData.date_time, '%Y-%m-%d %H:%M:%S.%f')
    date_time = db.Column(db.DateTime)  #
    # date stored as string yyyymmdd datetime.datetime.strptime(RawData.date, '%Y%m%d') for Sqlite3
    yearmonthdate_stamp = db.Column(db.String(64), index=True)
    date_stamp = db.Column(db.Integer)
    month_stamp = db.Column(db.Integer, index=True)
    year_stamp = db.Column(db.Integer)
     # time stored as HH:MM. datetime.datetime.strptime(RawData.date, '%H:%M')  for Sqlite3.
    time_stamp = db.Column(db.String(64), index=True)

    ch_avg = db.Column(db.Float, nullable=False)
    ch_sd = db.Column(db.Float, nullable=False)
    ch_max = db.Column(db.Float, nullable=False)
    ch_min = db.Column(db.Float, nullable=False)
    channel = db.relationship("Sensor", backref=db.backref('sensors_assoc'))
    filename = db.relationship("File", backref=db.backref('files_assoc'))

    def __repr__(self):
        return 'RawData file <%r> sensor <%r>' % (self.fk_filename, self.fk_sensor_id)

    def serialize(self):
        return {
            'id': self.id,
            'fk_filename': self.fk_filename,
            'fk_sensor_id': self.fk_sensor_id,
            'date_time': self.date_time.isoformat(),
            'ch_avg': self.ch_avg,
            'ch_sd': self.ch_sd,
            'ch_max': self.ch_max,
            'ch_min': self.ch_min
        }

    @staticmethod
    def assigndata(getdatalist, sensorlist, file_name):
        """
        This static function gets a Raw data line and assigns to appropriate channels
        :param getdatalist: List object with each field is a member of the list. Convention: 1st element is date time stamp
        then every four element belongs to a single channel. So, four 14 channels we have 4 * 14 = 56 elements after
        :param sensorlist: List of sensor objects parsed from file
        :param file_name: file object. The file currently being parsed
        :return: None
        """
        if not isinstance(getdatalist, list):
            raise TypeError("Expecting a list")
        else:
            for info in getdatalist:
                if not isinstance(info, str):
                    raise TypeError("Expecting String")
        if not isinstance(sensorlist, list):
            raise TypeError("Expecting a list")
        else:
            for sensor in sensorlist:
                if not isinstance(sensor, Sensor):
                    raise TypeError("Expecting String")
        if not isinstance(file_name, File):
            raise TypeError("Expecting File model")
        # ToDo-Rezwan older files had different timestamp...try both if both fails then catch exception. implemented subject to testing
        # if file_name.month_stamp > 3 and file_name.year_stamp <= 2015:  # date format in file changed from april
        try:
            date = datetime.datetime.strptime(getdatalist[0], '%d/%m/%Y %H:%M:%S')  # in dd/mm/yyyy HH (24hr):MM:SS
        except ValueError:
            print 'date ', getdatalist[0], ' filename', file_name.filename
            raise ValueError('unexpected date time in input file', )
        # else:
        #     try:
        #         date = datetime.datetime.strptime(getdatalist[0], '%m/%d/%Y %H:%M:%S')
        #     except ValueError:
        #         print 'date ', getdatalist[0], ' filename', file_name.filename
        #         raise ValueError('unexpected date time in input file')

        single_channel = list()  # empty list for raw data of single channel
        dataList = getdatalist[1:]  # datalist starts from second parameter as 1st one is datetime field
        dataList = [data for data in dataList if data != '']  # remove channels with blank data
        # print sensorlist.__len__()
        # print dataList.__len__()
        if dataList.__len__() != (sensorlist.__len__() * 4):
            raise ValueError("Raw data list length size mismatch")
        for j in range(0, sensorlist.__len__()):  # Iterate for all sensor in the list
            single_channel = dataList[0:4]  # 1st four items are for data for j-th channel
            dataList = dataList[4:]  # remove data of j-th from the list
            single_channel = [date] + single_channel  # add date time beginning of the data row of single channel
            # Create dictionary for named parameter of RawData constructor provided by sqlalchemy
            # Add the Foreign key of j-th Sensor and the file the raw data belongs
            raw = dict(date_time=single_channel[0],
                       yearmonthdate_stamp=str(date.year) + str(date.month) + str(date.day),
                       date_stamp=int(date.day), month_stamp=int(date.month), year_stamp=int(date.year),
                       time_stamp=str(date.hour) + ':' + str(date.minute),
                       ch_avg=float(single_channel[1]), ch_sd=float(single_channel[2]),
                       ch_max=float(single_channel[3]), ch_min=float(single_channel[4]),
                       channel=sensorlist[j], filename=file_name)
            db.session.add(RawData(**raw))  # **raw unpacks the dictionary as named parameter for the constructor


######################################################################################################################
class File(db.Model, SqlInterface):
    """
    sqlalchemy model for File
    superclass : Base (sqlAlchemy)
    implements interface: SqlInterface
    has foreign key from Logger
    has many to many relationship with Sensor. passive delete ensure cascading delete by DBMS

    """
    __tablename__ = 'files'
    filename = db.Column(db.String(128), primary_key=True, index=True)
    fileno = db.Column(db.Integer, nullable=True)
    site = db.Column(db.Integer, nullable=False)
    date = db.Column(db.Date, nullable=False)
    date_stamp = db.Column(db.Integer)
    month_stamp = db.Column(db.Integer)
    year_stamp = db.Column(db.Integer)
    fk_logger_id = db.Column(db.Integer, db.ForeignKey("loggers.id", ondelete="Cascade"))  # Foreign Key
    sensors = db.relationship("Sensor", secondary='rawdata', passive_deletes=True)  # many ro many relationship
    date_created = db.Column(db.DateTime, default=db.func.current_timestamp())
    date_modified = db.Column(db.DateTime, default=db.func.current_timestamp(), onupdate=db.func.current_timestamp())

    RegEx1 = '(?P<serial>\d\d\d\d)(?P<year>(?:19|20)\d\d)' \
             '(?P<month>0[1-9]|1[012])(?P<day>0[1-9]|[12][0-9]|3[01])(?P<FileNo>\d*)'
    RegEx2 = '(?P<serial>\d\d\d\d)(?P<year>(?:19|20)\d\d)(?P<month>0[1-9]|1[012])(?P<day>0[1-9]|[12][0-9]|3[01])' \
             '(?P<FileNo>\d*)(?P<extension>\.txt$)'


    def __init__(self, _filename='727820150330125'):
        Reg = re.match(File.RegEx1, _filename).groupdict()

        self.filename = _filename.strip('.txt')
        self.site = Reg['serial']
        self.date = datetime.date(int(Reg['year']), int(Reg['month']), int(Reg['day']))
        self.date_stamp = int(Reg['day'])
        self.month_stamp = int(Reg['month'])
        self.year_stamp = int(Reg['year'])
        self.fileno = int(Reg['FileNo'])

    def __repr__(self):
        return 'File name <%r> date <%r>' % (self.filename, self.date)

    def search(self, _filename):

        res = db.session.query(File).filter(File.filename == _filename)
        return res

    def insert(self):
        # print 'from INSERT ', self.search(self.filename).count()
        if self.search(self.filename).count() == 0:
            db.session.add(self)
            db.session.commit()
            return True
        else:
            print 'Record Exists filename'
            return False

    def update(self, *args):
        pass

    def delete(self, *args):
        pass


######################################################################################################################
class Site(db.Model, SqlInterface):
    """
     sqlalchemy model for Site
    superclass : Base (sqlAlchemy)
    implements interface: SqlInterface

    has 1 to 1 relationship with Logger. uselist = False enforces 1:1 relationship

    """
    __tablename__ = 'sites'
    _id = db.Column(db.Integer, primary_key=True, index=True)
    description = db.Column(db.String(256), nullable=False)
    projectCode = db.Column(db.String(64), nullable=False)
    location = db.Column(db.String(64))
    elevation = db.Column(db.String(128), nullable=False)
    latitude = db.Column(db.String(128), nullable=False)
    longitude = db.Column(db.String(128), nullable=False)
    timeOffset = db.Column(db.Float, nullable=False)
    # fk_logger_id = Column(Integer, ForeignKey("loggers.id", ondelete="Cascade"))
    logger = db.relationship("Logger", passive_deletes=True, backref=db.backref('sites', order_by=_id), uselist=False)
    date_created = db.Column(db.DateTime, default=db.func.current_timestamp())
    date_modified = db.Column(db.DateTime, default=db.func.current_timestamp(), onupdate=db.func.current_timestamp())


    def __init__(self, _id='7278', description='Cox', projectcode='60MW', projectdescription='New Project', location='',
                 elevation='000026', latitude='N 021.30.082', longitude='E 091.59.890', timeoffset='6'):
        self._id = int(_id)
        self.description = description
        self.projectCode = projectcode
        self.projectDescription = projectdescription
        self.location = location
        self.elevation = elevation
        latitude = latitude.replace('\xb0', ' deg')
        latitude = latitude.replace('\'', '')
        longitude = longitude.replace('\xb0', ' deg')
        longitude = longitude.replace('\'', '')
        self.latitude = latitude
        self.longitude = longitude
        self.timeOffset = float(timeoffset)

    def __repr__(self):
        return 'Site ID <%r> location <%r>' % (self._id, self.location)

    def search(self, _id):
        res = db.session.query(Site).filter(Site._id == _id)
        return res

    def insert(self):
        if self.search(self._id).count() == 0:
            # self.loggers = Logger_list
            db.session.add(self)
            db.session.commit()
            return True
        else:
            print 'Record Exists'
            return False

    def update(self, *args):
        pass

    def delete(self, *args):
        pass

######################################################################################################################
class Logger(db.Model, SqlInterface):
    """
        sqlalchemy model for Logger
        superclass : Base (sqlAlchemy)
        implements interface: SqlInterface
        has foreign key from Site
        has 1 to many relationship with Sensor. passive delete ensure cascading delete by DBMS
        has 1 to many relationship with File. passive delete ensure cascading delete by DBMS
    """
    __tablename__ = "loggers"
    id = db.Column(db.Integer, primary_key=True)
    model = db.Column(db.Integer, nullable=False)
    serial = db.Column(db.Integer, nullable=False, index=True)
    hw_rev = db.Column(db.String(64), nullable=False)
    fk_site_id = db.Column(db.Integer, db.ForeignKey("sites._id", ondelete="Cascade"))  # Foreign Key

    sensors = db.relationship("Sensor", passive_deletes=True, backref=db.backref("loggers", order_by=id))  # 1 to m relation
    files = db.relationship("File", passive_deletes=True, backref=db.backref("loggers", order_by=id))  # 1 to m relation

    date_created = db.Column(db.DateTime, default=db.func.current_timestamp())
    date_modified = db.Column(db.DateTime, default=db.func.current_timestamp(), onupdate=db.func.current_timestamp())

    def __init__(self, model='4941', serial='07278', hw_rev='034-035-057'):

        self.model = int(model)
        self.serial = int(serial)
        self.hw_rev = hw_rev

    def serialize(self):
        return {'id': self.id,
                'serial': self.serial,
                'hw_rev': self.hw_rev,
                'fk_site_id': self.fk_site_id
                }

    def __repr__(self):
        return 'Logger serial <%r>' % self.serial

    def search(self, _serial):
        res = db.session.query(Logger).filter(Logger.serial == _serial)
        return res

    def insert(self):
        if not self.search(self.serial).count():
            # print Site_list
            db.session.add(self)
            db.session.commit()
            return True
        else:
            print 'Record Exists'
            return False

    def update(self, *args):
        pass

    def delete(self, *args):
        pass


#####################################################################################################################
class Sensor(db.Model, SqlInterface):
    """
        sqlalchemy model for Sensor
        superclass : Base (sqlAlchemy)
        implements interface: SqlInterface
        has foreign key from Site
        has many to many relationship with File. passive delete ensure cascading delete by DBMS

    """
    __tablename__ = 'sensors'
    id = db.Column(db.Integer, primary_key=True)

    channel = db.Column(db.Integer, index=True)
    _type = db.Column(db.Integer, nullable=False)
    description = db.Column(db.String(256), nullable=False)
    details = db.Column(db.String(128), nullable=True)
    serialNo = db.Column(db.Integer, nullable=False)
    height = db.Column(db.Float, nullable=False)
    scaleFactor = db.Column(db.Float, nullable=False)
    offset = db.Column(db.Float, nullable=False)
    units = db.Column(db.String(64), nullable=False)
    fk_logger_id = db.Column(db.Integer, db.ForeignKey("loggers.id", ondelete="Cascade"),index=True)  #Foreign Key

    files = db.relationship('File', secondary='rawdata', passive_deletes=True)  # m:m relationship

    date_created = db.Column(db.DateTime, default=db.func.current_timestamp())
    date_modified = db.Column(db.DateTime, default=db.func.current_timestamp(), onupdate=db.func.current_timestamp())

    def __init__(self, channel='1', _type='1', description='NRG #40C Anem', details='', serialno='225300', height='110',
                 scalefactor='0.76', offset='0.34', units='m/s'):
        self.channel = int(channel)
        self._type = int(_type)
        self.description = description
        self.details = details
        self.serialNo = int(serialno)
        self.height = float(height)
        self.scaleFactor = float(scalefactor)
        self.offset = float(offset)
        self.units = units
        # datalist DateTime    CH1Avg	CH1SD	CH1Max	CH1Min
        self.data_list = list()

    def serialize(self):
        return {'id': self.id,
                'channel': self.channel,
                'description': self.description,
                'serialNo': self.serialNo,
                'height': self.height,
                'scaleFactor': self.scaleFactor,
                'offset': self.offset,
                'units': self.units,
                'fk_logger_id': self.fk_logger_id
                }

    def __repr__(self):
        return 'Sensor channel <%r> Description <%r>' % (self.channel, self.description)

    def add_data(self, date_time, ch_avg, ch_sd, ch_max, ch_min):

        tempch_avg = float(ch_avg)
        tempch_sd = float(ch_sd)
        tempch_max = float(ch_max)
        tempch_min = float(ch_min)
        templist = [date_time, tempch_avg, tempch_sd, tempch_max, tempch_min]
        self.data_list.append(templist)

    def print_data(self):

        for data in self.data_list:
            print data, self.channel

    def search(self, channel):
        res = db.session.query(Sensor).filter(Sensor.channel == channel)
        return res

    def insert(self):
        db.session.add(self)
        db.session.commit()
        return True

    def update(self, *args):
        pass

    def delete(self, *args):
        pass
#######################################################################################################################
from werkzeug.security import generate_password_hash, check_password_hash
from flask.ext.login import UserMixin
from app import login_manager

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class User(UserMixin, db.Model):
    __tablename__ = 'auth_user'
    id = db.Column(db.Integer, primary_key=True)

    # User Name
    username = db.Column(db.String(128), nullable=False, unique=True, index=True)
    # Identification Data: email & password
    email = db.Column(db.String(128), nullable=False,index=True)
    password_hash = db.Column(db.String(128), nullable=False)
    # Authorisation Data: role & status

    status = db.Column(db.SmallInteger, nullable=True)
    # New instance instantiation procedure
    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'))

    date_created = db.Column(db.DateTime, default=db.func.current_timestamp())
    date_modified = db.Column(db.DateTime, default=db.func.current_timestamp(), onupdate=db.func.current_timestamp())

    def __init__(self, username, email, password, role):
        self.username = username
        self.email = email
        self.password = password
        self.role = role

    def __repr__(self):
        return '<User %r>' % self.username

    @property
    def password(self):
        raise AttributeError('password is not a readable attribute')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

    def is_admin(self):
        query = Role.query.filter(Role.id == self.role_id).one()
        if query.name == 'admin':
            return True
        else:
            return False

    def get_current_user_role(self):
        query = Role.query.filter(Role.id == self.role_id).one()
        return str(query.name).lower()

##########################################################################
from flask.ext.login import AnonymousUserMixin


class AnonymousUser(AnonymousUserMixin):
    '''
        Added this to protect flask-admin blueprint
    '''
    def is_admin(self):
        return False

login_manager.anonymous_user = AnonymousUser


#############################################################################################################3333
class Role(db.Model):
    __tablename__ = 'roles'
    id = db.Column(db.Integer, primary_key=True)

    name = db.Column(db.String(64), unique=True)
    users = db.relationship('User', backref='role', lazy='dynamic')

    date_created = db.Column(db.DateTime, default=db.func.current_timestamp())
    date_modified = db.Column(db.DateTime, default=db.func.current_timestamp(), onupdate=db.func.current_timestamp())

    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return 'Role <%r>' % self.name
###################################################
