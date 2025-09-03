from pyspark.sql import SparkSession
from pyspark.sql.types import StructType, StructField, StringType, IntegerType

# Initialize Spark Session
spark = SparkSession.builder.appName("COBOL_to_PySpark").getOrCreate()

# Define schemas for FILE01, FILE02, and OUTFIL
file_schema = StructType([
    StructField("NUM", StringType(), True),
    StructField("FIRST_NAME", StringType(), True),
    StructField("LAST_NAME", StringType(), True),
    StructField("ACCT_BALANCE", IntegerType(), True),
    StructField("FILLER", StringType(), True)
])

# Function to read fixed-width files
def read_fixed_width_file(file_path, schema):
    return spark.read.text(file_path).rdd.map(lambda r: (
        r[0][:10],  # NUM
        r[0][10:20],  # FIRST_NAME
        r[0][20:30],  # LAST_NAME
        int(r[0][30:40]),  # ACCT_BALANCE
        r[0][40:]  # FILLER
    )).toDF(schema)

# Read FILE01
# Mapping: NUM-FILE01 -> NUM, FIRST-NAME-FILE01 -> FIRST_NAME, 
#          LAST-NAME-FILE01 -> LAST_NAME, ACCT-BALANCE-FILE01 -> ACCT_BALANCE
file01_df = read_fixed_width_file("FILE01", file_schema)

# Read FILE02
# Mapping: NUM-FILE02 -> NUM, FIRST-NAME-FILE02 -> FIRST_NAME, 
#          LAST-NAME-FILE02 -> LAST_NAME, ACCT-BALANCE-FILE02 -> ACCT_BALANCE
file02_df = read_fixed_width_file("FILE02", file_schema)

# Function to write fixed-width files
def write_fixed_width_file(df, file_path):
    df.select(
        df.NUM.cast("string").substr(1, 10),
        df.FIRST_NAME.cast("string").substr(1, 10),
        df.LAST_NAME.cast("string").substr(1, 10),
        df.ACCT_BALANCE.cast("string").substr(1, 10),
        df.FILLER
    ).rdd.map(lambda row: "".join(row)).saveAsTextFile(file_path)

# Note: OUTFIL processing would be done here before writing
# For example: outfil_df = file01_df.union(file02_df)

# Write OUTFIL
# Mapping: NUM-OUTFIL -> NUM, FIRST-NAME-OUTFIL -> FIRST_NAME, 
#          LAST-NAME-OUTFIL -> LAST_NAME, ACCT-BALANCE-OUTFIL -> ACCT_BALANCE
# write_fixed_width_file(outfil_df, "OUTFIL")

# ==== Rotinas convertidas (Procedure Division) ====

# ===== Rotina: 0400-WRITE =====

def R0400_WRITE(file01_df, file02_df, outfil_df, record_count):
    # Update ACCT_BALANCE in file01_df with values from file02_df
    updated_file01_df = file01_df.join(file02_df, "NUM", "left_outer") \
        .select(
            file01_df["*"],
            file02_df.ACCT_BALANCE.alias("NEW_ACCT_BALANCE")
        ) \
        .withColumn("ACCT_BALANCE", 
            when(col("NEW_ACCT_BALANCE").isNotNull(), col("NEW_ACCT_BALANCE"))
            .otherwise(col("ACCT_BALANCE"))
        ) \
        .drop("NEW_ACCT_BALANCE")

    # Append the updated record to OUTFIL
    outfil_df = outfil_df.union(updated_file01_df)

    # Increment record count
    record_count += 1

    return outfil_df, record_count

# ===== Rotina: 9999-CLOSE-OUT =====

def R9999_CLOSE_OUT(spark):
    # No explicit close operation is needed for DataFrames in PySpark
    # However, we can stop the SparkSession to release resources
    spark.stop()

# ===== Rotina: READ-FILE01 =====

def READ_FILE01(file01_df, record_count_read1):
    # Check if there are more records in FILE01
    if file01_df.count() > 0:
        # Read the next record
        current_record = file01_df.first()
        
        # Update record count
        record_count_read1 += 1
        
        # Return the current record and updated count
        return current_record, record_count_read1, False
    else:
        # If no more records, create a dummy record with NUM set to 9999999999
        dummy_record = {"NUM": "9999999999", "FIRST_NAME": "", "LAST_NAME": "", "ACCT_BALANCE": 0, "FILLER": ""}
        return dummy_record, record_count_read1, True

