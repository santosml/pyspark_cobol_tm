from pyspark.sql import SparkSession
from pyspark.sql.types import StructType, StructField, StringType, IntegerType

# Initialize Spark Session
spark = SparkSession.builder.appName("COBOL_to_PySpark").getOrCreate()

# Define schemas for input and output files
file01_schema = StructType([
    StructField("NUM_FILE01", StringType(), True),          # PIC X(10)
    StructField("FIRST_NAME_FILE01", StringType(), True),   # PIC X(10)
    StructField("LAST_NAME_FILE01", StringType(), True),    # PIC X(10)
    StructField("ACCT_BALANCE_FILE01", IntegerType(), True),# PIC 9(10)
    StructField("FILLER", StringType(), True)               # PIC X(48)
])

outfil_schema = StructType([
    StructField("NUM_OUTFIL", StringType(), True),          # PIC X(10)
    StructField("FIRST_NAME_OUTFIL", StringType(), True),   # PIC X(10)
    StructField("LAST_NAME_OUTFIL", StringType(), True),    # PIC X(10)
    StructField("ACCT_BALANCE_OUTFIL", IntegerType(), True),# PIC 9(10)
    StructField("CLIE_TIER_OUTFIL", StringType(), True),    # PIC X(05)
    StructField("FILLER", StringType(), True)               # PIC X(43)
])

def read_file01():
    """
    Read FILE01 using defined schema
    """
    return spark.read.format("csv") \
        .option("header", "false") \
        .option("delimiter", "") \
        .schema(file01_schema) \
        .load("FILE01.txt")

def write_outfil(df):
    """
    Write to OUTFIL using defined schema
    """
    df.write.format("csv") \
        .option("header", "false") \
        .option("delimiter", "") \
        .mode("overwrite") \
        .save("OUTFIL.txt")

# Main processing logic would go here
# For example:
# df_file01 = read_file01()
# processed_df = df_file01.withColumn("CLIE_TIER_OUTFIL", ...)
# write_outfil(processed_df)

# ==== Rotinas convertidas (Procedure Division) ====

# ===== Rotina: 0400-WRITE =====

def R0400_WRITE(df, record_count):
    # Write the current DataFrame to OUTFIL
    write_outfil(df)
    
    # Increment the record count
    record_count += 1
    
    return record_count

# ===== Rotina: 9999-CLOSE-OUT =====

def R9999_CLOSE_OUT():
    # No explicit close operation is needed in PySpark
    # The SparkSession and associated resources will be closed automatically
    # when the application terminates or when spark.stop() is called
    pass

# ===== Rotina: READ-FILE01 =====

def READ_FILE01(df_file01, record_count):
    if df_file01.rdd.isEmpty():
        return df_file01.withColumn("NUM_FILE01", lit("9999999999")), record_count
    else:
        current_row = df_file01.first()
        outfil_row = df_file01.select(
            col("NUM_FILE01").alias("NUM_OUTFIL"),
            col("FIRST_NAME_FILE01").alias("FIRST_NAME_OUTFIL"),
            col("LAST_NAME_FILE01").alias("LAST_NAME_OUTFIL"),
            col("ACCT_BALANCE_FILE01").alias("ACCT_BALANCE_OUTFIL"),
            lit("").alias("CLIE_TIER_OUTFIL"),
            col("FILLER")
        )
        remaining_rows = df_file01.filter(df_file01.NUM_FILE01 != current_row.NUM_FILE01)
        return remaining_rows, record_count + 1

# ===== Rotina: 0100-INITIALIZE =====

def R0100_INITIALIZE(df_file01, record_count):
    # OPEN INPUT FILE01 and OPEN OUTPUT OUTFIL are handled by PySpark read/write functions
    
    # Perform READ-FILE01
    df_file01, record_count = READ_FILE01(df_file01, record_count)
    
    return df_file01, record_count

# ===== Rotina: 0200-PROCESS =====

def R0200_PROCESS(df_file01, record_count):
    record_count_limit = record_count + 1
    if record_count_limit > 20:
        print('TRAVA LOOPING')
        return None  # Equivalent to STOP RUN

    df_processed = df_file01.withColumn("CLIE_TIER_OUTFIL",
        when(col("ACCT_BALANCE_FILE01") < 2000, "TIER5")
        .when(col("ACCT_BALANCE_FILE01") < 4000, "TIER4")
        .when(col("ACCT_BALANCE_FILE01") < 6000, "TIER3")
        .when(col("ACCT_BALANCE_FILE01") < 8000, "TIER2")
        .otherwise("TIER1")
    )

    R0400_WRITE(df_processed, record_count)
    
    return READ_FILE01(df_file01, record_count)

# ===== Rotina: 0000-MAIN =====

def R0000_MAIN():
    df_file01 = read_file01()
    record_count = 0

    df_file01, record_count = R0100_INITIALIZE(df_file01, record_count)

    print('START')
    print('EOF-FILE01', 'Y' if df_file01.rdd.isEmpty() else 'N')

    while not df_file01.rdd.isEmpty():
        df_file01, record_count = R0200_PROCESS(df_file01, record_count)

    R9999_CLOSE_OUT()

    print('RECORD WRITTEN :', record_count)

    spark.stop()

# ===== Função Principal (main) =====

def main():
    try:
        # Inicializar variáveis necessárias
        df_file01 = read_file01()
        record_count = 0

        # Chamar a rotina principal
        R0000_MAIN()

    except Exception as e:
        print(f"Erro durante a execução: {str(e)}")
    finally:
        # Encerrar a SparkSession
        spark.stop()


if __name__ == "__main__":
    main()
