# FIPE Application – Consulta e Previsão de Preços de Veículos

Aplicação composta por uma API em Django/DRF e um frontend estático para consultar veículos e prever preços com base em dados FIPE. Permite filtrar por marca, modelo, combustível, câmbio, ano e motor, ordenar resultados e obter uma estimativa de preço via modelo de machine learning.

## Recursos
- Filtros por `brand`, `model`, `fuel_type`, `gear_type`, `year`, `engine_size` com paginação.
- Ordenação por `price`, `year`, `engine_size` com chips selecionáveis.
- Mensagens de lista vazia e ocultação automática de paginação quando não há próximos/anteriores.
- Dropdown de ano iniciado no ano atual e botão “Prever” habilitado somente com todos os campos válidos.

## Arquitetura
- Backend Django/DRF com filtros e ordenação: `fipe_car/views.py:10`.
- Listas distintas com busca (`q`) e filtros dependentes: `fipe_car/views.py:18`.
- Endpoints agregados sob prefixo: `core/urls.py:26-28`.
- Previsão codificando atributos e inferindo com Random Forest: `predict/views.py:14`.
- Frontend estático consumindo APIs; base de chamadas em `frontend/interface.js:2`.

## APIs
- `GET /api/v1/fipe/car/?page_size=12&brand=&model=&fuel_type=&gear_type=&year=&engine_size=&fipe_id=&ordering=`
- `GET /api/v1/fipe/car/brands/?page_size=10&q=`
- `GET /api/v1/fipe/car/models/?page_size=10&brand=&q=`
- `GET /api/v1/fipe/car/fuel_types/?page_size=10&brand=&model=&q=`
- `GET /api/v1/fipe/car/gear_types/?page_size=10&brand=&model=&q=`
- `GET /api/v1/fipe/car/years/?page_size=10&brand=&model=`
- `GET /api/v1/fipe/car/engine_sizes/?page_size=10&brand=&model=`
- `POST /api/v1/predict/car/` body `{"consult_year": 2025, "year": 2018, "engine": 2.0, "brand": "Honda", "model": "Civic", "fuel": "Gasolina", "gear": "Automático"}`

## Quickstart
- Requisitos: Python 3.11+, `pip`, virtualenv.
- Criar `.env` no diretório raiz com:
  - `SECRET_KEY=uma_chave_segura`
  - `DEBUG=True`
- Instalação:
  - `python -m venv .venv && .venv\Scripts\activate`
  - `pip install -r requirements.txt`
  - `python manage.py migrate`
- Importar dados FIPE (opcional, mas recomendado):
  - Coloque `predict/machine_learn/fipe_cars.csv` no caminho indicado.
  - Execute `python manage.py import_fipe` (`fipe_car/management/commands/import_fipe.py:9`).
- Modelos de ML:
  - A API usa `predict/constants.py:16-18` para localizar `model_rf.joblib`.
  - Garanta que o arquivo exista em `predict/machine_learn/models_trained/model_rf.joblib`.
  - Encoders necessários em `predict/machine_learn/columns_encoded/` (`encoder_brand.pkl`, `encoder_model.pkl`, `encoder_fuel.pkl`, `encoder_gear.pkl`).
- Executar backend:
  - `python manage.py runserver` (padrão em `http://127.0.0.1:8000`).
- Executar frontend:
  - Abra `frontend/interface.html` com um servidor estático em `http://127.0.0.1:5500`.
  - Ex.: `python -m http.server 5500` na pasta `frontend` ou extensão Live Server.
- CORS permite `http://127.0.0.1:5500` em `core/settings.py:130-133`.

## Modelos de Regressão
- `DecisionTreeRegressor`:
  - Modelo simples e interpretável; captura relações não lineares.
  - Tende a sobreajustar sem poda/regularização; rápido para treinar.
  - Artefato esperado: `predict/machine_learn/models_trained/model_dt.joblib` (`predict/constants.py:12-14`).
- `RandomForestRegressor`:
  - Conjunto de árvores com amostragem; bom equilíbrio entre viés/variância.
  - Robusto a ruído e outliers; normalmente melhor generalização que uma única árvore.
  - Artefato esperado: `predict/machine_learn/models_trained/model_rf.joblib` (`predict/constants.py:16-18`).
- `HistGradientBoostingRegressor`:
  - Boosting gradiente com histogramas; alto desempenho em dados tabulares.
  - Requer cuidado com hiperparâmetros; pode ser mais sensível a ruído.
  - Artefato esperado: `predict/machine_learn/models_trained/model_hgb.joblib` (`predict/constants.py:20-22`).
- `VotingRegressor`:
  - Combina previsões de múltiplos modelos (p.ex., DT, RF, HGB) para maior estabilidade.
  - Útil quando os base learners têm erros complementares.
  - Artefato esperado: `predict/machine_learn/models_trained/model_voting.joblib` (`predict/constants.py:24-26`).

### Alternando o modelo de previsão
- Por padrão, o loader usa o Random Forest: `predict/model_loader.py:11-13` e é consumido em `predict/views.py:42-43`.
- Para usar outro modelo, ajuste o loader e a chamada de `predict/views.py` para carregar o artefato correspondente conforme caminhos definidos em `predict/constants.py`.
- Garanta que os encoders (`encoder_brand.pkl`, `encoder_model.pkl`, `encoder_fuel.pkl`, `encoder_gear.pkl`) estejam presentes, pois a API codifica atributos antes da inferência (`predict/views.py:24-28`).

## Notebook (Colab)
- Treino e exploração dos modelos: https://colab.research.google.com/drive/1fOE4rKyNI0M5bBQaPE2lnsgPoXRbQnIO?usp=sharing

## Uso
- Preencha filtros no painel lateral e clique em `Filtrar` para carregar a lista.
- Use chips para ordenar por preço/ano/motor; conflitos são prevenidos em `frontend/interface.js:346-371`.
- Clique em um item para preencher o painel de previsão; então `Prever` envia `POST /api/v1/predict/car/` e mostra o preço previsto.

## Referências de Código
- Carros: `fipe_car/views.py:10-17`, filtros: `fipe_car/views.py:14-15`.
- Listas distintas: `fipe_car/views.py:18-82`; subclasses: `fipe_car/views.py:83-99`.
- Previsão: `predict/views.py:14-43`, loader: `predict/model_loader.py:11-29`.
- Rotas raiz: `core/urls.py:21-28`.
- Frontend base URL: `frontend/interface.js:2`; endpoints usados ao longo do arquivo.

## Observações
- Banco padrão SQLite (`core/settings.py:81-86`).
- Ajuste CORS se usar outra origem além de `127.0.0.1:5500`.
- Em produção, configure `SECRET_KEY`, desative `DEBUG` e use WSGI/ASGI adequados.
