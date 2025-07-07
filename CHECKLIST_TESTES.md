# Checklist de Testes - API Biblioteca IoT

## ⚙️ Setup Inicial

- [x] Ativar ambiente virtual: `source iotenv/bin/activate`
- [x] Iniciar servidor: `uvicorn main:app --host 0.0.0.0 --port 8000 --reload`
- [x] Popular banco de dados:
  - [x] `python -m db.populate_beacons`
  - [x] `python -m db.populate_estantes`
  - [x] `python -m db.populate_livros`
  - [x] `python -m db.populate_instancias`
- [x] Acessar Swagger UI: `http://localhost:8000/docs`

---

## 📱 Acesso via Celular/Rede

**Configure seu IP:** Copie `.env.example` para `.env` e defina seu `LOCAL_IP`  
**Descobrir IP:** `ifconfig` (macOS/Linux) ou `ipconfig` (Windows)

- [x] Testar acesso básico: `http://SEU_IP:8000/beacons/`
- [x] Abrir Swagger UI no celular: `http://SEU_IP:8000/docs`
- [x] Verificar se firewall do macOS não está bloqueando

> **Exemplo:** Se seu IP for `192.168.1.100`, acesse `http://192.168.1.100:8000/docs`

---

## 🏠 Testes - Beacons

### Listar e Consultar
- [x] **GET** `/beacons/` - Listar todos os beacons
- [x] **GET** `/beacons/AA:BB:CC:DD:EE:01` - Obter beacon específico (Entrada Principal)
- [x] **GET** `/beacons/AA:BB:CC:DD:EE:02` - Obter beacon específico (Saída)
- [x] **GET** `/beacons/INEXISTENTE` - Teste de erro 404

### Criar
- [x] **POST** `/beacons/` - Criar novo beacon de teste:
```json
{
  "mac": "AA:BB:CC:DD:EE:99",
  "posX": 5.0,
  "posY": 3.0,
  "label": "Beacon Teste"
}
```

### Atualizar e Deletar
- [x] **PUT** `/beacons/AA:BB:CC:DD:EE:99` - Atualizar beacon criado:
```json
{
  "mac": "AA:BB:CC:DD:EE:99",
  "posX": 6.0,
  "posY": 4.0,
  "label": "Beacon Atualizado"
}
```
- [x] **DELETE** `/beacons/AA:BB:CC:DD:EE:99` - Deletar beacon de teste

---

## 📚 Testes - Estantes

### Listar e Consultar
- [x] **GET** `/estantes/` - Listar todas as estantes
- [x] **GET** `/estantes/E1` - Estante azul posição (1.75, 1.0)
- [x] **GET** `/estantes/E7` - Estante verde posição (6.25, 1.0)
- [x] **GET** `/estantes/E12` - Última estante verde
- [x] **GET** `/estantes/INEXISTENTE` - Teste de erro 404

### Criar
- [x] **POST** `/estantes/` - Criar nova estante:
```json
{
  "idEstante": "E99",
  "posX": 10.0,
  "posY": 5.0,
  "cor": "vermelho",
  "codigosCutter": ["C99", "C100"]
}
```

### Atualizar e Deletar
- [x] **PUT** `/estantes/E99` - Atualizar cor para "amarelo":
```json
{
  "idEstante": "E99",
  "posX": 10.0,
  "posY": 5.0,
  "cor": "amarelo",
  "codigosCutter": ["C99", "C100"]
}
```
- [x] **DELETE** `/estantes/E99` - Deletar estante de teste

---

## 📖 Testes - Livros

### Listar e Consultar
- [x] **GET** `/livros/` - Listar todos os livros
- [x] **GET** `/livros/978-85-01-00001-1` - Cálculo Volume 1 (James Stewart)
- [x] **GET** `/livros/978-85-01-00007-7` - Física I - Mecânica (Resnick, Halliday, Krane)
- [x] **GET** `/livros/978-85-01-00003-3` - Álgebra Linear (Howard Anton, Chris Rorres)
- [x] **GET** `/livros/978-85-01-00015-5` - Programação em Python (Mark Lutz)
- [x] **GET** `/livros/INEXISTENTE` - Teste de erro 404

### Criar
- [x] **POST** `/livros/` - Criar novo livro:
```json
{
  "idLivro": "978-1234567890",
  "titulo": "Introdução à Inteligência Artificial",
  "autor": "Russell Norvig",
  "editora": "Editora Tecnologia",
  "codigoCutter": "C01",
  "estanteId": "E1"
}
```

