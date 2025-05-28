
# Check Exists Query
CHECK_QUERY_COURIER = (""" 
        SELECT
            "courierTcNo"
        FROM
            "tbCourier"
        WHERE
            "courierTcNo" = %s
""")

# Add Query
ADD_QUERY_COURIER = (""" 
        INSERT INTO
            "tbCourier"
            ("courierTcNo", "courierName", "courierSurname", "courierPhone", "courierAdress", "_userId")
        VALUES
            (%s, %s, %s, %s, %s,
            (SELECT
                "userId"
            FROM
                "tbUser"
            WHERE
                "userName" = %s))  
""")

# Get All Query
GET_QUERY_ALL_COURIERS = (""" 
        SELECT
            cr."courierTcNo",
            cr."courierName",
            cr."courierSurname",
            cr."courierPhone",
            cr."courierAdress",
            u."userName"
        FROM
            "tbCourier" cr
        INNER JOIN
            "tbUser" u
        ON
            cr."_userId" = u."userId"
""")