# -*- coding: utf8 -*-
import json
import six
from missinglink.core.json_utils import clean_system_keys, get_json_items


def __create_chema_from_first_item(first_item):
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


def avro_from_data(data, write_to=None, key_name=None):
    from avro.datafile import DataFileWriter
    from avro.io import DatumWriter

    result = write_to or six.BytesIO()

    schema = None
    writer = None
    try:
        for i, item in enumerate(get_json_items(data, key_name=key_name)):
            item = clean_system_keys(item)

            if schema is None:
                schema = __create_chema_from_first_item(item)
                writer = DataFileWriter(result, DatumWriter(), schema)

            writer.append(item)
    finally:
        if writer is not None:
            writer.flush()

    return result
