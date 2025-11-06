import os
from datetime import datetime, timedelta
from bs4 import BeautifulSoup

def normalize_table_columns(html_path, table_id, colNum, output_path=None):
    """
    An automation Python tool that reads HTML files and locates a table with a specified ID.
    The tool will then adjust the table to a given column number, colNum.
    If a row does not contain the specified colNum, the script will shift items from the next row to fill the column.
    """
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

def rename_table_dates(html_path, table_id, output_path=None):
    """
    An automation Python tool that reads HTML files and locates a table with a specified ID.
    It will modify the date in each <td> element enclosed in <strong> to Day N, where N is a sequential number from 1 to the last.
    """
    with open(html_path, 'r', encoding='utf-8') as file:
        soup = BeautifulSoup(file, 'html.parser')

    table = soup.find('table', {'id': table_id})
    if not table:
        print(f"No table found with id='{table_id}'")
        return

    count = 1
    for td in table.find_all('td'):
        strong_tag = td.find('strong')
        if strong_tag:
            strong_tag.string = f"Day {count}"
            count += 1

    output_path = output_path or html_path
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(str(soup))

    print(f"Replaced all <strong> date entries with sequential Day N labels in table '{table_id}'.")

def add_weekday_dates_to_table(html_path, table_id, start_date_str, output_path=None):
    """
    An automation Python tool that reads HTML files and locates a table with a specified ID.
    It will add a date, surrounded by <strong></strong>, from a given date after the <strong>Day N</strong>. The dates will only be weekdays.
    """
    with open(html_path, 'r', encoding='utf-8') as file:
        soup = BeautifulSoup(file, 'html.parser')

    table = soup.find('table', {'id': table_id})
    if not table:
        print(f"No table found with id='{table_id}'")
        return

    start_date = datetime.strptime(start_date_str, "%Y-%m-%d")
    current_date = start_date
    count = 1

    for td in table.find_all('td'):
        strong_tag = td.find('strong')
        if strong_tag:
            while current_date.weekday() >= 5:  # Skip weekends
                current_date += timedelta(days=1)
            formatted_date = current_date.strftime("%b %d")
            strong_tag.string = f"Day {count} | {formatted_date}"
            count += 1
            current_date += timedelta(days=1)

    output_path = output_path or html_path
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(str(soup))

    print(f"Added weekday dates to <strong> tags in table '{table_id}' starting from {start_date_str}.")

def merge_days_in_table(html_path, table_id, output_path=None):
    """
    Reads an HTML file, finds a table by its ID, and merges every two adjacent 'Day' cells into one.
    The merged cell keeps the Day number of the first cell and appends the content of the next one.
    """
    with open(html_path, "r", encoding="utf-8") as f:
        soup = BeautifulSoup(f, "html.parser")

    table = soup.find("table", {"id": table_id})
    if not table:
        print(f"No table found with id='{table_id}'")
        return

    new_rows = []
    all_tds = table.find_all("td")

    merged_cells = []
    for i in range(0, len(all_tds), 2):
        td1 = all_tds[i]
        td2 = all_tds[i + 1] if i + 1 < len(all_tds) else None

        merged_td = soup.new_tag("td")
        merged_td["bgcolor"] = td1.get("bgcolor", "#FFFFFF")
        merged_td["valign"] = "top"

        # Merge contents cleanly
        combined_html = str(td1.decode_contents())
        if td2:
            combined_html += "\n" + str(td2.decode_contents())

        merged_td.append(BeautifulSoup(combined_html, "html.parser"))
        merged_cells.append(merged_td)

    # Build new rows with up to 5 <td> each (to keep table structure readable)
    new_tr = soup.new_tag("tr")
    for idx, td in enumerate(merged_cells, start=1):
        new_tr.append(td)
        if idx % 5 == 0:  # new row every 5 cells
            new_rows.append(new_tr)
            new_tr = soup.new_tag("tr")
    if len(new_tr.contents) > 0:
        new_rows.append(new_tr)

    # Replace old rows
    for tr in table.find_all("tr"):
        tr.decompose()
    for tr in new_rows:
        table.append(tr)

    output_path = output_path or html_path
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(str(soup))

    print(f"Merged every two <td> cells in table '{table_id}' → saved to {output_path}")

from bs4 import BeautifulSoup

def replace_second_day_with_br(html_path, table_id, output_path=None):
    """
    Reads an HTML file, finds a table by its ID, and replaces the second <strong>Day X</strong>
    inside each <td> with a <br /> while keeping the rest of the content intact.
    """
    with open(html_path, "r", encoding="utf-8") as f:
        soup = BeautifulSoup(f, "html.parser")

    table = soup.find("table", {"id": table_id})
    if not table:
        print(f"No table found with id='{table_id}'")
        return

    for td in table.find_all("td"):
        strong_tags = td.find_all("strong")
        if len(strong_tags) >= 2:
            # Replace the second <strong> tag with <br />
            second_strong = strong_tags[1]
            br_tag = soup.new_tag("br")
            a_tag = soup.new_tag("strong")
            a_tag.string = "After Break Task"
            br_tag.append(a_tag)
            second_strong.replace_with(br_tag)

    output_path = output_path or html_path
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(str(soup))

    print(f"Replaced second <strong>Day X</strong> with <br /> in table '{table_id}' → saved to {output_path}")

if __name__ == "__main__":
    html_file = "docs/ICD2O.html"
    # normalize_table_columns(html_file, "full-Calendar", 5) # Make Each Row have 5 values
    # rename_table_dates(html_file, "full-Calendar") # Rename to Day 1, Day 2, ...
    # merge_days_in_table(html_file, "full-Calendar") # combine every two days
    add_weekday_dates_to_table(html_file, "full-Calendar", "2025-11-10")
    # replace_second_day_with_br(html_file, "full-Calendar")
