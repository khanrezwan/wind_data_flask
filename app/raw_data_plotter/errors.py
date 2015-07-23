from flask import render_template
from . import raw_data_plotter


@raw_data_plotter.app_errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


@raw_data_plotter.app_errorhandler(500)
def internal_server_error(e):
    return render_template('500.html'), 500


@raw_data_plotter.app_errorhandler(403)
def internal_server_error(e):
    return render_template('403.html'), 403
