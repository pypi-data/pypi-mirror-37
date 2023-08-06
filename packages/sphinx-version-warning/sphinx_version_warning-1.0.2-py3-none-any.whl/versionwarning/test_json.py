# -*- coding: utf-8 -*-

# import pytest
import munch
from unittest import mock
import tempfile
from collections import namedtuple

from versionwarning.signals import generate_versionwarning_data_json


App = namedtuple('App', ('config',))


class Config:

    @classmethod
    def from_dict(cls, data):
        return munch.Munch(data)


@mock.patch(
    'versionwarning.signals.STATIC_PATH',
    tempfile.mkdtemp(suffix='_versionwarning'),
)
def test_json():
    data = {
        'versionwarning_admonition_type': 'warning',
        'versionwarning_api_url': '',
        'versionwarning_project_version': '',
        'versionwarning_messages': '',
        'versionwarning_default_message': '',
        'versionwarning_banner_html': '',
    }
    config = Config.from_dict(data)
    config.html_static_path = mock.MagicMock()

    import pdb; pdb.set_trace()
