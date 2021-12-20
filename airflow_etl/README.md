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

## Business Rules
- espaço destinado para documentação de regras de negócio (tanto regras comuns a todos os layers quanto regras específicas de cada domínio)

### Data Layers
#### Regras Comuns
- **Raw**
  - transforma todas as colunas em string

- **Intermediate**
  - dropa colunas não utilizadas

- **Primary**
  - replace da string `ID` por `Id`
  - transforma nome de colunas de camelcase para snakecase
  - ajusta tipo dos dados (e.g., int, float, string, ...)
  - valida schema com pandera

#### Regras Específicas
- Domínio: `employee`
  - Data layer: `primary`
    - filtra nulos na coluna `end_date`
    - dropa colunas
- Domínio: `date_time`
  - Data layer: `primary`
    - renomeia coluna
    - dropa valores duplicados
    - calcula coluna de ano
    - ordena valores ascendentemente pela data
    - cria coluna de id baseado na data
- Domínio: `sales`
  - Data layer: `primary`
    - Sub-domínio: `sales_detail`
      - calcula preço unitário por produto
      - dropa colunas
    - Sub-domínio: `sales_header`
      - replace `null` com `-999`
      - replace `.0` com `""`
  - Data layer: `feature`
    - cria `time_id` no sub-domínio `sales_header` usando o método de dense rank
    - `left join` entre domínio de `employee` e sub-domínio `sales_header` para pegar o `department_id`
      - o resultado desse join será o domínio `sales_department`
    - replace `null` com `-999` na coluna `department_id`
    - `inner join` entre o domínio criado `sales_department` e o sub-domínio `sales_detail` para pegar o `product_id`
    - dropa colunas
    - arredonda valores para 2 casas decimais