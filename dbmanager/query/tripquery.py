
# Create Trip Query
CREATE_TRIP_QUERY = (""" 
        INSERT INTO "tbTrip"
        ("tripCode", "tripLoadingProvince","tripLoadingDistrict","tripDestinationProvince","tripDestinationDistrict",
        "tripExplanation","tripStartTime","_tripStatusId","_userId","_vehicleId","_courierId","_driverId")
        VALUES
        (
        ('SF-'||TO_CHAR(NOW(),'YYMMDDHHMISS')),
        %s, %s, %s, %s, %s,
        (SELECT NOW()),
        %s,
        (SELECT "userId" FROM "tbUser" WHERE "userName" = %s), 
        %s, %s, %s)
""")
# Get Trips Still Opening
GET_TRIPS_STILL_OPENING = (""" 
        SELECT
            tr."tripCode",
            tr."tripStartTime",
            tr."tripLoadingProvince",
            tr."tripLoadingDistrict",
            tr."tripDestinationProvince",
            tr."tripDestinationDistrict",
            tr."tripExplanation",
            v."vehicleNumberPlate",
            d."driverName",
            d."driverSurname",
            c."courierName",
            c."courierSurname",
            u."userName"
        FROM "tbTrip" tr
        INNER JOIN "tbVehicle" v
        ON tr."_vehicleId" = v."vehicleId"
        INNER JOIN "tbDriver" d
        ON tr."_driverId" = d."driverId"
        INNER JOIN "tbCourier" c
        ON tr."_courierId" = c."courierId"
        INNER JOIN "tbUser" u
        ON tr."_userId" = u."userId" 
        WHERE tr."_tripStatusId" = '1'
        ORDER BY tr."tripStartTime" DESC
""")

LOAD_ORDER_TO_TRIP = (""" 
        UPDATE "tbOrder"
        SET "_tripId" = (SELECT "tripId" FROM "tbTrip" WHERE "tripCode" = %s),
                      "orderLoadingDate" = (SELECT NOW())
        WHERE "orderId" = %s
""")

UPDATE_TRIP_STATUS = (""" 
        UPDATE "tbTrip"
        SET "_tripStatusId" = (SELECT "tripStatusId" FROM "tbTripStatus" WHERE "tripStatusName" = 'YÜKLENDİ')
        WHERE "tripCode" = %s
""")   

