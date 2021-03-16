from flask import Blueprint,render_template,flash,redirect,url_for,request
from flask_login import login_user,logout_user,login_required,current_user
from myblog.forms import LoginForm
from myblog.models import Admin,User
from myblog.utils import redirect_back,generate_token,validate_token
from myblog.settings import Operations
from myblog.emails import send_confirm_email

auth_bp=Blueprint('auth',__name__)


@auth_bp.route('/login',methods=['GET','POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('blog.index'))
    form=LoginForm()
    if form.validate_on_submit():
        username=form.username.data
        password=form.password.data
        remember=form.remember.data
        admin=Admin.query.first()
        if admin:
            if username==admin.username and admin.validate_password(password):
                login_user(admin,remember)
                flash('welcome back','info')
                return redirect_back()
            flash('Invalid username or password','warning')
        else:
            flash('no account','warning')
    return render_template('auth/login.html',form=form)

@auth_bp.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Logout success ','info')
    return redirect_back()


@auth_bp.route("/register",methods=["POST","GET"])
def register():
    if current_user.is_authenticated:
        return redirect_back()
    if request.method=="POST":
        name=request.form.get("name")
        password=request.form.get("password")
        email=request.form.get("email")
        user=User(name=name,email=email)
        user.set_password(password)
        flash("注册成功")
        return redirect_back()

    return render_template("auth/register.html")


@auth_bp.route("/confirm/<token>")
def confirm(token):
    if current_user.is_authenticated:
        return redirect(url_for("blog.index"))

    if validate_token(user=current_user, token=token, operation=Operations.CONFIRM):
        flash("账户验证成功","success")
        return redirect(url_for("blog.index"))

    else:
        flash("Invalid or expired token", "danger")
        return redirect(url_for("auth.resend_confirm"))

@auth_bp.route("/resend_confirm")
def resend_confirm():
    if current_user.is_authenticated:
        return redirect(url_for("blog.index"))

    token = generate_token(user=current_user, operation=Operations.CONFIRM)
    send_confirm_email(user=current_user, token=token)
    flash("新的验证邮件已发送", "info")
    return redirect(url_for("blog.index"))