# ===== Rotina: READ-FILE02 =====

def READ_FILE02(file02_df, record_count_read2):
    # Check if there are more records in FILE02
    if not file02_df.rdd.isEmpty():
        # Get the next record
        current_record = file02_df.first()
        
        # Increment the record count
        record_count_read2 += 1
        
        # Return the current record and updated count
        return current_record, record_count_read2
    else:
        # If no more records, return a dummy record with NUM set to 9999999999
        dummy_record = {"NUM": "9999999999", "FIRST_NAME": "", "LAST_NAME": "", "ACCT_BALANCE": 0, "FILLER": ""}
        return dummy_record, record_count_read2

# ===== Rotina: 0100-INITIALIZE =====

def R0100_INITIALIZE(file01_df, file02_df, record_count_read1, record_count_read2):
    # OPEN INPUT FILE01 and FILE02 are not needed in PySpark as DataFrames are already loaded

    # OPEN OUTPUT OUTFIL is not needed here, as we'll write to OUTFIL later

    # Perform READ-FILE01
    file01_df, record_count_read1 = READ_FILE01(file01_df, record_count_read1)

    # Perform READ-FILE02
    file02_df, record_count_read2 = READ_FILE02(file02_df, record_count_read2)

    return file01_df, file02_df, record_count_read1, record_count_read2

# ===== Rotina: 0200-PROCESS =====

def R0200_PROCESS(file01_df, file02_df, outfil_df, record_count_limit, record_count_read1, record_count_read2):
    record_count_limit += 1
    if record_count_limit > 20:
        print('TRAVA LOOPING')
        return None, None, None, None, None, None  # Simulating STOP RUN

    # Get current records
    current_file01 = file01_df.first()
    current_file02 = file02_df.first()

    if current_file01 is None or current_file02 is None:
        return file01_df, file02_df, outfil_df, record_count_limit, record_count_read1, record_count_read2

    if current_file01['NUM'] < current_file02['NUM']:
        file01_df, record_count_read1 = READ_FILE01(file01_df, record_count_read1)
    elif current_file02['NUM'] < current_file01['NUM']:
        file02_df, record_count_read2 = READ_FILE02(file02_df, record_count_read2)
    else:
        outfil_df = R0400_WRITE(file01_df, file02_df, outfil_df, record_count_limit)
        file01_df, record_count_read1 = READ_FILE01(file01_df, record_count_read1)
        file02_df, record_count_read2 = READ_FILE02(file02_df, record_count_read2)

    return file01_df, file02_df, outfil_df, record_count_limit, record_count_read1, record_count_read2

# ===== Rotina: 0000-MAIN =====

def R0000_MAIN(spark, file01_df, file02_df, outfil_df):
    record_count_read1 = 0
    record_count_read2 = 0
    record_count = 0
    record_count_limit = float('inf')

    R0100_INITIALIZE(file01_df, file02_df, record_count_read1, record_count_read2)

    print('START')
    print('EOF-FILE01', file01_df.count() == 0)
    print('EOF-FILE02', file02_df.count() == 0)

    while file01_df.count() > 0 or file02_df.count() > 0:
        file01_df, file02_df, outfil_df, record_count = R0200_PROCESS(
            file01_df, file02_df, outfil_df, record_count_limit, record_count_read1, record_count_read2
        )

    R9999_CLOSE_OUT(spark)

    print('RECORD WRITTEN :', record_count)

    spark.stop()

# ===== Função Principal (main) =====

def main():
    try:
        # Initialize Spark Session
        spark = SparkSession.builder.appName("COBOL_to_PySpark").getOrCreate()

        # Read FILE01
        file01_df = read_fixed_width_file("FILE01", file_schema)

        # Read FILE02
        file02_df = read_fixed_width_file("FILE02", file_schema)

        # Initialize OUTFIL DataFrame (empty for now)
        outfil_df = spark.createDataFrame([], schema=file_schema)

        # Call the main routine
        R0000_MAIN(spark, file01_df, file02_df, outfil_df)

    except Exception as e:
        print(f"An error occurred: {str(e)}")
    finally:
        if 'spark' in locals():
            spark.stop()


if __name__ == "__main__":
    main()
