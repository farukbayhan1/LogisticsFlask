from flask import Blueprint, jsonify, request
from config.config import db_connection

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
            cursor.execute(""" 
            SELECT
                "employeeName"
            FROM 
                "tbEmployee"
            WHERE
                "employeeName" = %s

            """,(employee_name,))
            result = cursor.fetchone()
            if result:
                check_employee = result[0]
                return jsonify({"Hata":f"Müşteri Daha Önce Ekleniştir: {str(check_employee)}"})
            else:
                cursor.execute(""" 
                INSERT INTO
                    "tbEmployee"
                    ("employeeName", "employeePhone", "employeePhone2",
                        "employeeAuthority", "employeeAuthorityPhone", "employeeAuthorityPhone2",
                        "employeeAdress", "_userId")
                VALUES
                    (%s, %s, %s, %s, %s, %s, %s,
                (SELECT 
                    "userId"
                FROM
                    "tbUser"
                WHERE
                    "userName" = %s))
                """,(employee_name,employee_phone,employee_phone2,employee_authority,
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
        cursor.execute(""" 
        SELECT
            e."employeeName",
            e."employeePhone",
            e."employeePhone2",
            e."employeeAuthority",
            e."employeeAuthorityPhone",
            e."employeeAuthorityPhone2",
            e."employeeAdress",
            u."userName" 
        FROM
            "tbEmployee" e
        INNER JOIN
            "tbUser" u
        ON
            e."_userId" = u."userId"               
        """)
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
