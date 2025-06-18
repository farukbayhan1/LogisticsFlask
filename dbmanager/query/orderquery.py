

ADD_QUERY_ORDER = (""" 
        INSERT INTO "tbOrder"
            ("orderNo","orderDocumentNo","orderDeliveryAdress","orderNumberPlate","orderDriver","orderBoxCount","orderConfirmationDate",
            "orderPlanConfirmationDate","orderTripNumber","_employeeId","_userId","_orderStatusId")
        VALUES
            (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s,
            (SELECT "userId" FROM "tbUser" WHERE "userName" = %s),
            (SELECT "statusId" FROM "tbOrderStatus" WHERE "statusName" = 'OLUŞTURULDU'))
            ON CONFLICT ("orderNo") DO NOTHING
            RETURNING "orderNo"
""")

CHECK_QUERY_EMPLOYEE = (""" 
        SELECT "employeeId"
        FROM "tbEmployee"
        WHERE "employeeName" = %s
""")

ADD_QUERY_EMPLOYEE = (""" 
        INSERT INTO "tbEmployee"
        ("employeeName", "_userId")
        VALUES (%s, 
        (SELECT "userId" FROM "tbUser" WHERE "userName" = %s))
        RETURNING "employeeId"
""")

def build_get_order_query(filters: dict):
    base_query = """
        SELECT 
            o."orderId",
            o."orderNo",
            o."orderDocumentNo",
            o."orderDeliveryAdress",
            o."orderNumberPlate",
            e."employeeName",
            o."orderBoxCount",
            TO_CHAR(o."orderConfirmationDate" AT TIME ZONE 'Europe/Istanbul', 'DD.MM.YYYY HH24:MI') AS "orderConfirmationDateFormatted",
            TO_CHAR(o."orderPlanConfirmationDate" AT TIME ZONE 'Europe/Istanbul', 'DD.MM.YYYY HH24:MI') AS "orderPlanConfirmationDateFormatted",
            o."orderTripNumber"
        FROM "tbOrder" o
        LEFT JOIN "tbEmployee" e ON o."_employeeId" = e."employeeId"
        WHERE 1=1
    """
    values = []

    if "order_no" in filters:
        base_query += ' AND o."orderNo" = %s'
        values.append(filters["order_no"])

    if "employee_name" in filters:
        base_query += ' AND e."employeeName" = %s'
        values.append(filters["employee_name"])

    if "order_driver" in filters:
        base_query += ' AND o."orderDriver" = %s'
        values.append(filters["order_driver"])

    if "order_status" in filters:
        base_query += ' AND o."_orderStatusId" = (SELECT "statusId" FROM "tbOrderStatus" WHERE "statusName" = %s)'
        values.append(filters["order_status"])

    if "start_date" in filters and filters["start_date"]:
        base_query += ' AND o."orderConfirmationDate" >= %s'
        values.append(filters["start_date"])

    if "end_date" in filters and filters["end_date"]:
        base_query += ' AND o."orderConfirmationDate" <= %s'
        values.append(filters["end_date"])

    if "trip_code" in filters:
        base_query += ' AND t."tripCode" = %s'
        values.append(filters["trip_code"])

    return base_query, tuple(values)

UPDATE_CHECK_ORDER_QUERY = (""" 
    UPDATE "tbOrder"
    SET "orderCheckDate" = %s, "orderCheckName" = %s, "_orderCheckUserId" = (SELECT "userId" FROM "tbUser" WHERE "userName" = %s)
    WHERE "orderDocumentNo" = %s
""")