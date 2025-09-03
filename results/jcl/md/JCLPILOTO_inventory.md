# Inventário JCL/COBOL — `JCLPILOTO.TXT`

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
- **BR14A** — tipo: UTILITY  
  - PGM: `IEFBR14`
    - DD1: class=output, DSN=FLAIBAM.OUT.FSLDATU, DISP=MOD,DELETE,DELETE
- **PROG1** — tipo: COBOL  
  - PGM: `PROGRAM1`
  - Programas COBOL detectados: PROGRAM1
    - SYSPRINT: class=log
    - SYSUDUMP: class=log
    - SYSOUT: class=log
    - DD1: class=input, DSN=FLAIBAM.IN.FLCLI, DISP=SHR
    - DD2: class=input, DSN=FLAIBAM.IN.FLSLD, DISP=SHR
    - DD3: class=output, DSN=FLAIBAM.OUT.FSLDATU, DISP=NEW,CATLG,DELETE, RECFM=FB, LRECL=88
- **BR14A** — tipo: UTILITY  
  - PGM: `IEFBR14`
    - DD1: class=output, DSN=FLAIBAM.OUT.CLIATU, DISP=MOD,DELETE,DELETE
    - DD2: class=output, DSN=FLAIBAM.OUT.CLIZERO, DISP=MOD,DELETE,DELETE
- **PROG2** — tipo: COBOL  
  - PGM: `PROGRAM2`
  - Programas COBOL detectados: PROGRAM2
    - SYSPRINT: class=log
    - SYSUDUMP: class=log
    - SYSOUT: class=log
    - DD1: class=input, DSN=FLAIBAM.OUT.FSLDATU, DISP=SHR
    - DD2: class=input, DSN=FLAIBAM.IN.FLCRED, DISP=SHR
    - DD3: class=input, DSN=FLAIBAM.IN.FLDEB, DISP=SHR
    - DD4: class=output, DSN=FLAIBAM.OUT.CLIATU, DISP=NEW,CATLG,DELETE, RECFM=FB, LRECL=88
    - DD5: class=output, DSN=FLAIBAM.OUT.CLIZERO, DISP=NEW,CATLG,DELETE, RECFM=FB, LRECL=88
- **BR14A** — tipo: UTILITY  
  - PGM: `IEFBR14`
    - DD1: class=output, DSN=FLAIBAM.OUT.CLITIER, DISP=MOD,DELETE,DELETE
- **PROG3** — tipo: COBOL  
  - PGM: `PROGRAM3`
  - Programas COBOL detectados: PROGRAM3
    - SYSPRINT: class=log
    - SYSUDUMP: class=log
    - SYSOUT: class=log
    - DD1: class=input, DSN=FLAIBAM.OUT.CLIATU, DISP=SHR
    - DD2: class=output, DSN=FLAIBAM.OUT.CLITIER, DISP=NEW,CATLG,DELETE, RECFM=FB, LRECL=88

---
## Programas COBOL analisados
### PROGRAM1
- Fonte encontrado: **sim** (`C:\COBOL Files\batch2cloud_v3\files\cbl\PROGRAM1.cbl`)

### PROGRAM2
- Fonte encontrado: **sim** (`C:\COBOL Files\batch2cloud_v3\files\cbl\PROGRAM2.cbl`)

### PROGRAM3
- Fonte encontrado: **sim** (`C:\COBOL Files\batch2cloud_v3\files\cbl\PROGRAM3.cbl`)

---