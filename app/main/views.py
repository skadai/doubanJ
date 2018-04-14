# -*- coding: utf-8 -*-
# @Time : 2018/4/11 14:53
# @Author : csk
# @FileName: views.py
# @log:
import uuid
from flask import render_template, redirect, url_for, abort, flash, request,\
    current_app, make_response, jsonify
from flask_login import login_required, current_user
from flask_sqlalchemy import get_debug_queries
from . import main
from .forms import AskForm, PostForm, CommentForm
from .. import db, cache
from ..utils import log
from ..models import Permission, Role, Post, User,  Comment, Movie, Wish
# from ..decorators import admin_required, permission_required


@main.route('/', methods=['GET'])
def index():
    return render_template('index.html')

def make_cache_key(*args, **kwargs):
    """Dynamic creation the request url.
        如果是post方法保证不走缓存，通过uuid来实现
    """

    path = request.path
    if request.method == "POST":
        args = str(uuid.uuid4())
        cookies = " "
    else:
        cookies = str(hash(frozenset(request.cookies.items())))
        args = str(hash(frozenset(request.args.items())))
    log('建立缓存索引', args)
    return (path + args + cookies).encode('utf-8')


@main.route('/search/', methods=('GET', 'POST'))
@cache.cached(timeout=300, key_prefix=make_cache_key)
def search():
    form = AskForm()
    if form.validate_on_submit():
        log('确认提交, POST不走缓存')
        response = make_response(redirect(url_for('.search')))
        # response = make_response('<h1>cookie!</h1>')
        set_cookie(response,
                   runtime=form.runtime.data,
                   rate=form.rate.data,
                   date=form.date.data)
        return response

    rate = request.cookies.get('rate', 10, type=float)
    date = request.cookies.get('date', 1900, type=int)
    runtime = request.cookies.get('runtime', 0, type=int)
    page = request.args.get('page',1, type=int)
    form.runtime.data=runtime
    form.rate.data=rate
    form.date.data=date
    r = Movie.query_movie(rate, date, runtime)
    pagination = r.order_by(Movie.date.desc()).paginate(page,
                            per_page=current_app.config['DOUBANJ_MOVIES_PER_PAGE'],
                            error_out=False)
    movies = pagination.items
    return render_template('movies.html', form=form, movies=movies, pagination=pagination,
                        count=r.count())


@main.route('/user/<username>')
def user(username):
    user = User.query.filter_by(username=username).first_or_404()
    page = request.args.get('page', 1, type=int)
    pagination = user.movietosee.order_by(Wish.seen.desc()).paginate(
        page, per_page=current_app.config['DOUBANJ_MOVIES_PER_PAGE'],
        error_out=False)

    movies = [{'movie': item.movietosee,
               'timestamp': item.timestamp}
               for item in pagination.items]
    return render_template('user.html', user=user, movies=movies,
                           pagination=pagination)


@main.route('/wish/<int:movie_id>')
@login_required
def wish(movie_id):
    movie = Movie.query.filter_by(id=movie_id).first()
    if movie is None:
        flash('影片已经被删除了...')
        return redirect(url_for('.index'))
    if current_user.is_wishing(movie):
        flash('影片已经在你的待阅清单里')
        return redirect(url_for('.search'))
    current_user.wish(movie)
    db.session.commit()
    flash('已经成功加入 %s 到待阅清单!' %movie.name)
    return redirect(url_for('.search'))


@main.route('/seen/<int:movie_id>')
@login_required
def seen(movie_id):
    movie = Movie.query.filter_by(id=movie_id).first()
    if movie is None:
        flash('影片已经被删除了...')
        return redirect(url_for('.index'))
    if current_user.is_seen(movie):
        flash('影片已经在你的阅片清单里')
        return redirect(url_for('.search'))
    current_user.seen(movie)
    db.session.commit()
    flash('已经成功加入 %s 到待阅清单!' %movie.name)
    return redirect(url_for('.search'))


@main.route('/movie/<movie_id>', methods=["GET","POST"])
def movie_profile(movie_id):
    form = PostForm()
    if form.validate_on_submit():
        if not current_user.is_guest():
            post = Post(body=form.body.data,
                        author=current_user._get_current_object(),
                        movie_id = movie_id)
            db.session.add(post)
            db.session.commit()
            return redirect(url_for('.movie_profile', movie_id=movie_id))
        else:
            return redirect(url_for('auth.login'))
    movie = Movie.query.filter_by(id=movie_id).first_or_404()
    wishes = Wish.query.filter_by(movie_id=movie.id)
    users = [{'user': wish.seer, 'timestamp': wish.timestamp } for wish in wishes]
    posts = [post for post in movie.posts.all()]
    return render_template('movie_profile.html', form=form, user=current_user, movie=movie, users=users,
                           posts=posts)


@main.route('/post/<int:id>', methods=['GET', 'POST'])
@login_required
def post(id):
    post = Post.query.get_or_404(id)
    form = CommentForm()
    if form.validate_on_submit():
        comment = Comment(body=form.body.data,
                          post=post,
                          author=current_user._get_current_object())
        db.session.add(comment)
        db.session.commit()
        flash('Your comment has been published.')
        return redirect(url_for('.post', id=post.id, page=-1))
    page = request.args.get('page', 1, type=int)
    if page == -1:
        page = (post.comments.count() - 1) // \
            current_app.config['DOUBANJ_COMMENTS_PER_PAGE'] + 1
    pagination = post.comments.order_by(Comment.timestamp.asc()).paginate(
        page, per_page=current_app.config['DOUBANJ_COMMENTS_PER_PAGE'],
        error_out=False)
    comments = pagination.items
    return render_template('post.html', posts=[post], form=form,
                           comments=comments, pagination=pagination)


@main.route('/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit(id):
    post = Post.query.get_or_404(id)
    if current_user != post.author:
        abort(403)
    form = PostForm()
    if form.validate_on_submit():
        post.body = form.body.data
        db.session.add(post)
        db.session.commit()
        flash('影评已经更新了')
        return redirect(url_for('.post', id=post.id))
    form.body.data = post.body
    return render_template('edit_post.html', form=form)


def set_cookie(response,**kwargs):
    for k, v in kwargs.items():
        value = bytes(str(v),encoding='utf-8')
        response.set_cookie(k,value)



