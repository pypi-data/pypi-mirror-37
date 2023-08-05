# -*- coding: utf8 -*-
import json
import six
from missinglink.core.json_utils import clean_system_keys, get_json_items


class AvroWriter(object):
    def __init__(self, write_to=None, key_name=None):
        self.__key_name = key_name
        self.__write_to = write_to or six.BytesIO()
        self.__writer = None

    @property
    def stream(self):
        return self.__write_to

    @classmethod
    def __create_chema_from_first_item(cls, first_item):
        import avro

        schema_data = {
            "namespace": "ml.data",
            "type": "record",
            "name": "Data",
            "fields": [],
        }

        type_convert = {'str': 'string', 'bool': 'boolean', 'unicode': 'string', 'long': 'int'}
        for key, val in first_item.items():
            t = type(val).__name__
            t = type_convert.get(t, t)
            field_data = {'name': key, "type": [t, "null"]}
            schema_data['fields'].append(field_data)

        parse_method = getattr(avro.schema, 'parse', None) or getattr(avro.schema, 'Parse')
        return parse_method(json.dumps(schema_data))

    def close(self):
        if self.__writer is None:
            return

        self.__writer.flush()

    def append_data(self, data):
        from avro.datafile import DataFileWriter
        from avro.io import DatumWriter

        for i, item in enumerate(get_json_items(data, key_name=self.__key_name)):
            item = clean_system_keys(item)

            if self.__writer is None:
                schema = self.__create_chema_from_first_item(item)
                self.__writer = DataFileWriter(self.__write_to, DatumWriter(), schema)

            self.__writer.append(item)
