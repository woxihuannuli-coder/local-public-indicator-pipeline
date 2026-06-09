SELECT 도서관명, 소재지, COUNT(*) AS duplicate_count
FROM small_libraries
GROUP BY 도서관명, 소재지 HAVING COUNT(*) > 1;