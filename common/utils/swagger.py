from datetime import datetime
from typing import Type, Any, Dict
from pydantic import BaseModel
from rest_framework import serializers
from drf_spectacular.utils import inline_serializer

def generate_openapi_schema(dto_class: Type[BaseModel]) -> Dict[str, Any]:
    properties = {}
    required = []

    type_mapping = {
        'str': 'string',
        'int': 'integer',
        'float': 'number',
        'bool': 'boolean',
        'list': 'array',
        'dict': 'object',
        'datetime': 'string'
    }

    for field_name, field in dto_class.__fields__.items():
        field_type = field.outer_type_.__name__
        if field_type in type_mapping:
            openapi_type = type_mapping[field_type]
            field_info = {
                'type': openapi_type,
                'description': field.field_info.description,
                'examples': field.field_info.extra.get('examples', None)
            }
            if openapi_type == 'string' and field_type == 'datetime':
                field_info['format'] = 'date-time'
            if openapi_type == 'array':
                field_info['items'] = {'type': 'string'}

            if field_info['examples']:
                field_info['example'] = field_info['examples'][0]

            if field.allow_none:
                field_info['nullable'] = True
            if field.required:
                required.append(field_name)
            properties[field_name] = field_info
        else:
            # handle nested DTOs or unsupported types if necessary
            pass

    return {
        'type': 'object',
        'properties': properties,
        'required': required
    }


def generate_inline_serializer(dto_class: Type[BaseModel]):
    fields = {}
    for field_name, field in dto_class.__fields__.items():
        field_type = field.outer_type_
        if field_type == str:
            fields[field_name] = serializers.CharField(default=field.default or "")
        elif field_type == int:
            fields[field_name] = serializers.IntegerField(default=field.default or 0)
        elif field_type == float:
            fields[field_name] = serializers.FloatField(default=field.default or 0.0)
        elif field_type == bool:
            fields[field_name] = serializers.BooleanField(default=field.default or False)
        elif field_type == list:
            fields[field_name] = serializers.ListField(child=serializers.CharField(), default=field.default or [])
        elif field_type == dict:
            fields[field_name] = serializers.DictField(child=serializers.CharField(), default=field.default or {})
        elif field_type == datetime:
            fields[field_name] = serializers.DateTimeField(default=field.default or "2023-01-01T00:00:00Z")
        else:
            raise Exception(f"Unsupported field type: {field_type}")
    return inline_serializer(name=f'{dto_class.__name__}Serializer', fields=fields)
