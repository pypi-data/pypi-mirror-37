#!/usr/bin/env python
# -*- encoding: utf-8 -*-
# IDE: PyCharm 2017.2.4
# Author: Dajiang Ren<rendajiang@gagogroup.com>
# Created on 2018-10-07


from logging import Logger, getLogger


class SpecBase:
    def __init__(
            self,
            name: str
    ):
        self.name: str = name
        self.logger: Logger = getLogger(self.name)
