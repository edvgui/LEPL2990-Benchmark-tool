DROP TABLE IF EXISTS RecentPurchases;
CREATE TABLE RecentPurchases AS 
    SELECT *
    FROM Purchases
    WHERE time > date((SELECT MAX(time) FROM Purchases), '-10 days')
;
