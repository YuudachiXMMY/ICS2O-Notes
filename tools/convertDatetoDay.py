import os
from datetime import datetime, timedelta
from bs4 import BeautifulSoup

def rename_table_dates(html_path, table_id, output_path=None):
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


if __name__ == "__main__":
    html_file = "docs/ICD2O.html"
    #rename_table_dates(html_file, "full-Calendar")
    add_weekday_dates_to_table(html_file, "full-Calendar", "2025-11-10")