SELECT
    region_gu,
    COUNT(*) AS library_count
FROM small_libraries
GROUP BY region_gu
ORDER BY library_count DESC;
