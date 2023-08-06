# -*- coding: utf-8 -*-
from datetime import datetime as dt

import requests
from uritemplate import URITemplate

from . import __version__
from .exception import RRIException, InvalidInput, InvalidTldCredentials, \
    InvalidAccess, InvalidRequestMethod, GeneralFailure, NotImplemented, \
    UnknownStatus


__all__ = ['RRIClient']


class RRIClient:
    """
    Registry Reporting Interface client

    :param str tld: tld to query
    :param str rri_user: tld username
    :param str rri_pass: tld password
    :param client: alternative client
    :type client:
    :param str base_url: alternative base url
    """
    icann_url = URITemplate(
        r'https://{base_url}{/info}/report/{resource}/{tld}{/id}'
    )

    def __init__(self, tld, rri_user, rri_pass, client=None, base_url=None):
        self.tld = tld
        self.rri_user = rri_user
        self.rri_pass = rri_pass

        if client:
            self.client = client
        else:
            self.client = requests.session()
            self.client.headers.update({
                'User-Agent': self._get_default_useragent()
            })

        self.base_url = base_url if base_url else 'ry-api.icann.org'
        self.icann_url = self.icann_url.partial(base_url=self.base_url)
        self.client.auth = (self.rri_user, self.rri_pass)

        self.url = self.icann_url.partial(tld=tld)

        self.report = EscrowReport(self.client, self.url)
        self.notification = EscrowNotification(self.client, self.url)
        self.functions = RegistryFunctions(self.client, self.url)
        self.transactions = PerRegistrarTransactions(self.client, self.url)

    def _get_default_useragent(self, name='python-rri'):
        return f'{name}/{__version__}'

    def __repr__(self):
        return f'RRIClient("{self.tld}", "{self.rri_user}", "{self.rri_pass}")'


class RRIResponse:
    def __init__(self, success, response_body):
        self.success = success
        self.response_body = response_body


class RRIResource:
    """
    Abstract class for api resources
    """
    resource_name = ''
    date_format = ''
    content_type = ''

    def __init__(self, client, url: URITemplate):
        self.client = client

        self.info_url = url.partial(info='info', resource=self.resource_name)

        # Setting a URIVariable to None doesn't remove it using .partial,
        # so reconstruct the URITemplate
        submit_url = url.expand(info=None, resource=self.resource_name)
        self.submit_url = URITemplate(submit_url + '{/id}')

    def _raise_status(self, status):
        if status == 400: raise InvalidInput
        if status == 401: raise InvalidTldCredentials
        if status == 403: raise InvalidAccess
        if status == 405: raise InvalidRequestMethod
        if status == 500: raise GeneralFailure
        if status == 501: raise NotImplemented

        raise UnknownStatus

    def _check_status(self, status):
        if status == 200: return True
        if status == 404: return False

        self._raise_status(status)

    def _submit_status(self, status):
        if status == 200: return True
        if status == 400: return False

        self._raise_status(status)

    def _get_date_string(self, date=None) -> str:
        if not date:
            return dt.strftime(dt.now(), self.date_format)

        if isinstance(date, str):
            # Make sure it's a valid date string
            try:
                parsed_date = dt.strptime(date, self.date_format)
            except ValueError:
                raise

            return dt.strftime(parsed_date, self.date_format)

        return dt.strftime(date, self.date_format)

    def check(self, date=None):
        """Check the status of a resource endpoint

        :param date: The date to check, or today if None
        :type date: ``str`` or ``datetime.datetime``
        :return: True if HTTP/200, False if HTTP/404
        :rtype: ``bool``

        """
        try:
            url_date = self._get_date_string(date)
            check_url = self.info_url.expand(id=url_date)

            request = self.client.head(check_url)

            return self._check_status(request.status_code)
        except ValueError:
            raise
        except RRIException:
            raise

    def submit(self, report, date=None) -> RRIResponse:
        """Submit a report to the resource endpoint

        :param report:
        :param date:
        :return:
        """
        try:
            headers = {
                'Content-type': self.content_type,
                'Accept': self.content_type
            }

            url_date = self._get_date_string(date)
            submit_url = self.submit_url.expand(id=url_date)

            request = self.client.put(submit_url,
                                      data=report,
                                      headers=headers)

            success = self._submit_status(request.status_code)
            return RRIResponse(success, request.text)
        except ValueError:
            raise
        except RRIException:
            raise


class EscrowReport(RRIResource):
    """
    Data Escrow Report resource
    """
    resource_name = 'registry-escrow-report'
    date_format = '%Y-%m-%d'
    content_type = 'text/xml'

    def submit(self, report, id) -> RRIResponse:
        """Submit a registry escrow report passed in as report

        :param report:
        :type report: ``str``
        :param id:
        :type id: ``str``
        :return: ``RRIResponse``
        """
        try:
            headers = {
                'Content-type': self.content_type,
                'Accept': self.content_type
            }

            submit_url = self.submit_url.expand(id=id)

            request = self.client.put(submit_url,
                                      data=report,
                                      headers=headers)

            success = self._submit_status(request.status_code)
            return RRIResponse(success, request.text)
        except RRIException:
            raise


class EscrowNotification(RRIResource):
    """
    Data Escrow Notification resource
    """
    resource_name = 'escrow-agent-notification'
    date_format = '%Y-%m-%d'
    content_type = 'text/xml'

    def submit(self, report) -> RRIResponse:
        """Submit an escrow agent notification passed in as report

        :param report:
        :type report: ``str``
        :return: ``RRIResponse``
        """
        try:
            headers = {
                'Content-type': self.content_type,
                'Accept': self.content_type
            }

            submit_url = self.submit_url.expand(id=None)

            request = self.client.post(submit_url,
                                       data=report,
                                       headers=headers)

            success = self._submit_status(request.status_code)
            return RRIResponse(success, request.text)

        except RRIException:
            raise


class RegistryFunctions(RRIResource):
    """
    Registry Functions Activity resource
    """
    resource_name = 'registry-functions-activity'
    date_format = '%Y-%m'
    content_type = 'text/csv'


class PerRegistrarTransactions(RRIResource):
    """
    Per-Registrar Transactions resource
    """
    resource_name = 'registrar-transactions'
    date_format = '%Y-%m'
    content_type = 'text/csv'
