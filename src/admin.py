from __future__ import absolute_import, unicode_literals

from flask_admin import BaseView, expose


class AnalyticsView(BaseView):
    @expose('/')
    def index(self):
        return self.render('admin/analytics.html')