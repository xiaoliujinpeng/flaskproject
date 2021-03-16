
from flask import current_app,render_template
from flask_mail import Message
from myblog.extensions import mail
from threading import Thread

def _send_async_mail(app,message):
    with app.app_context():
        mail.send(message)

def send_mail(subject, to, template,**kwargs):
    app=current_app._get_current_object()
    message=Message(subject,recipients=[to])
    message.body=render_template(template+'.txt',**kwargs)
    message.html=render_template(template+'.html',**kwargs)
    app=current_app._get_current_object()
    thr=Thread(target=_send_async_mail,args=[app,message])
    thr.start()
    return thr

def send_confirm_email(user,token,to=None):
    send_mail(subject="Email Confirm",to=to,template="email/confirm",user=user,token=token)

def send_reset_password_email(user,token):
    send_mail(subject="密码重置",to=user.email,template="email/reset_password",user=user,token=token)

