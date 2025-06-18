from flask import Blueprint, jsonify, request
from dbmanager.query.employeequery import CHECK_QUERY_EMPLOYEE,ADD_QUERY_EMPLOYEE,GET_QUERY_ALL_EMPLOYEES,UPDATE_QUERY_EMPLOYEE
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
                "employeeId":row[0],
                "employeeName":row[1],
                "employeePhone":row[2],
                "employeePhone2":row[3],
                "employeeAuthority":row[4],
                "employeeAuthorityPhone":row[5],
                "employeeAuthorityPhone2":row[6],
                "employeeAdress":row[7],
                "userName":row[8]
            })
        return jsonify(employee_list),200

    except Exception as e:
        return jsonify({"Hata":f"Sunucu Hatası: {str(e)}"}),500

@employee_bp.route('',methods=['PUT'])
def update_employee():
    data = request.get_json()
    employee_id = data.get("employee_id")
    employee_phone = data.get("employee_phone")
    employee_phone2 = data.get("employee_phone2")
    employee_authority = data.get("employee_authority")
    employee_authority_phone = data.get("employee_authority_phone")
    employee_authority_phone2 = data.get("employee_authority_phone2")
    employee_adress = data.get("employee_adress")
    
    try:
        execute_query(UPDATE_QUERY_EMPLOYEE,params=(employee_phone,employee_phone2,employee_authority,employee_authority_phone,
                                                             employee_authority_phone2,employee_adress,employee_id),commit=True)
        return jsonify({"Bilgi":"Müşteri Bilgileri Başarıyla Güncellendi"}),201
    
    except Exception as e:
        return jsonify({"Hata":f"Sunucu Hatası: {str(e)}"})

