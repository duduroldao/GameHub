# GameHub - Catálogo Digital de Jogos

Projeto integrado de **DWS** (HTML, CSS, JavaScript), **POO** (Python + Flask) e **Banco de Dados** (MySQL).
O GameHub apresenta e organiza informações sobre jogos. Não executa, vende nem compra jogos.

## Estrutura

```
GameHub/
├── index.html                  página inicial (na raiz)
├── pages/  catalogo.html, detalhes.html, admin.html
├── css/    style.css
├── js/     script.js (comum), catalogo.js, detalhes.js, admin.js
├── img/jogos/                  13 capas (12 jogos + padrao.png)
├── backend/ app.py, models.py, dao.py, conexao.py
├── database/ gamehub.sql
├── requirements.txt, README.md, .gitignore
```

## Como executar localmente

**1. Banco de dados (MySQL)**
- Inicie o MySQL (no XAMPP, clique em *Start* ao lado de MySQL) ou use o serviço do MySQL instalado.
- Importe o script: `mysql -u root -p < database/gamehub.sql` (ou, no phpMyAdmin/Workbench, abra e execute `database/gamehub.sql`).
- O script não apaga nada. Se rodar de novo com os dados já inseridos, dará erro de chave duplicada, o que protege os registros.

**2. Back-end (Flask)**
```
cd backend
pip install -r ../requirements.txt
```
Abra `backend/conexao.py` e ajuste `usuario` e `senha` do SEU MySQL (no XAMPP padrão a senha é vazia: `""`). Não publique sua senha real no GitHub. Depois:
```
python app.py
```
A API sobe em `http://127.0.0.1:5000`. Teste no navegador: `http://127.0.0.1:5000/api/jogos`.

**3. Front-end**
- Abra a pasta do projeto no VS Code e use *Live Server* no `index.html`, ou abra o `index.html` direto no navegador. O `flask-cors` libera as chamadas à API.
- **Endereço da API:** fica em uma única constante, na primeira linha útil de `js/script.js`: `const API_URL = "http://127.0.0.1:5000/api";`. Se o Flask mudar de endereço, altere só ela.

## Rotas da API

| Método | Rota | O que faz | Códigos |
|---|---|---|---|
| GET | `/api/jogos` | lista os jogos (com gêneros) | 200, 500 |
| GET | `/api/jogos/<id>` | busca um jogo | 200, 404, 500 |
| POST | `/api/jogos` | cadastra | 201, 400, 500 |
| PUT | `/api/jogos/<id>` | atualiza | 200, 400, 404, 500 |
| DELETE | `/api/jogos/<id>` | exclui | 200, 404, 500 |
| GET | `/api/generos` | lista os gêneros | 200, 500 |

Corpo do POST/PUT: `{"titulo", "desenvolvedora", "ano_lancamento", "descricao", "imagem", "generos": [ids]}`. Erros voltam como `{"erro": "mensagem"}`.

## GitHub e GitHub Pages

O **GitHub Pages só hospeda arquivos estáticos** (HTML, CSS, JS). Ele não executa Python/Flask nem hospeda MySQL. Publicando só o front-end, as páginas abrem, mas o catálogo e o CRUD **não funcionam** sem um back-end Flask hospedado e ligado a um MySQL, com `API_URL` apontando para ele. Para a apresentação, rode tudo localmente.

Comandos Git do dia a dia:
```
git status                      # o que mudou
git add .                       # prepara tudo para o commit
git commit -m "mensagem"        # grava (escreva mensagens descritivas)
git push                        # envia ao GitHub
git pull                        # traz atualizações do GitHub
```
Primeira vez: `git init`, `git remote add origin <url-do-repo>`, depois `git push origin main`.

**Professor como colaborador (você precisa fazer):** no repositório, *Settings > Collaborators > Add people* e informe `leonardo.stephan@eaportal.org`. Faça commits regularmente, por exemplo: estrutura e SQL; conexão e classes; DAO e rotas; páginas e CSS; JavaScript e integração; ajustes finais.

## Modelagem (descrição textual para o brModelo)

**Modelo conceitual**
- Entidade **JOGO**: `id` (identificador), `titulo`, `desenvolvedora`, `ano_lancamento`, `descricao`, `imagem`. Todos atributos simples e monovalorados.
- Entidade **GENERO**: `id` (identificador), `nome`.
- Relacionamento **pertence_a** entre JOGO e GENERO, **N:N**. Um jogo tem **1 ou mais** gêneros (1,N); um gênero pode ter **0 ou mais** jogos (0,N). A obrigatoriedade de ao menos um gênero por jogo é garantida pela API, não pelo banco.

