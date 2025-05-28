from flask import Blueprint,jsonify,request
from config.config import db_connection
from query.userquery import CHECK_USER_QUERY,ADD_USER_QUERY,GET_USERS_QUERY

user_bp = Blueprint('user',__name__,url_prefix='/user')
@user_bp.route('',methods=['POST'])
def add_user():
    data = request.get_json()
    user_name = data.get("username")
    user_password = data.get("password")
    user_role = data.get("authority")

    # Check User
    if not user_name or not user_password or not user_role:
        return jsonify({"Hata": "Kullanıcı Adı, Parola, Kullanıcı Rolü Boş Olamaz"})
    else:
        conn = None
        try:
            conn = db_connection()
            cursor = conn.cursor()

            # Check User
            cursor.execute(CHECK_USER_QUERY,(user_name,))
            result = cursor.fetchone()
            if result is not None:
                check_user = result[0]
                if check_user == user_name:
                    return jsonify({"Hata": "Kullanıcı Daha Önce Eklenmiş"}),401
                
            else:
                cursor.execute(ADD_USER_QUERY,(user_name,user_password,user_role,))
                conn.commit()
                return jsonify({"Bilgi":"Kullanıcı Başarıyla Eklendi"}),200
                

        except Exception as e:
            return jsonify({"Hata": f"Sunucu Hatası{str(e)}"})
        finally:
            if conn:
                conn.close()

@user_bp.route('',methods=['GET'])
def get_user():
    conn = None
    try:
        conn = db_connection()
        cursor = conn.cursor()
        cursor.execute(GET_USERS_QUERY)
        rows = cursor.fetchall()
        user_list = []
        for row in rows:
            user_list.append({
                "userRoleName":row[0],
                "userName":row[1]
            })
        return jsonify(user_list)
    except Exception as e:
        return jsonify({"Hata":f"Sunucu Hatası {str(e)}"})