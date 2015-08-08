# Library Imports
from datetime import datetime
from flask import render_template, session, redirect, url_for, request, flash, g
from flask.ext.login import login_user, logout_user, login_required, current_user
# from werkzeug.security import check_password_hash, generate_password_hash

# App specific imports
# from app import login_manager
from . import auth
from .forms import *
from .. import db
from ..models import *
from ..decorators import requires_roles


# from ..wind_data_parser import Parser


# def base_page_dictionary_builder(brand_name='', navbar_dynamic_lis=list(),
#                                  navbar_view_specific_left_col_buttons=list(), flash_msg=''):
#     """
#     This function creates dictionary data structure for the base template page.
#     :param brand_name: Navigation bar brand name
#     :param title: Page Title string
#     :param navbar_dynamic_lis: Top navbar dynamic button elements. it's a python list of lists.
#     e.g.: [['Name of button 1', 'url'], ['Name of button 2', 'url'], ['Name of button 1']]
#     :param navbar_view_specific_left_col_buttons: Left navigation panel buttons.it's a python list of lists.
#     e.g.: [['Name of button 1', 'url'], ['Name of button 2', 'url'], ['Name of button 1']]
#     :param flash_msg: Message to be flashed on top. string
#     :return: a dictionary of base page parameters, to be unpacked by flask built-in render_template function
#     """
#     return {'brand_name': brand_name, 'navbar_dynamic_lis': navbar_dynamic_lis,
#             'navbar_view_specific_left_col_buttons': navbar_view_specific_left_col_buttons, 'flash_msg': flash_msg}

############################Log in##################################################
# set up default login view. In restricted pages, user will be
# redirected to the default login view

# login_manager.login_view = 'login'


# login manager loader class
# @login_manager.user_loader
# def user_loader(username):
#     return User.query.filter_by(username=username).first()


################
# login prompt #
################
@auth.route('/login', methods=['GET', 'POST'])
def login():
    # restrict view to already logged in users
    if current_user.is_authenticated():
        return redirect('/')
    # form object to pass into render template
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is not None and user.verify_password(form.password.data):
            login_user(user, form.rememberme.data)
            # session['username'] = user.username
            # session['logged_in'] = True
            return redirect(request.args.get('next') or url_for('main.index'))
        flash('Invalid username or password.')
    return render_template('auth/login.html', form=form)


##########
# logout #
##########
@auth.route('/logout')
@login_required
def logout():
    # logout user and destroy session
    logout_user()
    # for session_variables in session:
    #     session.pop(session_variables, None)
    # session.pop('username', None)
    # # session.pop('password', None)
    # session.pop('logged_in', None)
    flash('Logged Out', 'success')
    return redirect('/')


##########
# Register #
##########
@auth.route('/register', methods=['GET', 'POST'])
@login_required
@requires_roles('admin')
def registeruser():
    # if current_user.is_authenticated():
    #     flash('You are already logged in. <a href=\"%s\">Logout?</a>' % url_for('auth.logout'))
    #     return redirect('/')
    form = RegisterUser()
    form.choices = [("none", "----------")]

    if Role.query.count() == 0:
        flash('Please Add Roles before you register')
        return redirect(url_for('auth.addrole'))
    else:
        roles = Role.query.all()
        form.role.query = roles

    if request.method == 'POST' and form.validate_on_submit():
        username = form.username.data
        email = form.email.data
        role = form.role.data
        password = form.password.data
        user = User(username, email, password, role)

        db.session.add(user)
        db.session.commit()
        flash('Registered Successfully', 'success')
        # session['logged_in'] = True
        # session['username'] = User.username
        return redirect(url_for('auth.login'))

    return render_template('auth/register.html', form=form)


##########
# Add Roles #
##########
@auth.route('/addRole', methods=['GET', 'POST'])
@login_required
@requires_roles('admin')
def addrole():
    form = AddRoles()
    if request.method == 'POST' and form.validate_on_submit():
        name = str(form.name.data).lower()
        role = Role(name)

        if Role.query.filter(Role.name == role.name).count() == 0:
            db.session.add(role)
            db.session.commit()
            flash('Added %s role' % role.name)
        else:
            flash('Role is already in database')
            return render_template('auth/addrole.html', form=form)

    return render_template('auth/addrole.html', form=form)
