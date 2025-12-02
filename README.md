readme: |
  # 🏥 SGHSS – Sistema de Gestão Hospitalar e de Serviços de Saúde (VidaPlus)

  API Back-end desenvolvida para o projeto multidisciplinar da UNINTER (2025), com foco na modelagem, arquitetura e implementação de um sistema hospitalar para a instituição fictícia VidaPlus.

  A aplicação foi construída em **FastAPI**, seguindo boas práticas de segurança, autenticação, organização modular e documentação automática.

  ## 🚀 Funcionalidades Principais

  - Autenticação via **JWT**
  - Cadastro e gerenciamento de **usuários**
  - CRUD completo de **pacientes**
  - CRUD de **profissionais de saúde**
  - Cadastro de **unidades de atendimento**
  - Agendamento, atualização e listagem de **consultas**
  - Registro e consulta de **prontuários clínicos**
  - Armazenamento de **logs de ações** do sistema
  - Documentação automática via **Swagger** (`/docs`)

  ## 🛠 Tecnologias Utilizadas

  - Python 3.x
  - FastAPI
  - Uvicorn
  - SQLAlchemy
  - SQLite
  - Pydantic
  - python-jose (JWT)
  - Passlib (bcrypt)

  ## 📁 Estrutura do Projeto

  ```
  app/
    ├── routers/        # Rotas organizadas por domínio
    ├── models/         # Modelos ORM
    ├── schemas/        # Schemas Pydantic
    ├── security/       # Autenticação e geração de tokens JWT
    ├── database.py     # Configuração do banco de dados
    ├── main.py         # Ponto de entrada da aplicação
  ```

  ## ▶️ Como Executar o Projeto

  ### 1. Clone o repositório
  ```bash
  git clone https://github.com/SEU-USUARIO/vida-plus-backend.git
  cd vida-plus-backend
  ```

  ### 2. Crie um ambiente virtual
  ```bash
  python -m venv venv
  source venv/bin/activate   # Linux/Mac
  venv\Scripts\activate      # Windows
  ```

  ### 3. Instale as dependências
  ```bash
  pip install -r requirements.txt
  ```

  ### 4. Execute o servidor
  ```bash
  uvicorn main:app --reload
  ```

  ### 5. Acesse a documentação da API
  ```
  http://localhost:8000/docs
  ```

  ## 🗄 Observações Importantes

  - O arquivo de banco de dados (`.db`) **não é versionado**, sendo criado automaticamente.
  - O diretório `venv/` também **não é versionado**, seguindo boas práticas de desenvolvimento.
  - Prints de testes e evidências estão registrados no PDF entregue no ambiente acadêmico.
  - O projeto foi desenvolvido como **prova de conceito acadêmica**, não sendo adequado para produção.

  ## 📘 Objetivo Acadêmico

  Este projeto faz parte da disciplina **Projeto Multidisciplinar** e demonstra competências em:

  - Engenharia de software aplicada ao Back-end
  - Modelagem de dados e arquitetura
  - Implementação de APIs REST
  - Segurança e autenticação
  - Testes funcionais
  - Organização e documentação técnica

  ## 📚 Referências

  - FastAPI Documentation
  - SQLAlchemy Documentation
  - Python 3 Documentation
  - UNINTER – Roteiro de Projetos 2025A1
  - UNINTER – Orientações Unificadas do Projeto
  - UNINTER – FAQ Back-end
