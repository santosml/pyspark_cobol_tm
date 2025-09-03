# Inventário JCL/COBOL — `TCATBALF.JCL`

## Pastas
- JCL: `C:\COBOL Files\batch2cloud_v3\files\jcl`
- COBOL: `C:\COBOL Files\batch2cloud_v3\files\cbl`
- CPY: `C:\COBOL Files\batch2cloud_v3\files\cpy`
- SCHEMA: `C:\COBOL Files\batch2cloud_v3\files\schema`
- SORT: `C:\COBOL Files\batch2cloud_v3\files\sort`

## Pendências (resumo)
- Programas COBOL não encontrados: —
- Copybooks ausentes (files/cpy): —
- Includes DB2 ausentes (files/schema): —

## Steps do JCL
- **STEP05** — tipo: UTILITY  
  - PGM: `IDCAMS`
    - SYSPRINT: class=log
    - SYSIN: class=other
- **STEP10** — tipo: UTILITY  
  - PGM: `IDCAMS`
    - SYSPRINT: class=log
    - SYSIN: class=other
- **STEP15** — tipo: UTILITY  
  - PGM: `IDCAMS`
    - SYSPRINT: class=log
    - TCATBAL: class=input, DSN=AWS.M2.CARDDEMO.TCATBALF.PS, DISP=SHR
    - TCATBALV: class=input/unknown, DSN=AWS.M2.CARDDEMO.TCATBALF.VSAM.KSDS, DISP=OLD
    - SYSIN: class=other

---
## Programas COBOL analisados
_Nenhum programa COBOL identificado._

---