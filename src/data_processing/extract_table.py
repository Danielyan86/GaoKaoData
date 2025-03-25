import re
import csv


def extract_table_data(html_file):
    with open(html_file, "r", encoding="utf-8") as f:
        content = f.read()

    # Extract all table rows
    rows = re.findall(r"<tr[^>]*>.*?</tr>", content, re.DOTALL)

    data = []
    for row in rows:
        # Extract cells from each row
        cells = re.findall(r"<td[^>]*>(.*?)</td>", row)
        if cells:
            # Clean the cell content
            cleaned_cells = [cell.strip() for cell in cells]
            data.append(cleaned_cells)

    return data


def save_to_csv(data, output_file):
    with open(output_file, "w", encoding="utf-8", newline="") as f:
        writer = csv.writer(f)
        writer.writerows(data)


def main():
    input_file = "table.html"
    output_file = "score_distribution.csv"

    # Extract data from HTML table
    data = extract_table_data(input_file)

    # Save to CSV
    save_to_csv(data, output_file)
    print(f"Data has been successfully extracted and saved to {output_file}")


if __name__ == "__main__":
    main()
