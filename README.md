# Identifying "energy and carbon reports" in Companies House accounts
These two scripts perform the first two functions of a yet-to-be-completed process that aims to automate the extraction of sustainability-related data from Companies House (CH) accounts. The first script, when given a CSV containing a list of CH numbers, calls the CH API and returns a list of filed accounts from 2019 for each company. The second script then takes this list of accounts and scans through them using Tesseract OCR to identify which ones report data on "energy and carbon" usage.

## Next steps
(1) Identify more relevant companies (our internal data only takes us so far - additional research or another data source will need to be found).
(2) Parsing the accounts to extract the relevant data will be more difficult than originally thought, as the data is often presented in different formats, and many accounts are being filed in scanned PDFs only. This will require a very flexible approach, most likely involving advanced ML/NLP techniques. My initial experiments have been unsuccessful.

### Examples of tables

(example1.PNG)

(example2.PNG)

(example3.PNG)