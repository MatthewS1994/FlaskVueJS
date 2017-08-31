import logging
import os
import sys

from flask import Flask
from flask_cache import Cache
from flask_sqlalchemy import SQLAlchemy
from flask_mail import Mail
from flask_restless import APIManager
from flask_restful import Api
from flask_admin import Admin

from celery_conf import make_celery


app = Flask('RESTLESS API SERVER')
app.secret_key = os.environ.get('SECRET_KEY', '')
app.config.from_object(os.environ.get('APP_SETTINGS', 'config.DevelopmentConfig'))

cache = Cache(app)

db = SQLAlchemy(app)

api = Api(app)

celery = make_celery(app)

mail = Mail(app)

admin = Admin(app, name='Matthew Rest Admin', template_mode='bootstrap3')

api_prefix = app.config['API_PREFIX']
api_results_per_page = app.config['API_RESULT_PER_PAGE']


def clear_cache():
    cache.clear()


@app.after_request
def after_request(response):
  response.headers.add('Access-Control-Allow-Origin', '*')
  response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
  response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE,OPTIONS')
  return response


def start_resources():
    # OLD AND BUSTED
    from service.api import favicon, HealthApi, MenusApi, SiteConfigs
    api.add_resource(favicon, '/favicon.ico')
    api.add_resource(HealthApi, '{0}/health'.format(api_prefix))
    api.add_resource(MenusApi, '{0}/menus'.format(api_prefix))
    api.add_resource(SiteConfigs, '{0}/SiteConfigs/{1}'.format(api_prefix, '1234567890'))

    # NEW HOTNESS
    from server.models import UsersProfileData
    api_2 = APIManager(app, flask_sqlalchemy_db=db)
    api_2.create_api(UsersProfileData, methods=['GET', 'POST', 'DELETE'], url_prefix=api_prefix, results_per_page=api_results_per_page)


def normal_views():
    from views import zen
    app.add_url_rule("/", view_func=zen)


def admin_resources():
    from flask_admin.contrib.sqla import ModelView
    from server.models import UsersProfileData, Menu, MenuPosition, SiteConfig
    from admin import AnalyticsView

    admin.add_view(ModelView(UsersProfileData, db.session))
    admin.add_view(AnalyticsView(name='Analytics', endpoint='analytics'))
    admin.add_view(ModelView(Menu, db.session))
    admin.add_view(ModelView(MenuPosition, db.session))
    admin.add_view(ModelView(SiteConfig, db.session, name='Sites'))


if __name__ == '__main__':
    if app.config.get('DEVELOPMENT', False):
        handler = logging.StreamHandler(stream=sys.stdout)
        handler.setLevel(logging.DEBUG)
    else:
        handler = logging.StreamHandler(stream=sys.stdout)
        handler.setLevel(logging.INFO)

    # Start App Functions
    clear_cache()
    start_resources()
    normal_views()
    admin_resources()

    app.logger.addHandler(handler)
    app.logger.debug('Starting app')
    app.run(host='127.0.0.1', port=16000, debug=True, use_reloader=False)
