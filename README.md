# Biblioteca IoT - Backend FastAPI

Este projeto é um backend para um sistema de biblioteca inteligente com navegação indoor, utilizando FastAPI, SQLAlchemy e SQLite.

## ⚙️ Configuração Inicial

Antes de executar o projeto, configure seu ambiente:

1. **Copie o arquivo de configuração:**
   ```bash
   cp .env.example .env
   ```

2. **Edite o arquivo `.env`** e configure seu IP local:
   ```bash
   # Para descobrir seu IP:
   ifconfig  # macOS/Linux
   ipconfig  # Windows
   
   # Edite o arquivo .env e coloque seu IP
   LOCAL_IP=192.168.1.100  # substitua pelo seu IP
   ```

3. **O arquivo `.env` não será commitado** no git (está no `.gitignore`)

## Como rodar o projeto

1. **Configure o ambiente:**
   ```bash
   cp .env.example .env
   # Edite o arquivo .env e configure seu LOCAL_IP
   ```

2. Ative o ambiente virtual:
   ```bash
   source iotenv/bin/activate
   ```

3. Execute o servidor:
   ```bash
   uvicorn main:app --host 0.0.0.0 --port 8000 --reload
   ```

4. Popule o banco de dados:
   ```bash
   python -m db.populate_beacons
   python -m db.populate_estantes
   python -m db.populate_livros
   python -m db.populate_instancias
   ```

5. Acesse a documentação interativa: `http://localhost:8000/docs`

## URLs para Teste

- **Local:** `http://localhost:8000`
- **Rede local:** `http://SEU_IP:8000` (configure o IP no arquivo `.env`)
- **Swagger UI:** `http://localhost:8000/docs`

> **💡 Configuração de IP:** Copie o arquivo `.env.example` para `.env` e configure seu IP local. Para descobrir seu IP: `ifconfig` (macOS/Linux) ou `ipconfig` (Windows).

## API Endpoints Completos

### 🏠 Beacons

#### Listar todos os beacons
- **GET** `/beacons/`
- **Resposta:**
```json
[
  {
    "mac": "AA:BB:CC:DD:EE:01",
    "posX": 0.0,
    "posY": 0.0,
    "label": "Entrada Principal"
  },
  {
    "mac": "AA:BB:CC:DD:EE:02",
    "posX": 8.0,
    "posY": 0.0,
    "label": "Saída"
  }
]
```

#### Obter beacon específico
- **GET** `/beacons/{mac}`
- **Exemplo:** `/beacons/AA:BB:CC:DD:EE:01`
- **Resposta:**
```json
{
  "mac": "AA:BB:CC:DD:EE:01",
  "posX": 0.0,
  "posY": 0.0,
  "label": "Entrada Principal"
}
```

#### Criar novo beacon
- **POST** `/beacons/`
- **Body:**
```json
{
  "mac": "AA:BB:CC:DD:EE:99",
  "posX": 5.0,
  "posY": 3.0,
  "label": "Novo Beacon"
}
```
- **Resposta:** (mesmo formato do body)

#### Atualizar beacon
- **PUT** `/beacons/{mac}`
- **Body:** (mesmo formato do POST)
- **Resposta:** beacon atualizado

#### Deletar beacon
- **DELETE** `/beacons/{mac}`
- **Resposta:** `{"detail": "Beacon deletado com sucesso"}`

---

### 📚 Estantes

#### Listar todas as estantes
- **GET** `/estantes/`
- **Resposta:**
```json
[
  {
    "idEstante": "E1",
    "posX": 1.75,
    "posY": 1.0,
    "cor": "azul",
    "codigosCutter": ["C01"]
  },
  {
    "idEstante": "E2",
    "posX": 1.75,
    "posY": 2.5,
    "cor": "azul",
    "codigosCutter": ["C02"]
  }
]
```

#### Obter estante específica
- **GET** `/estantes/{id_estante}`
- **Exemplo:** `/estantes/E1`
- **Resposta:**
```json
{
  "idEstante": "E1",
  "posX": 1.75,
  "posY": 1.0,
  "cor": "azul",
  "codigosCutter": ["C01"]
}
```

#### Criar nova estante
- **POST** `/estantes/`
- **Body:**
```json
{
  "idEstante": "E99",
  "posX": 10.0,
  "posY": 5.0,
  "cor": "vermelho",
  "codigosCutter": ["C99", "C100"]
}
```

#### Atualizar estante
- **PUT** `/estantes/{id_estante}`
- **Body:** (mesmo formato do POST)

#### Deletar estante
- **DELETE** `/estantes/{id_estante}`
- **Resposta:** `{"detail": "Estante deletada com sucesso"}`

---

### 📖 Livros

#### Listar todos os livros
- **GET** `/livros/`
- **Resposta:**
```json
[
  {
    "isbn": "978-8535206951",
    "titulo": "Cálculo Volume 1",
    "autor": "James Stewart",
    "editora": "Cengage Learning",
    "ano": 2013,
    "assunto": "Matemática",
    "codigoCutter": "S849c"
  }
]
```

#### Obter livro específico
- **GET** `/livros/{isbn}`
- **Exemplo:** `/livros/978-8535206951`

#### Criar novo livro
- **POST** `/livros/`
- **Body:**
```json
{
  "isbn": "978-1234567890",
  "titulo": "Novo Livro",
  "autor": "Autor Exemplo",
  "editora": "Editora ABC",
  "ano": 2024,
  "assunto": "Tecnologia",
  "codigoCutter": "A987n"
}
```

#### Atualizar livro
- **PUT** `/livros/{isbn}`

#### Deletar livro
- **DELETE** `/livros/{isbn}`

---

### 📋 Instâncias de Livros

