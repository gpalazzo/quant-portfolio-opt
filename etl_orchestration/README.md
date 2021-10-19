# quant-portfolio-opt
Quantitative finance: Portfolio optimization with Python

## Setup do Projeto
1. criar ambiente virtual
   - existem várias opções, mas um exemplo com conda seria: `conda create -n ce263 python=3.7 -y`
     - isso irá criar um ambiente virtual de nome `ce263` e instalar a última versão do Python 3.7
2. instalar dependência inicial
   - `pip install -r requirements.txt`
3. instalar outras dependências
   - `poetry lock && poetry install`
4. instalar docker
5. criar arquivos com variáveis de ambiente
   - o nome dos arquivos devem ser obrigatoriamente `airflow_base.env` e `airflow_init.env`
6. colocar arquivos raw em uma pasta chamada `raw` dentro da pasta `data`

## Iniciar serviços do Airflow
1. mover-se para o mesmo diretório do arquivo `docker-compose.yaml`
2. já existem imagens "buildadas"?
  - se sim, então escreva `docker-compose up`
- se não, então escreva `docker-compose up airflow-init && docker-compose up`