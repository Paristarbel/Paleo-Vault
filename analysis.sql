SELECT year, COUNT(*) AS record_count
FROM records
WHERE year IS NOT NULL
GROUP BY year
ORDER BY year;

SELECT institutioncode, COUNT(*) AS records_per_institution
FROM records
GROUP BY institutioncode
ORDER BY records_per_institution DESC;

SELECT coordinatesvalid, COUNT(*) AS record_count
FROM records
GROUP BY coordinatesvalid
ORDER BY coordinatesvalid;