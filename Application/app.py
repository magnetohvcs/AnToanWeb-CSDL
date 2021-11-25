from flask import request, render_template, Flask, redirect, session
import re
from config import * 
from flask_wtf.csrf import CSRFProtect, CSRFError
from blueprints.routes import web, db
from blueprints.route_api import api
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address


app = Flask(__name__) 
app.config.from_object('config.Config')
csrf = CSRFProtect(app)

app.register_blueprint(api, url_prefix='/api')
app.register_blueprint(web, url_prefix='/')

@app.errorhandler(CSRFError)
def csrf_error(reason):
    return render_template('csrf.html', reason=reason)

@app.before_request
def intercept():
    if re.match(regexPath,request.path):
        pass
    else:
        try:
            session['user']
        except:
            return redirect('/login')

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

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
        return render_template('login.html')

    if not request.form['username'] or not request.form['password']:
        return render_template('login.html',error="Vui lòng nhập tên đăng nhập và mật khẩu")

    user,passwd =  request.form['username'] , request.form['password']  
    username = db.login(user,passwd)

    db.appendHistory('Đăng nhập',"exec sp_login '%s','%s'"%(user,passwd),username!=None)

    if username==None:
        return render_template('login.html',error="Đăng nhập thất bại")

    session['user'] = username
    return redirect('/')

def main(host : str = 'localhost', port : int = 80):
    app.secret_key =  app.config['SECRET_KEY'] 
    app.run(host,port,True)

if __name__=="__main__":
    main()    