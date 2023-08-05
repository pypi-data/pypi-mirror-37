#!/usr/bin/env python
# -*- encoding: utf-8 -*-
# IDE: PyCharm 2017.2.4
# Author: Dajiang Ren<rendajiang@gagogroup.com>
# Created on 2018-10-15


from gagospecs.v1.base.validator import Validator, \
    DataProperties, \
    CoordinateSystemFieldValidator
from gagospecs.v1.models.original.NDVI import NDVIModel
from gagospecs.v1.schemas.original.NDVI import NDVISchema


class NDVIValidator(Validator):
    """
    原始级NDVI产品校验
    """
    def __init__(self):
        super().__init__(
            'NDVIValidator',
            [CoordinateSystemFieldValidator()]
        )

    def _validate_data(
            self,
            data_properties: DataProperties,
            gmd: dict
    ) -> dict:
        ndvi_model: NDVIModel = NDVIModel()
        ndvi_model.data_type = data_properties.data_type
        ndvi_model.lines = data_properties.lines
        ndvi_model.rows = data_properties.rows
        ndvi_model.no_data = data_properties.no_data
        ndvi_model.compression = data_properties.compression
        ndvi_model.coordinate_system = data_properties.coordinate_system
        ndvi_model.extent = data_properties.extent
        ndvi_schema: NDVISchema = NDVISchema()
        _, errors = ndvi_schema.dumps(ndvi_model)
        return errors


def main():
    return NDVIValidator()
