from flask import Blueprint, jsonify, request
from config.config import db_connection 


login_bp = Blueprint('login',__name__,url_prefix='/login')

@login_bp.route('', methods=['POST'])
def check_user():
    data = request.get_json()
    user_name = data.get("username")
    user_password = data.get("password")
    
    # Check Data
    if not user_name or not user_password:
        return jsonify({"Hata": "Kullanıcı Adı ve Şifre Boş Olamaz"})
    else:
        conn = None
        try:
            conn = db_connection()
            cursor = conn.cursor()
            cursor.execute("""
            SELECT
                "userName", "userPassword"
            FROM
                "tbUser"
            WHERE
                "userName" = %s AND "userPassword" = %s
            """,(user_name,user_password))
            result = cursor.fetchone()
            if result:
                user_name = result[0]
                cursor.execute(""" 
                SELECT
                    ur."userRoleName"
                FROM
                    "tbUser" u
                INNER JOIN
                    "tbUserRole" ur
                ON
                    u."_userRoleId" = ur."userRoleId"
                WHERE
                    u."userName" = %s
            """,(user_name,))
                result = cursor.fetchone()
                user_role = result[0]
                return jsonify({"Bilgi": f"{user_role}"})
            else:
                return jsonify({"Hata": "Kullanıcı Adı ya da Şifre Hatalı"}),401
        except Exception as e:
            return jsonify({"Hata": f"Sunucu Hatası {str(e)}"})
        finally:
            if conn:
                conn.close()
        