# -*- coding: utf-8 -*-
# @Time : 2018/4/11 14:53
# @Author : csk
# @FileName: forms.py
# @log:
import time
from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, IntegerField, SelectField,\
    SubmitField, SelectMultipleField, DateTimeField, FloatField
from wtforms.validators import DataRequired, Length, Email, Regexp, NumberRange
from wtforms import ValidationError
from flask_pagedown.fields import PageDownField
from ..models import Role, User, Movie, MovieGenre



class AskForm(FlaskForm):
    rate = FloatField('最小评分[必选]', validators=[DataRequired(), NumberRange(7, 10, message="请输入7-10的评分")])
    date = IntegerField('上映时间(输入年份数字)',default=1900,validators=[NumberRange(1900,2020)])
    runtime = IntegerField('影片时长(分钟)',default=0)
    # genre = SelectMultipleField('影片类型', default=['1'],
    #                             choices=[(str(index), value) for index, value in enumerate(MovieGenre.movie_genre)])
    # director = TextAreaField('导演')
    # cast = TextAreaField('主演')
    # name = TextAreaField('影片名称(仅支持中文名)')
    submit = SubmitField('查询')


    def validate_runtime(self, field):
        print('runtime', field.data)
        if field.data is None:
            return
        elif field.data < 0 or field.data > 300:
            raise ValidationError('请输入0-300的数字')


class CommentForm(FlaskForm):
    body = StringField('Enter your comment', validators=[DataRequired()])
    submit = SubmitField('Submit')


class PostForm(FlaskForm):
    body = PageDownField("谈谈你的想法", validators=[DataRequired()])
    submit = SubmitField('Submit')
