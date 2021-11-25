import pyodbc


def connect(username : str, password : str , server : str = '127.0.0.1' , database : str = 'QLSVNhom'):    
    cnxn = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server};SERVER='+server+';DATABASE='+database+';UID='+username+';PWD='+ password)
    return cnxn, cnxn.cursor()

cnxn, cursor = connect('sa','123456')

def appendHistory(content : str, detail : str, result : bool):
    try:
        cursor.execute("""Insert into lichsu values(?,?,?,GETDATE())""", content,detail,result)
        cnxn.commit()
        return True        
    except:
        return False 

def getClasses():
    cursor.execute("SELECT * from lophoc") 
    row = cursor.fetchone() 
    data = []
    while row: 
        data.append(row)
        row = cursor.fetchone()
    return data

def getStaffs():
    cursor.execute("""SELECT MANV, HOTEN, EMAIL, cast(N'' as xml).value('xs:base64Binary(sql:column("NHANVIEN.LUONG"))', 'varchar(max)') as LUONG, tendn FROM NHANVIEN""") 
    row = cursor.fetchone() 
    data = []
    while row: 
        data.append(row)
        row = cursor.fetchone()
    return data

def getStaffById(id : str):
    cursor.execute("""SELECT HOTEN, EMAIL, cast(N'' as xml).value('xs:base64Binary(sql:column("NHANVIEN.LUONG"))', 'varchar(max)') as LUONG FROM NHANVIEN where MANV=?""",id) 
    return cursor.fetchone() 
    

def getClassById(id : str):
    cursor.execute("""SELECT tenlop,manv FROM lop where malop=?""",id) 
    return cursor.fetchone() 

def getStudentById(id : str):
    cursor.execute("""SELECT hoten,ngaysinh,diachi,malop FROM sinhvien where masv=?""",id) 
    return cursor.fetchone()   

def getMailById(id : str, idUser):
    cursor.execute("""SELECT SendFrom,Sendto,header,Contentmail from mail where id=? and (sendfrom=? or sendto=?)""",id,idUser,idUser) 
    return cursor.fetchone() 

def login(username : str, password : str):
    cursor.execute("exec sp_login ?,?",username,password) 
    row = cursor.fetchone() 
    try:
        return row[0]
    except:
        return None   # null 
 
def getHistories():
    cursor.execute("SELECT  * from LichSu order by id desc") 
    row = cursor.fetchone() 
    data = []
    while row: 
        data.append(row)
        row = cursor.fetchone()
    return data

def getMails(id):
    cursor.execute("SELECT id,SendFrom,Sendto,header,time from mail where SendFrom=? or Sendto=? order by id desc ",id,id) 
    row = cursor.fetchone() 
    data = []
    while row: 
        data.append(row)
        row = cursor.fetchone()
    return data

def getStudents():
    cursor.execute("SELECT masv,hoten,ngaysinh,diachi,malop from Sinhvien") 
    row = cursor.fetchone() 
    data = []
    while row: 
        data.append(row)
        row = cursor.fetchone()
    return data

def getClasses():
    cursor.execute("SELECT  * from lop") 
    row = cursor.fetchone() 
    data = []
    while row: 
        data.append(row)
        row = cursor.fetchone()
    return data

def editClass(id : str, name : str, idStaff : str ) -> bool:
    try:
        cursor.execute("""Update lop set tenlop=?, manv=? where malop=?""", name,idStaff,id)
        cnxn.commit()
        return True        
    except:
        return False 

def addClass(id : str, name : str, idStaff : str ) -> bool:
    try:
        cursor.execute("""Insert into lop values(?,?,?)""",id, name,idStaff)
        cnxn.commit()
        return True        
    except:
        return False 

def editStaff(id : str, name : str, email : str, salary  ) -> bool:
    try:
        cursor.execute("""exec SP_Update_NhanVien ?,?,?,?""",id, name,email,salary)
        cnxn.commit()
        return True        
    except:
        return False 

def addStaff(id : str, name : str, email : str, salary : str, username : str,password : str ) -> bool:
    try:
        pk = id
        cursor.execute("""exec SP_INS_PUBLIC_ENCRYPT_NHANVIEN ?,?,?,?,?,?,?""",id, name,email,salary,username,password, pk)
        cnxn.commit()
        return True        
    except:
        return False 


def editStudent(id : str, name : str, birthday : str, address : str, idClass : str) -> bool:
    try:
        cursor.execute("""Update sinhvien set hoten=?, ngaysinh=?,diachi=?,malop=? where masv=?""", name,birthday,address,idClass,id)
        cnxn.commit()
        return True        
    except:
        return False                

