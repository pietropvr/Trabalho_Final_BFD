<<<<<<< HEAD
```markdown
=======
>>>>>>> 9b358b82beb7b44c00cb676cb121f838cb0eb7cd
# Caderneta PET - Prontuário Digital

Bem-vindo à **Caderneta PET**, um sistema web desenvolvido para centralizar e facilitar a gestão do histórico de saúde de animais de estimação. Este projeto foi concebido como Projeto Integrador, aplicando conceitos avançados de Backend, Frontend, Banco de Dados Relacional e Integração de APIs.

A aplicação permite que os tutores cadastrem os seus pets, adicionem registros médicos (vacinas, consultas, exames) e recebam alertas visuais dinâmicos sobre prazos de validade e datas de retorno.

---

## Funcionalidades Principais

<<<<<<< HEAD
* **Gestão de Pets:** Cadastro detalhado de cães e gatos, suportando upload de fotografias, gestão de peso e número de microchip.
* **Prontuário Médico Inteligente:** Separação automática entre "Procedimentos Pendentes" (com cálculo de dias restantes para reforços) e "Histórico de Concluídos" geridos através de *checkboxes* dinâmicas.
* **Dashboard de Alertas:** Painel central que sinaliza automaticamente vacinas atrasadas (vermelho), a vencer hoje (laranja) ou próximas do vencimento (amarelo), integrando a API de Notificações nativa do sistema operacional (Web Push).
* **Exportação Offline (Standalone):** Geração de um ficheiro HTML independente contendo o histórico do pet, motor de pesquisa JavaScript e conversão da imagem do pet para *Base64*, garantindo funcionamento total sem internet.
* **Progressive Web App (PWA):** Suporte nativo para instalação como aplicação móvel (via `manifest.json`).
* **Integração API:** Consumo assíncrono da *The Dog API* para listagem automática de raças no formulário de cadastro.
* **Segurança:** Sistema de Autenticação gerido pelo Werkzeug (Hahs de senhas), e alteração de credenciais isolada no perfil do utilizador.
=======
* **Gestão de Pets:** Cadastro detalhado de cães e gatos, incluindo peso e número de microchip.
* **Prontuário Médico:** Histórico completo de eventos de saúde com cálculo inteligente de dias restantes para reforços.
* **Dashboard de Alertas:** Painel dinâmico que sinaliza automaticamente vacinas atrasadas (vermelho), próximas do vencimento (amarelo) ou em dia (verde).
* **Exportação Offline (Standalone):** Geração de um ficheiro HTML único contendo o histórico do pet e um motor de pesquisa JavaScript embutido, funcionando a 100% sem internet.
* **Progressive Web App (PWA):** Suporte nativo para instalação como aplicação móvel (via `manifest.json`).
* **Integração API:** Consumo assíncrono da *The Dog API* para listagem automática de raças no formulário de cadastro.
>>>>>>> 9b358b82beb7b44c00cb676cb121f838cb0eb7cd

---

## Tecnologias e Bibliotecas Utilizadas

### Frontend:
* HTML5 Semântico e CSS3 (CSS Grid & Flexbox)
<<<<<<< HEAD
* JavaScript (Vanilla) para requisições assíncronas (Fetch API), notificações e filtros offline
=======
* JavaScript (Vanilla) para requisições assíncronas (Fetch API) e filtros offline
>>>>>>> 9b358b82beb7b44c00cb676cb121f838cb0eb7cd
* Acessibilidade W3C/WCAG e Design Responsivo (Mobile-first)

### Backend:
* **Python 3.x**
* **Flask** (Padrão Application Factory e Blueprints)
<<<<<<< HEAD
* **Werkzeug** (Hashing e upload de arquivos seguros)
=======
* **Werkzeug** (Hashing de senhas para segurança)
>>>>>>> 9b358b82beb7b44c00cb676cb121f838cb0eb7cd
* **Jinja2** (Motor de templates)

### Persistência de Dados e Arquitetura:
* **SQLite** (Banco de dados relacional local)
* Programação Orientada a Objetos (POO) aplicada a regras de negócio
* Tratamento de Erros HTTP Personalizados (404, 500)

---

## Instalação e Execução (Guia do Avaliador)

O projeto foi configurado para ser testado de forma imediata e sem fricções. Siga os passos abaixo:

**1. Clone o repositório:**
```bash
<<<<<<< HEAD
git clone [https://github.com/pietropvr/Trabalho_Final_BFD.git](https://github.com/pietropvr/Trabalho_Final_BFD.git)
=======
git clone https://github.com/pietropvr/Trabalho_Final_BFD.git
>>>>>>> 9b358b82beb7b44c00cb676cb121f838cb0eb7cd
cd Trabalho_Final_BFD
```

**2. Crie e ative o ambiente virtual:**
* No Windows:
  ```bash
  python -m venv venv
  venv\Scripts\activate
  ```
* No Linux/Mac:
  ```bash
  python3 -m venv venv
  source venv/bin/activate
  ```

**3. Instale as dependências:**
```bash
pip install -r requirements.txt
```

**4. Inicialize e popule o Banco de Dados (Seed):**
```bash
python seed.py
```
*(Este comando recria a base de dados na pasta `instance` e insere um usuário e um pet de teste com registros médicos para visualização imediata dos alertas).*

**5. Execute a aplicação:**
```bash
flask run
```
Acesse no navegador: `http://127.0.0.1:5000`

---

<<<<<<< HEAD
=======
## Credenciais de Acesso (Testes)

Para acessar o sistema imediatamente como avaliador sem precisar realizar um novo cadastro, utilize as credenciais geradas pelo script `seed.py`:

* **E-mail:** `avaliador@teste.com`
* **Senha:** `123456`

---

>>>>>>> 9b358b82beb7b44c00cb676cb121f838cb0eb7cd
## Membros da Equipe e Divisão de Tarefas

* **[Pietro Veloso Rosa](https://github.com/pietropvr):** Estruturação da arquitetura Backend (Flask/Blueprints), Modelagem do Banco de Dados Relacional (SQLite), implementação de regras de negócio Orientadas a Objetos (`utils.py`), criação de testes unitários, scripts de migração (`seed.py`) e integração via Proxy com a The Dog API.
* **[Jéssica Vitória Almeida da Silva](https://github.com/jwssic):** Desenvolvimento da interface e integração da página de perfil de usuário (`perfil.html`), implementação e refinamento de design do sistema de autenticação (`login.html` e `register.html`), e elaboração do material visual e apresentação de slides (Pitch) para a entrega final do projeto.