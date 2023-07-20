import json
import requests
import boto3
import os
from datetime import datetime, timedelta
from flask import Flask, jsonify

app = Flask(__name__)

# ECB API endpoint for exchange rates
ECB_API_URL = "https://www.ecb.europa.eu/stats/eurofxref/eurofxref-daily.xml"

# Connect to DynamoDB Local using LocalStack's endpoint
dynamodb = boto3.resource('dynamodb', endpoint_url='http://localhost:4566', region_name='us-west-2')

table_name = 'ExchangeRates'
table = dynamodb.Table(table_name)

def fetch_exchange_rates():
    response = requests.get(ECB_API_URL)
    if response.status_code == 200:
        return response.text
    else:
        raise Exception("Failed to fetch exchange rates from ECB.")

def parse_exchange_rates(xml_data):
    # Parse the XML response and extract exchange rate data
    # (Implementation depends on your XML parsing library)
    # For this example, we'll use a static response
    return {
        "EUR": 1.0,
        "USD": 1.18,
        "GBP": 0.86,
        # Add other currencies and their rates here
    }

def calculate_rate_changes(current_rates, previous_rates):
    rate_changes = {}
    for currency, rate in current_rates.items():
        previous_rate = previous_rates.get(currency, None)
        if previous_rate:
            rate_changes[currency] = round(rate - previous_rate, 4)
        else:
            rate_changes[currency] = 0.0
    return rate_changes

def store_exchange_rates(data):
    # Save the data in the DynamoDB table with a timestamp as the partition key
    timestamp = datetime.now().isoformat()
    item = {
        "CurrencyCode": "ExchangeRates",
        "Timestamp": timestamp,
        "Rates": json.dumps(data)
    }
    table.put_item(Item=item)

@app.route('/exchange-rates', methods=['GET'])
def get_exchange_rates():
    try:
        # Fetch and parse exchange rate data
        xml_data = fetch_exchange_rates()
        exchange_rates = parse_exchange_rates(xml_data)

        # Fetch the previous day's rates from DynamoDB
        response = table.get_item(Key={"CurrencyCode": "ExchangeRates"})
        if 'Item' in response:
            previous_rates = json.loads(response['Item']['Rates'])
        else:
            previous_rates = {}

        # Calculate rate changes compared to the previous day
        rate_changes = calculate_rate_changes(exchange_rates, previous_rates)

        # Store the new exchange rates in DynamoDB
        store_exchange_rates(exchange_rates)

        # Return the exchange rates and rate changes as the API response
        response_data = {
            "exchange_rates": exchange_rates,
            "rate_changes": rate_changes
        }
        return jsonify(response_data), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)

