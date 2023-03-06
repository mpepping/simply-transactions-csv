# https://www.openfigi.com/api

import json
import os
import pandas as pd
import random
import requests
import string

## CONSTANTS
API_URL = 'https://api.openfigi.com/v1/mapping'
CURRENCY = ['USD', 'EUR', 'GBP']

UPLOAD_FOLDER = '/tmp'
ALLOWED_EXTENSIONS = {'csv'}

## VARIABLES
if os.environ.get('OPENFIGI_API_KEY'):
    api_key = os.environ.get('OPENFIGI_API_KEY')
else:
    api_key = None


## FUNCTIONS
def get_currency(currency):
    """Validate currency"""
    cur = currency.upper()
    try:
        if cur in CURRENCY:
            return cur
        else:
            raise ValueError("Currency not supported")
    except ValueError as e:
        print(e)
        exit(1)


def get_ticker_from_isin(isin):
    """Get ticker from ISIN"""

    # Use API key if available
    if api_key == None:
        headers = { 'Content-Type':'text/json' }
    else:
        headers = { 'Content-Type':'text/json', 'X-OPENFIGI-APIKEY': api_key }

    url = API_URL
    payload = '[{"idType":"ID_ISIN","idValue":"' + isin + '"}]'

    r = requests.post(url, headers=headers, data=payload)

    try:
        b = json.loads(r.text)
    except:
        pass

    #a = return b[0]['data'][0]['ticker']
    try:
        return b[0]['data'][0]['ticker']
    except:
        pass

def etl_degiro(csv_file_imp, currency):
    fields = ['Datum', 'ISIN', 'Aantal', 'Koers', 'Unnamed: 8' ]
    fields_out = ['Ticker', 'Date', 'Shares', 'Price', 'Type']

    get_currency(currency)

    print("Processing file: " + csv_file_imp + " for currency: " + currency)

    imp_file_path = os.path.join(UPLOAD_FOLDER, csv_file_imp)
    out_file_path = os.path.join(UPLOAD_FOLDER, "simply_wallst_" + csv_file_imp)
    out_csv = open(out_file_path, 'w')

    df = pd.read_csv(imp_file_path, skipinitialspace=True, usecols=fields, parse_dates=['Datum'], dayfirst=True)
    df.rename(columns = {   "Datum": "Date",
                            "Aantal": "Shares",
                            "Koers": "Price",
                            "Unnamed: 8": "Valuta"
                        }, inplace=True)

    # Use mm/dd/yyyy format
    df['Date'] = df['Date'].dt.strftime('%m/%d/%Y')

    # Replace ISIN with ticker
    df['Ticker'] = df.apply(lambda row: get_ticker_from_isin(row['ISIN']), axis=1)

    # Format price on two decimals - seems not necessary for simply import
    # df['Price'] = df.apply(lambda row: format(float(row['Price']), '.2f'), axis=1)

    # Determine buy or sell action
    df['Type'] = df.apply(lambda row: "Buy" if float(row['Shares']) > 0 else "Sell", axis=1)

    # Convert shares to positive number
    df['Shares'] = df.apply(lambda row: int(row['Shares']) * -1 if float(row['Shares']) < 0 else row['Shares'], axis=1)

    # Use columns matching currency
    a = df[df['Valuta'].str.match(currency)]
    print(a.to_csv(index=False, columns=fields_out))
    out_csv.writelines(a.to_csv(index=False, columns=fields_out))


def etl_other(csv_file_imp, csv_file_out, currency):
    in_csv = open(csv_file_imp, 'r')
    out_csv = open(csv_file_out, 'w')
    out_csv.write(in_csv.read())


def random_string(filename):
    """Generate random string"""
    letters = string.ascii_lowercase
    concat_filename = filename.replace(' ', '_').lower()
    return ''.join(random.choice(letters) for i in range(6)) + '_' + concat_filename
