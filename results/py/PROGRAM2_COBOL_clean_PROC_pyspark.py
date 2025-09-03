from pyspark.sql import SparkSession
from pyspark.sql.types import StructType, StructField, StringType, IntegerType

# Initialize Spark Session
spark = SparkSession.builder.appName("COBOL_to_PySpark").getOrCreate()

# Define schemas for input files
file01_schema = StructType([
    StructField("NUM", StringType(), True),
    StructField("FIRST_NAME", StringType(), True),
    StructField("LAST_NAME", StringType(), True),
    StructField("ACCT_BALANCE", IntegerType(), True),
    StructField("FILLER", StringType(), True)
])

file02_schema = StructType([
    StructField("NUM", StringType(), True),
    StructField("FIRST_NAME", StringType(), True),
    StructField("LAST_NAME", StringType(), True),
    StructField("ACCT_BALANCE", IntegerType(), True),
    StructField("FILLER", StringType(), True)
])

file03_schema = StructType([
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

def read_input_file(file_path, schema):
    """
    Read input file using the provided schema
    """
    return spark.read.csv(file_path, schema=schema, sep='\n', header=False)

# Read input files
file01_df = read_input_file("FILE01", file01_schema)
file02_df = read_input_file("FILE02", file02_schema)
file03_df = read_input_file("FILE03", file03_schema)

# Create empty DataFrames for output files
outfl1_df = spark.createDataFrame([], outfl_schema)
outfl2_df = spark.createDataFrame([], outfl_schema)
outfl3_df = spark.createDataFrame([], outfl_schema)

# Map COBOL fields to PySpark columns
# FILE01-AREA:
#   NUM-FILE01 -> NUM
#   FIRST-NAME-FILE01 -> FIRST_NAME
#   LAST-NAME-FILE01 -> LAST_NAME
#   ACCT-BALANCE-FILE01 -> ACCT_BALANCE
#   FILLER -> FILLER

# FILE02-AREA:
#   NUM-FILE02 -> NUM
#   FIRST-NAME-FILE02 -> FIRST_NAME
#   LAST-NAME-FILE02 -> LAST_NAME
#   ACCT-BALANCE-FILE02 -> ACCT_BALANCE
#   FILLER -> FILLER

# FILE03-AREA:
#   NUM-FILE03 -> NUM
#   FIRST-NAME-FILE03 -> FIRST_NAME
#   LAST-NAME-FILE03 -> LAST_NAME
#   ACCT-BALANCE-FILE03 -> ACCT_BALANCE
#   FILLER -> FILLER

# OUTFL1-AREA, OUTFL2-AREA, OUTFL3-AREA:
#   FILLER -> FILLER

# Note: The cluster is not stopped at the end of this script

# ==== Rotinas convertidas (Procedure Division) ====

# ===== Rotina: 0210-SOMA-CREDITO =====

def R0210_SOMA_CREDITO(file02_df, wk_acct_balance):
    # Assuming we're working with the current record of file02_df
    # and wk_acct_balance is a running total
    
    # Get the ACCT_BALANCE from the current record of file02_df
    acct_balance_file02 = file02_df.select("ACCT_BALANCE").first()[0]
    
    # Add ACCT_BALANCE to WK-ACCT-BALANCE
    wk_acct_balance += acct_balance_file02
    
    return wk_acct_balance

# ===== Rotina: 0400-WRITE-OUTFL1 =====

def R0400_WRITE_OUTFL1(file01_df, wk_acct_balance, outfl1_df, record_count_outfl1):
    # Create a new row with FILE01-AREA data and WK-ACCT-BALANCE
    new_row = file01_df.select(
        file01_df.NUM,
        file01_df.FIRST_NAME,
        file01_df.LAST_NAME,
        file01_df.FILLER
    ).withColumn("ACCT_BALANCE", wk_acct_balance)

    # Append the new row to OUTFL1-AREA
    outfl1_df = outfl1_df.union(new_row)

    # Increment RECORD-COUNT-OUTFL1
    record_count_outfl1 += 1

    return outfl1_df, record_count_outfl1

# ===== Rotina: 0400-WRITE-OUTFL2 =====

def R0400_WRITE_OUTFL2(file01_df, wk_acct_balance, outfl2_df, record_count_outfl2):
    # Create a new row for OUTFL2 based on FILE01 and WK-ACCT-BALANCE
    new_row = file01_df.select(
        file01_df.NUM,
        file01_df.FIRST_NAME,
        file01_df.LAST_NAME,
        (wk_acct_balance.cast("string")).alias("ACCT_BALANCE"),
        file01_df.FILLER
    )

    # Combine all fields into a single string column
    new_row = new_row.select(
        concat_ws(",", new_row.NUM, new_row.FIRST_NAME, new_row.LAST_NAME, new_row.ACCT_BALANCE, new_row.FILLER).alias("FILLER")
    )

    # Append the new row to OUTFL2
    outfl2_df = outfl2_df.union(new_row)

    # Increment the record count
    record_count_outfl2 += 1

    return outfl2_df, record_count_outfl2

# ===== Rotina: 0400-WRITE-OUTFL3 =====

def R0400_WRITE_OUTFL3(file01_df, wk_acct_balance, outfl3_df, record_count_outfl3):
    # Create a new row for OUTFL3 based on FILE01 and WK-ACCT-BALANCE
    new_row = file01_df.select(
        file01_df.NUM,
        file01_df.FIRST_NAME,
        file01_df.LAST_NAME,
        wk_acct_balance.alias("ACCT_BALANCE"),
        file01_df.FILLER
    )

    # Append the new row to OUTFL3
    outfl3_df = outfl3_df.union(new_row)

    # Increment the record count
    record_count_outfl3 += 1

    return outfl3_df, record_count_outfl3

# ===== Rotina: 9999-CLOSE-OUT =====

def R9999_CLOSE_OUT():
    # No need to explicitly close files in PySpark
    # PySpark handles resource management automatically
    
    # If you want to perform any cleanup or finalization, you can add it here
    # For example, you might want to stop the SparkSession:
    # spark.stop()
    
    # But since the instructions mention not to stop the cluster,
    # we'll leave this function empty as a placeholder
    pass

# ===== Rotina: READ-FILE01 =====

def READ_FILE01(file01_df, eof_file01, wk_acct_balance, record_count_file01):
    if eof_file01 == 'N':
        # Simulate reading next record
        next_record = file01_df.filter(file01_df.NUM != '9999999999').orderBy('NUM').limit(1)
        
        if next_record.count() == 0:
            eof_file01 = 'Y'
        else:
            wk_acct_balance = next_record.select('ACCT_BALANCE').first()[0]
            record_count_file01 += 1
            
            # Update file01_df to exclude the read record
            file01_df = file01_df.filter(file01_df.NUM != next_record.first().NUM)
    
    if eof_file01 == 'Y':
        num_file01 = '9999999999'
    else:
        num_file01 = next_record.select('NUM').first()[0]
    
    return file01_df, eof_file01, num_file01, wk_acct_balance, record_count_file01

# ===== Rotina: READ-FILE02 =====

def READ_FILE02(file02_df, eof_file02, record_count_file02):
    # Check if we've reached the end of the DataFrame
    if eof_file02 == 'N':
        # Get the next row
        next_row = file02_df.limit(1)
        
        # Check if there's a next row
        if next_row.count() == 0:
            eof_file02 = 'Y'
        else:
            record_count_file02 += 1
    
    # If we've reached the end of the file
    if eof_file02 == 'Y':
        # Set NUM-FILE02 to 9999999999
        file02_df = file02_df.withColumn("NUM", lit("9999999999"))
    
    return file02_df, eof_file02, record_count_file02

# ===== Rotina: READ-FILE03 =====

def READ_FILE03(file03_df, eof_file03, record_count_file03):
    if eof_file03 == 'N':
        # Simulate reading the next record
        next_record = file03_df.filter(file03_df.NUM != '9999999999').first()
        
        if next_record is None:
            eof_file03 = 'Y'
    
    if eof_file03 == 'Y':
        # Set NUM-FILE03 to 9999999999 to indicate end of file
        file03_df = file03_df.withColumn("NUM", lit("9999999999"))
    else:
        record_count_file03 += 1
    
    return file03_df, eof_file03, record_count_file03

# ===== Rotina: 0100-INITIALIZE =====

def R0100_INITIALIZE(file01_df, file02_df, file03_df, eof_file01, eof_file02, eof_file03, wk_acct_balance, record_count_file01, record_count_file02, record_count_file03):
    # No need to open files in PySpark as DataFrames are already loaded

    # Perform initial reads
    file01_df, eof_file01, wk_acct_balance, record_count_file01 = READ_FILE01(file01_df, eof_file01, wk_acct_balance, record_count_file01)
    file02_df, eof_file02, record_count_file02 = READ_FILE02(file02_df, eof_file02, record_count_file02)
    file03_df, eof_file03, record_count_file03 = READ_FILE03(file03_df, eof_file03, record_count_file03)

    return file01_df, file02_df, file03_df, eof_file01, eof_file02, eof_file03, wk_acct_balance, record_count_file01, record_count_file02, record_count_file03

# ===== Rotina: 0220-SUBTRAI-DEBITO =====

def R0220_SUBTRAI_DEBITO(file03_df, wk_acct_balance, outfl3_df, record_count_outfl3):
    print('0220-SUBTRAI-DEBITO')
    print(f'ACCT-BALANCE-FILE03= {file03_df.select("ACCT_BALANCE").first()[0]}')
    print(f'WK-ACCT-BALANCE    = {wk_acct_balance}')
    
    acct_balance_file03 = file03_df.select("ACCT_BALANCE").first()[0]
    wk_acct_balance -= acct_balance_file03
    
    outfl3_df, record_count_outfl3 = R0400_WRITE_OUTFL3(file03_df, wk_acct_balance, outfl3_df, record_count_outfl3)
    
    print(f'APOS               = {wk_acct_balance}')
    
    return wk_acct_balance, outfl3_df, record_count_outfl3

# ===== Rotina: 0230-CHECA-SALDO =====

def R0230_CHECA_SALDO(file01_df, wk_acct_balance, outfl2_df, record_count_outfl2):
    # Check if ACCT_BALANCE is zero
    if file01_df.filter(file01_df.ACCT_BALANCE == 0).count() > 0:
        # If ACCT_BALANCE is zero, call R0400_WRITE_OUTFL2
        outfl2_df, record_count_outfl2 = R0400_WRITE_OUTFL2(file01_df, wk_acct_balance, outfl2_df, record_count_outfl2)
    
    return outfl2_df, record_count_outfl2

# ===== Rotina: 0200-PROCESS =====

def R0200_PROCESS(file01_df, file02_df, file03_df, outfl1_df, outfl2_df, outfl3_df, record_count_limit, wk_acct_balance, record_count_file01, record_count_file02, record_count_file03, record_count_outfl1, record_count_outfl2, record_count_outfl3):
    record_count_limit += 1
    if record_count_limit > 50:
        print('TRAVA LOOPING')
        return None  # Equivalent to STOP RUN

    file01_num = file01_df.select("NUM").first()[0]
    file02_num = file02_df.select("NUM").first()[0]
    file03_num = file03_df.select("NUM").first()[0]

    if file01_num < file02_num and file01_num < file03_num:
        outfl1_df, record_count_outfl1 = R0400_WRITE_OUTFL1(file01_df, wk_acct_balance, outfl1_df, record_count_outfl1)
        wk_acct_balance = R0230_CHECA_SALDO(file01_df, wk_acct_balance, outfl2_df, record_count_outfl2)
        file01_df, eof_file01, wk_acct_balance, record_count_file01 = READ_FILE01(file01_df, False, wk_acct_balance, record_count_file01)
    elif file02_num < file01_num:
        file02_df, eof_file02, record_count_file02 = READ_FILE02(file02_df, False, record_count_file02)
    elif file03_num < file01_num:
        file03_df, eof_file03, record_count_file03 = READ_FILE03(file03_df, False, record_count_file03)

    if file01_num == file02_num:
        wk_acct_balance = R0210_SOMA_CREDITO(file02_df, wk_acct_balance)
        file02_df, eof_file02, record_count_file02 = READ_FILE02(file02_df, False, record_count_file02)

    if file01_num == file03_num:
        wk_acct_balance, outfl3_df, record_count_outfl3 = R0220_SUBTRAI_DEBITO(file03_df, wk_acct_balance, outfl3_df, record_count_outfl3)
        file03_df, eof_file03, record_count_file03 = READ_FILE03(file03_df, False, record_count_file03)

    return file01_df, file02_df, file03_df, outfl1_df, outfl2_df, outfl3_df, record_count_limit, wk_acct_balance, record_count_file01, record_count_file02, record_count_file03, record_count_outfl1, record_count_outfl2, record_count_outfl3

# ===== Rotina: 0000-MAIN =====

def R0000_MAIN(file01_df, file02_df, file03_df, outfl1_df, outfl2_df, outfl3_df):
    eof_file01, eof_file02, eof_file03 = False, False, False
    wk_acct_balance = 0
    record_count_file01, record_count_file02, record_count_file03 = 0, 0, 0
    record_count_outfl1, record_count_outfl2, record_count_outfl3 = 0, 0, 0
    record_count_limit = float('inf')

    eof_file01, eof_file02, eof_file03, wk_acct_balance, record_count_file01, record_count_file02, record_count_file03 = R0100_INITIALIZE(
        file01_df, file02_df, file03_df, eof_file01, eof_file02, eof_file03, wk_acct_balance, 
        record_count_file01, record_count_file02, record_count_file03
    )

    while not (eof_file01 and eof_file02 and eof_file03):
        file01_df, file02_df, file03_df, outfl1_df, outfl2_df, outfl3_df, wk_acct_balance, \
        record_count_file01, record_count_file02, record_count_file03, \
        record_count_outfl1, record_count_outfl2, record_count_outfl3, \
        eof_file01, eof_file02, eof_file03 = R0200_PROCESS(
            file01_df, file02_df, file03_df, outfl1_df, outfl2_df, outfl3_df,
            record_count_limit, wk_acct_balance,
            record_count_file01, record_count_file02, record_count_file03,
            record_count_outfl1, record_count_outfl2, record_count_outfl3
        )

    R9999_CLOSE_OUT()

    print('********************')
    print('FIM DE PROCESSAMENTO')
    print(f'RECORD READ  FILE01: {record_count_file01}')
    print(f'RECORD READ  FILE02: {record_count_file02}')
    print(f'RECORD READ  FILE03: {record_count_file03}')
    print(f'RECORD WRITE OUTFL1: {record_count_outfl1}')
    print(f'RECORD WRITE OUTFL2: {record_count_outfl2}')
    print(f'RECORD WRITE OUTFL3: {record_count_outfl3}')
    print('FIM DE PROCESSAMENTO')
    print('********************')

    return file01_df, file02_df, file03_df, outfl1_df, outfl2_df, outfl3_df
# Nenhum código encontrado na Procedure Division principal