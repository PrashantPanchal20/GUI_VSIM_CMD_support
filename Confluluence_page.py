import sys
sys.path.append( '......../.local/lib/python2.7/site-packages' )

import pandas as pd
import atlassian
from atlassian import Confluence
import json
import requests
from requests.auth import HTTPBasicAuth
import json
defines = ""
args = ""


def confluence_data():
    global defines, args, opset, tables_op_set1, table_opset_dataframe

    url_page = 'https://confluence_page.com/'
    headers = {"Accept": "application/json"}

    space = 'page_space name'
    title0 = 'titlename0'
    title1 = 'titlename1'
    username = "user_name"
    api_token = 'token_ID'
    page_id0 = "..........."
    page_id1 = "..........."
    space_key = "page_space name"

    confluence = Confluence(url=url_page, token=api_token)
    text = "API Testing"
    page0 = confluence.get_page_by_title(space, title0, start=None, limit=None, expand="body.storage")
    body0 = page0["body"]["storage"]["value"]

    tables_define0 = pd.read_html(body0)[0]
    tables_args0 = pd.read_html(body0)[8]

    defines = tables_define0['Option'].to_string(index=False)
    args = tables_args0['Option'].to_string(index=False).strip()

    page1 = confluence.get_page_by_title(space, title1, start=None, limit=None, expand="body.storage")
    body1 = page1["body"]["storage"]["value"]

    tables_op_set1 = pd.read_html(body1)
    # print(type(tables_op_set1[0]))
    table_opset_dataframe = tables_op_set1[0]

    # opset = [item[2] for item in tables_op_set1[0].values.tolist()]
    # # addition_arg_ = " \n \n".join([str(number) for number in opset])
    # print(opset[0])
    
    # print(type(tables))
    # print(tables)
    # # for i, table in enumerate(tables, start=1):
    # #     file_name = f'table_{i}.csv'
    #     table.to_csv(file_name)
    # cols = enumerate(tables, [1])
    # # values = tables[0]        
    # print(cols)

confluence_data()
