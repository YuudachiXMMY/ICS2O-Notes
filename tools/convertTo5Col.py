import os
from bs4 import BeautifulSoup

def normalize_table_columns(html_path, table_id, colNum, output_path=None):
    with open(html_path, 'r', encoding='utf-8') as file:
        soup = BeautifulSoup(file, 'html.parser')

    table = soup.find('table', {'id': table_id})
    if not table:
        print(f"No table found with id='{table_id}'")
        return

    rows = table.find_all('tr')
    flattened_cells = []

    for row in rows:
        tds = row.find_all('td')
        for td in tds:
            flattened_cells.append(td)

    new_rows = []
    while flattened_cells:
        new_row = flattened_cells[:colNum]
        flattened_cells = flattened_cells[colNum:]
        tr = soup.new_tag('tr')
        for td in new_row:
            tr.append(td)
        new_rows.append(tr)

    table.clear()
    for tr in new_rows:
        table.append(tr)

    output_path = output_path or html_path
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(str(soup))

    print(f"Table '{table_id}' normalized to {colNum} columns and saved to {output_path}")


# Example usage
if __name__ == "__main__":
    html_file = "docs/ICD2O.html"
    normalize_table_columns(html_file, "full-Calendar", 5)