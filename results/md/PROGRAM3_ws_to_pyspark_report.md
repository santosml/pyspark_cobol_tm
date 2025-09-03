# Conversão FILE SECTION + WORKING-STORAGE → PySpark

- Modelo preferido: `None` (roteado via política `convert`)
- Tokens máx. de saída: `1800`
- Tempo total: `70.01s`
- Arquivo de entrada (COBOL): `results\transform\PROGRAM3_COBOL_clean_WS.txt`
- Arquivo de prompt: `Prompt\04_cobol_pyspark_prompt otimizado_nova10.txt`
- Saída gerada: `results\py\ws\PROGRAM3_COBOL_clean_WS_pyspark.py`

## Observações
- O código foi gerado com base nos layouts de FILE/WS; ajuste paths e formatos de leitura conforme o ambiente.
- Caso os arquivos sejam posicionais, certifique-se de aplicar *schemas* com larguras fixas.
- Se houver múltiplos arquivos/tabelas, revise os `StructType` e as funções auxiliares geradas.
