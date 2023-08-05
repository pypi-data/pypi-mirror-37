import json
import os
import urllib2

import dateutil.parser

from . import dtslogger
from .utils import raise_wrapped, indent


class Storage(object):
    done = False


DEFAULT_DTSERVER = 'https://challenges.duckietown.org/v3'


def get_duckietown_server_url():
    V = 'DTSERVER'

    if V in os.environ:
        use = os.environ[V]
        if not Storage.done:
            msg = 'Using server %s instead of default %s' % (use, DEFAULT_DTSERVER)
            dtslogger.info(msg)
            Storage.done = True
        return use
    else:
        return DEFAULT_DTSERVER


class RequestException(Exception):
    pass


class ConnectionError(RequestException):
    """ The server could not be reached or completed request or
        provided an invalid or not well-formatted answer. """


class RequestFailed(RequestException):
    """
        The server said the request was invalid.

        Answered  {'ok': False, 'error': msg}
    """


def make_server_request(token, endpoint, data=None, method='GET', timeout=3):
    """
        Raise RequestFailed or ConnectionError.

        Returns the result in 'result'.
    """
    server = get_duckietown_server_url()
    url = server + endpoint

    headers = {'X-Messaging-Token': token}
    if data is not None:
        data = json.dumps(data)
    req = urllib2.Request(url, headers=headers, data=data)
    req.get_method = lambda: method
    try:
        res = urllib2.urlopen(req, timeout=timeout)
        data = res.read()
    except urllib2.HTTPError as e:
        msg = 'Operation failed for %s' % url
        msg += '\n\n' + e.read()
        raise ConnectionError(msg)
    except urllib2.URLError as e:
        msg = 'Cannot connect to server %s' % url
        raise_wrapped(ConnectionError, e, msg)
        raise

    try:
        result = json.loads(data)
    except ValueError as e:
        msg = 'Cannot read answer from server.'
        msg += '\n\n' + indent(data, '  > ')
        raise_wrapped(ConnectionError, e, msg)
        raise

    if not isinstance(result, dict) or 'ok' not in result:
        msg = 'Server provided invalid JSON response. Expected a dict with "ok" in it.'
        msg += '\n\n' + indent(data, '  > ')
        raise ConnectionError(msg)

    if result['ok']:
        if 'result' not in result:
            msg = 'Server provided invalid JSON response. Expected a field "result".'
            msg += '\n\n' + indent(result, '  > ')
            raise ConnectionError(msg)
        return result['result']
    else:
        msg = 'Failed request for %s:\n%s' % (url, result.get('error', result))
        raise RequestFailed(msg)


def get_dtserver_user_info(token):
    """ Returns a dictionary with information about the user """
    endpoint = '/info'
    method = 'GET'
    data = None
    return make_server_request(token, endpoint, data=data, method=method)


def dtserver_update_challenge(token, queue, challenge_parameters):
    endpoint = '/challenge-update'
    method = 'POST'
    data = {'queue': queue, 'challenge_parameters': challenge_parameters}
    return make_server_request(token, endpoint, data=data, method=method)


def dtserver_submit(token, queue, data):
    endpoint = '/submissions'
    method = 'POST'
    data = {'queue': queue, 'parameters': data}
    return make_server_request(token, endpoint, data=data, method=method)


def dtserver_retire(token, submission_id):
    endpoint = '/submissions'
    method = 'DELETE'
    data = {'submission_id': submission_id}
    return make_server_request(token, endpoint, data=data, method=method)


def dtserver_challenge_define(token, yaml):
    endpoint = '/challenge-define'
    method = 'POST'
    data = {'yaml': yaml}
    return make_server_request(token, endpoint, data=data, method=method)


def dtserver_get_user_submissions(token):
    """ Returns a dictionary with information about the user submissions """
    endpoint = '/submissions'
    method = 'GET'
    data = {}
    submissions = make_server_request(token, endpoint, data=data, method=method)

    for v in submissions.values():
        for k in ['date_submitted', 'last_status_change']:
            v[k] = dateutil.parser.parse(v[k])
    return submissions


# TODO: you can delete the following around Oct 15

def dtserver_work_submission(token, submission_id, machine_id, process_id, evaluator_version, features):
    endpoint = '/take-submission'
    method = 'GET'
    data = {'submission_id': submission_id,
            'machine_id': machine_id,
            'process_id': process_id,
            'evaluator_version': evaluator_version,
            'features': features}
    return make_server_request(token, endpoint, data=data, method=method)


def dtserver_report_job(token, job_id, result, stats, machine_id,
                        process_id, evaluation_container, evaluator_version):
    endpoint = '/take-submission'
    method = 'POST'
    data = {'job_id': job_id,
            'result': result,
            'stats': stats,
            'machine_id': machine_id,
            'process_id': process_id,
            'evaluation_container': evaluation_container,
            'evaluator_version': evaluator_version,
            }
    return make_server_request(token, endpoint, data=data, method=method)
