from flask import Blueprint, jsonify, request
from dbmanager.query.employeequery import CHECK_QUERY_EMPLOYEE,ADD_QUERY_EMPLOYEE,GET_QUERY_ALL_EMPLOYEES
from dbmanager.excutequery import execute_query

employee_bp = Blueprint('employee',__name__,url_prefix='/employee')

@employee_bp.route('',methods=['POST'])
def add_employee():
    data = request.get_json()
    employee_name = data.get("employee_name")
    employee_phone = data.get("employee_phone")
    employee_phone2 = data.get("employee_phone2")
    employee_authority = data.get("employee_authority")
    employee_authority_phone = data.get("employee_authority_phone")
    employee_authority_phone2 = data.get("employee_authority_phone2")
    employee_adress = data.get("employee_adress")
    username = data.get("username")

    # Check Employee
    if not employee_name:
        return jsonify({"Hata":"Müşteri Ünvanı Boş Olamaz"}),400
    else:
        try:
            # Check if employee was added before
            result = execute_query(CHECK_QUERY_EMPLOYEE,(employee_name,),fetchone=True)
            if result:
                return jsonify({"Hata":f"Müşteri Daha Önce Eklenmiştir"}),400
            
            # Add Employee
            else:
                execute_query(ADD_QUERY_EMPLOYEE,(employee_name,employee_phone,employee_phone2,employee_authority,
                     employee_authority_phone,employee_authority_phone2,
                     employee_adress,username),commit=True)
                return jsonify({"Bilgi":"Müşteri Ekleme İşlemi Başarılı"}),201
            
        except Exception as e:
            return jsonify({"Hata:"f"Sunucu Hatası: f{str(e)}"}),500
    
@employee_bp.route('',methods=['GET'])
def get_employees():
    try:
        rows = execute_query(GET_QUERY_ALL_EMPLOYEES,fetchall=True)
        employee_list = []
        for row in rows:
            employee_list.append({
                "employeeName":row[0],
                "employeePhone":row[1],
                "employeePhone2":row[2],
                "employeeAuthority":row[3],
                "employeeAuthorityPhone":row[4],
                "employeeAuthorityPhone2":row[5],
                "employeeAdress":row[6],
                "userName":row[7]
            })
        return jsonify(employee_list),200

    except Exception as e:
        return jsonify({"Hata":f"Sunucu Hatası: {str(e)}"}),500
