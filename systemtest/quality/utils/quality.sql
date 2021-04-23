SELECT
  WUMFGN AS system_number,
  WUMCTL AS workunit,
  WUWORN AS workunit_order,
  WUPROD AS product_line,
  WUNMBR AS operation_number,
  WUOPST AS operation_status,
  CASE
    WHEN cast(WUTWRC AS INT) > 1 THEN cast(WUTWRC AS INT) - 1
    WHEN cast(WUTWRC AS INT) = 1 THEN cast(WUTWRC AS INT) END
      AS workunit_qty
FROM QRYQ.MFSGWU10_GRC
  WHERE
    WUNMBR IN ('VI20','LDUQ','0650','0850')
    AND WUOPST = 'W'
    AND WUWTYP = 'R'
    AND WUPRLN not IN ('ZMMR_FRM','SHUTTLE ')
    AND (left(WUPRLN,1) not IN ('0','1','2','3','4','5','6','7','8','9')
      OR WUPRLN = '1.8M RS ')
    AND WUWORN not IN ('YMB5HP','YMB5H4','YMB5II','YBB07Q','$CYLVN')
    AND WUIDSS IN ('0000','IPRC')
    AND left(WUPROD,4) not IN ('3584','TNFB','LEN_','8960')
    AND (left(WUPROD,1) not IN ('0','2','3','4','5','6','7','8','9')
      OR WUPROD = '1.8M RS ')
    AND WUPRLN not IN ('RSRCK','MEXBMES','SLDR-ISU','ZEPP-ISU');
