from docx import Document
#Esse código existe porque o documento foi feito em uma tabela unica oq causa um comportamento diferente como pode ver no codigo abaixo para adicionar uma linha no 4. INTERVENÇÃO AMBIENTAL REQUERIDA eu precisei mesclar as celulas porque toda linha na tabela tem tecnicamente 12 colunas

# Abrir o documento
document = Document(r"c:\Users\DELL\Documents\Python\Site-1\2Modelo Parecer (Fabio) 2.docx")

# Selecionar a tabela (assumindo que você quer a primeira tabela)
table = document.tables[0]

# Exibir o conteúdo atual da tabela com índices para identificar posiçoes 
for row_index, row in enumerate(table.rows):
    for cell_index, cell in enumerate(row.cells):
        print(f"Row {row_index}, Cell {cell_index}: {cell.text}")

# Adicionar uma nova linha após a linha 18
row_index = 18  # Índice da linha com A1, A2, A3
new_row = table.add_row()  # Adiciona uma nova linha ao final da tabela

# Copiar a nova linha para logo após a linha 18
table._tbl.remove(new_row._tr)  # Remove a nova linha temporariamente
table._tbl.insert(row_index + 3, new_row._tr)  # Insere a nova linha após a linha 18

# Preencher a nova linha com os valores B1, B2, e B3
new_row.cells[0].text = "B1"
new_row.cells[3].text = "B2"
new_row.cells[8].text = "B3"

# Mesclar células na nova linha
# Mesclar células [0-2]
new_row.cells[0].merge(new_row.cells[2])

# Mesclar células [3-7]
new_row.cells[3].merge(new_row.cells[7])

# Mesclar células [8-12]
new_row.cells[8].merge(new_row.cells[12])

# Salvar o documento atualizado
document.save(r"c:\Users\DELL\Documents\Python\Site-1\2Modelo Parecer (Fabio) 2_updated.docx")