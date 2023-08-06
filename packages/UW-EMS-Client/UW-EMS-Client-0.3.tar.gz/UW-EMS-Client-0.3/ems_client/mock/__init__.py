"""
EMS API mock data class
"""
from hashlib import md5
from importlib import import_module
import json
from logging import getLogger
from six import string_types
import sys
import os
import re

from commonconf import settings
from restclients_core.util.mock import convert_to_platform_safe


class EMSMockData(object):
    app_resource_dirs = []

    def __init__(self):
        self._log = getLogger(__name__)

        if len(EMSMockData.app_resource_dirs) < 1:
            apps = getattr(settings, 'INSTALLED_APPS', [])
            if isinstance(apps, string_types):
                apps = [v.strip() for v in apps.split(',')]

            for app in apps:
                try:
                    mod = import_module(app)
                except ImportError as ex:
                    raise ImproperlyConfigured('ImportError %s: %s' % (
                        app, ex.args[0]))

                resource_dir = os.path.join(os.path.dirname(mod.__file__),
                                            'resources/ems/file')
                if os.path.isdir(resource_dir):
                    # Cheating, to make sure our resources are overridable
                    data = {
                        'path': resource_dir,
                        'app': app,
                    }
                    EMSMockData.app_resource_dirs.insert(0, data)

    def mock(self, portName, methodName, params):
        mock_path = self._mock_file_path(portName, methodName, params)
        for resource in EMSMockData.app_resource_dirs:
            mock_data = self._load_mock_resource_from_path(resource, mock_path)
            if mock_data:
                return mock_data

        return ''

    def _load_mock_resource_from_path(self, resource_dir, resource_path):
        orig_file_path = os.path.join(resource_dir['path'], resource_path)

        paths = [
            convert_to_platform_safe(orig_file_path),
        ]

        file_path = None
        handle = None
        for path in paths:
            try:
                file_path = path
                handle = open(path)
                break
            except IOError as ex:
                pass

        if handle is None:
            return None

        mock_data = handle.read()
        handle.close()

        return mock_data

    def _mock_file_path(self, portName, methodName, params):
        return os.path.join(portName, methodName,
                            md5(self._normalize(params)).hexdigest().upper())

    def _normalize(self, params):
        ignored = ['auth']
        normalized = {}

        for k in sorted(params.keys()):
            if k not in ignored:
                normalized[k] = params[k]

        return json.dumps(normalized, sort_keys=True).encode('ascii', 'ignore')
