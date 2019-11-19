# -*- coding: utf-8 -*-
import uuid


def guid():
    return str(uuid.uuid1()).replace('-', '')
