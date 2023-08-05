#!/usr/bin/env python
# -*- encoding: utf-8 -*-
# IDE: PyCharm 2017.2.4
# Author: Dajiang Ren<rendajiang@gagogroup.com>
# Created on 2018-10-17


from gagospecs.v1.base.model import DataProperties
from gagospecs.v1.base.validator import Validator, \
    CoordinateSystemFieldValidator
from gagospecs.v1.models.original.CropClassification \
    import CropClassificationModel
from gagospecs.v1.schemas.original.CropClassification \
    import CropClassificationSchema


class CropClassificationValidator(Validator):
    """
    Crop classification validator
    """
    def __init__(self):
        super().__init__(
            'CropClassificationValidator',
            [CoordinateSystemFieldValidator()]
        )

    def _validate_data(
            self,
            data_properties: DataProperties,
            gmd: dict
    ) -> dict:
        crop_classification_model: CropClassificationModel = \
            CropClassificationModel()
        crop_classification_model.data_type = \
            data_properties.data_type
        crop_classification_model.lines = \
            data_properties.lines
        crop_classification_model.rows = \
            data_properties.rows
        crop_classification_model.no_data = \
            data_properties.no_data
        crop_classification_model.compression = \
            data_properties.compression
        crop_classification_model.coordinate_system = \
            data_properties.coordinate_system
        crop_classification_model.extent = \
            data_properties.extent
        crop_classification_schema: CropClassificationSchema = \
            CropClassificationSchema()
        _, errors = \
            crop_classification_schema.dumps(crop_classification_model)

        return errors


def main():
    return CropClassificationValidator()
