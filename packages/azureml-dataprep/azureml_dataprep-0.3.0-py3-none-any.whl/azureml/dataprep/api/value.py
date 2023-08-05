# Copyright (c) Microsoft Corporation. All rights reserved.
import math
from datetime import datetime, timedelta, timezone
from typing import Any
from .engineapi.typedefinitions import DataField, FieldType


def to_dprep_value(value: Any) -> Any:
    try:
        import pandas
        import numpy
    except ImportError:
        raise RuntimeError('Pandas is not installed. To use pandas with azureml.dataprep, '
                           'pip install azureml.dataprep[pandas].')

    if isinstance(value, list):
        data = [to_dprep_value(v) for v in value]
        return data

    if isinstance(value, str):
        return value

    if value is None or isinstance(value, int) or isinstance(value, str) or isinstance(value, bool):
        return value
    if hasattr(value, 'dtype') and value.dtype.kind == 'i':  # numpy.int*
        return int(value)
    if hasattr(value, 'dtype') and value.dtype.kind == 'b':  # numpy.bool*
        return bool(value)

    if value == float('inf'):
        return {'n': 1}
    if value == -float('inf'):
        return {'n': -1}

    try:
        if numpy.isnan(value):
            return {'n': 0}
    except TypeError:
        pass

    if isinstance(value, float):
        return value
    if hasattr(value, 'dtype') and value.dtype.kind == 'f':  # numpy.float*
        return float(value)

    try:
        if isinstance(value, type(pandas.NaT)):
            return None
        if isinstance(value, pandas.Timestamp) or isinstance(value, numpy.datetime64):
            value = pandas.Timestamp(value).to_pydatetime()
    except TypeError:
        pass

    if isinstance(value, datetime):
        diff = value - datetime(1, 1, 1)
        ticks = diff.days * 864000000000 + diff.seconds * 10000000 + diff.microseconds * 10
        return {'d': ticks}

    if isinstance(value, dict):
        return {'r': [item for sublist in [[k, v] for (k, v) in value.items()] for item in sublist]}

    raise ValueError('The value ' + str(value) + ' cannot be used in an expression.')


_TIMESTAMP_KEY = 'timestamp'
_NAN_STRING = 'NaN'


def value_from_field(field: DataField) -> Any:
    if field.type == FieldType.DECIMAL and field.value == _NAN_STRING:
        return math.nan
    elif field.type == FieldType.DATE and _TIMESTAMP_KEY in field.value:
        return datetime.fromtimestamp(0, timezone.utc) + timedelta(milliseconds=field.value[_TIMESTAMP_KEY])
    else:
        return field.value
