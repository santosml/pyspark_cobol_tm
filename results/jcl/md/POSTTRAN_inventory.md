# Inventário JCL/COBOL — `POSTTRAN.JCL`

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
- **STEP15** — tipo: COBOL  
  - PGM: `CBTRN02C`
  - Programas COBOL detectados: CBTRN02C
    - STEPLIB: class=input, DSN=AWS.M2.CARDDEMO.LOADLIB, DISP=SHR
    - SYSPRINT: class=log
    - SYSOUT: class=log
    - TRANFILE: class=input, DSN=AWS.M2.CARDDEMO.TRANSACT.VSAM.KSDS, DISP=SHR
    - DALYTRAN: class=input, DSN=AWS.M2.CARDDEMO.DALYTRAN.PS, DISP=SHR
    - XREFFILE: class=input, DSN=AWS.M2.CARDDEMO.CARDXREF.VSAM.KSDS, DISP=SHR
    - DALYREJS: class=output, DSN=AWS.M2.CARDDEMO.DALYREJS(+1), DISP=NEW,CATLG,DELETE, RECFM=F, LRECL=430
    - ACCTFILE: class=input, DSN=AWS.M2.CARDDEMO.ACCTDATA.VSAM.KSDS, DISP=SHR
    - TCATBALF: class=input, DSN=AWS.M2.CARDDEMO.TCATBALF.VSAM.KSDS, DISP=SHR

---
## Programas COBOL analisados
### CBTRN02C
- Fonte encontrado: **sim** (`C:\COBOL Files\batch2cloud_v3\files\cbl\CBTRN02C.cbl`)

---