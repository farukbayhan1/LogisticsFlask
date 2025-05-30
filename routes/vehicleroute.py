from flask import Blueprint, jsonify, request
from dbmanager.query.vehiclequery import CHECK_VEHICLE_QUERY,ADD_VEHICLE_QUERY,GET_VEHICLE_QUERY
from dbmanager.excutequery import execute_query

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
        try:   
            
            # Check if vehicle was already exists
            result = execute_query(CHECK_VEHICLE_QUERY,(vehicle_number_plate,),fetchone=True)
            if result is not None:
                return jsonify({"Hata":f"Bu Plaka Daha Önce Eklenmiştir"}), 400
            else:
                execute_query(ADD_VEHICLE_QUERY,(vehicle_number_plate,vehicle_brand,vehicle_model,vehicle_model_year,
                     vehicle_type,vehicle_load_capacity,username),commit=True)
                return jsonify({"Bilgi":"Araç Ekleme İşlemi Başarıyla Tamamlandı"}),201
        except Exception as e:
            return jsonify({"Hata":f"Sunucu Hatası: {str(e)}"})
        
@vehicle_bp.route('',methods=['GET'])
def get_vehicles():
    
    try:
        rows = execute_query(GET_VEHICLE_QUERY,fetchall=True)
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
        return jsonify(vehicle_list), 200
    except Exception as e:
        return jsonify({"Hata": f"Sunucu Hatası: {str(e)}"}),500