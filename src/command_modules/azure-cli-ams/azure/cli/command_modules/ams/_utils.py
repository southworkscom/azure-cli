# --------------------------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for license information.
# --------------------------------------------------------------------------------------------

from datetime import datetime, timedelta

import uuid
import re
import json
import isodate


def _gen_guid():
    return uuid.uuid4()


def _is_guid(guid):
    try:
        uuid.UUID(guid)
        return True
    except ValueError:
        pass
    return False


def parse_iso_duration(str_duration):
    iso_duration_format_value = None
    if str_duration:
        iso_duration_format_value = isodate.duration_isoformat(parse_timedelta(str_duration))
    return iso_duration_format_value


def parse_timedelta(str_duration):
    if str_duration:
        datetime_duration = datetime.strptime(str_duration, '%H:%M:%S')
    return timedelta(hours=datetime_duration.hour or 0,
                     minutes=datetime_duration.minute or 0,
                     seconds=datetime_duration.second or 0)


def camel_to_snake(name):
    s1 = re.sub('(.)([A-Z][a-z]+)', r'\1_\2', name)
    return re.sub('([a-z0-9])([A-Z])', r'\1_\2', s1).lower()


def snake_to_camel_case(snake_str):
    components = snake_str.split('_')
    return components[0] + ''.join(x.title() for x in components[1:])


class JsonBytearrayEncoder(json.JSONEncoder):
    DATE_FORMAT = "%Y-%m-%d"
    TIME_FORMAT = "%H:%M:%S"

    def default(self, obj):  # pylint: disable=E0202,W0221
        if isinstance(obj, datetime):
            return obj.strftime("%s %s" % (self.DATE_FORMAT, self.TIME_FORMAT))

        if isinstance(obj, bytearray):
            return bytes(obj).decode('utf-8', 'ignore')

        try:
            return obj.toJSON()
        except Exception:  # pylint: disable=W0703
            obj = vars(obj)
            obj.pop('additional_properties', None)
            keys = list(obj.keys())
            for key in keys:
                obj[snake_to_camel_case(key)] = obj.pop(key)
            return obj


def create_ip_range(resource_name, ip):
    from azure.mgmt.media.models import IPRange
    from ipaddress import ip_network
    subnet_prefix_length = None
    try:
        ipv4_network = ip_network(ip)
        if ipv4_network.with_prefixlen == ip:
            subnet_prefix_length = ipv4_network.prefixlen
            ip = ipv4_network.network_address.compressed
    except ValueError:
        pass
    return IPRange(name=("{}_{}".format(resource_name, ip)), address=ip, subnet_prefix_length=subnet_prefix_length)
