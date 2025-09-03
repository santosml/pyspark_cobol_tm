from pyspark.sql import SparkSession
from pyspark.sql.types import StructType, StructField, StringType, IntegerType

# Initialize Spark Session
spark = SparkSession.builder.appName("COBOL_to_PySpark").getOrCreate()

# Define schemas for input files
file_schema = StructType([
    StructField("NUM", StringType(), True),
    StructField("FIRST_NAME", StringType(), True),
    StructField("LAST_NAME", StringType(), True),
    StructField("ACCT_BALANCE", IntegerType(), True),
    StructField("FILLER", StringType(), True)
])

# Define schema for output files
outfl_schema = StructType([
    StructField("FILLER", StringType(), True)
])

# Function to read input files
def read_input_file(file_path):
    return spark.read.format("csv") \
        .option("header", "false") \
        .option("delimiter", "") \
        .schema(file_schema) \
        .load(file_path)

# Read input files
file01_df = read_input_file("FILE01")
file02_df = read_input_file("FILE02")
file03_df = read_input_file("FILE03")

# Create empty DataFrames for output files
outfl1_df = spark.createDataFrame([], outfl_schema)
outfl2_df = spark.createDataFrame([], outfl_schema)
outfl3_df = spark.createDataFrame([], outfl_schema)

# Map COBOL fields to PySpark columns
# FILE01-AREA -> file01_df
# NUM-FILE01 -> NUM
# FIRST-NAME-FILE01 -> FIRST_NAME
# LAST-NAME-FILE01 -> LAST_NAME
# ACCT-BALANCE-FILE01 -> ACCT_BALANCE

# FILE02-AREA -> file02_df
# NUM-FILE02 -> NUM
# FIRST-NAME-FILE02 -> FIRST_NAME
# LAST-NAME-FILE02 -> LAST_NAME
# ACCT-BALANCE-FILE02 -> ACCT_BALANCE

# FILE03-AREA -> file03_df
# NUM-FILE03 -> NUM
# FIRST-NAME-FILE03 -> FIRST_NAME
# LAST-NAME-FILE03 -> LAST_NAME
# ACCT-BALANCE-FILE03 -> ACCT_BALANCE

# OUTFL1-AREA -> outfl1_df
# FILLER -> FILLER

# OUTFL2-AREA -> outfl2_df
# FILLER -> FILLER

# OUTFL3-AREA -> outfl3_df
# FILLER -> FILLER

# ==== Rotinas convertidas (Procedure Division) ====

# ===== Rotina: 0210-SOMA-CREDITO =====

def R0210_SOMA_CREDITO(file02_df, wk_acct_balance):
    # Assumindo que wk_acct_balance é um valor numérico
    # e que estamos processando um registro específico de file02_df
    
    # Obtém o valor de ACCT_BALANCE do registro atual de file02_df
    acct_balance_file02 = file02_df.select("ACCT_BALANCE").first()[0]
    
    # Soma o valor ao wk_acct_balance
    wk_acct_balance += acct_balance_file02
    
    return wk_acct_balance

# ===== Rotina: 0400-WRITE-OUTFL1 =====

def R0400_WRITE_OUTFL1(file01_df, wk_acct_balance, outfl1_df):
    # Create a new row for OUTFL1 based on FILE01 and WK-ACCT-BALANCE
    new_row = file01_df.select(
        file01_df.NUM,
        file01_df.FIRST_NAME,
        file01_df.LAST_NAME,
        wk_acct_balance.alias("ACCT_BALANCE")
    )

    # Convert the new row to a string representation
    new_row_str = new_row.select(
        concat(
            col("NUM"),
            col("FIRST_NAME"),
            col("LAST_NAME"),
            format_string("%010d", col("ACCT_BALANCE"))
        ).alias("FILLER")
    )

    # Append the new row to OUTFL1
    outfl1_df = outfl1_df.union(new_row_str)

    # Increment RECORD-COUNT-OUTFL1
    record_count_outfl1 = outfl1_df.count()

    return outfl1_df, record_count_outfl1

# ===== Rotina: 0400-WRITE-OUTFL2 =====

def R0400_WRITE_OUTFL2(file01_df, wk_acct_balance, outfl2_df):
    # Create a new row for OUTFL2 based on FILE01 and WK-ACCT-BALANCE
    new_row = file01_df.select(
        file01_df.NUM,
        file01_df.FIRST_NAME,
        file01_df.LAST_NAME,
        wk_acct_balance.alias("ACCT_BALANCE")
    )

    # Convert the new row to a string representation
    new_row_str = new_row.select(
        concat_ws("", new_row.NUM, new_row.FIRST_NAME, new_row.LAST_NAME, 
                  format_string("%010d", new_row.ACCT_BALANCE)).alias("FILLER")
    )

    # Append the new row to OUTFL2
    outfl2_df = outfl2_df.union(new_row_str)

    # Increment RECORD-COUNT-OUTFL2
    record_count_outfl2 = outfl2_df.count()

    return outfl2_df, record_count_outfl2

