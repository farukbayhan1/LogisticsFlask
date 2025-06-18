from flask import Blueprint, jsonify, request
from dbmanager.excutequery import execute_query
from dbmanager.query.orderquery import ADD_QUERY_ORDER, CHECK_QUERY_EMPLOYEE, ADD_QUERY_EMPLOYEE,build_get_order_query, UPDATE_CHECK_ORDER_QUERY

order_bp = Blueprint('order',__name__,url_prefix='/order')

@order_bp.route('',methods=['POST'])
def add_order():
    data = request.get_json()
    if not data:
        return jsonify({"Hata":"Data Bulunamadı"}),400
         
    else:
        orders = data if isinstance(data,list) else[data]
        for order in orders:
            try:
                order_no = order.get("order_no")
                order_document_no = order.get("order_document_no")
                order_delivery_adress = order.get("order_delivery_adress")
                order_number_plate = order.get("order_number_plate")
                order_driver = order.get("order_driver")
                order_box_count = order.get("order_box_count")
                order_confirmation_date = order.get("order_confirmation_date")
                order_plan_confirmation_date = order.get("order_plan_confirmation_date")
                order_trip_number = order.get("order_trip_number")
                employee_name = order.get("employee_name")
                username = order.get("username")
                
                # Find employeeId
                result = execute_query(CHECK_QUERY_EMPLOYEE,params=(employee_name,),fetchone=True)
                if result:
                    employee_id = result[0]
                else:
                    result = execute_query(ADD_QUERY_EMPLOYEE, params=(employee_name,username),commit=True,fetchone=True)
                    employee_id = result[0]
                    
                # Add Order
                execute_query(ADD_QUERY_ORDER,params=(order_no,order_document_no,order_delivery_adress,order_number_plate,
                                                      order_driver,order_box_count,order_confirmation_date,order_plan_confirmation_date,
                                                      order_trip_number,employee_id,username),commit=True)
        
            except Exception as e:
                return jsonify({"Hata":f"Sunucu Hatası: {str(e)}"})
        return jsonify({"Bilgi":"Sipariş Ekleme İşlemi Başarılı"})
        

@order_bp.route('', methods=['GET'])
def search_orders():
    try:
        filters = request.args.to_dict()
        query, values = build_get_order_query(filters)
        results = execute_query(query, params=values, fetchall=True)
        return jsonify(results)
    except Exception as e:
        return jsonify({"Hata": str(e)}), 500

@order_bp.route('',methods=['PUT'])
def update_order():
    data = request.get_json()
    try:
        for i in data:
            order_document_no = i.get("order_document_no")
            order_check_date = i.get("check_date")
            order_check_name = i.get("status")
            username = i.get("username")
            execute_query(UPDATE_CHECK_ORDER_QUERY,(order_check_date,order_check_name,username,order_document_no),commit=True)
        return jsonify({"Bilgi":"Sipariş Güncelleme İşlemi Başarılı"}),201
    except Exception as e:
        return jsonify({"Hata":f"Sipariş Güncelleme İşleminde Hata: {str(e)}"}),500
        