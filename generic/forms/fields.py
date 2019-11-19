# -*- coding: utf-8 -*-
from django.db import models

from generic.utils.gen_guid import guid


class GUIDField(models.CharField):
    def __init__(self, verbose_name=None, name=None, **kwargs):
        kwargs['unique'] = kwargs.get('unique', True)
        kwargs['max_length'] = kwargs.get('max_length', 128)
        kwargs['default'] = kwargs.get('default', guid)
        super(GUIDField, self).__init__(verbose_name, name, **kwargs)

    # override
    # 非常重要, 需要查看源码中的clone-deconstruct实现
    def deconstruct(self):
        name, path, args, kwargs = super(GUIDField, self).deconstruct()
        kwargs['unique'] = self.unique  # fix bugs
        return name, path, args, kwargs
