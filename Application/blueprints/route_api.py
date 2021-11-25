from flask import Blueprint, request, session
from flask.templating import render_template
from database import db
api = Blueprint('api',__name__)

@api.route('/mail/<id>')
def getMailbyId(id : str = ""):
    return render_template('getMail.html',data=db.getMailById(id,session['user']))

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

    data = db.getStaffById(id)

    result = db.editStaff(id,name,email,salary) 

    db.appendHistory(f'Người dùng {session["user"]} thay đổi thông tin nhân viên có mã là {id}',f"""{data[0]} -> {name},{data[1]} -> {email},{data[2]} -> {salary} """,result)
    
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
   
    id,name,email,salary,username,password = request.form['id'],request.form['name'],request.form['email'],request.form['salary'],request.form['username'],request.form['password']   
   
    result = db.addStaff(id,name,email,salary,username,password)
    
    db.appendHistory(f'Người dùng {session["user"]} thêm nhân viên mới',f"""Mã nhân viên: {id}, họ tên: {name}, email: {email}, lương: {salary}, tên đăng nhập {username}, mật khẩu {password} """,result)

    return { 'isSuccess':result}

@api.route('/addClass',methods=['POST'])
def addClass():
    if not request.form['id']:
        return {'isSuccess':'Vui lòng nhập mã lớp'}

    if not request.form['name']:
        return {'isSuccess':'Vui lòng nhập tên lớp'}

    if not request.form['idStaff']:
        return {'isSuccess':'Vui lòng nhập mã nhân viên'}
  
    id,name,idStaff = request.form['id'],request.form['name'],request.form['idStaff']
  
    result = db.addClass(id,name,idStaff)
  
    db.appendHistory(f'Người dùng {session["user"]} thêm lớp mới',f"""Mã lớp: {id}, tên lớp: {name}, mã nhân viên: {idStaff} """,result)
  
    return {'isSuccess':result}

@api.route('/editClass',methods=['POST'])
def editClass():
    if not request.form['id']:
        return {'isSuccess':'Vui lòng nhập mã lớp'}

    if not request.form['name']:
        return {'isSuccess':'Vui lòng nhập tên lớp'}

    if not request.form['idStaff']:
        return {'isSuccess':'Vui lòng nhập mã nhân viên'}

    id,name,idStaff = request.form['id'],request.form['name'],request.form['idStaff'] 

    data  = db.getClassById(id)

    result = db.editClass(id,name,idStaff)

    db.appendHistory(f'Người dùng {session["user"]} thay đổi thông tin lớp học có mã {id}',f"""{data[0]} -> {name},{data[1]} -> {idStaff} """,result)

    return { 'isSuccess':result}

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
  
    id,name,birthday,address,idClass =  request.form['idStudent'], request.form['name'], request.form['birthday'], request.form['address'], request.form['idClass']  
  
    data = db.getStudentById(id)
  
    result = db.editStudent(id,name,birthday,address,idClass)
  
    db.appendHistory(f'Người dùng {session["user"]} thay đổi thông tin sinh viên có mã {id}',f"""{data[0]} -> {name}, {data[1]} -> {birthday}, {data[2]}->{address}, {data[3]}->{idClass} """,result)
    return {'isSuccess':result}
