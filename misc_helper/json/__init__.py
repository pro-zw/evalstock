# -*- coding: utf-8 -*-


def date_serializer(obj):
    if hasattr(obj, 'isoformat'):
        return obj.isoformat()
    else:
        raise TypeError