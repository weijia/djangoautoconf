import logging

import base_settings
from djangoautoconf.base_setting_storage import ObjectSettingStorage

log = logging.getLogger(__name__)


class ModuleSettingStorage(ObjectSettingStorage):
    base_settings = base_settings
