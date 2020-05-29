from flask import (render_template, url_for, flash,
                   redirect, request, abort, Blueprint)
from flask_login import current_user, login_required
from way import db
from way.models import Article, Resource
from way.recommendations.forms import ArticleForm, ResourceForm

recommendations = Blueprint('recommendations', __name__)


@recommendations.route("/article/new", methods=['GET', 'POST'])
@login_required
def new_article():
    form = ArticleForm()
    if form.validate_on_submit():
        article = Article(title=form.title.data, content=form.content.data, author=current_user, tag=form.tag.data)
        db.session.add(article)
        db.session.commit()
        flash('Article has been created!', 'success')
        return redirect(url_for('users.account'))
    return render_template('add_recommendation.html', title='New Article',
                           form=form, legend='New Article')


@recommendations.route("/article/<int:article_id>")
def article(article_id):
    article = Article.query.get_or_404(article_id)
    return render_template('article.html', title=article.title, article=article)


@recommendations.route("/article/<int:article_id>/update", methods=['GET', 'POST'])
@login_required
def update_article(article_id):
    article = Article.query.get_or_404(article_id)
    if article.author != current_user:
        abort(403)
    form = ArticleForm()
    if form.validate_on_submit():
        article.title = form.title.data
        article.content = form.content.data
        db.session.commit()
        flash('Article has been updated!', 'success')
        return redirect(url_for('recommendations.article', article_id=article.id))
    elif request.method == 'GET':
        form.title.data = article.title
        form.content.data = article.content
    return render_template('add_recommendation.html', title='Update Article',
                           form=form, legend='Update Article')


@recommendations.route("/article/<int:article_id>/delete", methods=['POST'])
@login_required
def delete_article(article_id):
    article = Article.query.get_or_404(article_id)
    if article.author != current_user:
        abort(403)
    db.session.delete(article)
    db.session.commit()
    flash('Article has been deleted!', 'success')
    return redirect(url_for('users.account'))


@recommendations.route("/resource/new", methods=['GET', 'POST'])
@login_required
def add_resource():
    form = ResourceForm()
    if form.validate_on_submit():
        resource = Resource(title=form.title.data, link=form.content.data, author=current_user, tag=form.tag.data)
        db.session.add(resource)
        db.session.commit()
        flash('Resource has been added!', 'success')
        return redirect(url_for('users.account'))
    return render_template('add_recommendation.html', title='Add Resource',
                           form=form, legend='Add Resource')


@recommendations.route("/resource/<int:resource_id>")
def resource(resource_id):
    resource = Resource.query.get_or_404(resource_id)
    return render_template('resource.html', title=resource.title, resource=resource)


@recommendations.route("/resource/<int:resource_id>/update", methods=['GET', 'POST'])
@login_required
def update_resource(resource_id):
    resource = Resource.query.get_or_404(resource_id)
    if resource.author != current_user:
        abort(403)
    form = ResourceForm()
    if form.validate_on_submit():
        resource.title = form.title.data
        resource.link = form.content.data
        db.session.commit()
        flash('Resource has been updated!', 'success')
        return redirect(url_for('recommendations.resource', resource_id=resource.id))
    elif request.method == 'GET':
        form.title.data = resource.title
        form.content.data = resource.link
    return render_template('add_recommendation.html', title='Update Resource',
                           form=form, legend='Update Resource')


@recommendations.route("/article/<int:resource_id>/delete", methods=['POST'])
@login_required
def delete_resource(resource_id):
    resource = Resource.query.get_or_404(resource_id)
    if resource.author != current_user:
        abort(403)
    db.session.delete(resource)
    db.session.commit()
    flash('Resource has been deleted!', 'success')
    return redirect(url_for('users.account'))
