#!/usr/bin/env python
# -*- encoding: utf-8 -*-
# IDE: PyCharm 2017.2.4
# Author: Dajiang Ren<rendajiang@gagogroup.com>
# Created on 2018-10-25


from marshmallow import ValidationError, \
    validates
from marshmallow.fields import Integer, \
    Float

from gagospecs.v1.base.model import ProductLevelValues
from gagospecs.v1.base.schema import GMDSchema


class Level2GMDSchema(GMDSchema):
    """
    三级产品模式
    """
    @validates('level')
    def validate_level(self, value):
        if value != ProductLevelValues.Level2:
            raise ValidationError(
                '二级产品level字段必须为level2'
            )


class Level2RasterSchema(Level2GMDSchema):
    """
    二级栅格产品模式
    """
    columns = Integer(required=True, allow_none=False)
    rows = Integer(required=True, allow_none=False)
    resolution = Float(required=True, allow_none=False)

    @validates('columns')
    def validate_columns(self, value):
        if value <= 0:
            raise ValidationError('columns字段必须大于0')

    @validates('rows')
    def validate_rows(self, value):
        if value <= 0:
            raise ValidationError('rows字段必须大于0')

    @validates('resolution')
    def validate_resolution(self, value):
        if value <= 0:
            raise ValidationError('resolution字段必须大于0')
