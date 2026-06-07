SELECT COUNT(*) AS invalid_count
FROM small_libraries
WHERE region_gu NOT IN ('동탄구', '만세구', '효행구', '병점구')
   OR region_gu IS NULL
   OR TRIM(region_gu) = '';
