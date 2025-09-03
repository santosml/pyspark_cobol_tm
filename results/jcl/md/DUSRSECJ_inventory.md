# Inventário JCL/COBOL — `DUSRSECJ.JCL`

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
- **PREDEL** — tipo: UTILITY  
  - PGM: `IEFBR14`
    - DD01: class=output, DSN=AWS.M2.CARDDEMO.USRSEC.PS, DISP=MOD,DELETE,DELETE
- **STEP01** — tipo: UTILITY  
  - PGM: `IEBGENER`
    - SYSUT1: class=other
    - SYSUT2: class=output, DSN=AWS.M2.CARDDEMO.USRSEC.PS, DISP=NEW,CATLG,DELETE, RECFM=FB, LRECL=80
    - SYSPRINT: class=log
    - SYSIN: class=other
- **STEP02** — tipo: UTILITY  
  - PGM: `IDCAMS`
    - SYSPRINT: class=log
    - SYSIN: class=other
- **STEP03** — tipo: UTILITY  
  - PGM: `IDCAMS`
    - IN: class=input, DSN=AWS.M2.CARDDEMO.USRSEC.PS, DISP=SHR
    - OUT: class=input, DSN=AWS.M2.CARDDEMO.USRSEC.VSAM.KSDS, DISP=SHR
    - SYSOUT: class=log
    - SYSPRINT: class=log
    - SYSIN: class=other

---
## Programas COBOL analisados
_Nenhum programa COBOL identificado._

---