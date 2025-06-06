from flask import Flask, render_template, request, redirect, url_for, flash, send_from_directory, send_file
from shareplum import Site
from shareplum import Office365
from docx import Document
from io import BytesIO
import os
import json

app = Flask(__name__)
app.secret_key = "your_secret_key"  # Necessário para usar flash messages

# SharePoint credentials3
username = None
password = None


@app.route("/", methods=["GET", "POST"])
def login():
    global username, password
    if request.method == "POST":
        username = request.form.get("email")
        password = request.form.get("password")

        if not username or not password:
            flash("Email e senha não podem estar vazios!", "error")
            return redirect(url_for("login"))

        try:
            # Attempt to authenticate with SharePoint
            Office365('https://meioambientemg.sharepoint.com', username=username, password=password).GetCookies()
            flash("Login bem-sucedido!", "success")
            return redirect(url_for("main"))
        except Exception as e:
            flash(f"Erro no login: {e}", "error")
            return redirect(url_for("login"))

    return render_template("login.html")


@app.route("/main", methods=["GET", "POST"])
def main():
    try:
        # Authenticate and connect to SharePoint
        authcookie = Office365('https://meioambientemg.sharepoint.com', username=username, password=password).GetCookies()
        site = Site('https://meioambientemg.sharepoint.com/sites/BasedeDados', authcookie=authcookie)
        sp_list = site.List('Base de Dados')

        # Inicializar filtros
        status_filter = request.form.get("status_filter") if request.method == "POST" else None
        id_filter = request.form.get("id_filter") if request.method == "POST" else None

        # Construir a query com base nos filtros
        query = {}
        if status_filter:
            query.setdefault('Where', []).append(('Eq', 'Status', status_filter))
        if id_filter:
            query.setdefault('Where', []).append(('Eq', 'ID', id_filter))

        # Buscar itens com base na query
        items = sp_list.GetListItems(query=query) if query else sp_list.GetListItems()
    except Exception as e:
        flash(f"Erro ao acessar a lista do SharePoint: {e}", "error")
        items = []

    # Exemplo no seu route do Flask
    status_list = ["Edição", "Aprovado", "Invalidado"] 
    return render_template("main.html", items=items, status_list=status_list, status_filter=status_filter, id_filter=id_filter)


@app.route("/form", methods=["GET", "POST"])
def form():
    linhas_json = []
    status_list = ["Edição", "Aprovado", "Invalidado"]  # Adicione esta linha
    if request.method == "POST":
        # Get form data
        form_data = {
            'Status': request.form.get("status"),
            'Numero SEI': request.form.get("numero_sei"),
            'Nome': request.form.get("nome"),
            'Endereço': request.form.get("endereco"),
            'CPF/CNPJ': request.form.get("cpf_cnpj"),
            'Endereço Numero': request.form.get("endereco_numero"),
            'Bairro': request.form.get("bairro"),
            'UF': request.form.get("uf"),
            'CEP': request.form.get("cep"),
            'Telefone': request.form.get("telefone"),
        }

        # Processa campos dinâmicos
        tipo_intervencao_list = request.form.getlist('tipo_intervencao[]')
        quantidade_list = request.form.getlist('quantidade[]')
        unidade_list = request.form.getlist('unidade[]')
        linhas = []
        for tipo, qtd, un in zip(tipo_intervencao_list, quantidade_list, unidade_list):
            linhas.append({
                'tipo_intervencao': tipo,
                'quantidade': qtd,
                'unidade': un
            })
        form_data['JSON'] = json.dumps(linhas, ensure_ascii=False)

        # Check for required fields
        if not form_data['Status'] or not form_data['Numero SEI']:
            flash("Os campos 'Status' e 'Número SEI' são obrigatórios!", "error")
            return redirect(url_for("form"))

        try:
            # Authenticate and connect to SharePoint
            authcookie = Office365('https://meioambientemg.sharepoint.com', username=username, password=password).GetCookies()
            site = Site('https://meioambientemg.sharepoint.com/sites/BasedeDados', authcookie=authcookie)
            sp_list = site.List('Base de Dados')

            # Insert the new item
            sp_list.UpdateListItems(data=[form_data], kind='New')
            flash("Item inserido com sucesso no SharePoint!", "success")
        except Exception as e:
            flash(f"Erro ao inserir item: {e}", "error")

        return redirect(url_for("form"))

    # Se for GET e estiver editando, carrega o JSON existente
    item = None # ou busque o item do SharePoint se necessário
    if item and item.get('JSON'):
        try:
            linhas_json = json.loads(item['JSON'])
        except Exception:
            linhas_json = []
    return render_template("form.html", item=item, status_list=status_list, linhas_json=linhas_json)


