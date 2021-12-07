from flask import Blueprint, request, session, render_template, redirect
from database import db

web = Blueprint('web',__name__)

@web.route('/', methods=['GET'])
@web.route('/index',methods=['GET'])
def index():
    if session['role']!='admin':
        return redirect('/student')
    return redirect('/admin')

@web.route('/admin', methods=['GET'])
def admin():
    return render_template('admin.html',data=db.getHistories())
       
@web.route('/student',methods=['GET'])
def students():
    return render_template('students.html',data=db.getStudents())

@web.route('/staff',methods=['GET'])
def staffs():
    return render_template('staff.html',data=db.getStaffs())

@web.route('/class',methods=['GET'])
def classes():
    return render_template('class.html',data=db.getClasses())

@web.route('/mail',methods=['GET'])
def mail():
    return render_template('mail.html',data=db.getMails(session['user']))

@web.route('/subject',methods=['GET'])
def subject():
    return render_template('subject.html',data=db.getSubjects())

@web.route('/signout')
def logout():
    session['user']=None
    return redirect('/login')