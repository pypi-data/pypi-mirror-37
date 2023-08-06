#!/usr/bin/env python
# -*- encoding: utf-8 -*-
# IDE: PyCharm 2017.2.4
# Author: Dajiang Ren<rendajiang@gagogroup.com>
# Created on 2018-10-25


from marshmallow import ValidationError, \
    validates, \
    validates_schema
from marshmallow.fields import Integer

from gagospecs.v1.base.model import ProductLevelValues
from gagospecs.v1.base.schema import GMDSchema


class Level3GMDSchema(GMDSchema):
    """
    三级产品模式
    """
    @validates('level')
    def validate_level(self, value):
        if value != ProductLevelValues.Level3:
            raise ValidationError(
                '三级产品level字段必须为level3'
            )


class Level3RasterSchema(Level3GMDSchema):
    """
    三级栅格GMD模式
    """
    min_tile_level = Integer(required=True, allow_none=False)
    max_tile_level = Integer(required=True, allow_none=False)

    @validates('min_tile_level')
    def validate_min_tile_level(self, value):
        if value < 0 or value > 20:
            raise ValidationError(
                'min_tile_level字段必须大于等于0且小于等于20'
            )

    @validates('max_tile_level')
    def validate_max_tile_level(self, value):
        if value < 0 or value > 20:
            raise ValidationError(
                'max_tile_level字段必须大于等于0且小于等于20'
            )

    @validates_schema
    def validate_tile_levels(self, data):
        if data['min_tile_level'] > data['max_tile_level']:
            raise ValidationError(
                'min_tile_level字段不能大于max_tile_level字段'
            )
