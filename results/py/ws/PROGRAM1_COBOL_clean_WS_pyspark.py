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