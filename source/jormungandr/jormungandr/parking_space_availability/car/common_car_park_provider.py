# encoding: utf-8
# Copyright (c) 2001-2018, Canal TP and/or its affiliates. All rights reserved.
#
# This file is part of Navitia,
#     the software to build cool stuff with public transport.
#
# Hope you'll enjoy and contribute to this project,
#     powered by Canal TP (www.canaltp.fr).
# Help us simplify mobility and open public transport:
#     a non ending quest to the responsive locomotion way of traveling!
#
# LICENCE: This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.
#
# Stay tuned using
# twitter @navitia
# IRC #navitia on freenode
# https://groups.google.com/d/forum/navitia
# www.navitia.io

from __future__ import absolute_import, print_function, unicode_literals, division

import logging
import pybreaker
import requests as requests

from jormungandr import cache, app, utils, new_relic
from jormungandr.parking_space_availability import AbstractParkingPlacesProvider
from abc import abstractmethod


class CommonCarParkProvider(AbstractParkingPlacesProvider):

    def __init__(self, operators, dataset, timeout):
        self.operators = [o.lower() for o in operators]
        self.timeout = timeout
        self.dataset = dataset
        self.breaker = pybreaker.CircuitBreaker(fail_max=self.fail_max, reset_timeout=self.reset_timeout)
        self.log = logging.LoggerAdapter(logging.getLogger(__name__), extra={'dataset': self.dataset})

    @abstractmethod
    def _get_information(self, poi):
        pass

    def get_informations(self, poi):
        return self._get_information(poi)

    def support_poi(self, poi):
        properties = poi.get('properties', {})
        return properties.get('operator', '').lower() in self.operators

    def _call_webservice(self, request_url):
        try:
            if self.api_key:
                headers = {'Authorization': 'apiKey {}'.format(self.api_key)}
            else:
                headers = None
            data = self.breaker.call(requests.get, url=request_url, headers=headers, timeout=self.timeout)
            # record in newrelic
            self.record_call("OK")
            return data.json()
        except pybreaker.CircuitBreakerError as e:
            msg = '{} service dead (error: {})'.format(self.provider_name, e)
            self.log.error(msg)
            # record in newrelic
            utils.record_external_failure(msg, 'parking', self.provider_name)
        except requests.Timeout as t:
            msg = '{} service timeout (error: {})'.format(self.provider_name, t)
            self.log.error(msg)
            # record in newrelic
            utils.record_external_failure(msg, 'parking', self.provider_name)
        except:
            msg = '{} service error'.format(self.provider_name)
            self.log.exception(msg)
            # record in newrelic
            utils.record_external_failure(msg, 'parking', self.provider_name)

        return None

    def status(self):
        return {'operators': self.operators}

    def feed_publisher(self):
        return self._feed_publisher

    def record_call(self, status, **kwargs):
        """
        status can be in: ok, failure
        """
        params = {'parking_service': self.provider_name, 'dataset': self.dataset, 'status': status}
        params.update(kwargs)
        new_relic.record_custom_event('parking_service', params)
