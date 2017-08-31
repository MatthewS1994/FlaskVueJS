from __future__ import absolute_import, unicode_literals

import json
import re
import requests
import os
import requests

from flask import request
from flask_restful import Resource
from flask import Response
from flask import send_from_directory
from flask_sqlalchemy import abort
from app import cache, db, app

from server.mixims import status
from server.models import Menu, SiteConfig


def get_or_abort(model, object_id, code=404):
    """
    get an object with his given id or an abort error (404 is the default)
    """
    result = model.query.get(object_id)
    if result is None:
        abort(code)
    return result


class favicon(Resource):
    def get(self):
        return send_from_directory(os.path.join(app.root_path, 'static'), 'favicon.ico', mimetype='image/vnd.microsoft.icon')


class HealthApi(Resource):
    def get(self):
        request.headers = {favicon}
        app.logger.debug('In FileBox HealthApi')
        checks = [
            {
                'internet': 'yes',
                'datapump_is_connected': 'yes',
                'database_connection_healthy': 'yes',
                'celery_healthy': 'yes'
            },
            {
                'internet': 'yes',
                'datapump_is_connected': 'yes',
                'database_connection_healthy': 'yes',
                'celery_healthy': 'yes'
            }
        ]
        app.logger.debug(checks)
        return Response(json.dumps(checks), status=status.HTTP_200_OK, mimetype='application/json')


class MenusApi(Resource):
    def get(self):
        app.logger.debug(request.remote_addr)
        request.headers = {favicon}
        app.logger.debug('In FileBox HealthApi')
        menus_list = []
        menus = Menu.query.all()
        dict_object = {}
        counter = 0
        for menu in menus:
            if menu.is_parent():

                # GET ALL THE CHILDREN
                children = menu.children()
                sub_menus = []
                if children:
                    for sub_menu in children:
                        sub_menus.append({
                            'id': sub_menu.id,
                            'name': sub_menu.name,
                            'url': sub_menu.url,
                            'slug': sub_menu.slug,
                        })
                # DEFINE THE MAIN MENU ITEMS
                menus_list.append({
                    'id': menu.id,
                    'name': menu.name,
                    'url': menu.url,
                    'slug': menu.slug,
                    "sub_menus": sub_menus,
                })

                counter += 1

        dict_object['objects'] = menus_list
        dict_object['num_results'] = counter
        app.logger.debug(dict_object)
        return Response(json.dumps(dict_object, indent=2), status=status.HTTP_200_OK, mimetype='application/json')


class SiteConfigs(Resource):
    def get(self):
        headers = request.headers
        remote_addr = request.headers.environ['REMOTE_ADDR']
        host_port = request.headers.environ['REMOTE_PORT']
        app.logger.debug([remote_addr, host_port])
        try:
            # site = get_or_abort(SiteConfig, 1)
            site = SiteConfig.query.filter(SiteConfig.site_remote_address == remote_addr).first()
        except Exception as e:
            app.logger.error(e)
            return Response(
                {
                    'error': 'Host Address {0} Does Not exist on the system'.format(str(remote_addr) + str(host_port))
                },
                status=status.HTTP_403_FORBIDDEN,
                mimetype='application/json'
            )

        site_configs = {
            'site_name': site.site_display_name,
            'site_meta': site.site_meta,
            'site_theme': site.site_color_theme
        }
        return Response(json.dumps(site_configs, indent=2), status=status.HTTP_200_OK, mimetype='application/json')