### Atualizar e Deletar
- [x] **PUT** `/livros/978-1234567890` - Mudar autor e código Cutter
```json
{
  "idLivro": "978-1234567890",
  "titulo": "Introdução à Inteligência Artificial",
  "autor": "Stuart Russell, Peter Norvig",
  "editora": "Editora Tecnologia",
  "codigoCutter": "C02",
  "estanteId": "E2"
}
```
- [] **DELETE** `/livros/978-1234567890` - Deletar livro de teste

---

## 📋 Testes - Instâncias de Livros

### Listar e Consultar
- [x] **GET** `/instancias/` - Listar todas as instâncias
- [x] **GET** `/instancias/978-85-01-00001-1-EX1` - Instância 1 do Cálculo Volume 1
- [x] **GET** `/instancias/978-85-01-00005-5-EX2` - Instância 2 da Física I
- [x] **GET** `/instancias/978-85-01-00003-3-EX3` - Instância 3 da Álgebra Linear
- [x] **GET** `/instancias/INEXISTENTE` - Teste de erro 404

### Criar
- [x] **POST** `/instancias/` - Criar nova instância:
```json
{
  "idInstancia": "978-85-01-00001-1-EX99",
  "idLivro": "978-85-01-00001-1",
  "posX": 1.85,
  "prateleira": "MEIO",
  "situacao": "disponivel",
  "ultimaAtualizacao": "2025-01-07T12:00:00"
}
```

### Atualizar e Deletar
- [x] **PUT** `/instancias/978-1234567890-EX99` - Atualizar situação para "emprestado":
```json
{
  "idInstancia": "978-1234567890-EX99",
  "idLivro": "978-1234567890",
  "posX": 2,
  "prateleira": "MEIO",
  "situacao": "emprestado",
  "ultimaAtualizacao": "2025-01-07T13:00:00"
}
```
- [x] **DELETE** `/instancias/978-1234567890-EX99` - Deletar instância de teste

---

## 🔄 Testes - Fluxo Completo do Usuário

### Fluxo: Buscar → Selecionar → Ver Instâncias
- [x] **1. Buscar livros:** `GET /livros/buscar?q=calculo`
  - Deve retornar lista de livros que contêm "calculo" no título
- [x] **2. Pegar ID do livro:** Anotar o `idLivro` de um resultado (ex: "978-85-01-00001-1")
- [x] **3. Ver instâncias do livro:** `GET /livros/978-85-01-00007-7/instancias`
  - Deve retornar só as instâncias desse livro específico
- [x] **4. Selecionar instância:** Escolher uma instância da lista anterior
- [x] **5. Ver detalhes:** `GET /instancias/978-85-01-00001-1-EX1/detalhes`
  - Deve retornar detalhes completos incluindo localização

### Outros Testes de Fluxo
- [] **Fluxo Física:** Buscar "fisica" → Selecionar livro → Ver instâncias
- [] **Fluxo Álgebra:** Buscar "algebra" → Selecionar livro → Ver instâncias
- [] **Fluxo sem resultados:** Buscar "inexistente" → Lista vazia
- [] **Fluxo livro sem instâncias:** Selecionar livro que não tem instâncias

## 🔍 Testes - Buscas Especiais

### Buscar Livros por Nome (agora busca título E autor)
- [x] **GET** `/livros/buscar?q=calculo` - Buscar "calculo"
  - Deve retornar: Cálculo Volume 1 e 2 (James Stewart)
- [x] **GET** `/livros/buscar?q=fisica` - Buscar "fisica"
  - Deve retornar: Física I, II, III (Resnick, Halliday, Krane)
- [x] **GET** `/livros/buscar?q=algebra` - Buscar "algebra"
  - Deve retornar: Álgebra Linear e Álgebra Moderna
- [x] **GET** `/livros/buscar?q=geometria` - Buscar "geometria"
  - Deve retornar: Geometria Analítica e Geometria Diferencial
- [x] **GET** `/livros/buscar?q=programacao` - Buscar "programacao"
  - Deve retornar: Programação em Python (Mark Lutz)
- [x] **GET** `/livros/buscar?q=james` - Buscar por autor "james"
  - Deve retornar: Livros do James Stewart (Cálculo)
- [x] **GET** `/livros/buscar?q=stewart` - Buscar por sobrenome "stewart"
  - Deve retornar: Livros do James Stewart
- [x] **GET** `/livros/buscar?q=lutz` - Buscar por autor "lutz"
  - Deve retornar: Programação em Python (Mark Lutz)
- [x] **GET** `/livros/buscar?q=resnick` - Buscar por autor "resnick"
  - Deve retornar: Livros de Física (Resnick, Halliday, Krane)
