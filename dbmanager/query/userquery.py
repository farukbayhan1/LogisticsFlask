
# Check User Exists Query
CHECK_USER_QUERY = (""" 
        SELECT *
        FROM "tbUser"
        WHERE "userName" = %s
""")

# Add User Query
ADD_USER_QUERY = (""" 
        INSERT INTO
            "tbUser"
            ("userName", "userPassword", "_userRoleId")
        VALUES (%s, %s,
            (SELECT "userRoleId"
            FROM "tbUserRole"
            WHERE "userRoleName"= %s))
""")

# Get Users Query
GET_USERS_QUERY = (""" 
        SELECT
            ur."userRoleName",
            u."userName"
        FROM
            "tbUser" u
        INNER JOIN
            "tbUserRole" ur
        ON
            u."_userRoleId" = ur."userRoleId"
""")

