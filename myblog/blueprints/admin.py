from flask import send_from_directory,current_app,Blueprint,flash,redirect,url_for,render_template,request,abort,request
from flask_login import login_required,current_user
from myblog.forms import SettingForm,PostForm,CategoryForm,LinkForm
from myblog.extensions import db
from myblog.models import Post,Category,Link
from myblog.utils import redirect_back,allowed_file,get_json
from flask_ckeditor import upload_fail,upload_success
import os


admin_bp=Blueprint('admin',__name__)

@admin_bp.route('/settings',methods=['GET','POST'])
@login_required
def settings():
    form=SettingForm()
    if form.validate_on_submit():
        current_user.name=form.name.data
        current_user.blog_title=form.blog_title.data
        current_user.blog_sub_title=form.blog_sub_title.data
        current_user.about=form.about.data
        db.session.commit()
        flash('Setting updated','successs')
        return redirect(url_for('blog.index'))
    form.name.data=current_user.name
    form.blog_title.data=current_user.blog_title
    form.blog_sub_title=current_user.blog_sub_title
    form.about.data=current_user.about
    return render_template('admin/settings.html',form=form)

@admin_bp.route('/post/manage')
@login_required
def manage_post():
    page=request.args.get('page',1,type=int)
    pagination=Post.query.order_by(Post.timestamp.desc()).paginate(
        page,per_page=current_app.config['BLUELOG_MANAGE_POST_PER_PAGE']
    )
    posts=pagination.items
    return render_template('admin/manage_post.html',page=page,pagination=pagination,posts=posts)

@admin_bp.route('/post/new',methods=['GET','POST'])
@login_required
def new_post():
    form=PostForm()
    if form.validate_on_submit():
        title=form.title.data
        body_editormd=form.body_editormd.data
        category=Category.query.get(form.category.data)
        post=Post(title=title,body=body_editormd,category=category)
        db.session.add(post)
        db.session.commit()
        flash('Post created','sucess')
        return redirect(url_for('blog.show_post',post_id=post.id))
    return render_template('admin/new_post.html',form=form)

@admin_bp.route('/post/<int:post_id>/edit',methods=['GET','POST'])
@login_required
def edit_post(post_id):
    form=PostForm()
    post=Post.query.get_or_404(post_id)
    if form.validate_on_submit():
        post.title=form.title.data
        post.body=form.title.data
        post.category=Category.query.get(form.category.data)
        db.session.commit()
        flash('Post updated','success')
        return redirect(url_for('blog.show_post', post_id=post.id))
    form.title.data=post.title
    form.body_editormd.data=post.body
    form.category.data=post.category.id
    return render_template('admin/edit_post.html',form=form)

@admin_bp.route('/post/<int:post_id>/delete',methods=['GET','POST'])
@login_required
def delete_post(post_id):
    post=Post.query.get_or_404(post_id)
    db.session.delete(post)
    db.session.commit()
    flash('Post deleted','sucess')
    return redirect_back()



@admin_bp.route('/category/manage')
@login_required
def manage_category():
    return render_template('admin/manage_category.html')

@admin_bp.route('/category/new',methods=['GET','POST'])
@login_required
def new_category():

    if request.method=="POST":
        name=request.form.get("name");
        icon=request.form.get("icon_name")

        if not name or Category.query.filter_by(name=name).first():
            abort(404)
        category=Category(name=name,icon=icon)
        db.session.add(category)
        db.session.commit()
        return redirect(url_for("blog.index"))

    basedir=os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
    icons=get_json(basedir+"\\static\\icons.json")

    return render_template('admin/new_category.html',icons=icons)

@admin_bp.route('/category/<int:category_id>/edit',methods=['GET','POST'])
@login_required
def edit_category(category_id):

    category=Category.query.get_or_404(category_id)
    if category.id==1:
        flash('you can not edit the default category','warning')
        return redirect(url_for('blog.index'))
    if request.method=="POST":
        name=request.form.get("name");
        icon=request.form.get("icon_name")

        if not name:
            abort(404)
        category.name=name
        category.icon=icon
        db.session.add(category)
        db.session.commit()
        return redirect(url_for("blog.index"))
    basedir=os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
    icons=get_json(basedir+"\\static\\icons.json")

    return render_template('admin/edit_category.html',icons=icons,category=category)

@admin_bp.route('/category/<int:category_id>/delete',methods=['GET','POST'])
@login_required
def delete_category(category_id):
    category=Category.query.get_or_404(category_id)
    if category.id==1:
        flash("you can not delete the default category")
        return redirect(url_for('blog.index'))
    category.delete()
    flash('Category deleted','success')
    return redirect(url_for('.manage_category'))

@admin_bp.route('/link/mange')
@login_required
def manage_link():
    return render_template('admin/manage_link.html')

@admin_bp.route('/link/new',methods=['GET','POST'])
@login_required
def new_link():
    form=LinkForm()
    if form.validate_on_submit():
        name=form.name.data
        url=form.url.data
        link=Link(name=name,url=url)
        db.session.add(link)
        db.session.commit()
        flash('Link created','success')
        return redirect(url_for('.manage_link'))
    return render_template('admin/new_link.html',form=form)


@admin_bp.route('/link/<int:link_id>/edit',methods=['GET','POST'])
@login_required
def edit_link(link_id):
    form=LinkForm()
    link=Link.query.get_or_404(link_id)
    if form.validate_on_submit():
        link.name=form.name.data
        link.url=form.url.data
        db.session.commit()
        flash('Link updated','success')
        return redirect(url_for('.manage_link'))
    form.name.data=link.name
    form.url.data=link.url
    return render_template('admin/edit_link.html',form=form)

@admin_bp.route('/link/<int:link_id>/delete',methods=['GET','POST'])
@login_required
def delete_link(link_id):
    link=Link.query.get_or_404(link_id)
    db.session.delete(link)
    db.session.commit()
    flash('Link deleted','success')
    return redirect(url_for('.manage_link'))

@admin_bp.route('/uploads/<path:filename>')
def get_image(filename):
    return send_from_directory(current_app.config['BLUELOG_UPLOAD_PATH'],filename)


@admin_bp.route('/upload',methods=['POST'])
@login_required
def upload_image():
    f=request.files.get('upload')
    if not allowed_file(f.filename):
        return upload_fail('Image only!')
    f.save(os.path.join(current_app.config['BLUELOG_UPLOAD_PATH'],f.filename))
    url=url_for('.get_image',filename=f.filename)
    return upload_success(url,f.filename)


@admin_bp.route("/upload/file",methods=["POST"])
@login_required
def upload_file():

    title=request.form.get("title")
    category=Category.query.get(request.form.get("category"))
    file=request.files["uploadFile"]
    body=file.read().decode("utf-8")
    print(body)
    if body=="":
        abort(400)
    post=Post(title=title,category=category,body=body)
    db.session.add(post)
    db.session.commit()
    flash("上传成功")
    return redirect(url_for("blog.show_post",post_id=post.id))

@admin_bp.route("upload/files",methods=["POST"])
@login_required
def upload_files():
    files=request.files.items()
    basedir=os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
    if request.method=="POST":
        for key, f in files:
            if key.startswith('file'):
                f.save(os.path.join(basedir,os.path.join("static","files",f.filename)))
        return "上传成功",200
    return "上传失败,请重试",400