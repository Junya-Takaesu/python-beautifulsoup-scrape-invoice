from bs4 import BeautifulSoup
from collections import OrderedDict
from pprint import pprint
import csv

table_types = {
    "meta_info": 1,
    "customer_info": 2,
    "order_detail": 3,
    "price_summary": 4
}

excluded_headers = ["利用クーポンID一覧", "クーポン値引き", "ご要望"]

def generate_dictionary_from_table_data(th_tags, table_type="default"):
    result = OrderedDict()

    for th_tag in th_tags:
        th_tag_text = th_tag.text.strip()

        if th_tag.find_next_sibling("td") and th_tag_text not in excluded_headers:
            td_tag_text = th_tag.find_next_sibling("td").text.strip()

            if table_type == table_types["customer_info"]:
                if th_tag_text in result:
                    result[th_tag_text + "(ご請求先情報)"] = td_tag_text
                else:
                    result[th_tag_text] = td_tag_text
            else:
                result[th_tag_text] = td_tag_text

    return result


def retrieve_dictionary_data(purchase_order):
    data = OrderedDict()
    data_array = []
    tables = purchase_order.find_all("table", recursive=False)

    for index, table in enumerate(tables):
        if index == 0:
            continue
        elif index == table_types["customer_info"]:
            data = {**data, **generate_dictionary_from_table_data(table.select("th"), table_type=table_types["customer_info"])}
        elif index == table_types["order_detail"]:
            order_records = []
            for index, tr_tag in enumerate(table.select("tr")):
                if index == 0:
                    order_record_headers = list(map(lambda tag: tag.text.strip(), tr_tag.select("th")))
                else:
                    order_record_data = list(map(lambda tag: tag.text.strip(), tr_tag.select("td")))
                    order_record = list(zip(order_record_headers, order_record_data))
                    order_records.append(order_record)
        else:
            data = {**data, **generate_dictionary_from_table_data(table.select("th"))}

    for order_record in order_records:
        data_array.append(OrderedDict({**data, **OrderedDict(order_record)}))

    return data_array

def main():
    file = open("html/yahoo_dummy20210417.html")
    html_doc = file.read()
    soup = BeautifulSoup(html_doc, "html.parser")

    purchase_orders = soup.select("#wrapper")

    data_dictionaries = []

    for purchase_order in purchase_orders:
        for _data_dictionary in retrieve_dictionary_data(purchase_order=purchase_order):
            data_dictionaries.append(_data_dictionary)

    with open('result/data.csv', 'w', newline='') as csvfile:
        fieldnames = []

        for data in data_dictionaries:
            if not fieldnames:
                fieldnames = data.keys()

        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()

        for data in data_dictionaries:
            writer.writerow(data)

main()