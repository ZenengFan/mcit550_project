USE cis550proj;
---------------------------------------
create view rolling_difference as(
WITH temp0 AS(SELECT date, state, amount as confirmed_cases
FROM Cases JOIN Counties ON Cases.fips = Counties.fips),

temp1 AS
(SELECT state, confirmed_cases, date, date_format(date,'%Y-%m-01') newdate
FROM temp0),

temp2 AS
(SELECT date_sub(MAX(newdate), interval 1 month) as latest
FROM temp1
),

temp3 AS
(SELECT date_sub(latest, interval 7 month) as s
FROM temp2),

temp4 AS (SELECT year(date),month(date),newdate, state, sum(confirmed_cases) as total
FROM temp1
GROUP BY month(date), state
HAVING newdate >= (SELECT s FROM temp3) and  newdate <= (SELECT latest FROM temp2)),

temp5 AS (select newdate, state, total
FROM temp4
Where (newdate > (SELECT s FROM temp3)) and (newdate <= (SELECT latest FROM temp2))),

temp6 AS (select newdate, state, total
FROM temp4
Where newdate >= (SELECT s FROM temp3) and  newdate < (SELECT latest FROM temp2)),

temp7 AS (SELECT state, total, date_add(newdate, interval 1 month) as newdate1
from temp6)

SELECT (temp5.total - temp7.total) as difference, newdate, temp5.state
FROM temp5, temp7
WHERE temp5.state = temp7.state and temp5.newdate = temp7.newdate1)

----------------------------------------
CREATE view predicted AS (
WITH temp0 AS(SELECT date, state, amount as confirmed_cases
FROM Cases JOIN Counties ON Cases.fips = Counties.fips),

temp1 AS
(SELECT state, confirmed_cases, date, date_format(date,'%Y-%m-01') newdate
FROM temp0),

temp2 as(SELECT state, AVG(difference) as avg_diff
FROM rolling_difference
GROUP BY state),

temp3 as
(SELECT date_sub(MAX(newdate), interval 1 month) as latest
FROM temp1),

temp4 as (SELECT newdate, state, sum(confirmed_cases) as total
FROM temp1
GROUP BY newdate, state
HAVING newdate = (SELECT latest FROM temp3))

SELECT (avg_diff + total) as predicted_cases, temp2.state
FROM temp2
JOIN temp4 ON temp2.state =  temp4.state)

--------
CREATE TABLE WARNING_STATE AS(
WITH temp0 AS(SELECT Counties.state, Num_ICU_Beds as beds
FROM Cases c JOIN Counties ON c.fips = Counties.fips
JOIN Hospitals h ON c.fips = h.fips),

temp1 As (SELECT state, SUM(beds) as total_beds
FROM temp0
GROUP BY state)


SELECT temp1.state, (p.predicted_cases * 0.05) - total_beds as ICU_shortage
FROM predicted p
JOIN temp1 ON p.state = temp1.state
order by ICU_shortage DESC
limit 5)


