from bs4 import BeautifulSoup
import csv
import pprint
pp = pprint.PrettyPrinter(indent=4)

f = open("html/yahoo_dummy20210417.html")
html_doc = f.read()

soup = BeautifulSoup(html_doc, 'html.parser')

wrappers = soup.select("#wrapper")

rows = []

for wrapper in wrappers:
  wrapper_soup = BeautifulSoup(str(wrapper), 'html.parser')
  meta_table = BeautifulSoup(str(wrapper_soup.select("table")[1]), 'html.parser')
  customer_table = BeautifulSoup(str(wrapper_soup.select("table")[2]), 'html.parser')
  targets_from_customer_table = [2,3,4,5,6,7,14,15,16,17,18,19,22]
  invoice_table_range = [14,15,16,17,18,19]
  purchase_table_range = [22]


  if not rows:
    headers = []
    th_tags = meta_table.select("th")
    for th_tag in th_tags:
      headers.append(th_tag.text.strip())

    tr_tags = customer_table.select("tr")
    for target in targets_from_customer_table:
      tr_soup = BeautifulSoup(str(tr_tags[target]), 'html.parser')
      th_tags = tr_soup.select("th")
      for th_tag in th_tags:
        if th_tag.text.strip():
          if target in invoice_table_range:
            headers.append("請求情報: " + th_tag.text.strip())
          elif target in purchase_table_range:
            headers.append("購入時情報: " + th_tag.text.strip())
          else:
            headers.append(th_tag.text.strip())

    rows.append(headers)

  td_tags = meta_table.select("td")
  row = []
  for td_tag in td_tags:
    row.append(td_tag.text.strip())

  tr_tags = customer_table.select("tr")
  for target in targets_from_customer_table:
    if target < len(tr_tags):
      tr_soup = BeautifulSoup(str(tr_tags[target]), 'html.parser')
      div_tags = tr_soup.select("td div")
      for div_tag in div_tags:
        row.append(div_tag.text.strip())

  rows.append(row)

with open('result/sample_writer.csv', 'w') as f:
  writer = csv.writer(f)
  writer.writerows(rows)

print("done")