from bs4 import BeautifulSoup
from collections import OrderedDict
import csv

import pprint
pp = pprint.PrettyPrinter(indent=2)

table_types = {
    "meta_info": 1,
    "customer_info": 2,
    "order_dtail": 3,
    "price_summary": 4
}

excluded_headers = {
    "customer_info": [0, 1, 2, 17, 18, 19, 33, 36]
}

def prepend_invoice_label(element, index):
    headers_needs_additional_label = [14, 16, 18, 20, 22]
    if index in headers_needs_additional_label:
        return "ご請求先情報: " + element
    else:
        return element

def get_headers(table, type):
    th_tags = []
    if type in [table_types["meta_info"], table_types["order_dtail"], table_types["price_summary"]]:
        th_tags = list(map(lambda tag: tag.text.strip(), table.select("th")))
    elif type == table_types["customer_info"]:
        th_tags = list(map(lambda tag: tag.text.strip(), table.select("th")))
        th_tags = [th_tag for index, th_tag in enumerate(th_tags) if index not in excluded_headers["customer_info"]]

        indexes = list(list(zip(*enumerate(th_tags)))[0])
        th_tags = list(map(prepend_invoice_label, th_tags, indexes))
        th_tags = list(filter(len, th_tags))
    return th_tags

def get_rows(table, type):
    td_tags = []
    if type in [table_types["meta_info"]]:
        td_tags = list(map(lambda tag: tag.text.strip(), table.select("td")))
    if type == table_types["customer_info"]:
        td_tags = list(map(lambda tag: tag.text.strip(), table.find_all("td")))

    return td_tags

def retrieve_data(purchase_order):
    first_table_index = 0
    tables = purchase_order.find_all("table", recursive=False)
    headers = []
    rows = []
    for index, table in enumerate(tables):
        if index == first_table_index:
            continue
        headers = headers + get_headers(table=table, type=index)
        rows = rows + get_rows(table=table, type=index)

    exit()
    return ""

def main():
    file = open("html/yahoo_dummy20210417.html")
    html_doc = file.read()
    soup = BeautifulSoup(html_doc, "html.parser")

    purchase_orders = soup.select("#wrapper")

    data = []

    for purchase_order in purchase_orders:
        data.append(retrieve_data(purchase_order=purchase_order))

main()