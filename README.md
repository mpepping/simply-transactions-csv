# simply-transactions-csv

This app can be used to convert a [DEGIRO](https://www.degiro.nl) transactions CSV file to CSV format suitable for importing into a [Simply WallSt](https://simplywall.st/) portfolio.

## Running the app

**Using Python**:

* Run `pip install -r requirements.txt`
* Run `python app/app.py`
* Open `http://localhost:8080/` in your browser

Tested /w Python 3.11

**As a container**:

* `docker run -ti --rm --env OPENFIGI_API_KEY -p 8080:8080 ghcr.io/mpepping/simply-transactions-csv:latest`
* Open `http://localhost:8080/` in your browser

## OpenFIGI API usage

Ticker symbols are queried from the OpenFIG API. Without an API key, you can only make 30 requests per minute.
Set `OPENFIGI_API_KEY` environment variable to your API key. Register for a free API key at <https://openfigi.com/>

## Target CSV format

An example of the target CSV format can be found [here]()https://legacy.simplywall.st/documents/Simply%20Wall%20St%20-%20Example%20Import%20transactions.csv).

