import pyodbc, os
from flask import session

generatorPasswd = lambda x: os.urandom(x).hex()
def connect(username : str, password : str , server : str = '10.0.0.20' , database : str = 'QLSVNhom'):              
    cnxn = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server};SERVER='+server+';DATABASE='+database+';UID='+username+';PWD='+ password)
    return cnxn, cnxn.cursor()
    
cnxn, cursor = connect('QLSV_Admin','AdminP@ssword789!') 
cnxn_nv, cursor_nv = connect('QLSV_Nv','NHANVIENP@ssword456!') 
cnxn_login,cursor_login = connect('QLSV_Login','LoginP@ssword123!') 

def getCurrentCursor(role):
    return cursor if role=='admin' else cursor_nv 

def getCurrentCnxn(role):
    return cnxn if role=='admin' else cnxn_nv     

def appendHistory(content : str, detail : str, result : bool):
    try:
        cursor.execute("""Insert into lichsu values(?,?,?,GETDATE())""", content,detail,result)
        cnxn.commit()
        return True        
    except:
        return False 

def getClasses():
    currentCursor = getCurrentCursor(session['role'])
    currentCursor.execute("SELECT * from lophoc") 
    row = currentCursor.fetchone() 
    data = []
    while row: 
        data.append(row)
        row = currentCursor.fetchone()
    return data

def getSubjects():
    currentCursor = getCurrentCursor(session['role'])
    currentCursor.execute("SELECT * from hocphan") 
    row = currentCursor.fetchone() 
    data = []
    while row: 
        data.append(row)
        row = currentCursor.fetchone()
    return data

def getStaffs():
    currentCursor = getCurrentCursor(session['role'])
    currentCursor.execute("""SELECT MANV, HOTEN, EMAIL, cast(N'' as xml).value('xs:base64Binary(sql:column("NHANVIEN.LUONG"))', 'varchar(max)') as LUONG, tendn FROM NHANVIEN""") 
    row = currentCursor.fetchone() 
    data = []
    while row: 
        data.append(row)
        row = currentCursor.fetchone()
    return data

def getStaffById(id : str):
    currentCursor = getCurrentCursor(session['role'])
    currentCursor.execute("""SELECT HOTEN, EMAIL, cast(N'' as xml).value('xs:base64Binary(sql:column("NHANVIEN.LUONG"))', 'varchar(max)') as LUONG FROM NHANVIEN where MANV=?""",id) 
    return currentCursor.fetchone() 

def getSubjectById(id:str):
    currentCursor = getCurrentCursor(session['role'])
    currentCursor.execute("""SELECT tenhp,sotc from hocphan where mahp=?""",id) 
    return currentCursor.fetchone()

def getClassById(id : str):
    currentCursor = getCurrentCursor(session['role'])
    currentCursor.execute("""SELECT tenlop,manv FROM lop where malop=?""",id) 
    return currentCursor.fetchone() 

def getStudentById(id : str):
    currentCursor = getCurrentCursor(session['role'])
    currentCursor.execute("""SELECT hoten,ngaysinh,diachi,malop FROM sinhvien where masv=?""",id) 
    return currentCursor.fetchone()   

def getMailById(id : str, idUser):
    currentCursor = getCurrentCursor(session['role'])
    currentCursor.execute("""SELECT SendFrom,Sendto,header,Contentmail from mail where id=? and (sendfrom=? or sendto=?)""",id,idUser,idUser) 
    return currentCursor.fetchone() 

def login(username : str, password : str):
    cursor_login.execute("exec sp_login ?,?",username,password)
    row = cursor_login.fetchone() 
    try:
        username, idRole = row[1],row[-1]
        cursor_login.execute("select role from role where id=?",idRole)
        role = cursor_login.fetchone()[0]
        return username,role
    except:
        return None, None
 
def sendmail(id, idreceive,header,content):
    role = session['role']
    currentCursor,currentCnxn = getCurrentCursor(role), getCurrentCnxn(role)
    try:
        currentCursor.execute("""Insert into mail(sendfrom,sendto,header,contentmail,time) values(?,?,?,?,GETDATE())""",id, idreceive,header,content)
        currentCnxn.commit()
        result =  True        
    except:
        result =  False 
    appendHistory(f'Người dùng {session["user"]} gửi mail ',f"""Đến: {idreceive}, tiêu đề: {header}, nội dung: {content}""",result)
    return    result

def getHistories():
    currentCursor = getCurrentCursor(session['role'])
    currentCursor.execute("SELECT  * from LichSu order by id desc") 
    row = currentCursor.fetchone() 
    data = []
    while row: 
        data.append(row)
        row = currentCursor.fetchone()
    return data

