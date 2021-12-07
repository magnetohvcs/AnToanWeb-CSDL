from flask import request, render_template, Flask, redirect, session
import re,  requests, json, logging, config
from config import * 
from flask_wtf.csrf import CSRFProtect, CSRFError
from blueprints.routes import web, db
from blueprints.route_api import api
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from flask_mail import Mail, Message

app = Flask(__name__) 
app.config.from_object('config.Config')
app.config.from_object('config.ReCaptcha') 
app.config.from_object('config.Mail')

csrf = CSRFProtect(app)
mail= Mail(app)

app.register_blueprint(api, url_prefix='/api')
app.register_blueprint(web, url_prefix='/')

pub_key = app.config['RECAPTCHA_PUBLIC_KEY']
private_key = app.config['RECAPTCHA_PRIVATE_KEY']

@app.errorhandler(CSRFError)
def csrf_error(reason):
    return render_template('error.html',error='Detect CSRF', reason=reason)

@app.before_request
def intercept():
    if re.match(regexPath,request.path):
        pass
    else:
        if 'user' not in session:
            return redirect('/login')
    if re.match(regexPathAdmin,request.path):
        if session['role'] !='admin':
            return render_template('error.html',error='Permission denied',reason='Bạn không có quyền truy cập'), 403
    
@app.errorhandler(404)
def page_not_found(e):
    return render_template('error.html',error='404',reason=e), 404

@app.errorhandler(500)
def page_fail(e):
    return render_template('500.html'), 500

limiter = Limiter(
    app, 
    key_func=get_remote_address, 
    default_limits=["1000 per hour"]
)
@limiter.limit("2/second", override_defaults=True)
@app.route('/login',methods=['GET','POST'])
def login():
    if request.method=='GET':
        return render_template('login.html',pub_key=pub_key)
    captcha_response = request.form['g-recaptcha-response'] or None
    if captcha_response==None:
        return render_template('login.html',error='Nhập mã xác thực',pub_key=pub_key)   
    if not is_human(captcha_response):
        return render_template('login.html',error='Bạn không phải là người',pub_key=pub_key)      
    if not request.form['username'] or not request.form['password']:
        return render_template('login.html',error="Vui lòng nhập tên đăng nhập và mật khẩu",pub_key=pub_key)
    user,passwd =  request.form['username'] , request.form['password']  
    username,role = db.login(user,passwd)
    db.appendHistory('Đăng nhập',"exec sp_login '%s','%s'"%(user,passwd),username!=None)
    if username==None:
        return render_template('login.html',error="Đăng nhập thất bại",pub_key=pub_key)
    session['user'] = username
    session['role'] = role
    return redirect('/')

def is_human(captcha_response):
    payload = {'response':captcha_response, 'secret':private_key}
    response = requests.post('https://google.com/recaptcha/api/siteverify', data=payload)
    response_txt = json.loads(response.text)
    return response_txt['success']

@limiter.limit("2/second", override_defaults=True)
@app.route('/forget',methods=['GET','POST'])
def forget():
    if request.method=='GET':
        return render_template('forget.html',pub_key=pub_key)
    if not request.form['username']:
        return render_template('forget.html',error='Vui lòng nhập tên đăng nhập',pub_key=pub_key)
    captcha_response = request.form['g-recaptcha-response'] or None
    if captcha_response==None:
        return render_template('login.html',error='Nhập mã xác thực',pub_key=pub_key)   
    if not is_human(captcha_response):
        return render_template('login.html',error='Bạn không phải là người',pub_key=pub_key) 
    user = request.form['username']
    email, newpasswd = db.resetpassword(user)
    if email==None:
        return render_template('forget.html',error='không tìm thấy tên đăng nhập',pub_key=pub_key)
    msg = Message('Mật khẩu mới', sender = 'managatoonltw@gmail.com', recipients = [email])
    msg.html = "<p>Xin chào, bạn vừa yêu cầu mật khẩu mới, đây là mật khẩu của bạn: <h3>%s</h3>, vui lòng đổi mật khẩu sau khi đăng nhập</p>"%newpasswd
    mail.send(msg)
    return render_template('forget.html',error='mật khẩu mới đã được gửi vào email của bạn',pub_key=pub_key)

def main(host : str = '127.0.0.1', port : int = 80):
    logging.getLogger().setLevel("DEBUG")
    app.run(host,port,True)

if __name__=="__main__":
    main()    