
# Check Exists Query
CHECK_QUERY_EMPLOYEE = (""" 
        SELECT
            "employeeName"
        FROM 
            "tbEmployee"
        WHERE
            "employeeName" = %s
""")

ADD_QUERY_EMPLOYEE = (""" 
        INSERT INTO
            "tbEmployee"
            ("employeeName", "employeePhone", "employeePhone2","employeeAuthority", "employeeAuthorityPhone", "employeeAuthorityPhone2",
            "employeeAdress", "_userId")
        VALUES
            (%s, %s, %s, %s, %s, %s, %s,
        (SELECT 
            "userId"
        FROM
            "tbUser"
        WHERE
            "userName" = %s))
""")

GET_QUERY_ALL_EMPLOYEES = (""" 
        SELECT
            e."employeeId",
            e."employeeName",
            e."employeePhone",
            e."employeePhone2",
            e."employeeAuthority",
            e."employeeAuthorityPhone",
            e."employeeAuthorityPhone2",
            e."employeeAdress",
            u."userName" 
        FROM
            "tbEmployee" e
        INNER JOIN
            "tbUser" u
        ON
            e."_userId" = u."userId" 
""")

UPDATE_QUERY_EMPLOYEE = (""" 
        UPDATE "tbEmployee"
        SET  "employeePhone" = %s, "employeePhone2" = %s, "employeeAuthority" = %s, "employeeAuthorityPhone" = %s,
            "employeeAuthorityPhone2" = %s, "employeeAdress" = %s
        WHERE "employeeId" = %s
""")