@app.route("/edit/<item_id>", methods=["GET", "POST"])
def edit(item_id):
    try:
        # Authenticate and connect to SharePoint
        authcookie = Office365('https://meioambientemg.sharepoint.com', username=username, password=password).GetCookies()
        site = Site('https://meioambientemg.sharepoint.com/sites/BasedeDados', authcookie=authcookie)
        sp_list = site.List('Base de Dados')

        print(f"Editando item com ID: {item_id}")

        if request.method == "POST":
            # Get updated form data
            form_data = {
                'ID': item_id,
                'Status': request.form.get("status"),
                'Numero SEI': request.form.get("numero_sei"),
                'Nome': request.form.get("nome"),
                'Endereço': request.form.get("endereco"),
                'CPF/CNPJ': request.form.get("cpf_cnpj"),
                'Endereço Numero': request.form.get("endereco_numero"),
                'Bairro': request.form.get("bairro"),
                'UF': request.form.get("uf"),
                'CEP': request.form.get("cep"),
                'Telefone': request.form.get("telefone"),
            }
            # Processa campos dinâmicos
            tipo_intervencao_list = request.form.getlist('tipo_intervencao[]')
            quantidade_list = request.form.getlist('quantidade[]')
            unidade_list = request.form.getlist('unidade[]')
            linhas = []
            for tipo, qtd, un in zip(tipo_intervencao_list, quantidade_list, unidade_list):
                linhas.append({
                    'tipo_intervencao': tipo,
                    'quantidade': qtd,
                    'unidade': un
                })
            form_data['JSON'] = json.dumps(linhas, ensure_ascii=False)

            # Update the existing item
            sp_list.UpdateListItems(data=[form_data], kind='Update')
            flash("Item atualizado com sucesso no SharePoint!", "success")
            return redirect(url_for("main"))

        # Fetch the item data for pre-filling the form
        item = sp_list.GetListItems(
            fields=['ID', 'Status', 'Numero SEI', 'Nome', 'Endereço', 'CPF/CNPJ', 'Endereço Numero', 'Bairro', 'UF', 'CEP', 'Telefone', 'JSON'],
            query={'Where': [('Eq', 'ID', item_id)]}
        )
        if not item:
            flash("Item não encontrado!", "error")
            return redirect(url_for("main"))

        item = item[0]
        # Carregar o JSON para os campos dinâmicos
        linhas_json = []
        if item.get('JSON'):
            try:
                linhas_json = json.loads(item['JSON'])
            except Exception:
                linhas_json = []

        status_list = ["Edição", "Aprovado", "Invalidado"]
        return render_template("form.html", status_list=status_list, item=item, linhas_json=linhas_json)
    except Exception as e:
        flash(f"Erro ao acessar ou atualizar o item: {e}", "error")
        return redirect(url_for("main"))


