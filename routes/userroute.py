from flask import Blueprint,jsonify,request
from config.config import db_connection
from dbmanager.query.userquery import CHECK_USER_QUERY,ADD_USER_QUERY,GET_USERS_QUERY
from dbmanager.excutequery import execute_query

user_bp = Blueprint('user',__name__,url_prefix='/user')
@user_bp.route('',methods=['POST'])
def add_user():
    data = request.get_json()
    user_name = data.get("username")
    user_password = data.get("password")
    user_role = data.get("authority")

    # Check Data
    if not user_name or not user_password or not user_role:
        return jsonify({"Hata": "Kullanıcı Adı, Parola, Kullanıcı Rolü Boş Olamaz"}), 400

    try:
        # Kullanıcı zaten var mı kontrol et
        result = execute_query(CHECK_USER_QUERY, (user_name,),fetchone=True)
        if result:
            return jsonify({"Hata": "Kullanıcı Daha Önce Eklenmiş"}), 401

        # Kullanıcı ekle
        execute_query(ADD_USER_QUERY, (user_name, user_password, user_role),commit=True)
        return jsonify({"Bilgi": "Kullanıcı Başarıyla Eklendi"}), 201

    except Exception as e:
        return jsonify({"Hata": f"Sunucu Hatası: {str(e)}"}), 500


@user_bp.route('',methods=['GET'])
def get_user():
    try:
        rows = execute_query(GET_USERS_QUERY,fetchall=True)
        user_list = []
        for row in rows:
            user_list.append({
                "userRoleName":row[0],
                "userName":row[1]
            })
        return jsonify(user_list)
    except Exception as e:
        return jsonify({"Hata":f"Sunucu Hatası {str(e)}"}), 500
    