# ===== Rotina: 0400-WRITE-OUTFL3 =====

def R0400_WRITE_OUTFL3(file01_df, wk_acct_balance, outfl3_df):
    # Create a new row for OUTFL3
    new_row = file01_df.select(
        file01_df.NUM,
        file01_df.FIRST_NAME,
        file01_df.LAST_NAME,
        wk_acct_balance.alias("ACCT_BALANCE")
    )

    # Concatenate all fields into a single FILLER column
    new_row = new_row.select(
        concat_ws("", 
            new_row.NUM, 
            new_row.FIRST_NAME, 
            new_row.LAST_NAME, 
            format_string("%010d", new_row.ACCT_BALANCE)
        ).alias("FILLER")
    )

    # Append the new row to OUTFL3
    outfl3_df = outfl3_df.union(new_row)

    # Increment RECORD-COUNT-OUTFL3
    record_count_outfl3 = outfl3_df.count()

    return outfl3_df, record_count_outfl3

# ===== Rotina: 9999-CLOSE-OUT =====

def R9999_CLOSE_OUT(spark):
    # No need to explicitly close files in PySpark
    # PySpark handles resource management automatically
    
    # However, we can stop the SparkSession to release all resources
    spark.stop()

# ===== Rotina: READ-FILE01 =====

def READ_FILE01(file01_df, record_count_file01):
    # Simulating the read operation and EOF check
    if file01_df.count() > record_count_file01:
        # Read the next record
        current_record = file01_df.limit(record_count_file01 + 1).tail(1)[0]
        
        # Update WK-ACCT-BALANCE
        wk_acct_balance = current_record['ACCT_BALANCE']
        
        # Increment RECORD-COUNT-FILE01
        record_count_file01 += 1
        
        # Simulate NUM-FILE01 for non-EOF condition
        num_file01 = current_record['NUM']
    else:
        # EOF reached
        wk_acct_balance = None
        num_file01 = "9999999999"
    
    return wk_acct_balance, num_file01, record_count_file01

# ===== Rotina: READ-FILE02 =====

def READ_FILE02(file02_df, record_count_file02):
    # Get the next record from file02_df
    next_record = file02_df.limit(1)
    
    # Check if there's a next record
    if next_record.count() > 0:
        # Increment the record count
        record_count_file02 += 1
        
        # Return the next record and updated count
        return next_record.first(), record_count_file02
    else:
        # If no more records, return a dummy record with NUM = 9999999999
        from pyspark.sql.types import Row
        dummy_record = Row(NUM="9999999999", FIRST_NAME=None, LAST_NAME=None, ACCT_BALANCE=None, FILLER=None)
        
        return dummy_record, record_count_file02

# ===== Rotina: READ-FILE03 =====

def READ_FILE03(file03_df, record_count_file03):
    # Simulating EOF check by comparing the current record number to the total count
    total_records = file03_df.count()
    
    if record_count_file03.value < total_records:
        # Not at EOF, read next record
        current_record = file03_df.filter(f"NUM == '{record_count_file03.value + 1}'").first()
        if current_record:
            record_count_file03.add(1)
            return current_record
        else:
            # If no record found, treat as EOF
            return {"NUM": "9999999999"}
    else:
        # At EOF
        return {"NUM": "9999999999"}

# ===== Rotina: 0100-INITIALIZE =====

def R0100_INITIALIZE(file01_df, file02_df, file03_df, outfl1_df, outfl2_df, outfl3_df, record_count_file01, record_count_file02, record_count_file03):
    # No need to open files in PySpark as they are already loaded as DataFrames
    
    # Perform READ-FILE01
    file01_df, record_count_file01 = READ_FILE01(file01_df, record_count_file01)
    
    # Perform READ-FILE02
    file02_df, record_count_file02 = READ_FILE02(file02_df, record_count_file02)
    
    # Perform READ-FILE03
    file03_df, record_count_file03 = READ_FILE03(file03_df, record_count_file03)
    
    return file01_df, file02_df, file03_df, outfl1_df, outfl2_df, outfl3_df, record_count_file01, record_count_file02, record_count_file03

# ===== Rotina: 0220-SUBTRAI-DEBITO =====

