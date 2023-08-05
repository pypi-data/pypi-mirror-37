# -*- coding: utf-8 -*-
import re

import cnxml

from pathlib import Path

from .logger import logger


__all__ = (
    'is_valid_identifier',
    'validate_content',
    'validate_litezip',
)


VALID_ID_REGEX = re.compile("^(col\d{5,}\d*|m\d{4,}|m?NEW\d{,2})$")


def is_valid_identifier(id):
    """Validate that the given `id`."""
    return VALID_ID_REGEX.match(id) is not None


def validate_content(*objs):
    """Runs the correct validator for given `obj`ects. Assumes all same type"""
    from .main import Collection, Module
    validator = {
        Collection: cnxml.validate_collxml,
        Module: cnxml.validate_cnxml,
    }[type(objs[0])]
    return validator(*[obj.file for obj in objs])


def validate_litezip(struct):
    """Validate the given litezip as `struct`.
    Returns a list of validation messages.

    """
    msgs = []

    def _fmt_err(err):
        return (Path(err.filename), "{}:{} -- {}: {}".format(*(err[1:])))

    obj_by_type = {}
    for obj in struct:
        if not is_valid_identifier(obj.id):
            msg = (obj.file.parent,
                   "{} is not a valid identifier".format(obj.id),)
            logger.info("{}: {}".format(*msg))
            msgs.append(msg)
        obj_by_type.setdefault(type(obj), []).append(obj)

    for obtype in obj_by_type:
        content_msgs = list([_fmt_err(err) for err in
                             validate_content(*obj_by_type[obtype])])
        for msg in content_msgs:
            logger.info("{}: {}".format(*msg))
        msgs.extend(content_msgs)
    return msgs
