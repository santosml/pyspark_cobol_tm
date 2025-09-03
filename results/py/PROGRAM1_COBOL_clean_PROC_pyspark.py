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
file01_df = read_fixed_width_file("FILE01", file_schema)
# COBOL to PySpark mapping:
# NUM-FILE01 -> NUM
# FIRST-NAME-FILE01 -> FIRST_NAME
# LAST-NAME-FILE01 -> LAST_NAME
# ACCT-BALANCE-FILE01 -> ACCT_BALANCE
# FILLER -> FILLER

# Read FILE02
file02_df = read_fixed_width_file("FILE02", file_schema)
# COBOL to PySpark mapping:
# NUM-FILE02 -> NUM
# FIRST-NAME-FILE02 -> FIRST_NAME
# LAST-NAME-FILE02 -> LAST_NAME
# ACCT-BALANCE-FILE02 -> ACCT_BALANCE
# FILLER -> FILLER

# OUTFIL schema is the same as input files
outfil_df = spark.createDataFrame([], schema=file_schema)
# COBOL to PySpark mapping:
# NUM-OUTFIL -> NUM
# FIRST-NAME-OUTFIL -> FIRST_NAME
# LAST-NAME-OUTFIL -> LAST_NAME
# ACCT-BALANCE-OUTFIL -> ACCT_BALANCE
# FILLER -> FILLER

# Note: Further processing would be done here based on the COBOL program logic

# ==== Rotinas convertidas (Procedure Division) ====

# ===== Rotina: 0400-WRITE =====

def R0400_WRITE(file01_df, file02_df, outfil_df, record_count):
    # Update ACCT-BALANCE-FILE01 with ACCT-BALANCE-FILE02
    file01_df = file01_df.withColumn("ACCT_BALANCE", file02_df.select("ACCT_BALANCE").first()[0])
    
    # Write the updated FILE01 record to OUTFIL
    outfil_df = outfil_df.union(file01_df.limit(1))
    
    # Increment RECORD-COUNT
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
        # Read the next record from FILE01
        current_record = file01_df.first()
        
        # Update the DataFrame to remove the read record
        file01_df = file01_df.filter(file01_df.NUM != current_record.NUM)
        
        # Increment the record count
        record_count_read1 += 1
    else:
        # If no more records, set NUM to 9999999999
        current_record = file01_df.schema.toStruct()
        current_record['NUM'] = '9999999999'
    
    return file01_df, current_record, record_count_read1

# ===== Rotina: READ-FILE02 =====

def READ_FILE02(file02_df, record_count_read2):
    # Check if there are more records in FILE02
    if file02_df.count() > record_count_read2:
        # Simulate reading the next record
        current_record = file02_df.limit(record_count_read2 + 1).tail(1)[0]
        record_count_read2 += 1
        return current_record, record_count_read2
    else:
        # If end of file, return a dummy record with NUM set to 9999999999
        dummy_record = {"NUM": "9999999999", "FIRST_NAME": "", "LAST_NAME": "", "ACCT_BALANCE": 0, "FILLER": ""}
        return dummy_record, record_count_read2

# ===== Rotina: 0100-INITIALIZE =====

def R0100_INITIALIZE(file01_df, file02_df, outfil_df):
    # OPEN INPUT FILE01 and FILE02 are not needed in PySpark as DataFrames are already loaded
    # OPEN OUTPUT OUTFIL is not needed as outfil_df is already created
    
    # Initialize record counts
    record_count_read1 = [0]
    record_count_read2 = [0]
    
    # Perform READ-FILE01
    file01_df, record_count_read1[0] = READ_FILE01(file01_df, record_count_read1[0])
    
    # Perform READ-FILE02
    file02_df, record_count_read2[0] = READ_FILE02(file02_df, record_count_read2[0])
    
    return file01_df, file02_df, outfil_df, record_count_read1[0], record_count_read2[0]

# ===== Rotina: 0200-PROCESS =====

def R0200_PROCESS(file01_df, file02_df, outfil_df, record_count_limit):
    record_count_limit += 1
    if record_count_limit > 20:
        print('TRAVA LOOPING')
        return None, None, None, None, True  # Indica que deve parar a execução

    # Comparação dos números entre FILE01 e FILE02
    num_file01 = file01_df.select("NUM").first()[0]
    num_file02 = file02_df.select("NUM").first()[0]

    if num_file01 < num_file02:
        file01_df, record_count_read1 = READ_FILE01(file01_df, 0)
        return file01_df, file02_df, outfil_df, record_count_limit, False
    elif num_file02 < num_file01:
        file02_df, record_count_read2 = READ_FILE02(file02_df, 0)
        return file01_df, file02_df, outfil_df, record_count_limit, False
    else:
        outfil_df = R0400_WRITE(file01_df, file02_df, outfil_df, 0)
        file01_df, record_count_read1 = READ_FILE01(file01_df, 0)
        file02_df, record_count_read2 = READ_FILE02(file02_df, 0)
        return file01_df, file02_df, outfil_df, record_count_limit, False

# ===== Rotina: 0000-MAIN =====

def R0000_MAIN(file01_df, file02_df, outfil_df):
    record_count = 0
    
    # Perform 0100-INITIALIZE
    file01_df, file02_df, outfil_df = R0100_INITIALIZE(file01_df, file02_df, outfil_df)
    
    print('START')
    print('EOF-FILE01', file01_df.count() == 0)
    print('EOF-FILE02', file02_df.count() == 0)
    
    # Perform 0200-PROCESS until both files are empty
    while file01_df.count() > 0 or file02_df.count() > 0:
        file01_df, file02_df, outfil_df, record_count = R0200_PROCESS(file01_df, file02_df, outfil_df, record_count)
    
    # Perform 9999-CLOSE-OUT
    R9999_CLOSE_OUT(spark)
    
    print('RECORD WRITTEN :', record_count)
    
    return outfil_df, record_count

# ===== Função Principal (main) =====

def main():
    try:
        # Initialize DataFrames
        file01_df = read_fixed_width_file("FILE01", file_schema)
        file02_df = read_fixed_width_file("FILE02", file_schema)
        outfil_df = spark.createDataFrame([], schema=file_schema)

        # Call the main routine
        R0000_MAIN(file01_df, file02_df, outfil_df)

    except Exception as e:
        print(f"An error occurred: {str(e)}")
    finally:
        # Ensure SparkSession is stopped
        spark.stop()


if __name__ == "__main__":
    main()
