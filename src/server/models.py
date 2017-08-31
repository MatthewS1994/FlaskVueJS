from __future__ import absolute_import, unicode_literals
from app import db
from slugify import slugify
from sqlalchemy import Column, String, Integer


class UsersProfileData(db.Model):
    __tablename__ = 'user_profile_data'

    id = db.Column(Integer, primary_key=True, autoincrement=True)
    user_firstname = db.Column(db.String(225))
    user_lastname = db.Column(db.String(225))
    user_email = db.Column(db.String(225))
    user_role = db.Column(db.String(225))
    user_age = db.Column(db.Integer)

    def __repr__(self):
        return '<UsersProfileData: %s>' % self.user_firstname


class MenuPosition(db.Model):
    __tablename__ = 'menu_position'

    id = db.Column(Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(225))

    def __repr__(self):
        return self.name


class Menu(db.Model):
    __tablename__ = 'menu'

    id = db.Column(Integer, primary_key=True, autoincrement=True)
    parent_id = Column(Integer, db.ForeignKey('menu.id'), nullable=True)
    name = db.Column(db.String(225))
    url = db.Column(db.String(225))
    slug = db.Column(db.String(225))
    parent = db.relation('Menu', remote_side=[id])
    position_id = db.Column(Integer, db.ForeignKey('menu_position.id'))
    position = db.relation('MenuPosition', remote_side=[MenuPosition.id])

    def __repr__(self):
        return '<Menu %r>' % (self.name)

    def children(self):
        _children = Menu.query.filter(Menu.parent == self)
        for child in _children:
            child.parent = self  # Hack to avoid unnecessary DB queries further down the track.
        return _children

    def is_parent(self):
        if not self.parent_id:
            return True
        return False


class SiteConfig(db.Model):
    __tablename__ = 'site_config'

    id = db.Column(Integer, primary_key=True, autoincrement=True)

    site_display_name = db.Column(String(225), nullable=False, unique=True)
    site_domain = db.Column(String(225), nullable=False, unique=True)
    site_remote_address = db.Column(String(225), unique=True)
    site_meta = db.Column(db.Text)
    site_color_theme = db.Column(String(225))
    site_email = db.Column(String(225), nullable=True)

    email_active = db.Column(db.Boolean, default=False, nullable=True)
    email_from_name = db.Column(String(225), nullable=True)
    email_driver = db.Column(String(225), nullable=True)
    email_server_host = db.Column(String(225), nullable=True)
    email_server_port = db.Column(String(225), nullable=True)
    email_server_name = db.Column(String(225), nullable=True)
    email_server_password = db.Column(String(225), nullable=True)

    deleted = db.Column(db.Boolean, default=False, nullable=True)

    def __repr__(self):
        return '<Menu %r>' % (self.site_display_name)



