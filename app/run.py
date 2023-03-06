# Run ETL from the command line

import helpers

csv_file_imp = 'Transactions.csv'
csv_file_out = 'out.csv'
currency = 'USD'
broker = 'degiro'

def main():
    helpers.etl_degiro(csv_file_imp, currency)

if __name__ == "__main__":
    main()