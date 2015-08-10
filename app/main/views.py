# Library Imports
from datetime import datetime
from flask import render_template, session, redirect, url_for, request, flash, g
from flask.ext.login import login_required, current_user
# from werkzeug import check_password_hash, generate_password_hash
from flask import current_app as app
from werkzeug import secure_filename
import os
# App specific imports

from . import main
from .forms import *
from ..raw_data_plotter.Rawdata_plotter_helper import Rawdata_plotter_helper

from .. import db
from ..models import *
from ..wind_data_parser import Parser
from ..decorators import base_page_dictionary_builder, requires_roles


def build_logged_in_gist_view():
    date = RawData.query.with_entities(db.func.min(RawData.date_time).label('min'),
                                       db.func.max(RawData.date_time).label('max'))\
        .filter(RawData.fk_sensor_id == 1)
    # max_date = RawData.query.with_entities(db.func.max(RawData.date_time).label('date')).filter(RawData.fk_sensor_id == sensor_id).first()
    # min_date = db.session.query(db.func.min(RawData.date_time).label('min_date')).filter(RawData.fk_sensor_id == sensor_id).first() ## same effect
    if (date.first().min is None) or (date.first().max is None):
        return dict()
    latest_date = date.first().max
    earliest_date = date.first().min
    ch1_avg_query = Rawdata_plotter_helper.get_Data_Date_Range_Single_Point(earliest_date, latest_date, 1)
    ch2_avg_query = Rawdata_plotter_helper.get_Data_Date_Range_Single_Point(earliest_date, latest_date, 2)
    ch1_avg = float("{0:.2f}".format(ch1_avg_query['query'].first().ch_avg))
    ch2_avg = float("{0:.2f}".format(ch2_avg_query['query'].first().ch_avg))
    total_days_available_query = RawData.query.with_entities(RawData.yearmonthdate_stamp.distinct().label('date'))\
        .filter(RawData.fk_sensor_id == 1)

    day_count = total_days_available_query.count()
    return {
        'latest_date': latest_date,
        'earliest_date': earliest_date,
        'ch1_avg': ch1_avg,
        'ch2_avg': ch2_avg,
        'day_count': day_count
        }
    pass


@main.route('/', methods=['GET', 'POST'])
def index():
    if current_user.is_authenticated() == True:
        param_dict = build_logged_in_gist_view()
        return render_template('index.html', **param_dict)
    else:
        return render_template('index.html')
    pass


@main.route('/upload', methods=['GET', 'POST'])
@login_required
@requires_roles('admin')
def upload():
    process = False
    authenticated_files_count = 0
    illegal_files_count = 0
    # form object to pass into render template
    form = UploadForm()
    # check if the request method and fieldname is correct in incoming request
    if form.validate_on_submit() and 'uploadedfiles[]' in request.files:
        # get a list of files from the incoming request
        process = False
        files = request.files.getlist("uploadedfiles[]")
        # check if there are files in the list
        # even if no files are selected, request.files returns an empty file storage object
        if files[0].filename != '':
            # initialize our list
            filelist = []
            # get absolute folder path
            folderpath = app.config['UPLOAD_FOLDER']
            # process individual files
            for file in files:
                # get filename
                filename = secure_filename(file.filename)
                # validate filename with regular expression
                regex = '(?P<serial>\d\d\d\d)' \
                        '(?P<year>(?:19|20)\d\d)' \
                        '(?P<month>0[1-9]|1[012])' \
                        '(?P<day>0[1-9]|[12][0-9]|3[01])' \
                        '(?P<FileNo>\d*)' \
                        '(?P<extension>\.txt$)'
                if re.match(regex, filename):
                    # get absolute filepath
                    filepath = os.path.join(folderpath, filename)
                    # save filename and absolute path into the list
                    filelist.append({'filename':str(file.filename), 'path':str(filepath)})
                    # save the file temporarily
                    file.save(filepath)
                    authenticated_files_count += 1
                    # flash messages about the current operation
                    # flash('"%s" is saved at "%s"' % (filename, filepath), 'success')
                    process = True
                else:
                    # flash('Filename is not from trusted source', 'error')
                    illegal_files_count += 1
                    # process = False

                # To do:
                # var folderpath and list filelist should be passed to the parser at this point.
                # Status of success or failure could be returned with a list of msgs,
                # which could be displayed in the msgbox using flash.
                # After pursing, the parser will delete the temp files.
        else:
            # send error msg
            process = False
            flash('No files selected', 'error')
        # reload page
        if authenticated_files_count:
            flash('Files uploaded ' + str(authenticated_files_count))
        if illegal_files_count:
            flash('Files Not uploaded ' + str(illegal_files_count))

        return render_template('upload.html', form=form, process=process)
        # return redirect(request.path)
    return render_template('upload.html', form=form, process=process)

@main.route('/process', methods=['GET', 'POST'])
@login_required
@requires_roles('admin')
def call_parser():
    # response_dict = dict()
    parser = Parser(rawDataDirectory=app.config['UPLOAD_FOLDER'])
    parser.init_static_vars()
    response_dict = parser.parse()
    parser.cleanup()
    return render_template('parse_files.html', response_dict=response_dict)
    pass