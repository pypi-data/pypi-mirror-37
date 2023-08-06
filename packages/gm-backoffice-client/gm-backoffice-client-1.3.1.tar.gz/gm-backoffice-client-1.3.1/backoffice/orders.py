
import json
from os import path
from typing import List

from jsonschema import validate
from jsonschema.exceptions import ValidationError


class BackofficeValidationError(BaseException):
    pass


class BackofficeOrderValidator:
    @staticmethod
    def _get_schema(schema: str):
        filename = path.join(path.dirname(__file__), 'schemas', schema + '.schema.json')

        with open(filename, 'r') as f:
            return json.load(f)

    @classmethod
    def validate_order(cls, order: dict):
        try:
            validate(order, cls._get_schema('order'))

        except ValidationError as e:
            raise BackofficeValidationError(str(e))

        return True

    @classmethod
    def validate_items(cls, items: List):
        try:
            validate(items, cls._get_schema('items'))

        except ValidationError as e:
            raise BackofficeValidationError(str(e))

        return True
