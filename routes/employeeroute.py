from flask import Blueprint, jsonify, request
from config.config import db_connection
from query.employeequery import CHECK_QUERY_EMPLOYEE,ADD_QUERY_EMPLOYEE,GET_QUERY_ALL_EMPLOYEES

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
        return jsonify({"Hata":"Müşteri Ünvanı Boş Olamaz"})
    else:
        conn = None
        try:
            conn = db_connection()
            cursor = conn.cursor()
            
            # Check if employee was added before
            cursor.execute(CHECK_QUERY_EMPLOYEE,(employee_name,))
            result = cursor.fetchone()
            if result:
                check_employee = result[0]
                return jsonify({"Hata":f"Müşteri Daha Önce Ekleniştir: {str(check_employee)}"})
            else:
                cursor.execute(ADD_QUERY_EMPLOYEE,(employee_name,employee_phone,employee_phone2,employee_authority,
                     employee_authority_phone,employee_authority_phone2,
                     employee_adress,username))
                conn.commit()
                return jsonify({"Bilgi":"MÜşteri Ekleme İşlemi Başarılı"})
            
        except Exception as e:
            return jsonify({"Hata:"f"Sunucu Hatası: f{str(e)}"})
        finally:
            if conn:
                conn.close()
@employee_bp.route('',methods=['GET'])
def get_employees():
    conn = None
    try:
        conn = db_connection()
        cursor = conn.cursor()
        cursor.execute(GET_QUERY_ALL_EMPLOYEES)
        rows = cursor.fetchall()
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
        return jsonify(employee_list)

    except Exception as e:
        return jsonify({"Hata":f"Sunucu Hatası: {str(e)}"})
