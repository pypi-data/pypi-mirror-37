#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Tests for `rri` package."""
from datetime import datetime as dt

import pytest


from rri import RRIClient
from rri.exception import InvalidInput, InvalidTldCredentials, \
    InvalidAccess, InvalidRequestMethod, GeneralFailure, NotImplemented, \
    UnknownStatus


@pytest.fixture(scope='function')
def rric():
    return RRIClient('example', 'testuser', 'testpass')


@pytest.fixture(params=['report', 'notification', 'functions', 'transactions'])
def rric_resource(request, rric):
    if request.param == 'report': return rric.report
    if request.param == 'notification': return rric.notification
    if request.param == 'functions': return rric.functions
    if request.param == 'transactions': return rric.transactions

#
# Report
#
@pytest.mark.parametrize('return_value, expected', [
    (200, True),
    (404, False)
])
def test_report_check(rric, responses, return_value, expected):
    responses.add(responses.HEAD, status=return_value,
                  url='https://ry-api.icann.org/info/report/registry-escrow-report/example/2018-08-09')

    assert rric.report.check('2018-08-09') == expected


@pytest.mark.parametrize('date', [
    '2018-08-09',
    pytest.param(dt(2018, 8, 9), id='dt(2018, 8, 9)')
])
def test_report_check_datetype(rric, responses, date):
    responses.add(responses.HEAD, status=200,
                  url='https://ry-api.icann.org/info/report/registry-escrow-report/example/2018-08-09')

    assert rric.report.check(date) == True


@pytest.mark.withoutresponses
@pytest.mark.parametrize('date', [
    '2018-13-09',
    '2018-02-30',
    'not-a-date-string',
])
def test_report_check_datetype_failure(rric, date):
    with pytest.raises(ValueError):
        rric.report.check(date)


@pytest.mark.parametrize('return_value, expected_exception', [
    (400, InvalidInput),
    (401, InvalidTldCredentials),
    (403, InvalidAccess),
    (405, InvalidRequestMethod),
    (500, GeneralFailure),
    (501, NotImplemented),
    (999, UnknownStatus)
])
def test_report_check_failure_raises_exception(rric, responses, return_value, expected_exception):
    responses.add(responses.HEAD, status=return_value,
                  url='https://ry-api.icann.org/info/report/registry-escrow-report/example/2018-08-09')

    with pytest.raises(expected_exception):
        rric.report.check('2018-08-09')


@pytest.mark.parametrize('base_url, expected', [
    ('test.example', 'https://test.example/info/report/registry-escrow-report/example/2018-08-09'),
    (None, 'https://ry-api.icann.org/info/report/registry-escrow-report/example/2018-08-09')
])
def test_report_urls(responses, base_url, expected):
    responses.add(responses.HEAD, status=200 , url=expected)

    rric = RRIClient('example', 'testuser', 'testpass', base_url=base_url)

    rric.report.check('2018-08-09')

    assert responses.calls[0].request.url == expected


@pytest.mark.parametrize('return_value, expected', [
    (200, True),
    (400, False)
])
def test_report_submit(rric, responses, return_value, expected):
    responses.add(responses.PUT, status=return_value,
                  url='https://ry-api.icann.org/report/registry-escrow-report/example/EXAMPLEID')

    r = rric.report.submit('<examplereport></examplereport>', 'EXAMPLEID')
    assert r.success == expected

#
# Notification
#
@pytest.mark.parametrize('return_value, expected', [
    (200, True),
    (404, False)
])
def test_notification_check(rric, responses, return_value, expected):
    responses.add(responses.HEAD, status=return_value,
                  url='https://ry-api.icann.org/info/report/escrow-agent-notification/example/2018-08-09')

    assert rric.notification.check('2018-08-09') == expected


@pytest.mark.parametrize('date', [
    '2018-08-09',
    pytest.param(dt(2018, 8, 9), id='dt(2018, 8, 9)')
])
def test_notification_check_datetype(rric, responses, date):
    responses.add(responses.HEAD, status=200,
                  url='https://ry-api.icann.org/info/report/escrow-agent-notification/example/2018-08-09')

    assert rric.notification.check(date) == True


@pytest.mark.withoutresponses
@pytest.mark.parametrize('date', [
    '2018-13-09',
    '2018-02-30',
    'not-a-date-string',
])
def test_notification_check_datetype_failure(rric, date):
    with pytest.raises(ValueError):
        rric.notification.check(date)


@pytest.mark.parametrize('return_value, expected_exception', [
    (400, InvalidInput),
    (401, InvalidTldCredentials),
    (403, InvalidAccess),
    (405, InvalidRequestMethod),
    (500, GeneralFailure),
    (501, NotImplemented),
    (999, UnknownStatus)
])
def test_notification_failed_check_raises_exception(rric, responses, return_value, expected_exception):
    responses.add(responses.HEAD, status=return_value,
                  url='https://ry-api.icann.org/info/report/escrow-agent-notification/example/2018-08-09')

    with pytest.raises(expected_exception):
        rric.notification.check('2018-08-09')


@pytest.mark.parametrize('base_url, expected', [
    ('test.example', 'https://test.example/info/report/escrow-agent-notification/example/2018-08-09'),
    (None, 'https://ry-api.icann.org/info/report/escrow-agent-notification/example/2018-08-09')
])
def test_notification_urls(responses, base_url, expected):
    responses.add(responses.HEAD, status=200 , url=expected)

    rric = RRIClient('example', 'testuser', 'testpass', base_url=base_url)

    rric.notification.check('2018-08-09')

    assert responses.calls[0].request.url == expected
