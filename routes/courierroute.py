from flask import Blueprint, jsonify, request
from dbmanager.excutequery import execute_query
from dbmanager.query.courierquery import CHECK_QUERY_COURIER, ADD_QUERY_COURIER, GET_QUERY_ALL_COURIERS

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
        return jsonify({"Hata":"Tc No, Ad, Soyad ve Telefon Boş Olamaz"}),401
    else:
        try:
            # Courier Exists
            check_query = execute_query(query=CHECK_QUERY_COURIER,params=(courier_tc_no,),fetchone=True)
            if check_query is not None:
                return jsonify({"Hata":"Kurye Daha Önce Eklenmiştir"}),401
            
            # Add Courier
            else:
                execute_query(query=ADD_QUERY_COURIER,params=(courier_tc_no, courier_name, courier_surname, courier_phone, courier_adress, username),
                                          commit=True)
                return jsonify({"Bilgi":"Kurye Ekleme İşlemi Başarılı"}),201
            
        except Exception as e:
            return jsonify({"Hata": f"Sunucu Hatası {str(e)}"}),500
    

@couerier_bp.route('',methods=['GET'])
def get_couriers():
    
    try:
        rows = execute_query(GET_QUERY_ALL_COURIERS,fetchall=True)
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
        return jsonify(courier_list),200   
    except Exception as e:
        return jsonify({"Hata":f"Sunucu Hatası: {str(e)}"})