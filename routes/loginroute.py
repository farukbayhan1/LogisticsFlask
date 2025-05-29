from flask import Blueprint, jsonify, request
from dbmanager.query.loginquery import GET_USER_ROLE_QUERY, LOGIN_QUERY
from dbmanager.excutequery import execute_query


login_bp = Blueprint('login',__name__,url_prefix='/login')

@login_bp.route('', methods=['POST'])
def check_user():
    data = request.get_json()
    user_name = data.get("username")
    user_password = data.get("password")
    
    # Check Data
    if not user_name or not user_password:
        return jsonify({"Hata": "Kullanıcı Adı ve Şifre Boş Olamaz"}),401
    else:
        
        # Login
        try:
            result = execute_query(LOGIN_QUERY,(user_name,user_password),fetchone=True)
            if result:
                user_name = result[0]
                user_role = execute_query(GET_USER_ROLE_QUERY,(user_name,),fetchone=True)[0]
                return jsonify({"Bilgi": f"{user_role}"}),200
            else:
                return jsonify({"Hata": "Kullanıcı Adı ya da Şifre Hatalı"}),401
            
        except Exception as e:
            return jsonify({"Hata": f"Sunucu Hatası {str(e)}"}),500
