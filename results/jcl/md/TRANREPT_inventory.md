# Inventário JCL/COBOL — `TRANREPT.JCL`

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
- **STEP05R** — tipo: UNKNOWN  
  - PROC: `REPROC`
- **STEP05R** — tipo: UTILITY  
  - PGM: `SORT`
    - SORTIN: class=input, DSN=AWS.M2.CARDDEMO.TRANSACT.BKUP(+1), DISP=SHR
    - SYMNAMES: class=other
    - SYSIN: class=other
    - SYSOUT: class=log
    - SORTOUT: class=output, DSN=AWS.M2.CARDDEMO.TRANSACT.DALY(+1), DISP=NEW,CATLG,DELETE
- **STEP10R** — tipo: COBOL  
  - PGM: `CBTRN03C`
  - Programas COBOL detectados: CBTRN03C
    - STEPLIB: class=input, DSN=AWS.M2.CARDDEMO.LOADLIB, DISP=SHR
    - SYSOUT: class=log
    - SYSPRINT: class=log
    - TRANFILE: class=input, DSN=AWS.M2.CARDDEMO.TRANSACT.DALY(+1), DISP=SHR
    - CARDXREF: class=input, DSN=AWS.M2.CARDDEMO.CARDXREF.VSAM.KSDS, DISP=SHR
    - TRANTYPE: class=input, DSN=AWS.M2.CARDDEMO.TRANTYPE.VSAM.KSDS, DISP=SHR
    - TRANCATG: class=input, DSN=AWS.M2.CARDDEMO.TRANCATG.VSAM.KSDS, DISP=SHR
    - DATEPARM: class=input, DSN=AWS.M2.CARDDEMO.DATEPARM, DISP=SHR
    - TRANREPT: class=output, DSN=AWS.M2.CARDDEMO.TRANREPT(+1), DISP=NEW,CATLG,DELETE, RECFM=FB, LRECL=133

---
## Programas COBOL analisados
### CBTRN03C
- Fonte encontrado: **sim** (`C:\COBOL Files\batch2cloud_v3\files\cbl\CBTRN03C.cbl`)

---