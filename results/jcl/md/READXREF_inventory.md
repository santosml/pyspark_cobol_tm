# Inventário JCL/COBOL — `READXREF.JCL`

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
  - PGM: `CBACT03C`
  - Programas COBOL detectados: CBACT03C
    - STEPLIB: class=input, DSN=AWS.M2.CARDDEMO.LOADLIB, DISP=SHR
    - XREFFILE: class=input, DSN=AWS.M2.CARDDEMO.CARDXREF.VSAM.KSDS, DISP=SHR
    - SYSOUT: class=log
    - SYSPRINT: class=log

---
## Programas COBOL analisados
### CBACT03C
- Fonte encontrado: **sim** (`C:\COBOL Files\batch2cloud_v3\files\cbl\CBACT03C.cbl`)

---