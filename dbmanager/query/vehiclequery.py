
# Check Vehicle Query
CHECK_VEHICLE_QUERY = (""" 
        SELECT
            "vehicleNumberPlate"
        FROM
            "tbVehicle"
        WHERE
            "vehicleNumberPlate" = %s
""")

# Add Vehicle Query
ADD_VEHICLE_QUERY = (""" 
        INSERT INTO
            "tbVehicle"
            ("vehicleNumberPlate", "vehicleBrand", "vehicleModel",
                        "vehicleModelYear", "vehicleType", "vehicleLoadCapacity",
                        "_userId")
        VALUES
            (%s, %s, %s, %s, %s, %s,
            (SELECT "userId"
            FROM "tbUser"
            WHERE "userName" = %s))
""")

# Get Vehicle Query
GET_VEHICLE_QUERY = (""" 
        SELECT
            v."vehicleId",
            v."vehicleNumberPlate",
            v."vehicleBrand",
            v."vehicleModel",
            v."vehicleModelYear",
            v."vehicleType",
            v."vehicleLoadCapacity",
            u."userName"
        FROM
            "tbVehicle" v
        INNER JOIN
            "tbUser" u
        ON
            v."_userId" = u."userId"
""")

UPDATE_VEHICLE_QUERY  = (""" 
        UPDATE "tbVehicle"
        SET "vehicleNumberPlate" = %s, "vehicleBrand" = %s, "vehicleModel" = %s, "vehicleModelYear" = %s, "vehicleType" = %s,
            "vehicleLoadCapacity" = %s
        WHERE "vehicleId" = %s
""")