def getMails(id):
    currentCursor = getCurrentCursor(session['role'])
    currentCursor.execute("SELECT id,SendFrom,Sendto,header,time from mail where SendFrom=? or Sendto=? order by id desc ",id,id) 
    row = currentCursor.fetchone() 
    data = []
    while row: 
        data.append(row)
        row = currentCursor.fetchone()
    return data

def getStudents():
    currentCursor = getCurrentCursor(session['role'])
    currentCursor.execute("SELECT masv,hoten,ngaysinh,diachi,malop from Sinhvien") 
    row = currentCursor.fetchone() 
    data = []
    while row: 
        data.append(row)
        row = currentCursor.fetchone()
    return data

def getClasses():
    currentCursor = getCurrentCursor(session['role'])
    currentCursor.execute("SELECT  * from lop") 
    row = currentCursor.fetchone() 
    data = []
    while row: 
        data.append(row)
        row = currentCursor.fetchone()
    return data

def editClass(id : str, name : str, idStaff : str ) -> bool:
    role = session['role']
    currentCursor,currentCnxn = getCurrentCursor(role), getCurrentCnxn(role)
    data  = getClassById(id)
    try:
        currentCursor.execute("""Update lop set tenlop=?, manv=? where malop=?""", name,idStaff,id)
        currentCnxn.commit()
        result =  True        
    except:
        result = False 
    appendHistory(f'Người dùng {session["user"]} thay đổi thông tin lớp học có mã {id}',f"""{data[0]} -> {name},{data[1]} -> {idStaff} """,result)
    return result

def addClass(id : str, name : str, idStaff : str ) -> bool:
    role = session['role']
    currentCursor,currentCnxn = getCurrentCursor(role), getCurrentCnxn(role)
    try:
        currentCursor.execute("""Insert into lop values(?,?,?)""",id, name,idStaff)
        currentCnxn.commit()
        result =  True        
    except:
        result =  False 
    appendHistory(f'Người dùng {session["user"]} thêm lớp mới',f"""Mã lớp: {id}, tên lớp: {name}, mã nhân viên: {idStaff} """,result)
    return    result

def addSubject(id : str, name : str, sotc : int) -> bool:
    role = session['role']
    currentCursor,currentCnxn = getCurrentCursor(role), getCurrentCnxn(role)
    try:
        currentCursor.execute("""Insert into hocphan values(?,?,?)""",id, name,sotc)
        currentCnxn.commit()
        result =  True        
    except:
        result =  False 
    appendHistory(f'Người dùng {session["user"]} thêm học phần',f"""Mã học phần: {id}, tên học phần: {name}, số tín chỉ: {sotc}""",result)
    return    result

def editSubject(id : str, name : str, sotc : int) -> bool:
    role = session['role']
    currentCursor,currentCnxn = getCurrentCursor(role), getCurrentCnxn(role)
    data = getSubjectById(id)
    if data==None:
        return False
    try:
        currentCursor.execute("""update hocphan set tenhp=?, sotc=? where mahp=?""", name,sotc,id)
        currentCnxn.commit()
        result =  True        
    except:
        result = False 
    appendHistory(f'Người dùng {session["user"]} thay đổi thông tin học phần có mã {id}',f"""Tên học phần: {data[0]} -> {name}, Số tín chỉ: {data[1]} -> {sotc} """,result)
    return result

def editStaff(id : str, name : str, email : str, salary  ) -> bool:
    role = session['role']
    currentCursor,currentCnxn = getCurrentCursor(role), getCurrentCnxn(role)
    data = getStaffById(id)
    try:
        currentCursor.execute("""exec SP_Update_NhanVien ?,?,?,?""",id, name,email,salary)
        currentCnxn.commit()
        result =  True        
    except:
        result =  False 
    appendHistory(f'Người dùng {session["user"]} thay đổi thông tin nhân viên có mã là {id}',f"""{data[0]} -> {name},{data[1]} -> {email},{data[2]} -> {salary} """,result)
    return result

def addStaff(id : str, name : str, email : str, salary : str, username : str,password : str ) -> bool:
    role = session['role']
    currentCursor, currentCnxn = getCurrentCursor(role), getCurrentCnxn(role)
    #try:
    pk = id
    currentCursor.execute("""exec SP_INS_PUBLIC_ENCRYPT_NHANVIEN ?,?,?,?,?,?,?,2""",id, name,email,salary,username,password, pk)
    currentCnxn.commit()
    result = True        
    #except:
        #result = False 
    appendHistory(f'Người dùng {session["user"]} thêm nhân viên mới',f"""Mã nhân viên: {id}, họ tên: {name}, email: {email}, lương: {salary}, tên đăng nhập {username}, mật khẩu {password} """,result)
    return result

