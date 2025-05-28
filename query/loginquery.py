
# Login Query
LOGIN_QUERY = (""" 
        SELECT
            "userName", "userPassword"
        FROM
            "tbUser"
        WHERE
            "userName" = %s AND "userPassword" = %s
""")

# Get User Role Query
GET_USER_ROLE_QUERY = (""" 
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
""")