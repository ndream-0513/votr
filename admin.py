from flask_admin.contrib.sqla import ModelView
from flask import session, redirect, url_for, request
from flask_admin.model import typefmt
from datetime import datetime

class AdminView(ModelView):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.static_folder = 'static'

    def is_accessible(self):
        return session.get('user') == '111'

    def inaccessible_callback(self, name, **kwargs):
        if not self.is_accessible():
            return redirect(request.args.get('next') or url_for('home'))

class TopicView(AdminView):
    def __init__(self, *args, **kwargs):
        super(TopicView, self).__init__(*args, **kwargs)

    column_list = ('title', 'date_created', 'date_modified', 'status')
    column_searchable_list = ('title',)
    column_default_sort = ('date_created', True)
    column_filters = ('status',)
