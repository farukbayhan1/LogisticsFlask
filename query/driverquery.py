
# Check Exists Query
CHECK_QUERY_DRIVER = ("""
        SELECT
            "driverTcNo"
        FROM
            "tbDriver"
        WHERE
            "driverTcNo" = %s
""")

# Add Query
ADD_QUERY_DRIVER = (""" 
        INSERT INTO
            "tbDriver"
            ("driverTcNo", "driverName", "driverSurname","driverPhone","driverAdress","_userId")
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
GET_QUERY_ALL_DRIVERS = ("""
        SELECT
            dr."driverTcNo",
            dr."driverName",
            dr."driverSurname",
            dr."driverPhone",
            dr."driverAdress",
            u."userName"
        FROM
            "tbDriver" dr
        INNER JOIN
            "tbUser" u
        ON
            dr."_userId" = u."userId"
""")
