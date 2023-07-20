# Currency Exchange Tracking Application Documentation
## Introduction
The Currency Exchange Tracking Application is a web application designed to fetch and track exchange rates for different currencies on a daily basis. The application relies on data from the European Central Bank (ECB) and stores the exchange rates in a local DynamoDB table using LocalStack. LocalStack allows us to emulate AWS services locally, making it easier to develop and test the application without incurring actual AWS costs.

## Requirements
The application is designed to meet the following business requirements:

Provide current exchange rates for different currencies.
Display the change in exchange rates compared to the previous day.

## Technologies Used
Python
Flask: A micro web framework for Python./n
boto3: The AWS SDK for Python, used to interact with AWS services.
LocalStack: An open-source tool to emulate AWS services locally.
DynamoDB Local: An emulated version of AWS DynamoDB provided by LocalStack.

## Getting Started
To run the application locally, follow these steps:

Install Python and pip: Make sure you have Python (3.6 or higher) and pip (package installer) installed on your system.

Install Flask and boto3: Use pip to install the required Python packages.
bash
Copy code
### pip install Flask boto3
Install LocalStack: Follow the installation instructions for LocalStack from the GitHub repository: LocalStack on GitHub.

## Start LocalStack: After installing LocalStack, start it by running the following command:

### localstack start
Create the DynamoDB Table: Define and deploy the DynamoDB table locally using any IaC framework of your choice, such as AWS CDK, CloudFormation, or Terraform. Set the endpoint_url to 'http://localhost:4566' to connect to LocalStack DynamoDB.

Run the Flask Application: Start the Flask application by running the following command in your terminal:

python app.py

Access the Application: The application will be available at http://localhost:5000. You can use tools like curl or Postman to test the /exchange-rates endpoint.

Application Flow
Fetch Exchange Rates: The application fetches exchange rate data from the European Central Bank (ECB) API (https://www.ecb.europa.eu/stats/eurofxref/eurofxref-daily.xml).

Parse Exchange Rates: The XML response from the ECB API is parsed to extract exchange rate data for different currencies.

Calculate Rate Changes: The application compares the current exchange rates with the previous day's rates (stored in DynamoDB). It calculates the change in exchange rates for each currency.

Store Exchange Rates: The current exchange rates are stored in the LocalStack DynamoDB table with a timestamp as the partition key.

REST API Endpoint: The application exposes a REST API endpoint (/exchange-rates) that provides the current exchange rate information for all tracked currencies and their changes compared to the previous day.

## API Endpoint
Endpoint: /exchange-rates
Method: GET
Response: JSON format with the following structure:
json
{
  "exchange_rates": {
    "EUR": 1.0,
    "USD": 1.18,
    "GBP": 0.86,
    // Add other currencies and their rates here
  },
  "rate_changes": {
    "EUR": 0.0,
    "USD": -0.02,
    "GBP": 0.01,
    // Add other currencies and their rate changes here
  }
}
## Limitations
The application uses a static response for exchange rates for demonstration purposes. In a real-world scenario, it should parse the actual XML response from the ECB API.
The LocalStack environment is for local development and testing only and should not be used in production.
## Conclusion
The Currency Exchange Tracking Application demonstrates how to fetch and track exchange rates using LocalStack to emulate AWS services locally. By using LocalStack, developers can develop and test the application without incurring actual AWS costs. For production use, switch to using actual AWS services in the cloud.

## References
LocalStack on GitHub
AWS SDK for Python (Boto3) Documentation
Flask Documentation
ECB API Documentation
