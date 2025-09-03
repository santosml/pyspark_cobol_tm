# Inventário JCL/COBOL — `PRTCATBL.JCL`

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
- **DELDEF** — tipo: UTILITY  
  - PGM: `IEFBR14`
    - THEFILE: class=output, DSN=AWS.M2.CARDDEMO.TCATBALF.REPT, DISP=MOD,DELETE
- **STEP05R** — tipo: UNKNOWN  
  - PROC: `REPROC`
- **STEP10R** — tipo: UTILITY  
  - PGM: `SORT`
    - SORTIN: class=input, DSN=AWS.M2.CARDDEMO.TCATBALF.BKUP(+1), DISP=SHR
    - SYMNAMES: class=other
    - SYSIN: class=other
    - SYSOUT: class=log
    - SORTOUT: class=output, DSN=AWS.M2.CARDDEMO.TCATBALF.REPT, DISP=NEW,CATLG,DELETE, RECFM=FB, LRECL=40

---
## Programas COBOL analisados
_Nenhum programa COBOL identificado._

---