- [x] **GET** `/livros/buscar?q=` - Busca vazia (deve retornar tudo)
- [x] **GET** `/livros/buscar?q=INEXISTENTE` - Busca sem resultados

### Detalhes Completos de Instâncias
- [x] **GET** `/instancias/978-85-01-00001-1-EX1/detalhes` - Detalhes da instância 1 do Cálculo
  - Verificar se inclui: instância, livro, estante, beacons próximos
- [x] **GET** `/instancias/978-85-01-00005-5-EX2/detalhes` - Detalhes da instância 2 da Física
- [] **GET** `/instancias/978-85-01-00003-3-EX3/detalhes` - Detalhes da instância 3 da Álgebra
- [] **GET** `/instancias/978-85-01-00007-7-EX1/detalhes` - Detalhes da instância 1 da Geometria
- [] **GET** `/instancias/978-85-01-00009-9-EX2/detalhes` - Detalhes da instância 2 de Programação
- [] **GET** `/instancias/INEXISTENTE/detalhes` - Teste de erro 404

---

## 🧪 Testes de Edge Cases

### Validação de Dados
- [] **POST** `/beacons/` com MAC duplicado - Deve dar erro
- [] **POST** `/estantes/` com ID duplicado - Deve dar erro
- [] **POST** `/livros/` com ISBN duplicado - Deve dar erro
- [] **POST** `/instancias/` com número tombo duplicado - Deve dar erro
- [] **POST** `/instancias/` com ISBN inexistente - Deve dar erro
- [] **POST** `/instancias/` com estante inexistente - Deve dar erro

### Métodos HTTP Inválidos
- [] **PATCH** em qualquer endpoint - Deve retornar 405
- [] **OPTIONS** verificar se CORS está funcionando

---

## 📊 Verificação Final

### Consistência dos Dados
- [x] Verificar se todas as instâncias têm livros válidos
- [x] Verificar se todas as instâncias têm estantes válidas
- [x] Verificar se posições X,Y das instâncias batem com suas estantes
- [x] Verificar se códigos Cutter estão consistentes (C01-C12)
- [x] Verificar se todos os livros têm campo "autor" preenchido
- [x] Verificar se códigos Cutter dos livros batem com os das estantes

### Performance
- [] Cronometrar tempo de resposta das buscas
- [] Testar com múltiplas requisições simultâneas
- [] Verificar se não há vazamentos de memória

### Documentação
- [] Swagger UI carrega corretamente
- [] Todos os endpoints aparecem na documentação
- [] Exemplos de request/response estão corretos

---

## 📝 Notas de Teste

**Data:** ___________  
**Testador:** ___________  
**Ambiente:** ___________  

### Problemas Encontrados:
- [] ________________________________
- [] ________________________________
- [] ________________________________

### Melhorias Sugeridas:
- [] ________________________________
- [] ________________________________
- [] ________________________________

---

## 🎯 Resumo de Cobertura

- **Beacons:** ___/15 testes ✅
- **Estantes:** ___/10 testes ✅  
- **Livros:** ___/10 testes ✅
- **Instâncias:** ___/10 testes ✅
- **Buscas:** ___/15 testes ✅
- **Edge Cases:** ___/10 testes ✅
- **Verificações:** ___/10 testes ✅

**Total:** ___/80 testes concluídos

---

## 📚 Empréstimo e Devolução

- [x] **POST** `/instancias/978-85-01-00001-1-EX1/emprestar` - Emprestar livro disponível
  - Deve alterar situação: disponivel → emprestado
  - Não empresta livro já emprestado
  - Não empresta livro cativo
- [x] **POST** `/instancias/978-85-01-00001-1-EX1/devolver` - Devolver livro
  - Só devolve livro emprestado
  ```json
  {
    "nova_posX": 2.0,
    "nova_prateleira": "BAIXO"
  }
  ```
  - Deve alterar: emprestado → disponivel + nova posição
- [] **POST** `/instancias/978-85-01-00001-1-EX2/emprestar` - Tentar emprestar livro cativo (deve dar erro)
- [] **POST** `/instancias/978-85-01-00001-1-EX1/emprestar` - Tentar emprestar livro já emprestado (deve dar erro)
- [] **POST** `/instancias/978-85-01-00001-1-EX3/devolver` - Tentar devolver livro disponível (deve dar erro)
  ```json
  {
    "nova_posX": 1.8,
    "nova_prateleira": "CIMA"
  }
  ```
- [] **POST** `/instancias/978-85-01-00001-1-EX1/devolver` - Testar validação de prateleira inválida (deve dar erro)
  ```json
  {
    "nova_posX": 2.0,
    "nova_prateleira": "INVALIDA"
  }
  ```
