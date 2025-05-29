from flask import Blueprint,jsonify,request
from config.config import db_connection
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
    vehicle_number_plate = data.get("vehicle_number_plate")
    driver_tc_no = data.get("driver_tc_no")
    courier_tc_no = data.get("courier_tc_no")
    user_name = data.get("username")
    trip_explanation = data.get("trip_explanation")

    # Field Check All Filed is True
    check_list = [trip_loading_province,trip_loading_district,
                  trip_destination_province,trip_destination_district,
                  vehicle_number_plate, driver_tc_no, courier_tc_no, user_name,trip_explanation,]
    if not all(check_list):
        return jsonify({"Hata":"Lütfen Tüm Alanları Doldurunuz"}), 400
    else:
        try:
            create_query = execute_query(query=CREATE_TRIP_QUERY,params=(trip_loading_province,trip_loading_district,
                                                          trip_destination_province, trip_destination_district,
                                                          vehicle_number_plate,driver_tc_no,courier_tc_no,user_name,trip_explanation),
                                                          commit=True,fetchone=True)
            trip_id = create_query[0]
            return jsonify({"Bilgi": f"Yeni Sefer Başarıyla Oluşturuldu: {str(trip_id)}"}), 200
        except Exception as e:
            return jsonify({"Hata": f"Sunucu Hatası: {str(e)}"}), 500
    

    
       

def get_trip_still_opening():
    pass


