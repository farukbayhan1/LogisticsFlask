from flask import Blueprint,jsonify,request
from dbmanager.excutequery import execute_query
from dbmanager.query.tripstatusquery import GET_TRIP_STATUS
tripstatus_bp = Blueprint('tripstatus',__name__,url_prefix='/tripstatus')

@tripstatus_bp.route('',methods=['GET'])
def get_trip_status():
    try:
        rows = execute_query(GET_TRIP_STATUS,fetchall=True)
        trip_status_list = []
        for row in rows:
            trip_status_list.append({
                "tripStatusId":row[0],
                "tripStatusName":row[1]
            })
        return jsonify(trip_status_list), 200
    except Exception as e:
        return jsonify({"Hata": f"Sunucu Hatası: {str(e)}"}),500
