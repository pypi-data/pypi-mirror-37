# -*- coding: utf-8 -*-
from __future__ import absolute_import, print_function, division
import os
import sys
import logging
import json
from functools import wraps
import scrapy
from .models import BaseModel, Column, INTEGER, String
import unittest


class ItemModel(BaseModel):
    __table_args__ = {"useexisting": True}
    __tablename__ = 'data_article_dxy'
    id = Column(INTEGER, primary_key=True, autoincrement=True)
    name = Column(String(300), nullable=False)


class Item(scrapy.Item):
    id = scrapy.Field()
    name = scrapy.Field()


class TestModel(unittest.TestCase):

    def test_init(self):
        item = Item(id=100, name="aaa")
        kwargs = {"id": 1000}
        model = ItemModel.save(item, **kwargs)
        print(model.__dict__)
        self.assertEqual(1000, model.id)
        self.assertEqual("aaa", model.name)


if __name__ == '__main__':
    unittest.main()

