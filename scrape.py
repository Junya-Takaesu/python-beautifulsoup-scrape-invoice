from bs4 import BeautifulSoup
import csv

table_types = {
    "meta_info": 1,
    "customer_info": 2,
    "order_dtail": 3,
    "price_summary": 4
}

excluded_headers = {
    "customer_info": [0, 1, 2, 17, 18, 19, 33, 36]
}

def get_headers(table, type):
    th_tags = []
    if type in [table_types["meta_info"], table_types["order_dtail"], table_types["price_summary"]]:
        th_tags = list(map(lambda tag: tag.text.strip(), table.select("th")))
    elif type == table_types["customer_info"]:
        th_tags = list(map(lambda tag: tag.text.strip(), table.select("th")))
        th_tags = [th_tag for index, th_tag in enumerate(th_tags) if index not in excluded_headers["customer_info"]]
        th_tags = list(filter(len, th_tags))
    return th_tags

def get_rows(table, type):
    return "hoge"

def retrieve_data(purchase_order):
    result = {}
    first_table_index = 0
    # th_tags = purchase_order.select("th")
    # result = map(lambda tag: tag.text.strip(), th_tags)
    # return list(result)
    # tables = purchase_order.select("table")
    tables = purchase_order.find_all("table", recursive=False)
    headers = []
    for index, table in enumerate(tables):
        if index == first_table_index:
            continue
        headers = headers + get_headers(table=table, type=index)
        rows = get_rows(table=table, type=index)

    return headers

def main():
    file = open("html/yahoo_dummy20210417.html")
    html_doc = file.read()
    soup = BeautifulSoup(html_doc, "html.parser")

    purchase_orders = soup.select("#wrapper")

    rows = {}

    for purchase_order in purchase_orders:
        data = retrieve_data(purchase_order=purchase_order)
        print(data)
        # {"注文ID": "283982938", "注文日時": "2021年4月15日8時34分18秒", ....}

main()