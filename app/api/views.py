# -*- coding: utf-8 -*-
# @Time : 2018/4/11 14:53
# @Author : csk
# @FileName: views.py
# @log:
from flask import  abort, flash, request,\
    current_app, make_response, jsonify
from flask_login import login_required, current_user
from . import api
from .. import db
from ..models import Permission, Role, User, Comment, Movie, Wish
from ..utils import log
# from ..decorators import admin_required, permission_required


@api.route('movie/wanna' , methods=['POST'])
@login_required
def wish():
    form = request.get_json()
    movie_id = int(form['id'])
    movie = Movie.query.filter_by(id=movie_id).first()
    if movie is None:
        d = dict(
            message='影片已经被删除了...'
        )
        return jsonify(d)
    if current_user.is_seen(movie) or current_user.is_wishing(movie):
        d = dict(
            message='影片已经在你的清单里'
        )
        return jsonify(d)
    current_user.wish(movie)
    d = dict(
        message='已想看'
    )
    return jsonify(d)


@api.route('movie/swift/<status>', methods=["POST"])
@login_required
def swift(status):
    form = request.get_json()
    movie_id = int(form['id'])
    w = Wish.query.filter_by(movie_id=movie_id).first_or_404()
    if not w:
        d = dict(
            message='没找到'
        )
    else:
        w.seen = 0 if status=='seen' else 1
        db.session.add(w)
        db.session.commit()
        d = dict(
            message='已转换'
        )
    return jsonify(d)


@api.route('movie/seen', methods=["POST"])
@login_required
def seen():
    form = request.get_json()
    movie_id = int(form['id'])
    movie = Movie.query.filter_by(id=movie_id).first()
    if movie is None:
        d = dict(
            message='影片已经被删除了...'
        )
        return jsonify(d)
    if current_user.is_seen(movie) or current_user.is_wishing(movie):
        d = dict(
            message='影片已经在你的清单里'
        )
        return jsonify(d)
    current_user.seen(movie)
    d = dict(
        message='已看过'
    )
    return jsonify(d)


@api.route('movie/remove', methods=["POST"])
@login_required
def remove():
    form = request.get_json()
    movie_id = int(form['id'])
    w = Wish.query.filter_by(movie_id=movie_id).first()
    if w:
        db.session.delete(w)
        db.session.commit()
        d = dict(
            message='已删除'
        )
    else:
        d = dict(
            message='没找到'
        )
    return jsonify(d)