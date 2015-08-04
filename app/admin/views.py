__author__ = 'rezwan'
# Library imports
from flask_admin import BaseView, expose
from flask.ext.login import current_user
from flask import redirect, url_for, request, abort
from flask_admin.contrib.sqla import ModelView

# app related imports
from .. import admin
from ..models import User, Logger, File, Sensor, Site, RawData, Role
from app import db


class MyView(BaseView):
    @expose('/')
    def index(self):
        # if not login.current_user.is_authenticated():
        #     return redirect(url_for('.login_view'))
        # return super(MyAdminIndexView, self).ind

        return self.render('admin/index.html')

    def is_accessible(self):
        # print current_user.is_authenticated()
        return current_user.is_admin()

    def _handle_view(self, name, **kwargs):
        # print 'outside'
        if not self.is_accessible():
            print 'inside'
            abort(403)


class UserView(ModelView):
    # Override displayed fields
    column_list = ('username', 'email', 'role')

    def __init__(self, session, **kwargs):
        # You can pass name and other parameters if you want to
        super(UserView, self).__init__(User, session, **kwargs)

    def is_accessible(self):
        # print current_user.is_admin()
        # print current_user.is_authenticated()
        return current_user.is_admin()

    def _handle_view(self, name, **kwargs):
        # print 'outside'
        if not self.is_accessible():
            abort(403)


class RoleView(ModelView):
    def __init__(self, session, **kwargs):
        # You can pass name and other parameters if you want to
        super(RoleView, self).__init__(Role, session, **kwargs)

    def is_accessible(self):
        # print current_user.is_admin()
        # print current_user.is_authenticated()
        return current_user.is_admin()

    def _handle_view(self, name, **kwargs):
        # print 'outside'
        if not self.is_accessible():
            abort(403)


class LoggerView(ModelView):
    def __init__(self, session, **kwargs):
        # You can pass name and other parameters if you want to
        super(LoggerView, self).__init__(Logger, session, **kwargs)

    def is_accessible(self):
        return current_user.is_admin()

    def _handle_view(self, name, **kwargs):
        # print 'outside'
        if not self.is_accessible():
            abort(403)


class FileView(ModelView):
    column_list = ('filename', 'site', 'date', 'fileno', 'date_stamp', 'month_stamp', 'year_stamp', 'fk_logger_id',
                   'date_created', 'date_modified')

    def __init__(self, session, **kwargs):
        # You can pass name and other parameters if you want to
        super(FileView, self).__init__(File, session, **kwargs)

    def is_accessible(self):
        # print current_user.is_admin()
        # print current_user.is_authenticated()
        return current_user.is_admin()

    def _handle_view(self, name, **kwargs):
        if not self.is_accessible():
            abort(403)


class SensorView(ModelView):
    def __init__(self, session, **kwargs):
        # You can pass name and other parameters if you want to
        super(SensorView, self).__init__(Sensor, session, **kwargs)

    def is_accessible(self):
        # print current_user.is_admin()
        # print current_user.is_authenticated()
        return current_user.is_admin()

    def _handle_view(self, name, **kwargs):
        # print 'outside'
        if not self.is_accessible():
            abort(403)


class SiteView(ModelView):
    def __init__(self, session, **kwargs):
        # You can pass name and other parameters if you want to
        super(SiteView, self).__init__(Site, session, **kwargs)

    def is_accessible(self):
        # print current_user.is_admin()
        # print current_user.is_authenticated()
        return current_user.is_admin()

    def _handle_view(self, name, **kwargs):
        # print 'outside'
        if not self.is_accessible():
            abort(403)


class RawDataView(ModelView):
    def __init__(self, session, **kwargs):
        # You can pass name and other parameters if you want to
        super(RawDataView, self).__init__(RawData, session, **kwargs)

    def is_accessible(self):
        # print current_user.is_admin()
        # print current_user.is_authenticated()
        return current_user.is_admin()

    def _handle_view(self, name, **kwargs):
        # print 'outside'
        if not self.is_accessible():
            abort(403)


admin.add_view(UserView(db.session))
admin.add_view(RoleView(db.session))
admin.add_view(SiteView(db.session))
admin.add_view(LoggerView(db.session))
admin.add_view(FileView(db.session))
admin.add_view(SensorView(db.session))
admin.add_view(RawDataView(db.session))


# admin.add_view(ModelView(User, db.session))
# admin.add_view(ModelView(Logger, db.session))
# admin.add_view(ModelView(File, db.session))
# admin.add_view(ModelView(Sensor, db.session))
# admin.add_view(ModelView(Site, db.session))
# admin.add_view(ModelView(RawData, db.session))
# admin.add_view(ModelView(Role, db.session))
