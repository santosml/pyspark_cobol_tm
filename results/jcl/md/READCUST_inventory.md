# Inventário JCL/COBOL — `READCUST.JCL`

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
- **STEP05** — tipo: COBOL  
  - PGM: `CBCUS01C`
  - Programas COBOL detectados: CBCUS01C
    - STEPLIB: class=input, DSN=AWS.M2.CARDDEMO.LOADLIB, DISP=SHR
    - CUSTFILE: class=input, DSN=AWS.M2.CARDDEMO.CUSTDATA.VSAM.KSDS, DISP=SHR
    - SYSOUT: class=log
    - SYSPRINT: class=log

---
## Programas COBOL analisados
### CBCUS01C
- Fonte encontrado: **sim** (`C:\COBOL Files\batch2cloud_v3\files\cbl\CBCUS01C.cbl`)

---