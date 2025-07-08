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
    "idLivro": "978-85-01-00001-1",
    "titulo": "Cálculo Volume 1",
    "autor": "James Stewart",
    "editora": "Cengage Learning",
    "codigoCutter": "C01",
    "estanteId": "E1"
  },
  {
    "idLivro": "978-85-01-00015-5",
    "titulo": "Programação em Python",
    "autor": "Mark Lutz",
    "editora": "Novatec",
    "codigoCutter": "C08",
    "estanteId": "E8"
  }
]
```

#### Obter livro específico
- **GET** `/livros/{idLivro}`
- **Exemplo:** `/livros/978-85-01-00001-1`
- **Resposta:**
```json
{
  "idLivro": "978-85-01-00001-1",
  "titulo": "Cálculo Volume 1",
  "autor": "James Stewart",
  "editora": "Cengage Learning",
  "codigoCutter": "C01",
  "estanteId": "E1"
}
```

#### Criar novo livro
- **POST** `/livros/`
- **Body:**
```json
{
  "idLivro": "978-1234567890",
  "titulo": "Novo Livro de IA",
  "autor": "Stuart Russell, Peter Norvig",
  "editora": "Editora Tecnologia",
  "codigoCutter": "C01",
  "estanteId": "E1"
}
```

#### Atualizar livro
- **PUT** `/livros/{idLivro}`

#### Deletar livro
- **DELETE** `/livros/{idLivro}`

---

### 📋 Instâncias de Livros

#### Listar todas as instâncias
- **GET** `/instancias/`
- **Resposta:**
```json
[
  {
    "idInstancia": "978-85-01-00001-1-EX1",
    "idLivro": "978-85-01-00001-1",
    "posX": 1.85,
    "situacao": "disponivel",
    "ultimaAtualizacao": "2025-07-07T10:30:00"
  }
]
```

#### Obter instância específica
- **GET** `/instancias/{idInstancia}`
- **Exemplo:** `/instancias/978-85-01-00001-1-EX1`

#### Criar nova instância
- **POST** `/instancias/`
- **Body:**
```json
{
  "idInstancia": "978-85-01-00001-1-EX99",
  "idLivro": "978-85-01-00001-1",
  "posX": 1.85,
  "situacao": "disponivel"
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
  "nova_posX": 2.0
}
```
- **Funcionalidade:**
  - Altera situação: `emprestado` → `disponivel`
  - Atualiza posição física (posX)
  - Atualiza `ultimaAtualizacao` automaticamente
  - **Validações:**
    - ❌ Apenas livros `emprestado` podem ser devolvidos
    - ✅ Validação automática via Pydantic
- **Resposta:** Instância atualizada com nova situação e posição

---

### 🔍 Endpoints de Busca Especiais

#### Buscar livros por nome ou autor
- **GET** `/livros/buscar?q={termo}`
- **Exemplo:** `/livros/buscar?q=calculo` ou `/livros/buscar?q=james` ou `/livros/buscar?q=stewart`
- **Funcionalidade:**
  - Busca no **título** E no **autor**
  - Busca parcial e insensível a acentos
  - Retorna lista de livros que contenham o termo
- **Resposta:**
```json
[
  {
    "idLivro": "978-85-01-00001-1",
    "titulo": "Cálculo Volume 1",
    "autor": "James Stewart",
    "editora": "Cengage Learning",
    "codigoCutter": "C01",
    "estanteId": "E1"
  },
  {
    "idLivro": "978-85-01-00002-2",
    "titulo": "Cálculo Volume 2",
    "autor": "James Stewart",
    "editora": "Cengage Learning",
    "codigoCutter": "C01",
    "estanteId": "E1"
  }
]
```
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

## 📚 Sistema de Códigos Cutter

O sistema utiliza **códigos Cutter compatíveis** entre estantes e livros para organização:

### Estrutura dos Códigos
- **Estantes:** `C01`, `C02`, `C03`, ..., `C12` (12 estantes)
- **Livros:** Mesmo código da estante onde estão localizados

### Organização por Assunto
- **C01 (E1):** Matemática/Cálculo - James Stewart
- **C02 (E2):** Álgebra - Howard Anton, Paulo Winterle  
- **C03 (E3):** Geometria - Alfredo Steinbruch, Manfredo do Carmo
- **C04 (E4):** Física Mecânica - Resnick, Halliday, Krane
- **C05 (E5):** Física Termodinâmica - Yunus Cengel
- **C06 (E6):** Eletromagnetismo - David Griffiths
- **C07 (E7):** Química - John McMurry
- **C08 (E8):** Programação - Mark Lutz, Luciano Ramalho
- **C09 (E9):** Estruturas de Dados - Michael Goodrich, Thomas Cormen
- **C10 (E10):** Banco de Dados - Ramez Elmasri, Carlos Heuser
- **C11 (E11):** Redes - Andrew Tanenbaum, James Kurose
- **C12 (E12):** Engenharia de Software - Ian Sommerville, Robert Martin

### Consistência
✅ **Todos os livros** têm códigos Cutter compatíveis com suas estantes  
✅ **Busca por código Cutter** funciona tanto em livros quanto estantes  
✅ **Navegação indoor** baseada na localização das estantes por código

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
