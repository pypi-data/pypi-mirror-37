import requests
import logging

from django.contrib.auth.models import UserManager
from django.conf import settings

from auth_uuid import settings as app_settings


class SimpleUserManager(UserManager):

    def get_by_natural_key(self, username):
        try:
            user = self.get(uuid=username)
        except self.model.DoesNotExist:
            user = self.retrieve_remote_user_by_uuid(username)
        return user

    def retrieve_remote_user_by_uuid(self, uuid):
        logger = logging.getLogger(app_settings.LOGGER_NAME)
        url = settings.URL_VALIDATE_USER_UUID.format(uuid)
        response = None
        try:
            response = requests.get(url)
        except Exception as err:
            message = 'requests.Exception: {}'.format(err)
            logger.error(message)
            response = None

        if response and response.status_code == requests.codes.ok:
            user = self.create(uuid=response.json().get('uuid'))
            return user
        return None

    def retrieve_remote_user_by_cookie(self, cookies):
        logger = logging.getLogger(app_settings.LOGGER_NAME)
        url = settings.URL_VALIDATE_USER_COOKIE
        response = None
        try:
            response = requests.get(url, cookies=cookies)
        except Exception as err:
            message = 'requests.Exception: {}'.format(err)
            logger.error(message)
            response = None

        if response and response.status_code == requests.codes.ok:
            try:
                data = response.json()[0]
            except IndexError:
                return None
            user, _ = self.update_or_create(
                uuid=data.get('uuid'),
                defaults={
                    'is_active': data.get('is_active'),
                    'is_superuser': data.get('is_superuser'),
                    'is_staff': data.get('is_staff'),
                }
            )
            return user
        return None
