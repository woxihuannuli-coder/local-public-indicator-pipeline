SELECT COUNT(*) AS null_count
FROM small_libraries
WHERE region_gu IS NULL
   OR TRIM(region_gu) = '';
