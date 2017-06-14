# -*- coding: utf-8 -*-


class DatabaseAsAServiceApi(object):
    def __init__(self, credentials):
        self.credentials = credentials

    @property
    def endpoint(self):
        return self.credentials.endpoint

    @property
    def user(self):
        return self.credentials.user

    @property
    def password(self):
        return self.credentials.password

    @property
    def tenant_name(self):
        return self.credentials.project

    @property
    def is_secure(self):
        value = str(self.credentials.get_parameter_by_name('is_secure'))
        return value.lower() == 'true'

    @property
    def category(self):
        return int(self.credentials.get_parameter_by_name('category_id'))

    @property
    def access_permission(self):
        return str(self.credentials.get_parameter_by_name('access_permission'))

    @property
    def tenant_id(self):
        return str(self.credentials.get_parameter_by_name('tenant_id'))

    @property
    def token_endpoint(self):
        return str(self.credentials.get_parameter_by_name('token_endpoint'))

    @property
    def resource_endpoint(self):
        return str(self.credentials.get_parameter_by_name('resource_endpoint'))
