"""
Exemplo de job Spark para processar dados no MinIO
"""
from pyspark.sql import SparkSession
from datetime import datetime

def create_spark_session():
    """Cria sessão Spark com configuração para MinIO"""
    spark = SparkSession.builder \
        .appName("MinIO-Spark-Example") \
        .config("spark.hadoop.fs.s3a.endpoint", "http://minio:9000") \
        .config("spark.hadoop.fs.s3a.access.key", "minioadmin") \
        .config("spark.hadoop.fs.s3a.secret.key", "minioadmin123") \
        .config("spark.hadoop.fs.s3a.path.style.access", "true") \
        .config("spark.hadoop.fs.s3a.impl", "org.apache.hadoop.fs.s3a.S3AFileSystem") \
        .getOrCreate()
    
    return spark

def main():
    """Função principal"""
    print("="*50)
    print("Iniciando job Spark...")
    print("="*50)
    
    spark = create_spark_session()
    
    # Criar DataFrame de exemplo
    data = [
        (1, "Alice", 100, datetime.now()),
        (2, "Bob", 200, datetime.now()),
        (3, "Charlie", 300, datetime.now()),
        (4, "Diana", 400, datetime.now()),
        (5, "Eve", 500, datetime.now()),
    ]
    
    columns = ["id", "name", "value", "timestamp"]
    df = spark.createDataFrame(data, columns)
    
    print("\n📊 DataFrame criado:")
    df.show()
    
    print("\n📈 Estatísticas:")
    df.describe().show()
    
    # Salvar no MinIO (comentado para exemplo - descomente se tiver bucket configurado)
    # output_path = "s3a://bronze/exemplo/data.parquet"
    # df.write.mode("overwrite").parquet(output_path)
    # print(f"\n✅ Dados salvos em: {output_path}")
    
    spark.stop()
    print("\n✅ Job concluído com sucesso!")

if __name__ == "__main__":
    main()
