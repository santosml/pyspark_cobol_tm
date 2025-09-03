# Inventário JCL/COBOL — `COMBTRAN.JCL`

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
- **STEP05R** — tipo: UTILITY  
  - PGM: `SORT`
    - SORTIN: class=input, DSN=AWS.M2.CARDDEMO.TRANSACT.BKUP(0), DISP=SHR
    - SYMNAMES: class=other
    - SYSIN: class=other
    - SYSOUT: class=log
    - SORTOUT: class=output, DSN=AWS.M2.CARDDEMO.TRANSACT.COMBINED(+1), DISP=NEW,CATLG,DELETE
- **STEP10** — tipo: UTILITY  
  - PGM: `IDCAMS`
    - SYSPRINT: class=log
    - TRANSACT: class=input, DSN=AWS.M2.CARDDEMO.TRANSACT.COMBINED(+1), DISP=SHR
    - TRANVSAM: class=input, DSN=AWS.M2.CARDDEMO.TRANSACT.VSAM.KSDS, DISP=SHR
    - SYSIN: class=other

---
## Programas COBOL analisados
_Nenhum programa COBOL identificado._

---