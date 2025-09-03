# Conversão COBOL → PySpark por rotina
- Programa: `program2`
- Rotinas detectadas: **13**

## 0210-SOMA-CREDITO
- ✅ Convertida
- Chama: (nenhuma)
- Chamada por: 0200-PROCESS
## 0400-WRITE-OUTFL1
- ✅ Convertida
- Chama: (nenhuma)
- Chamada por: 0200-PROCESS
## 0400-WRITE-OUTFL2
- ✅ Convertida
- Chama: (nenhuma)
- Chamada por: 0230-CHECA-SALDO
## 0400-WRITE-OUTFL3
- ✅ Convertida
- Chama: (nenhuma)
- Chamada por: 0220-SUBTRAI-DEBITO
## 9999-CLOSE-OUT
- ✅ Convertida
- Chama: (nenhuma)
- Chamada por: 0000-MAIN
## READ-FILE01
- ✅ Convertida
- Chama: (nenhuma)
- Chamada por: 0100-INITIALIZE, 0200-PROCESS
## READ-FILE02
- ✅ Convertida
- Chama: (nenhuma)
- Chamada por: 0100-INITIALIZE, 0200-PROCESS
## READ-FILE03
- ✅ Convertida
- Chama: (nenhuma)
- Chamada por: 0100-INITIALIZE, 0200-PROCESS
## 0100-INITIALIZE
- ✅ Convertida
- Chama: READ-FILE01, READ-FILE02, READ-FILE03
- Chamada por: 0000-MAIN
## 0220-SUBTRAI-DEBITO
- ✅ Convertida
- Chama: 0400-WRITE-OUTFL3
- Chamada por: 0200-PROCESS
## 0230-CHECA-SALDO
- ✅ Convertida
- Chama: 0400-WRITE-OUTFL2
- Chamada por: 0200-PROCESS
## 0200-PROCESS
- ✅ Convertida
- Chama: 0210-SOMA-CREDITO, 0220-SUBTRAI-DEBITO, 0230-CHECA-SALDO, 0400-WRITE-OUTFL1, READ-FILE01, READ-FILE02, READ-FILE03
- Chamada por: 0000-MAIN
## 0000-MAIN
- ✅ Convertida
- Chama: 0100-INITIALIZE, 0200-PROCESS, 9999-CLOSE-OUT
- Chamada por: (ninguém)

---
**Resumo:** ✅ 13 | ❌ 0
