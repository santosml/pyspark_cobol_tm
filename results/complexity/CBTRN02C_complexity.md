# Análise de Complexidade — CBTRN02C

## Resumo
- **Linhas totais (arquivo):** 732
- **Linhas de código (sem comentários/brancos):** 619
- **Rotinas (parágrafos) na Procedure Division:** 27
- **Score (ajustável no JSON):** 1099.9
- **Nível:** **complexo** _(muito simples, simples, médio, complexo, muito complexo)_
- Termômetro: `████░`

### Rotinas detectadas

0000-DALYTRAN-OPEN, 0100-TRANFILE-OPEN, 0200-XREFFILE-OPEN, 0300-DALYREJS-OPEN, 0400-ACCTFILE-OPEN, 0500-TCATBALF-OPEN, 1000-DALYTRAN-GET-NEXT, 1500-VALIDATE-TRAN, 1500-A-LOOKUP-XREF, 1500-B-LOOKUP-ACCT, 2000-POST-TRANSACTION, 2500-WRITE-REJECT-REC, 2700-UPDATE-TCATBAL, 2700-A-CREATE-TCATBAL-REC, 2700-B-UPDATE-TCATBAL-REC, 2800-UPDATE-ACCOUNT-REC, END-REWRITE, 2900-WRITE-TRANSACTION-FILE, 9000-DALYTRAN-CLOSE, 9100-TRANFILE-CLOSE, 9200-XREFFILE-CLOSE, 9300-DALYREJS-CLOSE, 9400-ACCTFILE-CLOSE, 9500-TCATBALF-CLOSE, Z-GET-DB2-FORMAT-TIMESTAMP, 9999-ABEND-PROGRAM, 9910-DISPLAY-IO-STATUS

## Linhas por Seção

| Seção | Linhas |
|---|---|
| IDENTIFICATION DIVISION | 3 |
| ENVIRONMENT DIVISION | 37 |
| DATA DIVISION | 128 |
| PROCEDURE DIVISION | 539 |

### Sub-seções da DATA DIVISION

| Sub-seção | Linhas |
|---|---|
| FILE | 33 |
| WORKING-STORAGE | 93 |

## Comandos COBOL — Frequência

| Comando COBOL | Qtd |
|---|---|
| MOVE | 127 |
| PERFORM | 61 |
| IF | 48 |
| DISPLAY | 26 |
| EXIT | 23 |
| CONTINUE | 22 |
| ADD | 7 |
| CLOSE | 6 |
| OPEN | 6 |
| READ | 4 |
| WRITE | 3 |
| REWRITE | 2 |
| CALL | 1 |
| COMPUTE | 1 |
| GOBACK | 1 |
| INITIALIZE | 1 |
| PERFORM UNTIL | 1 |
| START | 1 |

## DB2 / SQL — Métricas

_Nenhum bloco EXEC SQL encontrado._
