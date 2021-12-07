from flask import Blueprint, request, session
from flask.templating import render_template
from werkzeug.utils import redirect
from database import db
api = Blueprint('api',__name__)

@api.route('/mail/<id>')
def getMailbyId(id : str = ""):
    return render_template('getMail.html',data=db.getMailById(id,session['user']))

@api.route('/sendmail', methods=['POST'])
def sendmail():
    id, idreceive,header,content = session['user'], request.form['id'], request.form['header'], request.form['content']
    print(id)
    result = db.sendmail(id, idreceive,header,content)
    print(result)
    return redirect('/mail')

@api.route('/editStaff',methods=['POST'])
def editStaff():
    if not request.form['id']:
        return {'isSuccess':'Vui lòng nhập mã nhân viên'}
    if not request.form['name']:
        return {'isSuccess':'Vui lòng nhập họ tên'}
    if not request.form['email']:
        return {'isSuccess':'Vui lòng nhập email'}
    if not request.form['salary']:
        return {'isSuccess':'Vui lòng nhập lương'}
    id,name,email,salary = request.form['id'],request.form['name'],request.form['email'],request.form['salary']    
    result = db.editStaff(id,name,email,salary) 
    return { 'isSuccess':result}

@api.route('/addStaff',methods=['POST'])
def addStaff():
    if not request.form['id']:
        return {'isSuccess':'Vui lòng nhập mã nhân viên'}
    if not request.form['name']:
        return {'isSuccess':'Vui lòng nhập họ tên'}
    if not request.form['email']:
        return {'isSuccess':'Vui lòng nhập email'}
    if not request.form['salary']:
        return {'isSuccess':'Vui lòng nhập lương'}
    if not request.form['username']:
        return {'isSuccess':'Vui lòng nhập tên đăng nhập'}
    if not request.form['password']:
        return {'isSuccess':'Vui lòng nhập mật khẩu'}       
    return { 'isSuccess':db.addStaff(request.form['id'],request.form['name'],request.form['email'],request.form['salary'],request.form['username'],request.form['password']   )}

@api.route('/addClass',methods=['POST'])
def addClass():
    if not request.form['id']:
        return {'isSuccess':'Vui lòng nhập mã lớp'}
    if not request.form['name']:
        return {'isSuccess':'Vui lòng nhập tên lớp'}
    if not request.form['idStaff']:
        return {'isSuccess':'Vui lòng nhập mã nhân viên'}
    return {'isSuccess':db.addClass(request.form['id'],request.form['name'],request.form['idStaff'])}

@api.route('/addStudent',methods=['POST'])
def addStudent():
    if not request.form['id']:
        return {'isSuccess':'Vui lòng nhập mã sinh viên'}
    if not request.form['name']:
        return {'isSuccess':'Vui lòng nhập tên học sinh'}
    return {'isSuccess':db.addStudent(request.form['id'], request.form['name'], request.form['birthday'] or None,request.form['address'] or None,request.form['idClass'] or None)}

@api.route('/addSubject',methods=['POST'])
def addSubject():
    if not request.form['id']:
        return {'isSuccess':'Vui lòng nhập mã học phần'}
    if not request.form['name']:
        return {'isSuccess':'Vui lòng nhập tên học phần'}
    id,name,sotc = request.form['id'], request.form['name'], request.form['sotc'] or None
    try:
        if sotc!=None:
            sotc = int(sotc)
            if sotc<0:
                return {'isSuccess':'Số tín chỉ không hợp lệ, vui lòng nhập lại'}
    except:
        return {'isSuccess':'Số tín chỉ không hợp lệ, vui lòng nhập lại'}
    return {'isSuccess':db.addSubject(id,name,sotc)}

@api.route('/editClass',methods=['POST'])
def editClass():
    if not request.form['id']:
        return {'isSuccess':'Vui lòng nhập mã lớp'}
    if not request.form['name']:
        return {'isSuccess':'Vui lòng nhập tên lớp'}
    if not request.form['idStaff']:
        return {'isSuccess':'Vui lòng nhập mã nhân viên'}
    return { 'isSuccess':db.editClass(request.form['id'],request.form['name'],request.form['idStaff'] )}

@api.route('/editSubject',methods=['POST'])
def editSubject():
    if not request.form['id']:
        return {'isSuccess':'Vui lòng nhập mã học phần'}
    if not request.form['name']:
        return {'isSuccess':'Vui lòng nhập tên học phần'}
    return { 'isSuccess':db.editSubject(request.form['id'], request.form['name'], request.form['sotc'] or None)}

@api.route('/editStudent',methods=['POST'])
def editStudent():
    if not request.form['idStudent']:
        return {'isSuccess':'Vui lòng nhập sinh viên'}
    if not request.form['name']:
        return {'isSuccess':'Vui lòng nhập họ tên'}
    if not request.form['birthday']:
        return {'isSuccess':'Vui lòng nhập ngày sinh'}
    if not request.form['address']:
        return {'isSuccess':'Vui lòng nhập địa chỉ'}
    if not request.form['idClass']:
        return {'isSuccess':'Vui lòng nhập mã lớp'}
    return {'isSuccess':db.editStudent(request.form['idStudent'], request.form['name'], request.form['birthday'], request.form['address'], request.form['idClass']  )}

@api.route('/delClass',methods=['POST'])
def delClass():
    id = request.form['id'] or None
    if id == None:
        return {'isSuccess':'Vui lòng nhập mã lớp'}
    return {'isSuccess':db.delClass(id)}

@api.route('/delStudent',methods=['POST'])
def delStudent():
    id = request.form['id'] or None
    if id == None:
        return {'isSuccess':'Vui lòng nhập mã sinh viên'}
    return {'isSuccess':db.delStudent(id)}

@api.route('/delStaff',methods=['POST'])
def delStaff():
    id = request.form['id'] or None
    if id == None:
        return {'isSuccess':'Vui lòng nhập mã nhân viên'}
    return {'isSuccess':db.delStaff(id)}    

@api.route('/delSubject',methods=['POST'])
def delSubject():
    id = request.form['id'] or None
    if id == None:
        return {'isSuccess':'Vui lòng nhập mã học phần'}
    return {'isSuccess':db.delSubject(id)}        