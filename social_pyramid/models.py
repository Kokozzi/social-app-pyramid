"""Pyramid SQLAlchemy ORM models for Social Auth"""
import inspect
from pony.orm import *
from pony.orm.core import Attribute
from social_core.utils import setting_name, module_member
from social_pony.storage import PonyUserMixin, \
                                  PonyAssociationMixin, \
                                  PonyNonceMixin, \
                                  PonyCodeMixin, \
                                  PonyPartialMixin, \
                                  BasePonyStorage


class PyramidStorage(BasePonyStorage):
    user = None
    nonce = None
    association = None
    code = None
    partial = None


def build_from_abstract(name, classes, attrs):
    for _class in classes:
        attrs.update(inspect.getmembers(
            _class, lambda x: isinstance(x, Attribute)
        ))
    return type(name, classes, attrs)


def init_pony(User, db):
    # if hasattr(config, 'registry'):
    #     config = config.registry.settings
    UID_LENGTH = 255 #config.get(setting_name('UID_LENGTH'), 255)
    # User = module_member(config[setting_name('USER_MODEL')])
    # app_session = session

    class _AppSession(object):
        'history.auth.models.User'
        COMMIT_SESSION = False

        # @classmethod
        # def _session(cls):
        #     return app_session

    class __UserSocialAuth__:
        _user = None

        @property
        def user(self):
            if not self._user:
                self._user = User.get(lambda x: x.id == self.user_id)
            return self._user

        @classmethod
        def username_max_length(cls):
            if User.username.args:
                return User.username.args[0]
            return User.username.converters[0].provider.varchar_default_max_len

        @classmethod
        def user_model(cls):
            return User


    # Set the references in the storage class

    # UserSocialAuth =
    PyramidStorage.user = build_from_abstract('UserSocialAuth', (db.Entity, __UserSocialAuth__, PonyUserMixin), {
        'uid': Required(str, UID_LENGTH),
        'user': Required(User)
        # 'user_id': Required(User.id.py_type, index=True)
    })
    PyramidStorage.nonce = build_from_abstract('Nonce', (db.Entity, PonyNonceMixin), {})
    PyramidStorage.association = build_from_abstract('Association', (db.Entity, PonyAssociationMixin), {})
    PyramidStorage.code = build_from_abstract('Code', (db.Entity, PonyCodeMixin), {})
    PyramidStorage.partial = build_from_abstract('Partial', (db.Entity, PonyPartialMixin), {})
