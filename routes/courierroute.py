from flask import Blueprint, jsonify, request
from config.config import db_connection

couerier_bp = Blueprint('courier',__name__,url_prefix='/courier')

@couerier_bp.route('',methods=['POST'])
def add_courier():
    data = request.get_json()
    courier_tc_no = data.get("courier_tc_no")
    courier_name = data.get("courier_name")
    courier_surname = data.get("courier_surname")
    courier_phone = data.get("courier_phone")
    courier_adress = data.get("courier_adress")
    username = data.get("username")
    # Check Courier Data
    if not courier_tc_no or not courier_name or not courier_surname or not courier_phone:
        return jsonify({"Hata":"Tc No, Ad, Soyad ve Telefon Boş Olamaz"})
    else:
        conn = None
        try:
            conn = db_connection()
            cursor = conn.cursor()

            # Courier was added before
            cursor.execute(""" 
            SELECT
                "courierTcNo"
            FROM
                "tbCourier"
            WHERE
                "courierTcNo" = %s
            """,(courier_tc_no,))
            result = cursor.fetchone()
            if result is not None:
                check_courier = result[0]
                return jsonify({"Hata":"Kurye Daha Önce Eklenmiştir"}),401
            else:
                cursor.execute(""" 
                INSERT INTO
                    "tbCourier"
                    ("courierTcNo", "courierName", "courierSurname", "courierPhone", "courierAdress", "_userId")
                VALUES
                    (%s,%s,%s,%s,%s,
                    (SELECT
                        "userId"
                    FROM
                        "tbUser"
                    WHERE
                        "userName" = %s))

                """,(courier_tc_no,courier_name,courier_surname,courier_phone,courier_adress,username))
                conn.commit()
                return jsonify({"Bilgi":"Kurye Ekleme İşlemi Başarılı"}),200
            
        except Exception as e:
            return jsonify({"Hata": f"Sunucu Hatası {str(e)}"})
    

@couerier_bp.route('',methods=['GET'])
def get_couriers():
    conn = None
    try:
        conn = db_connection()
        cursor = conn.cursor()
        cursor.execute(""" 
        SELECT
            cr."courierTcNo",
            cr."courierName",
            cr."courierSurname",
            cr."courierPhone",
            cr."courierAdress",
            u."userName"
        FROM
            "tbCourier" cr
        INNER JOIN
            "tbUser" u
        ON
            cr."_userId" = u."userId"
        """)
        rows = cursor.fetchall()
        courier_list = []
        for row in rows:
            courier_list.append({
                "courierTcNo":row[0],
                "courierName":row[1],
                "courierSurname":row[2],
                "courierPhone":row[3],
                "courierAdress":row[4],
                "userName":row[5]
            })
        return jsonify(courier_list)    
    except Exception as e:
        return jsonify({"Hata":f"Sunucu Hatası: {str(e)}"})