import requests
import pandas as pd

import config # My API key is stored in a separate config.py file
api_key = config.api_key # Replace with your actual API key

# Load a CSV with a column named "company_number"
companies_df = pd.read_csv("ch_numbers.csv")

# Convert company numbers to string to add leading zeros if less than 8 digits
companies_df['company_number'] = companies_df['company_number'].astype(str)
companies_df['company_number'] = companies_df['company_number'].str.zfill(8)

results = []

for index, row in companies_df.iterrows():
    company_number = str(row['company_number'])
    print(f"Processing company number: {company_number}")
    
    # Construct the API endpoint URL
    url = f'https://api.company-information.service.gov.uk/company/{company_number}/filing-history'
    
    response = requests.get(url, auth=(api_key, '')) # No password
    
    if response.status_code == 200:
        data = response.json()  # Convert the response to a dictionary
        filings = data.get('items', []) 
        
        for filing in filings:
            if filing.get('category') == "accounts" and filing.get('date') >= "2019-01-01" and filing.get('pages') > 5:
                results.append({
                    'company_number': company_number,
                    'transaction_id': filing.get('transaction_id'),
                    'category': filing.get('category'),
                    'date': filing.get('date'),
                    'action_date': filing.get('action_date'),
                    'pages': filing.get('pages')
                })
    else:
        print(f"Error fetching filing history for company {company_number}. Status code: {response.status_code}")


results_df = pd.DataFrame(results)
results_df['link'] = results_df.apply(
    lambda row: f"https://find-and-update.company-information.service.gov.uk/company/{row['company_number']}/filing-history/{row['transaction_id']}/document?format=pdf", axis=1
)

results_df.to_csv("filing_history.csv", index=False)
