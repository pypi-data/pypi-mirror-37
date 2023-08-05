#!/usr/bin/env python
# -*- encoding: utf-8 -*-
# IDE: PyCharm 2017.2.4
# Author: Dajiang Ren<rendajiang@gagogroup.com>
# Created on 2018-10-15


import struct

from osgeo import gdal

from gagospecs.v1.base.converter import Converter


class NDVIConverter(Converter):
    def __init__(self):
        super().__init__('ndvi')

    def convert(
            self,
            src_ndvi_tiff_path: str,
            dst_ndvi_tiff_path: str
    ):
        """
        按照佳格NDVI原始级数据产品规范要求，转换一幅普通NDVI产品
        :param src_ndvi_tiff_path: 源NDVI栅格数据，按照常用数据类型存放
        :param dst_ndvi_tiff_path: 目标NDVI栅格数据，按照佳格NDVI规范存放
        :return: None
        """
        gdal.AllRegister()

        src_ds: gdal.Dataset = gdal.Open(
            src_ndvi_tiff_path,
            gdal.OF_READONLY
        )
        tiff_driver: gdal.Driver = gdal.GetDriverByName('GTiff')
        dst_ds: gdal.Dataset = tiff_driver.Create(
            dst_ndvi_tiff_path,
            src_ds.RasterXSize,
            src_ds.RasterYSize,
            1,
            gdal.GDT_Byte
        )
        dst_ds.SetProjection(src_ds.GetProjection())
        dst_ds.SetGeoTransform(src_ds.GetGeoTransform())

        src_band: gdal.Band = src_ds.GetRasterBand(1)
        src_data_type = src_band.DataType
        src_data_type_name = gdal.GetDataTypeName(src_data_type)
        src_data_length = int(gdal.GetDataTypeSize(src_data_type) / 8)
        dst_band: gdal.Band = dst_ds.GetRasterBand(1)

        byte_count_per_row = src_data_length * src_band.XSize
        for row_index in range(src_band.YSize):
            data: bytes = src_band.ReadRaster(
                0,
                row_index,
                src_band.XSize,
                1
            )
            l: int = len(data)
            start_index: int = 0
            dst_data_list: list = list()
            while True:
                src_ndvi_value, = struct.unpack(
                    'f',
                    data[start_index:start_index + src_data_length]
                )
                src_ndvi_value: float = src_ndvi_value
                if src_ndvi_value > 1 or src_ndvi_value < -1:
                    print('invalid ndvi value: %f' % src_ndvi_value)
                dst_ndvi_value: int = int(src_ndvi_value * 127 + 126)
                dst_data_list.append(dst_ndvi_value)
                start_index += src_data_length
                if start_index >= byte_count_per_row:
                    break

            dst_data = struct.pack(
                '%dB' % len(dst_data_list),
                *dst_data_list
            )
            dst_ds.WriteRaster(
                0,
                row_index,
                src_band.XSize,
                1,
                dst_data
            )
