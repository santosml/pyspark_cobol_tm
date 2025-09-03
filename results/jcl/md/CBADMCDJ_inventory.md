# Inventário JCL/COBOL — `CBADMCDJ.JCL`

## Pastas
- JCL: `C:\COBOL Files\batch2cloud_v3\files\jcl`
- COBOL: `C:\COBOL Files\batch2cloud_v3\files\cbl`
- CPY: `C:\COBOL Files\batch2cloud_v3\files\cpy`
- SCHEMA: `C:\COBOL Files\batch2cloud_v3\files\schema`
- SORT: `C:\COBOL Files\batch2cloud_v3\files\sort`

## Pendências (resumo)
- Programas COBOL não encontrados: DFHCSDUP
- Copybooks ausentes (files/cpy): —
- Includes DB2 ausentes (files/schema): —

## Steps do JCL
- **STEP1** — tipo: COBOL  (PARM='CSD(READWRITE))
  - PGM: `DFHCSDUP`
  - Programas COBOL detectados: DFHCSDUP
    - STEPLIB: class=input, DSN=OEM.CICSTS.V05R06M0.CICS.SDFHLOAD, DISP=SHR
    - DFHCSD: class=input, DSN=OEM.CICSTS.DFHCSD, DISP=SHR
    - OUTDD: class=other
    - SYSPRINT: class=log
    - SYSIN: class=other

---
## Programas COBOL analisados
### DFHCSDUP
- Fonte encontrado: **não**

---