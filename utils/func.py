import pandas as pd
import time, config
from urllib.parse import quote_plus as urlparse
from sqlalchemy import create_engine
import json

_USER_ = config._USER_
_PASS_ = urlparse(config._PASS_)
_IP_ = config._IP_
_DB_NAME_ = config._DB_NAME_

con = f"mysql+mysqlconnector://{_USER_}:{_PASS_}@{_IP_}/{_DB_NAME_}"
engine = create_engine(con)

def logging(text):
    t = time.strftime('%Y-%m-%d %X (%z)')
    print(f"[{t}] - {text}")

def get_all_topping():
    try:
        q = f"""SELECT 
                    m.menu_id,m.menu_name,m.base_price,
                    t.topping_id,t.topping_name,t.topping_price
                FROM menu m 
                LEFT JOIN topping t on t.menu_id = m.menu_id"""
        dft = pd.read_sql(q, engine)
        return dft
    except Exception as e:
        return f"Error occurred while fetching topping data: {str(e)}"

def get_all_fillings():
    try:
        q = f"""SELECT 
                    m.menu_id,m.menu_name,m.base_price,
                    f.filling_id,f.filling_name,f.filling_price 
                FROM menu m 
                LEFT JOIN filling f on f.menu_id = m.menu_id"""
        dff = pd.read_sql(q, engine)
        return dff
    except Exception as e:
        return f"Error occurred while fetching filling data: {str(e)}"
    
def count(payload, type):
    ret = {'message' : 'failed'}
    count_list = []

    for order in payload["orders"]:
        menu_id = order["menu_id"]
        quantity = order["quantity"]

        for item in order[type]:
            count_list.append({
                'menu_id': menu_id,
                'quantity': quantity,
                'item_id': item[type[:-1] + '_id'],
                'item_name': item[type[:-1] + '_name'], 
            })

    count_df = pd.DataFrame(count_list)
    # Menambahkan pemeriksaan bahwa setiap order untuk suatu menu hanya memiliki satu jenis topping
    menu_counts = count_df.groupby(['menu_id', 'quantity']).size().reset_index(name='total_count')
    menu_counts = menu_counts.sort_values(by=['menu_id', 'quantity'])

    if (menu_counts['total_count'] > 1).any():
        ret['message'] = 'failed'
        return ret
    
    ret['message'] = 'success'
    return ret

def get_all_menu():
    topping_data = get_all_topping()
    # Error message handler
    if isinstance(topping_data, str):
        return topping_data

    filling_data = get_all_fillings()
    # Error message handler
    if isinstance(filling_data, str):
        return filling_data

    topping_df = pd.DataFrame(topping_data)
    filling_df = pd.DataFrame(filling_data)

    # Grouping berdasarkan menu_id
    grouped_topping = topping_df.groupby(['menu_id', 'menu_name', 'base_price']).apply(
        lambda group: group[['topping_id', 'topping_name', 'topping_price']].to_dict(orient='records')
    ).reset_index().rename(columns={0: 'toppings'})

    grouped_filling = filling_df.groupby(['menu_id', 'menu_name', 'base_price']).apply(
        lambda group: group[['filling_id', 'filling_name', 'filling_price']].to_dict(orient='records')
    ).reset_index().rename(columns={0: 'fillings'})

    # Merge hasil grouping topping dan filling
    result_df = pd.merge(grouped_topping, grouped_filling, on=['menu_id', 'menu_name', 'base_price'])

    # Convert DataFrame ke JSON
    result_json = json.loads(result_df.to_json(orient='records'))

    return result_json

def count_price(payload):
    ret = {
        'Status': 'Failed',
        'Message': ''
    }

    if type(payload) is not dict: 
       ret['Message'] = f'Payload must in dict'
       return ret
    if len(payload.keys()) == 0: 
       ret['Message'] = f'Payload must not empty'
       return ret
    logging(f'data payload : {payload}')

    cek_topping = count(payload, 'toppings')
    if cek_topping['message'] != 'success':
        ret['Message'] = f'hanya boleh 1 jenis topping untuk setiap menu'
        return ret
    
    cek_fillings = count(payload, 'fillings')
    if cek_fillings['message'] != 'success':
        ret['Message'] = f'hanya boleh 1 jenis filling untuk setiap menu'
        return ret
    
    df = pd.json_normalize(payload, "orders", ["user", "date"])
    df["total_price"] = (
        df["quantity"] * df["base_price"] +
        df["toppings"].apply(lambda x: sum(t.get("topping_price", 0) for t in x)) * df["quantity"] +
        df["fillings"].apply(lambda x: sum(f.get("filling_price", 0) for f in x)) * df["quantity"]
    )
    logging(f'{df[["menu_id", "menu_name", "quantity", "total_price"]]}')

    total_order_price = df["total_price"].sum()
    logging(f'total price : {total_order_price}')
    
    ret["orders"] = df.to_dict(orient="records")
    ret['user'] = payload['user']
    ret['date'] = payload['date']
    ret["total_order_price"] = int(total_order_price)
    ret['Status'] = 'Success'

    return ret
