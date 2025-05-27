from flask import Blueprint, jsonify, request
from config.config import db_connection

vehicle_bp = Blueprint('vehicle',__name__,url_prefix='/vehicle')

@vehicle_bp.route('',methods=['POST'])
def add_vehicle():
    data = request.get_json()
    vehicle_number_plate = data.get("vehicle_number_plate")
    vehicle_brand = data.get("vehicle_brand")
    vehicle_model = data.get("vehicle_model")
    vehicle_model_year = data.get("vehicle_model_year")
    vehicle_type = data.get("vehicle_type")
    vehicle_load_capacity = data.get("vehicle_load_capacity")
    username = data.get("username")

    # Check Vehicle
    if not vehicle_number_plate or not vehicle_brand:
        return jsonify({"Hata": "Araç Plakası ve Markası Boş Olamaz"})
    else:
        conn = None
        try:
            conn = db_connection()
            cursor = conn.cursor()
            
            # Check if vehicle was already exists
            cursor.execute(""" 
            SELECT
                "vehicleNumberPlate"
            FROM
                "tbVehicle"
            WHERE
                "vehicleNumberPlate" = %s
            """,(vehicle_number_plate,))
            result = cursor.fetchone()

            if result is not None:
                check_vehicle_number_plate = result[0]
                return jsonify({"Hata":f"Bu Plaka Daha Önce Eklenmiştir: {str(check_vehicle_number_plate)}"})
            else:
                cursor.execute(""" 
                INSERT INTO
                    "tbVehicle"
                    ("vehicleNumberPlate", "vehicleBrand", "vehicleModel",
                               "vehicleModelYear", "vehicleType", "vehicleLoadCapacity",
                               "_userId")
                VALUES
                    (%s, %s, %s, %s, %s, %s,
                    (SELECT
                        "userId"
                    FROM
                        "tbUser"
                    WHERE
                        "userName" = %s))
                """,(vehicle_number_plate,vehicle_brand,vehicle_model,vehicle_model_year,
                     vehicle_type,vehicle_load_capacity,username))
                conn.commit()
                return jsonify({"Bilgi":"Araç Ekleme İşlemi Başarıyla Tamamlandı"})
        except Exception as e:
            return jsonify({"Hata":f"Sunucu Hatası: {str(e)}"})
        finally:
            if conn:
                conn.close()
@vehicle_bp.route('',methods=['GET'])
def get_vehicles():
    conn = None
    try:
        conn = db_connection()
        cursor = conn.cursor()
        cursor.execute(""" 
        SELECT
            v."vehicleNumberPlate",
            v."vehicleBrand",
            v."vehicleModel",
            v."vehicleModelYear",
            v."vehicleType",
            v."vehicleLoadCapacity",
            u."userName"
        FROM
            "tbVehicle" v
        INNER JOIN
            "tbUser" u
        ON
            v."_userId" = u."userId"
        """)
        rows = cursor.fetchall()
        vehicle_list = []
        for row in rows:
            vehicle_list.append({
                "vehicleNumberPlate":row[0],
                "vehicleBrand":row[1],
                "vehicleModel":row[2],
                "vehicleModelYear":row[3],
                "vehicleType":row[4],
                "vehicleLoadCapacity":row[5],
                "userName":row[6]
            })
        return jsonify(vehicle_list)
    except Exception as e:
        return jsonify({"Hata": f"Sunucu Hatası: {str(e)}"})