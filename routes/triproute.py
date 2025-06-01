from flask import Blueprint,jsonify,request
from dbmanager.excutequery import execute_query
from dbmanager.query.tripquery import CREATE_TRIP_QUERY, GET_TRIPS_STILL_OPENING, UPDATE_TRIP_END_TIME

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
    

    
       

def get_trip_still_opening():
    pass


