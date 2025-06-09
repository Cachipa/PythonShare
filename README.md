# PythonShare

## Visão Geral

O **PythonShare** é uma aplicação web desenvolvida em Python com Flask para facilitar o cadastro, edição, consulta e exportação de dados ambientais integrados ao SharePoint. O sistema permite que usuários autenticados preencham formulários dinâmicos, salvem os dados em uma lista do SharePoint e gerem documentos Word personalizados a partir dessas informações.

---

## Funcionalidades

- **Login:**  
  Autenticação de usuários utilizando credenciais do SharePoint.

- **Cadastro e Edição de Itens:**  
  Formulário web para inserir e editar registros, incluindo campos dinâmicos para múltiplas intervenções ambientais.

- **Consulta e Filtros:**  
  Página principal com listagem dos itens cadastrados, filtros por status e ID.

- **Exportação para Word:**  
  Geração automática de documentos Word (.docx) preenchidos com os dados do item, incluindo a inserção dos campos dinâmicos em tabelas do modelo.

- **Integração Total com SharePoint:**  
  Todos os dados são salvos e lidos diretamente de uma lista do SharePoint, garantindo centralização e segurança.

---

## Como Funciona

1. **Login:**  
   O usuário acessa a página inicial, informa e-mail e senha do SharePoint. O sistema autentica e libera o acesso.

2. **Cadastro/Edição:**  
   - O usuário preenche o formulário, incluindo campos fixos (nome, endereço, etc.) e campos dinâmicos (tipo de intervenção, quantidade, unidade).
   - Os campos dinâmicos podem ser adicionados ou removidos conforme a necessidade.
   - Ao salvar, os dados são enviados para o SharePoint, sendo os campos dinâmicos armazenados em formato JSON.

3. **Consulta:**  
   - A página principal exibe todos os itens cadastrados.
   - É possível filtrar por status ou ID.
   - Cada item pode ser editado (se não estiver aprovado) ou exportado para Word (se aprovado).

4. **Exportação para Word:**  
   - Ao clicar em "Download", o sistema gera um arquivo Word baseado em um modelo.
   - Os dados do item são inseridos nos campos correspondentes do documento, incluindo a tabela de intervenções ambientais preenchida dinamicamente a partir do JSON.

---

## Estrutura dos Principais Arquivos

- `app.py`  
  Código principal da aplicação Flask, contendo as rotas, integração com SharePoint, processamento dos formulários e geração do Word.

- `templates/`  
  - `login.html`: Página de login.
  - `main.html`: Página principal com listagem e filtros.
  - `form.html`: Formulário de cadastro/edição com campos dinâmicos.

- `static/`  
  - `style.css`: Estilos gerais da aplicação.
  - `login.css`: Estilos exclusivos para a página de login.
  - `images/bgFloresta.jpg`: Imagem de fundo utilizada no layout.

- `2Modelo Parecer (Fabio) 2.docx`  
  Modelo Word utilizado para exportação dos dados.

---

## Como Executar

Esse código foi desenvolvido para trabalhar com uma base de dados especifica com acesso restrito, portanto não pode ser executado por qualquer pessoa.

1. **Pré-requisitos:**
   - Python 3.x
   - Instalar dependências:
     ```
     pip install flask shareplum python-docx
     ```

2. **Configuração:**
   - Coloque o modelo Word na raiz do projeto com o nome `2Modelo Parecer (Fabio) 2.docx`.
   - Ajuste a URL e nome da lista do SharePoint em `app.py` se necessário.

3. **Execução:**
   - Execute o aplicativo Flask:
     ```
     python app.py
     ```
   - Acesse pelo navegador: `http://127.0.0.1:5000`

---

## Considerações Finais

Este código foi desenvolvido durante os ultimos meses do meu estágio, com o objetivo de trabalhar especificamente com o documento modelo e uma base de dados criada a partir dele. Ele servirá como base para o próximo estagiário concluir e aprimorar a solução conforme as necessidades do setor.

Para mais informações, consulte a documentação do Flask e do SharePoint API.

---