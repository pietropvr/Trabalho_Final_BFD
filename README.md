
# Caderneta Pet - Sistema de Gestão Veterinária

## Objetivo

A "Caderneta Pet" é uma aplicação web desenvolvida em Python e Flask que permite aos tutores gerir o histórico médico dos seus animais de estimação. O sistema centraliza informações de saúde, cria alertas de vencimento para vacinas e consultas, e permite a exportação do prontuário para consultas veterinárias.

## Funcionalidades Principais

* **Autenticação Segura:** Registo e login de utilizadores.
* **CRUD de Pets:** Cadastro, edição e remoção de animais (incluindo número de microchip).
* **Integração com API Externa:** Consumo da *The Dog/Cat API* via JavaScript para autocompletar raças em tempo real de forma dinâmica.
* **Prontuário Médico:** Registo de vacinas, consultas, cirurgias e vermífugos.
* **Inteligência de Alertas:** Painel dinâmico que calcula dias restantes e avisa o tutor sobre retornos médicos atrasados ou a vencer nos próximos 30 dias.
* **Exportação de Dados:** Geração dinâmica de ficheiros `.csv` com o histórico médico completo para download (suporte nativo UTF-8/BOM para Excel).

## Tecnologias Utilizadas

* **Backend:** Python, Flask, Jinja2
* **Base de Dados:** SQLite (com arquitetura de relacional e integridade referencial)
* **Frontend:** HTML5, CSS3, JavaScript (Fetch API)
* **Arquitetura:** Padrão MVC utilizando Flask Blueprints (`auth` e `core`)

## Como Executar o Projeto Localmente

1. Clone este repositório:
   `git clone https://github.com/SEU_USUARIO/SEU_REPOSITORIO.git`
2. Crie e ative um ambiente virtual:
   `python -m venv venv`
   *(Windows)* `venv\Scripts\activate` ou *(Mac/Linux)* `source venv/bin/activate`
3. Instale as dependências:
   `pip install -r requirements.txt`
4. Inicialize a base de dados:
   `python seed.py` *(ou o comando correspondente para criar o caderneta.db)*
5. Inicie o servidor:
   `flask run`
6. Aceda no navegador através de `http://127.0.0.1:5000`
