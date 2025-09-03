# Inventário JCL/COBOL — `INTCALC.JCL`

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
- **STEP15** — tipo: COBOL  (PARM='2022071800')
  - PGM: `CBACT04C`
  - Programas COBOL detectados: CBACT04C
    - STEPLIB: class=input, DSN=AWS.M2.CARDDEMO.LOADLIB, DISP=SHR
    - SYSPRINT: class=log
    - SYSOUT: class=log
    - TCATBALF: class=input, DSN=AWS.M2.CARDDEMO.TCATBALF.VSAM.KSDS, DISP=SHR
    - XREFFILE: class=input, DSN=AWS.M2.CARDDEMO.CARDXREF.VSAM.KSDS, DISP=SHR
    - XREFFIL1: class=input, DSN=AWS.M2.CARDDEMO.CARDXREF.VSAM.AIX.PATH, DISP=SHR
    - ACCTFILE: class=input, DSN=AWS.M2.CARDDEMO.ACCTDATA.VSAM.KSDS, DISP=SHR
    - DISCGRP: class=input, DSN=AWS.M2.CARDDEMO.DISCGRP.VSAM.KSDS, DISP=SHR
    - TRANSACT: class=output, DSN=AWS.M2.CARDDEMO.SYSTRAN(+1), DISP=NEW,CATLG,DELETE, RECFM=F, LRECL=350

---
## Programas COBOL analisados
### CBACT04C
- Fonte encontrado: **sim** (`C:\COBOL Files\batch2cloud_v3\files\cbl\CBACT04C.cbl`)

---