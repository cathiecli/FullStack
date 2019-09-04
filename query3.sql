WITH not_found_query AS (
    SELECT DATE(time) the_date, status, COUNT(DATE(time)) ctn
      FROM log
     WHERE status LIKE '%404%'
  GROUP BY DATE(time), status
  ORDER BY ctn DESC
), full_query AS (
    SELECT DATE(time) the_date, COUNT(DATE(time)) ctn
      FROM log
  GROUP BY DATE(time)
  ORDER BY ctn DESC)
SELECT TO_CHAR(a.the_date, 'fmMonth DD,YYYY'), TO_CHAR(((a.ctn::decimal / b.ctn::decimal) * 100.0)::float, 'FM999999990.00') || '%'
  FROM not_found_query a, full_query b
 WHERE a.the_date = b.the_date AND
        ((a.ctn::decimal / b.ctn::decimal) * 1) > 0.01
