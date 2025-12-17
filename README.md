# 🚀 Mini Datalake Stack

Projeto compacto de Data Lake com Apache Airflow, Apache Spark e MinIO rodando em containers Docker.

## 📋 Índice

- [Visão Geral](#visão-geral)
- [Arquitetura](#arquitetura)
- [Pré-requisitos](#pré-requisitos)
- [Estrutura do Projeto](#estrutura-do-projeto)
- [Instalação e Configuração](#instalação-e-configuração)
- [Como Usar](#como-usar)
- [Acesso aos Serviços](#acesso-aos-serviços)
- [Exemplos](#exemplos)
- [Troubleshooting](#troubleshooting)
- [Comandos Úteis](#comandos-úteis)

## 🎯 Visão Geral

Este projeto fornece uma stack completa de Data Lake com:

- **MinIO**: Armazenamento de objetos S3-compatible (camadas Raw/Bronze/Silver/Gold)
- **Apache Spark**: Processamento distribuído de dados (Master + Worker)
- **Apache Airflow**: Orquestração de pipelines de dados (Webserver + Scheduler)
- **PostgreSQL**: Banco de metadados do Airflow

## 🏗️ Arquitetura

```
┌─────────────────────────────────────────────────────────────┐
│                     MINI DATALAKE STACK                     │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  ┌──────────────┐    ┌──────────────┐    ┌──────────────┐ │
│  │   Airflow    │    │    Spark     │    │    MinIO     │ │
│  │  Webserver   │◄──►│    Master    │◄──►│   Storage    │ │
│  │   :8081      │    │    :8080     │    │ :9000/:9001  │ │
│  └──────┬───────┘    └──────┬───────┘    └──────────────┘ │
│         │                   │                              │
│  ┌──────▼───────┐    ┌──────▼───────┐                     │
│  │   Airflow    │    │    Spark     │                     │
│  │  Scheduler   │    │    Worker    │                     │
│  └──────┬───────┘    └──────────────┘                     │
│         │                                                  │
│  ┌──────▼───────┐                                         │
│  │  PostgreSQL  │                                         │
│  │  (Metadata)  │                                         │
│  └──────────────┘                                         │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

### Componentes

| Serviço | Descrição | Porta(s) |
|---------|-----------|----------|
| **MinIO** | Object Storage S3-compatible | 9000 (API), 9001 (Console) |
| **Spark Master** | Coordenador do cluster Spark | 8080 (UI), 7077 (Master) |
| **Spark Worker** | Nó worker para processamento | - |
| **Airflow Webserver** | Interface web do Airflow | 8081 |
| **Airflow Scheduler** | Agendador de DAGs | - |
| **PostgreSQL** | Banco de metadados | 5432 |

## 📦 Pré-requisitos

- **Docker**: versão 20.10 ou superior
- **Docker Compose**: versão 2.0 ou superior
- **Recursos mínimos**:
  - 8GB RAM
  - 4 CPU cores
  - 20GB espaço em disco

### Verificar instalação

```bash
docker --version
docker-compose --version
docker info
```

## 📁 Estrutura do Projeto

```
mini-datalake-stack/
├── README.md                 # Este arquivo
├── docker-compose.yml        # Definição dos serviços
├── .env                      # Variáveis de ambiente
├── .gitignore               # Arquivos ignorados pelo git
├── requirements.txt          # Dependências Python
├── startup.sh               # Script para iniciar todos os serviços
├── shutdown.sh              # Script para parar todos os serviços
├── restart.sh               # Script para reiniciar serviços
│
├── config/                   # Arquivos de configuração
│   └── spark-defaults.conf  # Configuração do Spark
│
├── dags/                     # DAGs do Airflow
│   └── exemplo_pipeline.py  # DAG de exemplo
│
├── spark-apps/              # Aplicações Spark
│   └── exemplo_spark_job.py # Job Spark de exemplo
│
├── scripts/                 # Scripts auxiliares
│   ├── check-status.sh      # Verificar status dos serviços
│   └── setup-minio.sh       # Configurar buckets no MinIO
│
└── data/                    # Dados persistidos (criado automaticamente)
    ├── minio/               # Armazenamento MinIO
    ├── postgres/            # Dados do PostgreSQL
    ├── spark/               # Event logs do Spark
    └── logs/                # Logs do Airflow
```

## 🚀 Instalação e Configuração

### Passo 1: Navegue até o diretório do projeto

```bash
cd /home/<usuario-logado>/datalake-air-flow/mini-datalake-stack
```

### Passo 2: Dê permissão de execução aos scripts

```bash
chmod +x startup.sh shutdown.sh restart.sh
chmod +x scripts/*.sh
```

### Passo 3: Inicie todos os serviços

```bash
./startup.sh
```

Este script irá:
1. ✅ Verificar se o Docker está rodando
2. ✅ Criar os diretórios de dados necessários
3. ✅ Subir todos os containers
4. ✅ Inicializar o banco de dados do Airflow
5. ✅ Criar o usuário admin do Airflow
6. ✅ Mostrar o status dos serviços

**Tempo estimado**: 2-3 minutos para primeira execução

### Passo 4: Configure os buckets no MinIO (opcional)

```bash
./scripts/setup-minio.sh
```

Este script cria os buckets padrão para as camadas do Data Lake:
- `raw` - Dados brutos
- `bronze` - Dados ingeridos
- `silver` - Dados refinados
- `gold` - Dados analíticos

## 🎮 Como Usar

### Iniciando o ambiente

```bash
./startup.sh
```

### Parando o ambiente

```bash
./shutdown.sh
```

### Reiniciando os serviços

```bash
./restart.sh
```

### Verificando status

```bash
./scripts/check-status.sh
# ou
docker-compose ps
```

## 🌐 Acesso aos Serviços

### MinIO Console
- **URL**: http://localhost:9001
- **Usuário**: `minioadmin`
- **Senha**: `minioadmin123`
- **Uso**: Gerenciar buckets e objetos, visualizar dados armazenados

### Spark Master UI
- **URL**: http://localhost:8080
- **Uso**: Monitorar jobs Spark, workers, executores e recursos

### Airflow Web UI
- **URL**: http://localhost:8081
- **Usuário**: `admin`
- **Senha**: `admin`
- **Uso**: Gerenciar DAGs, visualizar logs, monitorar execuções

## 📚 Exemplos

### Exemplo 1: Executar DAG de teste

1. Acesse Airflow: http://localhost:8081
2. Faça login (admin/admin)
3. Encontre a DAG `exemplo_datalake_pipeline`
4. Clique no botão "Play" para executar
5. Acompanhe a execução na interface

### Exemplo 2: Executar job Spark

```bash
# Acessar o container do Spark Master
docker exec -it spark-master bash

# Executar o job de exemplo
/opt/bitnami/spark/bin/spark-submit \
  --master spark://spark-master:7077 \
  /opt/spark-apps/exemplo_spark_job.py
```

### Exemplo 3: Acessar MinIO via Python

```python
from minio import Minio

# Criar cliente MinIO
client = Minio(
    "localhost:9000",
    access_key="minioadmin",
    secret_key="minioadmin123",
    secure=False
)

# Listar buckets
buckets = client.list_buckets()
for bucket in buckets:
    print(bucket.name)
```

### Exemplo 4: Criar uma nova DAG

Crie um arquivo em `dags/minha_dag.py`:

```python
from datetime import datetime
from airflow import DAG
from airflow.operators.python import PythonOperator

def minha_funcao():
    print("Olá do Airflow!")
    return "Sucesso!"

with DAG(
    'minha_primeira_dag',
    start_date=datetime(2024, 1, 1),
    schedule_interval=None,
    catchup=False
) as dag:
    
    tarefa = PythonOperator(
        task_id='executar_funcao',
        python_callable=minha_funcao
    )
```

A DAG aparecerá automaticamente na interface do Airflow em alguns segundos.

## 🔧 Troubleshooting

### Problema: Containers não iniciam

```bash
# Verificar logs
docker-compose logs -f

# Verificar recursos do Docker
docker system df
docker system prune  # Limpar recursos não utilizados
```

### Problema: Airflow não acessa

```bash
# Verificar se o container está rodando
docker-compose ps airflow-webserver

# Ver logs do Airflow
docker-compose logs -f airflow-webserver

# Reiniciar o Airflow
docker-compose restart airflow-webserver
```

### Problema: Spark job falha

```bash
# Ver logs do Spark Master
docker-compose logs -f spark-master

# Ver logs do Spark Worker
docker-compose logs -f spark-worker

# Acessar UI do Spark para detalhes
# http://localhost:8080
```

### Problema: MinIO não conecta

```bash
# Verificar container
docker-compose ps minio

# Ver logs
docker-compose logs -f minio

# Testar conectividade
curl http://localhost:9000/minio/health/live
```

### Resetar tudo (CUIDADO: apaga todos os dados)

```bash
docker-compose down -v
rm -rf data/
./startup.sh
```

## 📝 Comandos Úteis

### Docker Compose

```bash
# Ver logs de todos os serviços
docker-compose logs -f

# Ver logs de um serviço específico
docker-compose logs -f airflow-webserver

# Listar containers
docker-compose ps

# Acessar shell de um container
docker exec -it <container-name> bash

# Ver uso de recursos
docker stats
```

### Airflow

```bash
# Acessar CLI do Airflow
docker exec -it airflow-webserver bash
airflow dags list
airflow tasks list <dag_id>
airflow dags trigger <dag_id>

# Testar uma task
airflow tasks test <dag_id> <task_id> 2024-01-01
```

### Spark

```bash
# Submit job Spark
docker exec -it spark-master spark-submit \
  --master spark://spark-master:7077 \
  /opt/spark-apps/seu_job.py

# Spark Shell interativo
docker exec -it spark-master spark-shell

# PySpark interativo
docker exec -it spark-master pyspark
```

### MinIO

```bash
# Usar MinIO Client (mc)
docker run --rm --network mini-datalake-stack_datalake-network \
  minio/mc:latest \
  mc alias set myminio http://minio:9000 minioadmin minioadmin123

# Listar buckets
docker run --rm --network mini-datalake-stack_datalake-network \
  minio/mc:latest \
  mc ls myminio
```

## 🔐 Credenciais Padrão

| Serviço | Usuário | Senha |
|---------|---------|-------|
| Airflow | admin | admin |
| MinIO | minioadmin | minioadmin123 |
| PostgreSQL | airflow | airflow |

**⚠️ IMPORTANTE**: Altere as credenciais padrão em produção!

## 🎯 Próximos Passos

1. **Personalize as configurações** no arquivo `.env`
2. **Crie suas próprias DAGs** no diretório `dags/`
3. **Desenvolva jobs Spark** no diretório `spark-apps/`
4. **Configure camadas do Data Lake** no MinIO (Raw, Bronze, Silver, Gold)
5. **Implemente pipelines de dados** completos

## 📖 Referências

- [Apache Airflow Documentation](https://airflow.apache.org/docs/)
- [Apache Spark Documentation](https://spark.apache.org/docs/latest/)
- [MinIO Documentation](https://min.io/docs/)
- [Docker Compose Documentation](https://docs.docker.com/compose/)

## 📄 Licença

Este projeto é fornecido "como está" para fins educacionais e de desenvolvimento.

---

**Desenvolvido para facilitar o aprendizado e desenvolvimento de Data Lakes** 🚀

Para dúvidas ou melhorias, consulte a documentação oficial de cada ferramenta.
