from flask import Flask
from routes.loginroute import login_bp
from routes.userroute import user_bp
from routes.driverroute import driver_bp
from routes.courierroute import couerier_bp
from routes.employeeroute import employee_bp
from routes.vehicleroute import vehicle_bp
from routes.triproute import trip_bp
from routes.orderroute import order_bp
#from routes.tripstatusroute import tripstatus_bp



app = Flask(__name__)
app.register_blueprint(login_bp)
app.register_blueprint(user_bp)
app.register_blueprint(driver_bp)
app.register_blueprint(couerier_bp)
app.register_blueprint(employee_bp)
app.register_blueprint(vehicle_bp)
app.register_blueprint(trip_bp)
app.register_blueprint(order_bp)


if __name__ == '__main__':
    app.run(host='0.0.0.0',debug=True)