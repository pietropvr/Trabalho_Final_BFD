# Relatório de Processo - Projeto Integrador: Caderneta PET

## 1. Fontes e Ferramentas Extra-aula Utilizadas

Durante o desenvolvimento da Caderneta PET, recorri a algumas ferramentas externas para garantir a qualidade profissional e o cumprimento dos requisitos técnicos:

* **Mermaid Live Editor:** Utilizado para desenhar e exportar o Diagrama de Arquitetura do sistema sem a necessidade de softwares pesados de design.
* **Google Fonts:** Importação da tipografia *Nunito* para melhorar a legibilidade e a interface de utilizador (UI).
* **The Dog API:** Documentação oficial consultada para a integração via requisição assíncrona (AJAX/Fetch) no formulário de criação de pets, garantindo a listagem dinâmica de raças.
* **Inteligência Artificial (Gemini):** Utilizada como "Thought Partner" (Parceiro de Pensamento) e assistente de *pair programming*. A IA auxiliou na refatoração de código repetitivo, na formatação do CSS Grid visando os padrões de Acessibilidade (WCAG) e na construção das expressões regulares e lógica de datas encapsulada na classe Orientada a Objetos (`CalculadoraAlertas`).

### Arquitetura do Sistema

Abaixo apresentamos o diagrama da arquitetura MVC adaptada que utilizamos na aplicação, evidenciando a separação entre Frontend, Backend e Banco de Dados:

```mermaid
flowchart TD
    classDef frontend fill:#0ea5e9,stroke:#0284c7,stroke-width:2px,color:#fff
    classDef backend fill:#10b981,stroke:#047857,stroke-width:2px,color:#fff
    classDef database fill:#f59e0b,stroke:#b45309,stroke-width:2px,color:#fff
    classDef external fill:#8b5cf6,stroke:#6d28d9,stroke-width:2px,color:#fff

    subgraph Cliente ["Frontend (Navegador / PWA)"]
        UI["Interface HTML5 / CSS Grid"]:::frontend
        Jinja["Templates Jinja2"]:::frontend
        UI <--> Jinja
    end

    subgraph Servidor ["Backend (Python / Flask)"]
        App["App Factory (init.py)"]:::backend
        Auth["Autenticação (auth.py)"]:::backend
        Core["Gestão Core (core.py)"]:::backend
        POO["CalculadoraAlertas (utils.py)"]:::backend

        Jinja <-->|Requisições HTTP| App
        App --> Auth
        App --> Core
        Core <-->|Usa Classe POO| POO
    end

    subgraph Dados ["Persistência"]
        DB[("SQLite (caderneta.db)")]:::database
        Auth <-->|SQL Queries| DB
        Core <-->|SQL Queries| DB
    end

    subgraph Externo ["APIs de Terceiros"]
        API["The Dog API"]:::external
        Core <-->|Proxy HTTP Seguro| API
    end
```

## Dificuldades Encontradas e Soluções

<<<<<<< HEAD
O maior desafio técnico ocorreu na integração da Exportação Offline do Prontuário. O objetivo era gerar um ficheiro HTML único, independente, que pudesse ser aberto sem internet, mantendo a fotografia do animal de estimação (uma vez que os ficheiros locais seriam perdidos após a transferência).

**Como foi superado:** Recorremos à biblioteca `base64` do Python. O backend abre a fotografia física do animal guardada no servidor (`static/uploads/`), converte a imagem num código textual denso e injeta esse texto diretamente no HTML exportado (`<img src="data:image/jpeg;base64,...">`). Isto garantiu que o tutor terá a imagem do seu pet para sempre, independentemente de onde abrir o ficheiro. Adicionalmente, também resolvemos falhas de sincronização entre o banco de dados (SQLite) e a aplicação através do padrão *App Factory*, reconstruindo a base física sempre que o *Schema* recebesse novas colunas (como "peso", "microchip" ou "foto").

## Autoavaliação

* **O que foi compreendido bem:** Sentimos muita segurança no fluxo MVC (Model-View-Controller) adaptado pelo Flask. A criação de Blueprints (`auth.py` e `core.py`), a gestão de sessões globais de utilizadores (`g.tutor`), a manipulação de ficheiros (upload seguro) e a injeção de dados complexos no frontend usando Jinja2 tornaram-se processos muito naturais. O desenvolvimento do CSS Grid aliado à responsividade também foi um ponto alto.
* **O que ainda preciso melhorar:** O gerenciamento de migrações de banco de dados. Apagar o ficheiro `.db` e recriá-lo é viável em ambiente de desenvolvimento, mas entendemos que para aplicações reais em produção, precisaremos dominar ferramentas como o Alembic ou o Flask-Migrate para atualizar tabelas sem perder os dados dos utilizadores.

## Sugestões e Avaliação do Curso

O formato orientado a projeto foi excelente por forçar a resolução de problemas reais. Como sugestão de melhoria para as próximas edições do curso, seria interessante a inclusão de um módulo curto focado especificamente em "Migrações de Banco de Dados", preparando os alunos para cenários onde a exclusão da base de testes não seja uma opção, e talvez uma abordagem mais aprofundada em Service Workers para PWA.
=======
O maior desafio técnico ocorreu na integração entre o Backend e a Persistência de Dados. Ao evoluir o projeto para incluir os campos "Peso" e "Microchip", o sistema começou a retornar *Erros 500 (Internal Server Error)* e `sqlite3.OperationalError: no such column`.

**Como foi superado:** Percebemos que o esquema lógico do banco de dados (o ficheiro `schema.sql`) estava dessincronizado com os formulários HTML e as rotas Flask. Para resolver, refatorei o `schema.sql` padronizando os nomes das colunas, adicionei a instrução `ON DELETE CASCADE` para evitar registos órfãos ao excluir um pet, apaguei o ficheiro físico antigo (`caderneta.db`) e forcei o sistema a recriar a estrutura do zero através do padrão *App Factory*. Além disso, enfrentei falsos-positivos de CSS no VS Code devido à sintaxe do Jinja2 no HTML, o que foi resolvido separando a lógica visual em blocos `<style>` e classes dinâmicas.

## Autoavaliação

* **O que foi compreendido bem:** Sinto muita segurança no fluxo MVC (Model-View-Controller) adaptado pelo Flask. A criação de *Blueprints* (`auth.py` e `core.py`), a gestão de sessões globais de utilizadores (`g.tutor`) e a injeção de dados no frontend usando *Jinja2* tornaram-se processos muito naturais. O desenvolvimento do *CSS Grid* aliado à responsividade (Media Queries) também foi um ponto alto do meu aprendizado.
* **O que ainda preciso melhorar:** O gerenciamento de migrações de banco de dados. Apagar o ficheiro `.db` e recriá-lo é viável em ambiente de desenvolvimento, mas entendo que para aplicações reais em produção precisarei de dominar ferramentas como o *Alembic* ou o *Flask-Migrate* para atualizar tabelas sem perder os dados dos utilizadores.

## Sugestões e Avaliação do Curso

O formato orientado a projeto foi excelente por forçar a resolução de problemas reais (como o CORS e o bloqueio de requisições a APIs externas em navegadores, que resolvemos criando um Proxy HTTP no Backend). Como sugestão de melhoria para as próximas edições do curso, seria interessante a inclusão de um módulo curto focado especificamente em "Migrações de Banco de Dados", preparando os alunos para cenários onde a exclusão da base de testes não seja uma opção.
>>>>>>> 9b358b82beb7b44c00cb676cb121f838cb0eb7cd
