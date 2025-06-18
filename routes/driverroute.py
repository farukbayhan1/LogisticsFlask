from flask import Blueprint, jsonify, request
from dbmanager.query.driverquery import CHECK_QUERY_DRIVER, ADD_QUERY_DRIVER, GET_QUERY_ALL_DRIVERS, UPDATE_QUERY_DRIVER
from dbmanager.excutequery import execute_query

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
        return jsonify({"Hata": "Tc No, Ad, Soyad, Telefon Boş Olamaz"}), 401
    else:
        try:

            # Check if driver already exists
            result = execute_query(CHECK_QUERY_DRIVER,params=(driver_tc_no,),fetchone=True)
            if result is not None:
               return jsonify({"Hata":f"Sürücü Daha Önce Eklenmiştir"}), 401
            
            # Add Driver 
            else:
                execute_query(ADD_QUERY_DRIVER,(driver_tc_no,driver_name,driver_surname,driver_phone,driver_adress,username),commit=True)  
                return jsonify({"Bilgi":"Sürücü Başarıyla Eklendi"}),201
        except Exception as e:
            return jsonify({"Hata": f"Sunucu Hatası {str(e)}"}), 500
       

@driver_bp.route('', methods=['GET'])
def get_drivers():
    
    try:
        rows = execute_query(GET_QUERY_ALL_DRIVERS,fetchall=True)
        driver_list = []
        for row in rows:
            driver_list.append({
                "driverId":row[0],
                "driverTcNo":row[1],
                "driverName":row[2],
                "driverSurname":row[3],
                "driverPhone":row[4],
                "driverAdress":row[5],
                "userName":row[6]
            })
        return jsonify(driver_list),200
    except Exception as e:
        return jsonify({"Hata":f"Sunucu Hatası: {str(e)}"}), 500

@driver_bp.route('',methods=['PUT'])
def update_driver():
    data = request.get_json()
    driver_id = data.get("driver_id")
    driver_name = data.get("driver_name")
    driver_surname = data.get("driver_surname")
    driver_phone = data.get("driver_phone")
    driver_adress = data.get("driver_adress")

    if not all([driver_name,driver_surname,driver_phone]):
        return jsonify({"Hata":"Sürücü İsim Soyisim ve Telefon Zorunludur"})
    else:
        try:
            execute_query(UPDATE_QUERY_DRIVER,params=(driver_name,driver_surname,driver_phone,driver_adress,driver_id),commit=True)
            return jsonify({"Bilgi":"Sürücü Bilgileri Güncellendi"}),201
        except Exception as e:
            return jsonify({"Hata":f"Sunucu Hatası {str(e)}"}),500