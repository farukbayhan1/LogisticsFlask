from flask import Blueprint, jsonify, request
from config.config import db_connection 

driver_bp = Blueprint('driver',__name__,url_prefix='/driver')

@driver_bp.route('', methods=['POST'])
def add_driver():
    data = request.get_json()
    driver_tc_no = data.get("driver_tc_no")
    driver_name = data.get("driver_name")
    driver_surname = data.get("driver_surname")
    driver_phone = data.get("driver_phone")
    driver_adress = data.get("driver_adress")
    username = data.get("username")


    # Check Data 
    if not driver_tc_no or not driver_name or not driver_surname or not driver_phone:
        return jsonify({"Hata": "Tc No, Ad, Soyad, Telefon Boş Olamaz"}), 400
    else:
        conn = None
        try:
            conn = db_connection()
            cursor = conn.cursor()
            # Check if driver already exists
            cursor.execute(""" 
            SELECT
                "driverTcNo"
            FROM
                "tbDriver"
            WHERE
                "driverTcNo" = %s
            """, (driver_tc_no,))
            result = cursor.fetchone()
            if result is not None:
               check_tc = result[0]
               return jsonify({"Hata":f"Sürücü Daha Önce Eklenmiştir"})
            else:
                cursor.execute(""" 
                INSERT INTO
                    "tbDriver"
                    ("driverTcNo", "driverName", "driverSurname","driverPhone","driverAdress","_userId")
                VALUES
                    (%s, %s, %s, %s, %s,
                (SELECT
                    "userId"
                FROM
                    "tbUser"
                WHERE
                    "userName" = %s)
                )
                """,(driver_tc_no,driver_name,driver_surname,driver_phone,driver_adress,username))
                conn.commit()
                return jsonify({"Bilgi":"Sürücü Başarıyla Eklendi"})
            


        except Exception as e:
            return jsonify({"Hata": f"Sunucu Hatası {str(e)}"}), 500
        finally:
            if conn:
                conn.close() 
@driver_bp.route('', methods=['GET'])
def get_drivers():
    conn = None
    try:
        conn = db_connection()
        cursor = conn.cursor()
        cursor.execute(""" 
        SELECT
            dr."driverTcNo",
            dr."driverName",
            dr."driverSurname",
            dr."driverPhone",
            dr."driverAdress",
            u."userName"
        FROM
            "tbDriver" dr
        INNER JOIN
            "tbUser" u
        ON
            dr."_userId" = u."userId"
        """) 
        rows = cursor.fetchall()
        driver_list = []
        for row in rows:
            driver_list.append({
                "driverTcNo":row[0],
                "driverName":row[1],
                "driverSurname":row[2],
                "driverPhone":row[3],
                "driverAdress":row[4],
                "userName":row[5]
            })
        return jsonify(driver_list) 
    
    except Exception as e:
        return jsonify({"Hata":f"Sunucu Hatası: {str(e)}"})
