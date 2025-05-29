
# Create Trip Query
CREATE_TRIP_QUERY =(""" 
        INSERT INTO "tbTrips"
        ("tripLoadingProvince", "tripLoadingDistrict", "tripDestinationProvince", "tripDestinationDistrict",
        "_vehicleId", "_driverId", "_courierId", "tripStartTime", "_userId", "tripExplanation")
        VALUES
        (%s, %s, %s, %s,
        (SELECT "vehicleId" FROM "tbVehicle" WHERE "vehicleNumberPlate" = %s),
        (SELECT "driverId" FROM "tbDriver" WHERE "driverTcNo" = %s),
        (SELECT "courierId" FROM "tbCourier" WHERE "courierTcNo" = %s),
        NOW(),
        (SELECT "userId" FROM "tbUser" WHERE "userName" = %s),
        %s)
        RETURNING "tripId"              
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
        FROM "tbTrips" tr
        INNER JOIN "tbVehicle" v
        ON tr."_vehicleId" = v."vehicleId"
        INNER JOIN "tbDriver" d
        ON tr."_driverId" = d."driverId"
        INNER JOIN "tbCourier" c
        ON tr."_courierId" = c."courierId"
        INNER JOIN "tbUser" u
        ON tr."_userId" = u."userId" 
        WHERE tr."tripEndTime" IS NULL
        ORDER BY tr."tripStartTime" DESC
""")

# Update Trip End Time
UPDATE_TRIP_END_TIME = (""" 
        UPDATE "tbTrips"
        SET "tripEndTime" = %s
        WHERE "tripCode" = %s
""")