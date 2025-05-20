import json
from docx import Document
from shareplum import Site, Office365

# Autenticar no SharePoint
authcookie = Office365('https://meioambientemg.sharepoint.com', username='daniel.franca@meioambiente.mg.gov.br', password='Semad@2021').GetCookies()
site = Site('https://meioambientemg.sharepoint.com/sites/BasedeDados', authcookie=authcookie)
sp_list = site.List('Base de Dados')

# Obter os dados da lista
items = sp_list.GetListItems(fields=['ID', 'JSON'])

# Selecionar o item desejado (exemplo: ID = 1)
item = next((i for i in items if i['ID'] == '2'), None)
if not item:
    raise ValueError("Item não encontrado!")

# Carregar os dados da tabela a partir do JSON
dados_tabela = json.loads(item['JSON'])
print(dados_tabela)

# Abrir o documento
document = Document(r"c:\Users\DELL\Documents\Python\Site-1\2Modelo Parecer (Fabio) 2.docx")

# Selecionar a tabela (assumindo que você quer a primeira tabela)
table = document.tables[0]

# Determinar o número máximo de linhas
max_rows = max(len(dados_tabela["coluna_1"]), len(dados_tabela["coluna_2"]), len(dados_tabela["coluna_3"]))

# Adicionar linhas dinamicamente e preencher os dados
row_index = 18  # Índice da linha com A1, A2, A3
for i in range(max_rows):
    new_row = table.add_row()  # Adiciona uma nova linha ao final da tabela

    # Mover a nova linha para logo após a linha 18
    table._tbl.remove(new_row._tr)  # Remove a nova linha temporariamente
    table._tbl.insert(row_index + 3 + i, new_row._tr)  # Insere a nova linha após a linha 18

    # Preencher as células da linha com os dados das colunas
    new_row.cells[0].text = dados_tabela[f"coluna_{i+1}"][0] if i < len(dados_tabela[f"coluna_{i+1}"]) else ""
    new_row.cells[3].text = dados_tabela[f"coluna_{i+1}"][1] if i < len(dados_tabela[f"coluna_{i+1}"]) else ""
    new_row.cells[8].text = dados_tabela[f"coluna_{i+1}"][2] if i < len(dados_tabela[f"coluna_{i+1}"]) else ""

    # Mesclar células na nova linha
    # Mesclar células [0-2]
    new_row.cells[0].merge(new_row.cells[2])

    # Mesclar células [3-7]
    new_row.cells[3].merge(new_row.cells[7])

    # Mesclar células [8-12]
    new_row.cells[8].merge(new_row.cells[12])

# Salvar o documento atualizado
document.save(r"c:\Users\DELL\Documents\Python\Site-1\2Modelo Parecer (Fabio) 2_updated.docx")

