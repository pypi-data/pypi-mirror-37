#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: ai ts=4 sts=4 et sw=4 nu
"""
(c) 2015 Ronan Delacroix
Job Manager Job Abstract Class
:author: Ronan Delacroix
"""
import os
import logging
import mongoengine
import mongoengine.signals
import tbx
import tbx.process
import tbx.service
import tbx.log
import tbx.text
import uuid as UUID
import traceback
import tempfile
import shutil
from datetime import datetime, timedelta
import jobmanager.common as common
from tbx.code import cached_property
from datetime import date
from marshmallow import Schema, fields, pprint
from marshmallow_jsonschema import JSONSchema

class ArtistSchema(Schema):
    name = fields.Str()

class AlbumSchema(Schema):
    title = fields.Str()
    release_date = fields.Date()
    artist = fields.Nested(ArtistSchema())

bowie = dict(name='David Bowie')
album = dict(artist=bowie, title='Hunky Dory', release_date=date(1971, 12, 17))

a_schema = AlbumSchema()
result = a_schema.dump(album)
pprint(result, indent=2)

json_schema = JSONSchema()
json_schema.dump(a_schema)