**Modelo lógico (e físico, mesma estrutura)**
- `generos` (**PK** `id` INT AUTO_INCREMENT; `nome` VARCHAR(50) NOT NULL UNIQUE)
- `jogos` (**PK** `id` INT AUTO_INCREMENT; `titulo` VARCHAR(100) NOT NULL; `desenvolvedora` VARCHAR(100) NOT NULL; `ano_lancamento` INT NOT NULL com CHECK entre 1970 e 2100; `descricao` TEXT NOT NULL; `imagem` VARCHAR(255) NOT NULL DEFAULT 'padrao.png')
- `jogo_genero` (tabela associativa do N:N; **PK composta** (`jogo_id`, `genero_id`); **FK** `jogo_id` -> `jogos(id)`; **FK** `genero_id` -> `generos(id)`)

**Diagrama de Classes (UML)**
- `Entidade` (abstrata): `- id: int`; `+ to_dict(): dict` (abstrato).
- `Genero` herda de `Entidade`: `- nome: str`; `+ to_dict()`.
- `Jogo` herda de `Entidade`: `- titulo: str`, `- desenvolvedora: str`, `- ano_lancamento: int`, `- descricao: str`, `- imagem: str`, `- generos: list`; `+ adicionar_genero(genero)`, `+ to_dict()`, `+ from_dict(dados)`.
- Associação: `Jogo` 0..* ---- 1..* `Genero`.
- `JogoDAO`: `+ listar_todos()`, `+ buscar_por_id(id)`, `+ inserir(jogo)`, `+ atualizar(id, jogo)`, `+ excluir(id)`. `GeneroDAO`: `+ listar_todos()`. Os DAOs usam `Jogo` e `Genero`; as classes de domínio não conhecem os DAOs.
- Exceções (herdam de `Exception`): `ValidacaoError` (dados inválidos) e `ErroBancoDados` (falha no MySQL).

## Onde cada conceito das apostilas aparece

- **DWS:** HTML semântico, caminhos relativos (`../`), variáveis CSS, Flexbox, media queries mobile first, `querySelector`, `createElement`, `addEventListener`, `fetch` com `async/await` e `try/catch`, `JSON.stringify`, validação com `required`/`minlength`/`pattern`.
- **POO:** encapsulamento com `@property`, classe abstrata (`ABC`), herança com `super()`, polimorfismo (`to_dict`), exceções personalizadas, `from_dict`, DAO, Flask (`jsonify`, `request.json`, `<int:id>`).
- **Banco:** `CREATE DATABASE/TABLE`, constraints, PK composta, FK, `INSERT`, `INNER JOIN`, `LEFT JOIN`, `GROUP BY`, `COUNT`.

### Pontos que NÃO estão nas apostilas (informe ao professor)

1. **`mysql-connector-python`**: a POO 4 ensina `sqlite3`. O fluxo é o mesmo (`connect`, `cursor`, `execute`, `commit`, `fetchall`, `lastrowid`); muda o marcador `%s` no lugar de `?`, e a conexão é fechada com `close()` num `finally`.
2. **`flask-cors`**: é ensinado na DWS 4.
3. **`URLSearchParams` / `window.location.search`** (`js/detalhes.js`): necessários para ler o `id` da URL.
4. **`event.preventDefault()`** (`js/admin.js`): necessário para o formulário não recarregar a página antes do `fetch`.
5. Em vez de `ON DELETE CASCADE` (não ensinado), o DAO apaga primeiro as linhas de `jogo_genero` e depois o jogo.
6. As capas são imagens **originais geradas** (gradiente com o título), não as capas oficiais. Para trocar, coloque o arquivo em `img/jogos/` e edite o jogo na administração.

## Relatório de testes (o que foi e o que NÃO foi verificado)

**Verificado neste ambiente:**
- Sintaxe de todos os `.js` (`node --check`) e varredura por métodos não ensinados (`.map`, `.filter`, `.find`, `.join`, `.includes`, `FormData`, `localStorage` etc.): nenhum, além das exceções 3 e 4.
- Estrutura, caminhos relativos de todas as páginas, ids usados pelo JS, classes CSS e capas citadas no SQL: sem erros.
- **29 testes** do DAO, das rotas e das classes (CRUD, validações, 400/404/500, exclusão de jogo com FK, banco fora do ar), executados com um **dublê do conector MySQL baseado em SQLite**.
- O `gamehub.sql`, convertido para SQLite, cria as 3 tabelas e insere 12 jogos, 13 gêneros e 30 ligações; as consultas de verificação deram o esperado (nenhum jogo sem gênero).
- **21 testes de ponta a ponta no Chromium** (início, catálogo, detalhes, administração com POST/PUT/DELETE, validação HTML5, mensagens, menu do celular, sem rolagem horizontal), usando o dublê de banco e um dublê do CORS.

**NÃO verificado (faça na sua máquina):**
- O `gamehub.sql` **não foi executado em um MySQL real**.
- O `mysql-connector-python` e o `flask-cors` **reais não estavam instalados** aqui. A integração Flask + MySQL real ainda precisa ser testada por você.
- Não há teste automático do comportamento da API para `/api/jogos/abc` (id não numérico): o Flask devolve a página 404 padrão e o front mostra mensagem de erro genérica.
