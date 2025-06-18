from flask import Blueprint,jsonify,request
from dbmanager.excutequery import execute_query
from dbmanager.query.tripquery import CREATE_TRIP_QUERY, GET_TRIPS_STILL_OPENING, LOAD_ORDER_TO_TRIP, UPDATE_TRIP_STATUS

trip_bp = Blueprint('trip',__name__,url_prefix='/trip')

@trip_bp.route('',methods=['POST'])
def create_trip():
    data = request.get_json()
    trip_loading_province = data.get("trip_loading_province")
    trip_loading_district = data.get("trip_loading_district")
    trip_destination_province = data.get("trip_destination_province")
    trip_destination_district = data.get("trip_destination_district")
    trip_explanation = data.get("trip_explanation")
    trip_status_id = data.get("trip_status_id")
    username = data.get("username")
    vehicle_id = data.get("vehicle_id")
    courier_id = data.get("courier_id")
    driver_id = data.get("driver_id")

    # Field Check All Field is True
    check_list = [trip_loading_province,trip_loading_district,trip_destination_province,trip_destination_district,
                  trip_status_id,username,vehicle_id,courier_id,driver_id]
    if not all(check_list):
        return jsonify({"Hata":"Lütfen Tüm Alanları Doldurunuz"}), 400
    else:
        try:
            execute_query(CREATE_TRIP_QUERY,params=(
                trip_loading_province,trip_loading_district,trip_destination_province,trip_destination_district,
                trip_explanation,trip_status_id,username,vehicle_id,courier_id,driver_id),commit=True)
                
            return jsonify({"Bilgi":"Yeni Sefer Başarıyla Oluşturuldu"})
        except Exception as e:
            return jsonify({"Hata": f"Sunucu Hatası: {str(e)}"}), 500
    

@trip_bp.route('',methods=['GET'])
def get_trip_still_opening():
    rows = execute_query(GET_TRIPS_STILL_OPENING,fetchall=True)
    trip_list = []
    try:
        for row in rows:
            trip_list.append({
                "tripCode" : row[0],
                "tripStartTime" : row[1],
                "tripLoadingProvince" : row[2],
                "tripLoadingDistrict" : row[3],
                "tripDestinationProvince" : row[4],
                "tripDestinationDistrict" : row[5],
                "tripExplanation" : row[6],
                "vehicleNumberPlate" : row[7],
                "driverName" : row[8],
                "driverSurname" : row[9],
                "courierName" : row[10],
                "courierSurname" : row[11],
                "userName" : row[12]
            })
        return jsonify(trip_list)
    except Exception as e:
        return jsonify({"Hata":f"Sunucu Hatası {str(e)}"})
    
@trip_bp.route('',methods=['PUT'])
def load_orders_to_trip():
    data = request.get_json()
    try:
        for i in data:
            order_id = i.get("order_id")
            trip_code = i.get("trip_code")
            execute_query(LOAD_ORDER_TO_TRIP,params=(trip_code,order_id),commit=True)
        trip_code = data[0].get("trip_code")
        execute_query(UPDATE_TRIP_STATUS,params=(trip_code,), commit=True)
        return jsonify({"Bilgi":"Sefer Oluşturma İşlemi Başarılı"}),201
    except Exception as e:
        return jsonify({"Hata":f"Sunucu Hatası: {str(e)}"}),500