@app.route("/download/<item_id>", methods=["GET"])
def download(item_id):
    try:
        # Authenticate and connect to SharePoint
        authcookie = Office365('https://meioambientemg.sharepoint.com', username=username, password=password).GetCookies()
        site = Site('https://meioambientemg.sharepoint.com/sites/BasedeDados', authcookie=authcookie)
        sp_list = site.List('Base de Dados')

        print(f"Gerando download para o item com ID: {item_id}")

        # Fetch the item data
        item = sp_list.GetListItems(
            fields=['Nome', 'Endereço', 'Telefone', 'JSON'],
            query={'Where': [('Eq', 'ID', item_id)]}
        )
        if not item:
            print("DEBUG: Item não encontrado!")
            flash("Item não encontrado!", "error")
            return redirect(url_for("main"))

        item = item[0]

        # Load the Word template
        template_path = os.path.join(os.path.dirname(__file__), "2Modelo Parecer (Fabio) 2.docx")
        if not os.path.exists(template_path):
            print(f"DEBUG: Template não encontrado em {template_path}")
            flash("Template Word não encontrado!", "error")
            return redirect(url_for("main"))

        print(f"DEBUG: Template encontrado em {template_path}")
        doc = Document(template_path)

        # --- ADICIONAR O JSON NA TABELA EXISTENTE ---
        if item.get("JSON"):
            try:
                dados_tabela = json.loads(item["JSON"])
                # Supondo que o JSON é uma lista de dicts com as chaves: tipo_intervencao, quantidade, unidade
                table = doc.tables[0]  # Use o índice correto da tabela desejada
                row_index = 18  # Índice da linha onde começa a inserir (ajuste conforme seu modelo)
                for i, linha in enumerate(dados_tabela):
                    new_row = table.add_row()
                    # Mover a nova linha para logo após a linha desejada
                    table._tbl.remove(new_row._tr)
                    table._tbl.insert(row_index + 2 + i, new_row._tr)
                    # Preencher as células (ajuste os índices conforme sua tabela)
                    new_row.cells[0].text = linha.get("tipo_intervencao", "")
                    new_row.cells[3].text = linha.get("quantidade", "")
                    new_row.cells[8].text = linha.get("unidade", "")
                    # Mesclar células conforme seu padrão
                    new_row.cells[0].merge(new_row.cells[2])
                    new_row.cells[3].merge(new_row.cells[7])
                    new_row.cells[8].merge(new_row.cells[12])
            except Exception as e:
                doc.add_paragraph("Erro ao processar dados de intervenção ambiental.")


        # Função para substituir texto em parágrafos e células de tabelas
        def replace_text_in_paragraphs(paragraphs, replacements):
            for paragraph in paragraphs:
                for key, value in replacements.items():
                    if key in paragraph.text:
                        paragraph.text = paragraph.text.replace(key, value)

        # Função para substituir texto em tabelas
        def replace_text_in_tables(tables, replacements):
            for table in tables:
                for row in table.rows:
                    for cell in row.cells:
                        replace_text_in_paragraphs(cell.paragraphs, replacements)

        # Substituições a serem feitas
        replacements = {
            "{{Nome}}": item.get("Nome", ""),
            "{{Endereço}}": item.get("Endereço", ""),
            "{{Telefone}}": item.get("Telefone", "")
        }

        # Substituir texto nos parágrafos do corpo do documento
        replace_text_in_paragraphs(doc.paragraphs, replacements)

        # Substituir texto nas tabelas
        replace_text_in_tables(doc.tables, replacements)

        # Substituir texto nos cabeçalhos e rodapés
        for section in doc.sections:
            replace_text_in_paragraphs(section.header.paragraphs, replacements)
            replace_text_in_paragraphs(section.footer.paragraphs, replacements)

        # Save to in-memory buffer
        buffer = BytesIO()
        doc.save(buffer)
        buffer.seek(0)

        # Send file directly from memory
        return send_file(
            buffer,
            as_attachment=True,
            download_name=f"Parecer_{item_id}.docx",
            mimetype="application/vnd.openxmlformats-officedocument.wordprocessingml.document"
        )

    except Exception as e:
        print("DEBUG: Exception capturada no download:", e)
        flash(f"Erro ao gerar o arquivo Word: {e}", "error")
        return redirect(url_for("main"))


if __name__ == "__main__":
    app.run(debug=True)
