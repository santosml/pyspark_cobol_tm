#v6_5 --> lendo debito e credito com schema correto.
from pyspark.sql import SparkSession
from pyspark.sql.functions import col, when, lit, substring, sum as spark_sum

def program1(spark):
    # Leitura de arquivos texto com layout fixo
    flcli = spark.read.text("s3://hackthon202411/input/FLCLI.txt").withColumnRenamed("value", "line")
    flsld = spark.read.text("s3://hackthon202411/input/FLSLD.txt").withColumnRenamed("value", "line")

    # Extraindo campos de acordo com o layout fixo
    flcli = flcli.select(
        substring("line", 1, 10).alias("NUM"),
        substring("line", 11, 10).alias("FIRST_NAME"),
        substring("line", 21, 10).alias("LAST_NAME"),
        substring("line", 31, 10).cast("long").alias("BALANCE")
    )
    flsld = flsld.select(
        substring("line", 1, 10).alias("NUM"),
        substring("line", 11, 10).alias("FIRST_NAME"),
        substring("line", 21, 10).alias("LAST_NAME"),
        substring("line", 31, 10).cast("long").alias("BALANCE")
    )

    # União baseada no número do cliente (NUM) e agregando o saldo para evitar duplicação
    joined = flcli.union(flsld).groupBy("NUM", "FIRST_NAME", "LAST_NAME").agg(spark_sum("BALANCE").alias("BALANCE"))

    # Salvando no arquivo de saída em formato CSV
    joined.write.csv("s3://hackthon202411/output/FSLDATU.csv", header=True, mode="overwrite")
    print("Program 1: Saldo de clientes atualizado com sucesso.")

def program2(spark):
    # Leitura de arquivos texto com layout fixo
    fslcli = spark.read.csv("s3://hackthon202411/output/FSLDATU.csv", header=True)
    flcred = spark.read.text("s3://hackthon202411/input/FLCRED.txt").withColumnRenamed("value", "line")
    fldb = spark.read.text("s3://hackthon202411/input/FLDEB.txt").withColumnRenamed("value", "line")
    print("\nSaldo Incial")
    fslcli.show()
    # Extraindo campos de acordo com o layout fixo para crédito
    flcred = flcred.select(
        substring("line", 1, 10).alias("NUM"),
        substring("line", 31, 10).cast("long").alias("CREDIT")
    ).groupBy("NUM").agg(spark_sum("CREDIT").alias("CREDIT"))
    print("\nCredito")
    flcred.show()
    # Extraindo campos de acordo com o layout fixo para débito
    fldb = fldb.select(
        substring("line", 1, 10).alias("NUM"),
        substring("line", 31, 10).cast("long").alias("DEBIT")
    ).groupBy("NUM").agg(spark_sum("DEBIT").alias("DEBIT"))
    print("\nDebito")
    fldb.show()
    # Extraindo campos de acordo com o layout fixo para saldo dos clientes
    fslcli = fslcli.select(
        col("NUM"),
        col("FIRST_NAME"),
        col("LAST_NAME"),
        col("BALANCE").cast("long")
    )

    # Adicionando crédito
    updated_credit = fslcli \
        .join(flcred, "NUM", "left_outer") \
        .fillna(0, subset=["CREDIT"]) \
        .withColumn("BALANCE", col("BALANCE") + col("CREDIT"))
    print("\nCredito")    
    updated_credit.show()
    # Subtraindo débito
    updated_balance = updated_credit \
        .join(fldb, "NUM", "left_outer") \
        .fillna(0, subset=["DEBIT"]) \
        .withColumn("BALANCE", col("BALANCE") - col("DEBIT"))
    print("\nBalance Final")       
    updated_balance.show()
    # Divisão para os arquivos de saída
    outfl1 = updated_balance.filter(col("BALANCE") > 0)
    outfl2 = updated_balance.filter(col("BALANCE") == 0)
    outfl1.show()
    # Salvando os resultados em formato CSV
    outfl1.write.csv("s3://hackthon202411/output/CLIATU.csv", header=True, mode="overwrite")
    outfl2.write.csv("s3://hackthon202411/output/CLIZERO.csv", header=True, mode="overwrite")
    print("Program 2: Saldo atualizado e arquivos gerados com sucesso.")

def program3(spark):
    # Leitura de arquivos texto com layout fixo
    cliatual = spark.read.csv("s3://hackthon202411/output/CLIATU.csv", header=True)

    # Extraindo campos de acordo com o layout fixo
    cliatual = cliatual.select(
        col("NUM"),
        col("FIRST_NAME"),
        col("LAST_NAME"),
        col("BALANCE").cast("long")
    )

    # Classificação em tiers
    cliatual = cliatual.withColumn("TIER", when(col("BALANCE") < 2000, "TIER5")
                                   .when(col("BALANCE") < 4000, "TIER4")
                                   .when(col("BALANCE") < 6000, "TIER3")
                                   .when(col("BALANCE") < 8000, "TIER2")
                                   .otherwise("TIER1"))

    # Salvando os resultados em formato CSV
    cliatual.write.csv("s3://hackthon202411/output/CLITIER.csv", header=True, mode="overwrite")
    print("Program 3: Classificação de clientes em tiers concluída com sucesso.")

def main():
    spark = SparkSession.builder.appName("COBOL Sequential Files Conversion").getOrCreate()
    print("Iniciando programas convertidos para PySpark com arquivos texto...")

    print("\nExecutando Program 1...")
    program1(spark)

    print("\nExecutando Program 2...")
    program2(spark)

    print("\nExecutando Program 3...")
    program3(spark)

    print("Processamento concluído.")

if __name__ == "__main__":
    main()