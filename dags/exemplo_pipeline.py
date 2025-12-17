"""
Exemplo de DAG para demonstrar integração com Spark e MinIO
"""
from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.operators.bash import BashOperator

default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': datetime(2024, 1, 1),
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

def test_minio_connection():
    """Testa conexão com MinIO"""
    from minio import Minio
    
    client = Minio(
        "minio:9000",
        access_key="minioadmin",
        secret_key="minioadmin123",
        secure=False
    )
    
    # Lista buckets
    buckets = client.list_buckets()
    print("Buckets disponíveis:")
    for bucket in buckets:
        print(f"  - {bucket.name}")
    
    return True

def generate_sample_data():
    """Gera dados de exemplo"""
    import pandas as pd
    from datetime import datetime
    
    data = {
        'id': range(1, 101),
        'timestamp': [datetime.now()] * 100,
        'value': [i * 10 for i in range(1, 101)],
        'category': ['A', 'B', 'C', 'D'] * 25
    }
    
    df = pd.DataFrame(data)
    print(f"Gerados {len(df)} registros")
    return True

with DAG(
    'exemplo_datalake_pipeline',
    default_args=default_args,
    description='Pipeline de exemplo com Spark e MinIO',
    schedule_interval=None,
    catchup=False,
    tags=['exemplo', 'datalake']
) as dag:

    # Task 1: Testar conexão com MinIO
    test_minio = PythonOperator(
        task_id='test_minio_connection',
        python_callable=test_minio_connection
    )

    # Task 2: Gerar dados de exemplo
    generate_data = PythonOperator(
        task_id='generate_sample_data',
        python_callable=generate_sample_data
    )

    # Task 3: Verificar status do Spark
    check_spark = BashOperator(
        task_id='check_spark_status',
        bash_command='curl -s http://spark-master:8080 > /dev/null && echo "Spark OK" || echo "Spark NOT OK"'
    )

    # Definir ordem de execução
    test_minio >> generate_data >> check_spark
