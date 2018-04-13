# -*- coding: utf-8 -*-
# @Time : 2018/4/11 14:53
# @Author : csk
# @FileName: __init__.py
# @log:

from flask import Blueprint

main = Blueprint('main', __name__)

from . import views, errs

