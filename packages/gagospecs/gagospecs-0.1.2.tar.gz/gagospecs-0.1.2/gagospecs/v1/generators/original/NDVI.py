#!/usr/bin/env python
# -*- encoding: utf-8 -*-
# IDE: PyCharm 2017.2.4
# Author: Dajiang Ren<rendajiang@gagogroup.com>
# Created on 2018-10-08


from gagospecs.v1.base.generator import GMDGenerator
from gagospecs.v1.models.original.NDVI import NDVIModel
from gagospecs.v1.schemas.original.NDVI import NDVISchema


class NDVIGMDGenerator(GMDGenerator):
    def __init__(self):
        super().__init__(
            'NDVIProductGenerator'
        )

    def generate(
            self,
            ndvi_model: NDVIModel
    ) -> (str, dict):
        schema: NDVISchema = NDVISchema()
        return schema.dumps(ndvi_model)


def main():
    return NDVIGMDGenerator()
