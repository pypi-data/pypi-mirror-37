#!/usr/bin/env python
# -*- encoding: utf-8 -*-
# IDE: PyCharm 2017.2.4
# Author: Dajiang Ren<rendajiang@gagogroup.com>
# Created on 2018-10-07


from gagospecs.base.base import SpecBase
from gagospecs.v1.base.field_mappings import FIELD_MAPPINGS
from gagospecs.v1.base.load_module import create_module
from gagospecs.v1.base.model import DataProperties
from gagospecs.v1.base.schema import GMDSchema, create_schema


class FieldValidator(SpecBase):
    """
    Field validator
    """
    def __init__(
            self,
            name: str,
            field_name: str
    ):
        super().__init__(name)
        self.field_name = field_name

    def validate(
            self,
            value
    ):
        pass


class Validator(SpecBase):
    """
    Spec validator base class
    """
    def __init__(
            self,
            name: str,
            init_field_validators: list
    ):
        super().__init__(name)
        self.field_validators: dict = dict()
        for field_validator in init_field_validators:
            if field_validator.field_name \
                    not in self.field_validators:
                self.field_validators[field_validator.field_name] = \
                    field_validator

    @staticmethod
    def validate(
            product_level: str,
            product_name: str,
            gmd: dict
    ) -> dict:
        """
        validate a given ghf model
        :param product_level
        :param product_name
        :param gmd:
        :return:
        """
        schema: GMDSchema = create_schema(
            product_level,
            product_name
        )
        return schema.validate(gmd)

    def validate_data(
            self,
            data_properties: DataProperties,
            gmd: dict
    ) -> dict:
        """
        Validate the data properties
        :param data_properties: data properties
        :param gmd: gago meta data dict object
        :return:
        """
        for k, v in self.field_validators:
            field_name: str = k
            field_validator: FieldValidator = v
            if hasattr(data_properties, field_name):
                field_validator.validate(getattr(data_properties, field_name))
        errors: dict = self._validate_data(data_properties, gmd)
        input_errors = dict()
        if errors:
            for k, v in errors.items():
                field_name: str = k
                error_msg: str = v
                if field_name in FIELD_MAPPINGS:
                    input_errors[FIELD_MAPPINGS[field_name]] = error_msg
                else:
                    self.logger.error(
                        'field name %s not in FIELD_MAPPING',
                        field_name
                    )
        return input_errors

    def _validate_data(
            self,
            data_properties: DataProperties,
            gmd: dict
    ) -> dict:
        raise NotImplementedError


class CoordinateSystemFieldValidator(FieldValidator):
    def __init__(self):
        super().__init__(
            'CoordinateSystemFieldValidator',
            'coordinate_system'
        )

    def validate(
            self,
            value
    ):
        if isinstance(value, (float, int)):
            raise ValueError('coordinate system input error')


def create_validator(
        product_level: str,
        product_type: str
) -> Validator or None:
    m = create_module(
        'validators',
        product_level,
        product_type
    )
    if m and hasattr(m, 'main'):
        return m.main()
    return None
