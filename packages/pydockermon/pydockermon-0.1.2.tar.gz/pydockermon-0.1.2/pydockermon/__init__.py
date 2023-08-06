"""
A python module to interact with ha-dockermon.

This code is released under the terms of the MIT license. See the LICENSE
file for more details.
"""
import logging
import json
import requests

HEADERS = {'content-type': 'application/octet-stream'}


def logger(message, level=10):
    """Handle logging in this module."""
    logging.getLogger(__name__).log(level, str(message))

    # Enable this for local debug:
    # print('Log level: "' + str(level) + '", message: "' + str(message) + '"')


def list_containers(host, port='8126',
                    username=None, password=None):
    """Get a list of all containers."""
    baseurl = 'http://' + host + ':' + port
    commandurl = baseurl + '/containers'
    logger('Fetching a list of all containers.')
    try:
        data = requests.get(commandurl,
                            auth=(username, password), headers=HEADERS)
        if data:
            containernames = []
            for container in data.json():
                containernames.append(container['Names'][0][1:])
            return_value = {'success': True, 'data': containernames}
    except requests.exceptions.RequestException as exception:
        return_value = {'success': False, 'data': [None]}
        logger(exception, 40)
    except json.decoder.JSONDecodeError as exception:
        return_value = {'success': False, 'data': [None]}
        logger(exception, 40)
    try:
        logger(return_value)
    except UnboundLocalError as exception:
        return_value = {'success': False, 'data': {}}
        logger(exception, 40)
    return return_value


def get_container_state(container, host, port='8126',
                        username=None, password=None):
    """Get the state of a container."""
    baseurl = 'http://' + host + ':' + port
    commandurl = baseurl + '/container/' + container
    logger('Fetching container state for ' + container)
    try:
        data = requests.get(commandurl,
                            auth=(username, password), headers=HEADERS)
        if data:
            return_value = {'success': True, 'data': data.json()}
    except requests.exceptions.RequestException as exception:
        return_value = {'success': False, 'data': {}}
        logger(exception, 40)
    except json.decoder.JSONDecodeError as exception:
        return_value = {'success': False, 'data': {}}
        logger(exception, 40)
    try:
        logger(return_value)
    except UnboundLocalError as exception:
        return_value = {'success': False, 'data': {}}
        logger(exception, 40)
    return return_value


def get_container_stats(container, host, port='8126',
                        username=None, password=None):
    """Get the state of a container."""
    baseurl = 'http://' + host + ':' + port
    commandurl = baseurl + '/container/' + container + '/stats'
    logger('Fetching container stats for ' + container)
    try:
        data = requests.get(commandurl,
                            auth=(username, password), headers=HEADERS)
        if data:
            return_value = {'success': True, 'data': data.json()}
    except requests.exceptions.RequestException as exception:
        return_value = {'success': False, 'data': {}}
        logger(exception, 40)
    except json.decoder.JSONDecodeError as exception:
        return_value = {'success': False, 'data': {}}
        logger(exception, 40)
    try:
        logger(return_value)
    except UnboundLocalError as exception:
        return_value = {'success': False, 'data': {}}
        logger(exception, 40)
    return return_value


def start_container(container, host, port='8126',
                    username=None, password=None):
    """Start a spesified container."""
    baseurl = 'http://' + host + ':' + port
    commandurl = baseurl + '/container/' + container + '/start'
    logger('Starting the container ' + container)
    try:
        data = requests.get(commandurl,
                            auth=(username, password), headers=HEADERS)
        if data.status_code == 200:
            return_value = {'success': True, 'data': {}}
        else:
            return_value = {'success': False, 'data': {}}
            logger(data.status_code, 40)
    except requests.exceptions.RequestException as exception:
        return_value = {'success': False, 'data': {}}
        logger(exception, 40)
    except json.decoder.JSONDecodeError as exception:
        return_value = {'success': False, 'data': {}}
        logger(exception, 40)
    except AttributeError as exception:
        return_value = {'success': False, 'data': {}}
        logger(exception, 40)
    try:
        logger(return_value)
    except UnboundLocalError as exception:
        return_value = {'success': False, 'data': {}}
        logger(exception, 40)
    return return_value


def stop_container(container, host, port='8126',
                   username=None, password=None):
    """Start a spesified container."""
    baseurl = 'http://' + host + ':' + port
    commandurl = baseurl + '/container/' + container + '/stop'
    logger('Stopping the container ' + container)
    try:
        data = requests.get(commandurl,
                            auth=(username, password), headers=HEADERS)
        if data.status_code == 200:
            return_value = {'success': True, 'data': {}}
        else:
            return_value = {'success': False, 'data': {}}
            logger(data.status_code, 40)
    except requests.exceptions.RequestException as exception:
        return_value = {'success': False, 'data': {}}
        logger(exception, 40)
    except json.decoder.JSONDecodeError as exception:
        return_value = {'success': False, 'data': {}}
        logger(exception, 40)
    except AttributeError as exception:
        return_value = {'success': False, 'data': {}}
        logger(exception, 40)
    try:
        logger(return_value)
    except UnboundLocalError as exception:
        return_value = {'success': False, 'data': {}}
        logger(exception, 40)
    return return_value


def restart_container(container, host, port='8126',
                      username=None, password=None):
    """Start a spesified container."""
    baseurl = 'http://' + host + ':' + port
    commandurl = baseurl + '/container/' + container + '/restart'
    logger('Restarting the container ' + container)
    try:
        data = requests.get(commandurl,
                            auth=(username, password), headers=HEADERS)
        if data.status_code == 200:
            return_value = {'success': True, 'data': {}}
        else:
            return_value = {'success': False, 'data': {}}
            logger(data.status_code, 40)
    except requests.exceptions.RequestException as exception:
        return_value = {'success': False, 'data': {}}
        logger(exception, 40)
    except json.decoder.JSONDecodeError as exception:
        return_value = {'success': False, 'data': {}}
        logger(exception, 40)
    except AttributeError as exception:
        return_value = {'success': False, 'data': {}}
        logger(exception, 40)
    try:
        logger(return_value)
    except UnboundLocalError as exception:
        return_value = {'success': False, 'data': {}}
        logger(exception, 40)
    return return_value
