#!/usr/bin/env python3
"""Generate HTML music collection table from Discogs CSV export."""

import csv


def generate_html(csv_file, output_file):
    """Read CSV and generate HTML table."""
    rows = []

    with open(csv_file, 'r', encoding='utf-8') as f:
        reader = csv.reader(f)
        next(reader)  # Skip header row

        for row in reader:
            # Skip rows that don't have enough columns
            if len(row) < 7:
                continue

            rows.append(
                f'      <tr>\n'
                f'        <td>{row[1]}</td>\n'
                f'        <td>{row[2]}</td>\n'
                f'        <td>{row[6]}</td>\n'
                f'      </tr>'
            )

    html_content = f'''<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Music Collection</title>
  <style>
    body {{
      margin: 1em;
      padding-bottom: 2em;
      font-family: "Courier New", Courier, monospace;
      font-size: 0.9em;
      font-weight: 600;
    }}

    .album-table {{
      background-color: #ffffff;
      border: 5px solid #000;
      border-collapse: separate;
      border-spacing: 1px;
      margin: 2em 0;
    }}

    .album-table th {{
      font-family: Arial, sans-serif;
      font-weight: bold;
      color: #0000ff;
      padding: 8px;
      border: 2px inset #999;
      text-align: left;
    }}

    .album-table td {{
      padding: 8px;
      border: 2px inset #999;
      font-weight: normal;
    }}

    .back-link {{
      color: #008000;
      text-decoration: underline;
    }}
  </style>
</head>
<body>
  <table class="album-table">
    <thead>
      <tr>
        <th>Artist</th>
        <th>Title</th>
        <th>Released</th>
      </tr>
    </thead>
    <tbody>
{chr(10).join(rows)}
    </tbody>
  </table>

  <p>
    <a href="../../index.html" class="back-link">Back.</a>
  </p>
</body>
</html>'''

    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(html_content)

    print(f'Generated {output_file} with {len(rows)} albums!')


if __name__ == '__main__':
    generate_html('discogs.csv', 'index.html')