def R0220_SUBTRAI_DEBITO(file03_df, wk_acct_balance, outfl3_df):
    print('0220-SUBTRAI-DEBITO')
    print(f'ACCT-BALANCE-FILE03= {file03_df.select("ACCT_BALANCE").first()[0]}')
    print(f'WK-ACCT-BALANCE    = {wk_acct_balance}')
    
    acct_balance_file03 = file03_df.select("ACCT_BALANCE").first()[0]
    wk_acct_balance -= acct_balance_file03
    
    outfl3_df = R0400_WRITE_OUTFL3(file03_df, wk_acct_balance, outfl3_df)
    
    print(f'APOS               = {wk_acct_balance}')
    
    return wk_acct_balance, outfl3_df

# ===== Rotina: 0230-CHECA-SALDO =====

def R0230_CHECA_SALDO(file01_df, wk_acct_balance, outfl2_df):
    # Verifica se o saldo da conta é zero
    if file01_df.filter(file01_df.ACCT_BALANCE == 0).count() > 0:
        # Se for zero, chama a função para escrever em OUTFL2
        outfl2_df = R0400_WRITE_OUTFL2(file01_df, wk_acct_balance, outfl2_df)
    
    return outfl2_df

# ===== Rotina: 0200-PROCESS =====

def R0200_PROCESS(file01_df, file02_df, file03_df, outfl1_df, outfl2_df, outfl3_df, record_count_file01, record_count_file02, record_count_file03, wk_acct_balance):
    record_count_limit = 0
    
    while True:
        record_count_limit += 1
        if record_count_limit > 50:
            print('TRAVA LOOPING')
            return None
        
        num_file01 = file01_df.select("NUM").first()[0]
        num_file02 = file02_df.select("NUM").first()[0]
        num_file03 = file03_df.select("NUM").first()[0]
        
        if num_file01 < num_file02 and num_file01 < num_file03:
            outfl1_df = R0400_WRITE_OUTFL1(file01_df, wk_acct_balance, outfl1_df)
            outfl2_df = R0230_CHECA_SALDO(file01_df, wk_acct_balance, outfl2_df)
            file01_df, record_count_file01 = READ_FILE01(file01_df, record_count_file01)
        elif num_file02 < num_file01:
            file02_df, record_count_file02 = READ_FILE02(file02_df, record_count_file02)
        elif num_file03 < num_file01:
            file03_df, record_count_file03 = READ_FILE03(file03_df, record_count_file03)
        
        if num_file01 == num_file02:
            wk_acct_balance = R0210_SOMA_CREDITO(file02_df, wk_acct_balance)
            file02_df, record_count_file02 = READ_FILE02(file02_df, record_count_file02)
        
        if num_file01 == num_file03:
            wk_acct_balance, outfl3_df = R0220_SUBTRAI_DEBITO(file03_df, wk_acct_balance, outfl3_df)
            file03_df, record_count_file03 = READ_FILE03(file03_df, record_count_file03)
        
        if file01_df.count() == 0 or file02_df.count() == 0 or file03_df.count() == 0:
            break
    
    return file01_df, file02_df, file03_df, outfl1_df, outfl2_df, outfl3_df, record_count_file01, record_count_file02, record_count_file03, wk_acct_balance

# ===== Rotina: 0000-MAIN =====

def R0000_MAIN(file01_df, file02_df, file03_df, outfl1_df, outfl2_df, outfl3_df):
    record_count_file01, record_count_file02, record_count_file03, wk_acct_balance = R0100_INITIALIZE(file01_df, file02_df, file03_df, outfl1_df, outfl2_df, outfl3_df, 0, 0, 0)
    
    while not (file01_df.rdd.isEmpty() and file02_df.rdd.isEmpty() and file03_df.rdd.isEmpty()):
        file01_df, file02_df, file03_df, outfl1_df, outfl2_df, outfl3_df, record_count_file01, record_count_file02, record_count_file03, wk_acct_balance = R0200_PROCESS(
            file01_df, file02_df, file03_df, outfl1_df, outfl2_df, outfl3_df, 
            record_count_file01, record_count_file02, record_count_file03, wk_acct_balance
        )
    
    R9999_CLOSE_OUT(spark)
    
    print('********************')
    print('FIM DE PROCESSAMENTO')
    print(f'RECORD READ  FILE01: {record_count_file01}')
    print(f'RECORD READ  FILE02: {record_count_file02}')
    print(f'RECORD READ  FILE03: {record_count_file03}')
    print(f'RECORD WRITE OUTFL1: {outfl1_df.count()}')
    print(f'RECORD WRITE OUTFL2: {outfl2_df.count()}')
    print(f'RECORD WRITE OUTFL3: {outfl3_df.count()}')
    print('FIM DE PROCESSAMENTO')
    print('********************')
    
    spark.stop()
# Nenhum código encontrado na Procedure Division principal