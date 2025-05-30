from flask import Blueprint, jsonify, request
from dbmanager.query.vehiclequery import CHECK_VEHICLE_QUERY,ADD_VEHICLE_QUERY,GET_VEHICLE_QUERY,UPDATE_VEHICLE_QUERY
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
                "vehicleId":row[0],
                "vehicleNumberPlate":row[1],
                "vehicleBrand":row[2],
                "vehicleModel":row[3],
                "vehicleModelYear":row[4],
                "vehicleType":row[5],
                "vehicleLoadCapacity":row[6],
                "userName":row[7]
            })
        return jsonify(vehicle_list), 200
    except Exception as e:
        return jsonify({"Hata": f"Sunucu Hatası: {str(e)}"}),500
    
@vehicle_bp.route('',methods=['PUT'])
def update_vehicle():
    try:
        data = request.get_json()
        required_fields = [
            "vehicle_id", "vehicle_number_plate", "vehicle_brand",
            "vehicle_model", "vehicle_model_year", "vehicle_type",
            "vehicle_load_capacity"
        ]
        missing_fields = [field for field in required_fields if not data.get(field)]
        if missing_fields:
            return jsonify({"Hata": f"Eksik alanlar: {', '.join(missing_fields)}"}), 400
        
        vehicle_id = data.get("vehicle_id")
        vehicle_number_plate = data.get("vehicle_number_plate")
        vehicle_brand = data.get("vehicle_brand")
        vehicle_model = data.get("vehicle_model")
        vehicle_model_year = data.get("vehicle_model_year")
        vehicle_type = data.get("vehicle_type")
        vehicle_load_capacity = data.get("vehicle_load_capacity")
        execute_query(UPDATE_VEHICLE_QUERY,(vehicle_number_plate,vehicle_brand,vehicle_model,vehicle_model_year,
                                            vehicle_type, vehicle_load_capacity,vehicle_id),commit=True)
        return jsonify({"Bilgi": "Araç Güncelleme İşlemi Başarılı"}),201
    except Exception as e:
        return jsonify({"Hata": f"Sunucu Hatası: {str(e)}"}),500