#### Listar todas as instâncias
- **GET** `/instancias/`
- **Resposta:**
```json
[
  {
    "numeroTombo": "T001",
    "isbn": "978-8535206951",
    "idEstante": "E1",
    "disponivel": true,
    "posX": 1.75,
    "posY": 1.0
  }
]
```

#### Obter instância específica
- **GET** `/instancias/{numero_tombo}`

#### Criar nova instância
- **POST** `/instancias/`
- **Body:**
```json
{
  "numeroTombo": "T999",
  "isbn": "978-8535206951",
  "idEstante": "E1",
  "disponivel": true,
  "posX": 1.75,
  "posY": 1.0
}
```

#### Atualizar instância
- **PUT** `/instancias/{numero_tombo}`

#### Deletar instância
- **DELETE** `/instancias/{numero_tombo}`

---

### 📚 Empréstimo e Devolução

#### Emprestar livro
- **POST** `/instancias/{idInstancia}/emprestar`
- **Exemplo:** `/instancias/978-85-01-00001-1-EX1/emprestar`
- **Funcionalidade:**
  - Altera situação: `disponivel` → `emprestado`
  - Atualiza `ultimaAtualizacao` automaticamente
  - **Validações:**
    - ❌ Livros `cativo` não podem ser emprestados
    - ❌ Livros já `emprestado` não podem ser emprestados novamente
- **Resposta:** Instância atualizada com nova situação

#### Devolver livro
- **POST** `/instancias/{idInstancia}/devolver`
- **Exemplo:** `/instancias/978-85-01-00001-1-EX1/devolver`
- **Body (JSON):**
```json
{
  "nova_posX": 2.0,
  "nova_prateleira": "BAIXO"
}
```
- **Funcionalidade:**
  - Altera situação: `emprestado` → `disponivel`
  - Atualiza posição física (posX e prateleira)
  - Atualiza `ultimaAtualizacao` automaticamente
  - **Validações:**
    - ❌ Apenas livros `emprestado` podem ser devolvidos
    - ❌ Prateleira deve ser: `CIMA`, `MEIO` ou `BAIXO`
    - ✅ Validação automática via Pydantic
- **Resposta:** Instância atualizada com nova situação e posição

---

### 🔍 Endpoints de Busca Especiais

#### Buscar livros por nome
- **GET** `/instancias/livros/buscar?q={termo}`
- **Exemplo:** `/instancias/livros/buscar?q=calculo`
- **Resposta:**
```json
[
  {
    "livro": {
      "isbn": "978-8535206951",
      "titulo": "Cálculo Volume 1",
      "autor": "James Stewart",
      "editora": "Cengage Learning",
      "ano": 2013,
      "assunto": "Matemática",
      "codigoCutter": "S849c"
    },
    "instancias": [
      {
        "numeroTombo": "T001",
        "isbn": "978-8535206951",
        "idEstante": "E1",
        "disponivel": true,
        "posX": 1.75,
        "posY": 1.0
      }
    ]
  }
]
```

#### Detalhes completos de uma instância
- **GET** `/instancias/{numero_tombo}/detalhes`
- **Exemplo:** `/instancias/T001/detalhes`
- **Resposta:**
```json
{
  "instancia": {
    "numeroTombo": "T001",
    "isbn": "978-8535206951",
    "idEstante": "E1",
    "disponivel": true,
    "posX": 1.75,
    "posY": 1.0
  },
  "livro": {
    "isbn": "978-8535206951",
    "titulo": "Cálculo Volume 1",
    "autor": "James Stewart",
    "editora": "Cengage Learning",
    "ano": 2013,
    "assunto": "Matemática",
    "codigoCutter": "S849c"
  },
  "estante": {
    "idEstante": "E1",
    "posX": 1.75,
    "posY": 1.0,
    "cor": "azul",
    "codigosCutter": ["C01"]
  },
  "beacons_proximos": [
    {
      "mac": "AA:BB:CC:DD:EE:01",
      "posX": 0.0,
      "posY": 0.0,
      "label": "Entrada Principal",
      "distancia": 2.06
    }
  ]
}
```

## Estrutura do Projeto

```
biblioteca-iot/
├── main.py              # Aplicação FastAPI principal
├── models/              # Modelos ORM e Pydantic
│   ├── base.py         # Base declarativa do SQLAlchemy
│   ├── beacon.py       # Modelo Beacon
│   ├── estante.py      # Modelo Estante
│   ├── livro.py        # Modelo Livro
│   └── instancia_livro.py # Modelo InstanciaLivro
├── routes/              # Rotas/endpoints da API
│   ├── beacons.py      # CRUD beacons
│   ├── estantes.py     # CRUD estantes
│   ├── livros.py       # CRUD livros
│   └── instancias.py   # CRUD instâncias + buscas
├── schemas/             # Schemas Pydantic para respostas
│   └── instancia_schemas.py
├── db/                  # Configuração e população do banco
│   ├── session.py      # Configuração SQLAlchemy
│   ├── init_db.py      # Inicialização do banco
│   └── populate_*.py   # Scripts para popular dados
└── biblioteca.db        # Banco SQLite
```

## Comandos Úteis

### Limpar dados do banco:
```bash
sqlite3 biblioteca.db "DELETE FROM instancias_livro; DELETE FROM estantes;"
```

### Ver dados no banco:
```bash
sqlite3 biblioteca.db "SELECT * FROM beacons;"
sqlite3 biblioteca.db "SELECT * FROM estantes;"
sqlite3 biblioteca.db "SELECT * FROM livros;"
sqlite3 biblioteca.db "SELECT * FROM instancias_livro;"
```

## CORS Configurado

O CORS está liberado para permitir acesso de qualquer origem, facilitando o desenvolvimento de apps mobile e frontend em rede local.
