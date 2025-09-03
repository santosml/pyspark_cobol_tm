# Inventário JCL/COBOL — `CREASTMT.JCL`

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
- **DELDEF01** — tipo: UTILITY  
  - PGM: `IDCAMS`
    - SYSPRINT: class=log
    - SYSIN: class=other
- **STEP010** — tipo: UTILITY  
  - PGM: `SORT`
    - SORTIN: class=input, DSN=AWS.M2.CARDDEMO.TRANSACT.VSAM.KSDS, DISP=SHR
    - SYSPRINT: class=log
    - SYSOUT: class=log
    - SORTOUT: class=output, DSN=AWS.M2.CARDDEMO.TRXFL.SEQ, DISP=NEW,CATLG,DELETE, RECFM=FB, LRECL=350
    - SYSIN: class=other
- **STEP020** — tipo: UTILITY  
  - PGM: `IDCAMS`
    - SYSPRINT: class=log
    - INFILE: class=input, DSN=AWS.M2.CARDDEMO.TRXFL.SEQ, DISP=SHR
    - OUTFILE: class=input, DSN=AWS.M2.CARDDEMO.TRXFL.VSAM.KSDS, DISP=SHR
    - SYSIN: class=other
- **STEP030** — tipo: UTILITY  
  - PGM: `IEFBR14`
    - HTMLFILE: class=output, DSN=AWS.M2.CARDDEMO.STATEMNT.HTML, DISP=MOD,DELETE,DELETE, RECFM=FB, LRECL=80
    - STMTFILE: class=output, DSN=AWS.M2.CARDDEMO.STATEMNT.PS, DISP=MOD,DELETE,DELETE, RECFM=FB, LRECL=80
- **STEP040** — tipo: COBOL  
  - PGM: `CBSTM03A`
  - Programas COBOL detectados: CBSTM03A
    - STEPLIB: class=input, DSN=AWS.M2.CARDDEMO.LOADLIB, DISP=SHR
    - SYSPRINT: class=log
    - SYSOUT: class=log
    - TRNXFILE: class=input, DSN=AWS.M2.CARDDEMO.TRXFL.VSAM.KSDS, DISP=SHR
    - XREFFILE: class=input, DSN=AWS.M2.CARDDEMO.CARDXREF.VSAM.KSDS, DISP=SHR
    - ACCTFILE: class=input, DSN=AWS.M2.CARDDEMO.ACCTDATA.VSAM.KSDS, DISP=SHR
    - CUSTFILE: class=input, DSN=AWS.M2.CARDDEMO.CUSTDATA.VSAM.KSDS, DISP=SHR
    - STMTFILE: class=output, DSN=AWS.M2.CARDDEMO.STATEMNT.PS, DISP=NEW,CATLG,DELETE, RECFM=FB, LRECL=80
    - HTMLFILE: class=output, DSN=AWS.M2.CARDDEMO.STATEMNT.HTML, DISP=NEW,CATLG,DELETE, RECFM=FB, LRECL=100

---
## Programas COBOL analisados
### CBSTM03A
- Fonte encontrado: **sim** (`C:\COBOL Files\batch2cloud_v3\files\cbl\CBSTM03A.cbl`)

---