#
#
# @pytest.mark.parametrize('base_url, expected', [
#     ('test.example', 'https://test.example/info/report/registry-escrow-report/example{/id}'),
#     (None, 'https://ry-api.icann.org/info/report/registry-escrow-report/example{/id}')
# ])
# @pytest.mark.internal
# def test_report_urls(base_url, expected):
#     rric = RRIClient('example', 'testuser', 'testpass', base_url=base_url)
#
#     assert str(rric.report.info_url) == expected
#

#
# Functions
#
@pytest.mark.parametrize('return_value, expected', [
    (200, True),
    (404, False)
])
def test_functions_check(rric, responses, return_value, expected):
    responses.add(responses.HEAD, status=return_value,
                  url='https://ry-api.icann.org/info/report/registry-functions-activity/example/2018-08')

    assert rric.functions.check('2018-08') == expected


@pytest.mark.parametrize('date', [
    '2018-08',
    pytest.param(dt(2018, 8, 9), id='dt(2018, 8, 9)')
])
def test_functions_check_datetype(rric, responses, date):
    responses.add(responses.HEAD, status=200,
                  url='https://ry-api.icann.org/info/report/registry-functions-activity/example/2018-08')

    assert rric.functions.check(date) == True


@pytest.mark.withoutresponses
@pytest.mark.parametrize('date', [
    '2018-13-09',
    '2018-02-30',
    'not-a-date-string',
])
def test_functions_check_datetype_failure(rric, date):
    with pytest.raises(ValueError):
        rric.functions.check(date)


@pytest.mark.parametrize('return_value, expected_exception', [
    (400, InvalidInput),
    (401, InvalidTldCredentials),
    (403, InvalidAccess),
    (405, InvalidRequestMethod),
    (500, GeneralFailure),
    (501, NotImplemented),
    (999, UnknownStatus)
])
def test_functions_failed_check_raises_exception(rric, responses, return_value, expected_exception):
    responses.add(responses.HEAD, status=return_value,
                  url='https://ry-api.icann.org/info/report/registry-functions-activity/example/2018-08')

    with pytest.raises(expected_exception):
        rric.functions.check('2018-08')


@pytest.mark.parametrize('base_url, expected', [
    ('test.example', 'https://test.example/info/report/registry-functions-activity/example/2018-08'),
    (None, 'https://ry-api.icann.org/info/report/registry-functions-activity/example/2018-08')
])
def test_functions_urls(responses, base_url, expected):
    responses.add(responses.HEAD, status=200 , url=expected)

    rric = RRIClient('example', 'testuser', 'testpass', base_url=base_url)

    rric.functions.check('2018-08')

    assert responses.calls[0].request.url == expected


#
# Transactions
#
@pytest.mark.parametrize('return_value, expected', [
    (200, True),
    (404, False)
])
def test_transactions_check(rric, responses, return_value, expected):
    responses.add(responses.HEAD, status=return_value,
                  url='https://ry-api.icann.org/info/report/registrar-transactions/example/2018-08')

    assert rric.transactions.check('2018-08') == expected


@pytest.mark.parametrize('date', [
    '2018-08',
    pytest.param(dt(2018, 8, 9), id='dt(2018, 8, 9)')
])
def test_transactions_check_datetype(rric, responses, date):
    responses.add(responses.HEAD, status=200,
                  url='https://ry-api.icann.org/info/report/registrar-transactions/example/2018-08')

    assert rric.transactions.check(date) == True


@pytest.mark.withoutresponses
@pytest.mark.parametrize('date', [
    '2018-13-09',
    '2018-02-30',
    'not-a-date-string',
])
def test_transactions_check_datetype_failure(rric, date):
    with pytest.raises(ValueError):
        rric.transactions.check(date)


@pytest.mark.parametrize('return_value, expected_exception', [
    (400, InvalidInput),
    (401, InvalidTldCredentials),
    (403, InvalidAccess),
    (405, InvalidRequestMethod),
    (500, GeneralFailure),
    (501, NotImplemented),
    (999, UnknownStatus)
])
def test_transactions_failed_check_raises_exception(rric, responses, return_value, expected_exception):
    responses.add(responses.HEAD, status=return_value,
                  url='https://ry-api.icann.org/info/report/registrar-transactions/example/2018-08')

    with pytest.raises(expected_exception):
        rric.transactions.check('2018-08')


@pytest.mark.parametrize('base_url, expected', [
    ('test.example', 'https://test.example/info/report/registrar-transactions/example/2018-08'),
    (None, 'https://ry-api.icann.org/info/report/registrar-transactions/example/2018-08')
])
def test_transactions_urls(responses, base_url, expected):
    responses.add(responses.HEAD, status=200 , url=expected)

    rric = RRIClient('example', 'testuser', 'testpass', base_url=base_url)

    rric.transactions.check('2018-08')

    assert responses.calls[0].request.url == expected


# @pytest.mark.parametrize('date', [
#     pytest.param(dt(2018, 8, 9), id='dt(2018, 8, 9)')
# ])
# def test_check_datetype(rric_resource, responses, date):
#     target_url = 'https://ry-api.icann.org/info/report/{}/example/{}'.format(
#         rric_resource.resource_name,
#         dt.strftime(date, rric_resource.date_format)
#     )
#
#     responses.add(responses.HEAD, status=200, url=target_url)
#
#     assert rric_resource.check(date) == True
