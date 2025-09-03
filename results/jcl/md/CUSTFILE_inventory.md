# Inventário JCL/COBOL — `CUSTFILE.JCL`

## Pastas
- JCL: `C:\COBOL Files\batch2cloud_v3\files\jcl`
- COBOL: `C:\COBOL Files\batch2cloud_v3\files\cbl`
- CPY: `C:\COBOL Files\batch2cloud_v3\files\cpy`
- SCHEMA: `C:\COBOL Files\batch2cloud_v3\files\schema`
- SORT: `C:\COBOL Files\batch2cloud_v3\files\sort`

## Pendências (resumo)
- Programas COBOL não encontrados: SDSF
- Copybooks ausentes (files/cpy): —
- Includes DB2 ausentes (files/schema): —

## Steps do JCL
- **CLCIFIL** — tipo: COBOL  
  - PGM: `SDSF`
  - Programas COBOL detectados: SDSF
    - ISFOUT: class=other
    - CMDOUT: class=other
    - ISFIN: class=other
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
    - CUSTDATA: class=input, DSN=AWS.M2.CARDDEMO.CUSTDATA.PS, DISP=SHR
    - CUSTVSAM: class=input, DSN=AWS.M2.CARDDEMO.CUSTDATA.VSAM.KSDS, DISP=SHR
    - SYSIN: class=other
- **OPCIFIL** — tipo: COBOL  
  - PGM: `SDSF`
  - Programas COBOL detectados: SDSF
    - ISFOUT: class=other
    - CMDOUT: class=other
    - ISFIN: class=other

---
## Programas COBOL analisados
### SDSF
- Fonte encontrado: **não**

---