def addStudent(id,name,birthday, address,idClass ) -> bool:
    role = session['role']
    currentCursor, currentCnxn = getCurrentCursor(role), getCurrentCnxn(role)
    try:
        currentCursor.execute("""insert into sinhvien values(?,?,?,?,?,?,?)""",id,name,birthday, address,idClass, None,None)
        currentCnxn.commit()
        result = True        
    except:
        result = False 
    appendHistory(f'Người dùng {session["user"]} thêm sinh viên',f"""Mã sinh viên: {id}, họ tên: {name}, ngày sinh: {birthday}, địa chỉ: {address}, mã lớp {idClass} """,result)
    return result

def editStudent(id : str, name : str, birthday : str, address : str, idClass : str) -> bool:
    role = session['role']
    currentCursor,currentCnxn = getCurrentCursor(role), getCurrentCnxn(role)
    data = getStudentById(id)
    try:
        currentCursor.execute("""Update sinhvien set hoten=?, ngaysinh=?,diachi=?,malop=? where masv=?""", name,birthday,address,idClass,id)
        currentCnxn.commit()
        result = True        
    except:
        result = False 
    appendHistory(f'Người dùng {session["user"]} thay đổi thông tin sinh viên có mã {id}',f"""{data[0]} -> {name}, {data[1]} -> {birthday}, {data[2]}->{address}, {data[3]}->{idClass} """,result)
    return result              

def delClass(id):
    role = session['role']
    currentCursor, currentCnxn = getCurrentCursor(role), getCurrentCnxn(role)
    try:
        currentCursor.execute("""delete from lop where malop=?""", id)
        currentCnxn.commit()
        result = True        
    except:
        result = False  
    appendHistory(f'Người dùng {session["user"]} xóa lớp có mã là {id}',None,result)
    return result    

def delStudent(id):
    idNv, role = session['user'], session['role']
    currentCursor,currentCnxn = getCurrentCursor(role), getCurrentCnxn(role)
    if role != 'admin':
        try:
            currentCursor.execute("""select MANV from SINHVIEN, lop where masv=? and SINHVIEN.MALOP=lop.MALOP""", id)
            idNv_ = currentCursor.fetchone()[0], None
            if idNv_ != idNv:
                appendHistory(f'Người dùng {session["user"]} xóa sinh viên có mã là {id}',"Không có quyền xóa",False)
                return False
        except:
            appendHistory(f'Người dùng {session["user"]} xóa sinh viên có mã là {id}',"Không có quyền xóa",False)
            return False
    try:
        currentCursor.execute("""delete from sinhvien where masv=?""", id)
        currentCnxn.commit()
        result = True        
    except:
        result = False 
    appendHistory(f'Người dùng {session["user"]} xóa sinh viên có mã là {id}',None,result)
    return result

def delStaff(id):
    role =  session['role']
    result = False
    if id != 'admin':
        currentCursor,currentCnxn = getCurrentCursor(role), getCurrentCnxn(role)
        try:
            currentCursor.execute("""delete from nhanvien where manv=?""", id)
            currentCnxn.commit()
            result = True        
        except:
            result = False 
    appendHistory(f'Người dùng {session["user"]} xóa nhân viên có mã là {id}',result or None,result)        
    return result      

def delSubject(id):
    role =  session['role']
    currentCursor,currentCnxn = getCurrentCursor(role), getCurrentCnxn(role)
    try:
        currentCursor.execute("""delete from hocphan where mahp=?""", id)
        currentCnxn.commit()
        result = True
    except:
        result = False
    appendHistory(f'Người dùng {session["user"]} xóa học phần có mã là {id}',result or None,result)
    return result

def resetpassword(username):
    newpasswd = generatorPasswd(15)
    cursor_login.execute("exec sp_renewpasswd ?,?",username,newpasswd)    
    row = cursor_login.fetchone()
    cnxn_login.commit()
    email = row[0] if row != None else None
    appendHistory('Yêu cầu mật khẩu mới',"exec SP_RenewPasswd '%s','%s'"%(username,newpasswd),email!=None)
    return email, newpasswd

def getAcademyTranscript():
    role = session['role']
    currentCursor,currentCnxn = getCurrentCursor(role), getCurrentCnxn(role)
    currentCursor.execute('select  * from')