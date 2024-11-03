# refer back to: https://www.databricks.com/glossary/pyspark

# Import necessary libraries
from pyspark.sql import SparkSession
from pyspark.sql.functions import *
from pyspark.sql.types import StructType, StructField, StringType, IntegerType, FloatType, DateType
import matplotlib.pyplot as plt
import pandas as pd


# Start a Spark session
spark = spark = SparkSession.builder \
    .appName("CustomerTransactionAnalysis") \
    .config("spark.jars.packages", "io.delta:delta-core_2.12:2.0.0") \
    .getOrCreate()


# Define schema for loading data
schema = StructType([
    StructField("CustomerID", StringType(), True),
    StructField("TransactionDate", DateType(), True),
    StructField("TransactionAmount", FloatType(), True),
    StructField("ProductCategory", StringType(), True),
])

# Load the data
data_path = "customer_transactions.csv"
transactions_df = spark.read.csv(data_path, header=True, schema=schema)

# Clean the data
# Remove rows with null values in critical columns
transactions_df = transactions_df.dropna(subset=["CustomerID", "TransactionDate", "TransactionAmount"])

# Convert TransactionAmount to absolute values (if there are refunds/negative values)
transactions_df = transactions_df.withColumn("TransactionAmount", abs(col("TransactionAmount")))

# Aggregate data to get total spend and number of transactions per customer
customer_agg_df = transactions_df.groupBy("CustomerID").agg(
    sum("TransactionAmount").alias("TotalSpend"),
    count("TransactionAmount").alias("TransactionCount")
)

# Add a column for average spend per transaction
customer_agg_df = customer_agg_df.withColumn("AvgSpendPerTransaction", col("TotalSpend") / col("TransactionCount"))

# Save processed data to Delta Lake for future use
delta_output_path = "/mnt/delta/customer_summary"
customer_agg_df.write.format("delta").mode("overwrite").save(delta_output_path)

# Top 10 customers by total spend
top_customers_df = customer_agg_df.orderBy(desc("TotalSpend")).limit(10)
top_customers_df.show()

# Filter data for transactions in specific category (e.g., "Electronics")
electronics_df = transactions_df.filter(col("ProductCategory") == "Electronics")

# Aggregate electronics transactions over time
electronics_time_df = electronics_df.groupBy("TransactionDate").agg(
    sum("TransactionAmount").alias("TotalElectronicsSales")
).orderBy("TransactionDate")

# Convert to Pandas for visualization
electronics_time_pd = electronics_time_df.toPandas()

# Plot total electronics sales over time
plt.figure(figsize=(10, 6))
plt.plot(electronics_time_pd["TransactionDate"], electronics_time_pd["TotalElectronicsSales"], color="blue", marker="o")
plt.title("Total Electronics Sales Over Time")
plt.xlabel("Date")
plt.ylabel("Total Sales")
plt.xticks(rotation=45)
plt.grid()
plt.show()

# Advanced analysis: calculate customer lifetime value (CLV) for each customer
# CLV estimation = TotalSpend * Avg Transaction Count / Avg Customer Lifecycle (in months)
# Assuming a 12-month customer lifecycle for simplicity
customer_agg_df = customer_agg_df.withColumn("EstimatedCLV", col("TotalSpend") * (col("TransactionCount") / 12))

# Save CLV data to Delta Lake
clv_output_path = "/mnt/delta/customer_clv"
customer_agg_df.write.format("delta").mode("overwrite").save(clv_output_path)

# Load CLV data and display top customers by CLV
customer_clv_df = spark.read.format("delta").load(clv_output_path)
top_clv_customers_df = customer_clv_df.orderBy(desc("EstimatedCLV")).limit(10)
top_clv_customers_df.show()

# Additional visualization: Distribution of transaction amounts
transaction_amounts_pd = transactions_df.select("TransactionAmount").toPandas()

plt.figure(figsize=(8, 6))
plt.hist(transaction_amounts_pd["TransactionAmount"], bins=30, color="green", edgecolor="black")
plt.title("Distribution of Transaction Amounts")
plt.xlabel("Transaction Amount")
plt.ylabel("Frequency")
plt.grid()
plt.show()

# Stop the Spark session
spark.stop()


from langchain_databricks import ChatDatabricks

chat_model = ChatDatabricks(
    endpoint="databricks-meta-llama-3-1-70b-instruct",
    temperature=0.1,
    max_tokens=250,
)
chat_model.invoke("How to use Databricks?")
