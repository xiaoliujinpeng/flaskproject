from flask import Blueprint,render_template,request,current_app,url_for,flash,redirect,abort,make_response
from myblog.models import Post,Category
import os
import base64
from myblog.utils import redirect_back,get_json

blog_bp=Blueprint('blog',__name__)
@blog_bp.route('/')
def index():
    page=request.args.get('page',1,type=int)
    per_page=current_app.config['BLUELOG_POST_PER_PAGE']
    pagination=Post.query.order_by(Post.timestamp.desc()).paginate(page,per_page=per_page)
    posts=pagination.items
    basedir=os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
    icons=get_json(basedir+"\\static\\icons.json")
    return render_template('blog/index.html',pagination=pagination,posts=posts,icons=icons)

@blog_bp.route('/about')
def about():
    return render_template('blog/about.html')

@blog_bp.route('/category/<int:category_id>')
def show_category(category_id):
    category=Category.query.get_or_404(category_id)
    page=request.args.get('page',1,type=int)
    per_page=current_app.config['BLUELOG_POST_PER_PAGE']
    pagination=Post.query.with_parent(category).order_by(Post.timestamp.desc()).paginate(page,per_page)
    posts=pagination.items
    basedir=os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
    icons=get_json(basedir+"\\static\\icons.json")
    return render_template('blog/category.html',category=category,pagination=pagination,posts=posts,icons=icons)

@blog_bp.route("/category/<string:name>")
def show_category_by_name(name):
    category=Category.query.filter_by(name=name).first()
    page=request.args.get("page",1,type=int)
    per_page=current_app.config["BLUELOG_POST_PER_PAGE"]
    pagination=Post.query.with_parent(category).paginate(page,per_page)
    posts=pagination.items
    basedir=os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
    icons=get_json(basedir+"\\static\\icons.json")
    return render_template("blog/category.html",category=category,pagination=pagination,posts=posts,icons=icons)


@blog_bp.route("/post/<string:name>",methods=["GET","POST"])
def show_post_by_name(name):

    post=Post.query.filter_by(title=name).first()
    if post==None:
        abort(404)
    return render_template("blog/post.html",post=post)


@blog_bp.route('/post/<int:post_id>',methods=['GET','POST'])
def show_post(post_id):
    post=Post.query.get_or_404(post_id)
    return render_template('blog/post.html',post=post)


@blog_bp.route('/change-theme/<theme_name>')
def change_theme(theme_name):
    if theme_name not in current_app.config['BLUELOG_THEMES'].keys():
        abort(404)

    response=make_response(redirect_back())
    response.set_cookie('theme',theme_name,max_age=30*24*60*60)
    return response

@blog_bp.route("/filer")
def filer():
    return render_template("blog/filer.html")