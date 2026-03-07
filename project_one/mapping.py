### mapping.py
### Stores process rules and accounting information that is passed through the processor.

### Not every column from the original Order Summary is required throughout the process. summary_columns_keep stores
### the columns to be maintained in a list to be passed through the .loc[] method.
summary_columns_keep = [
    'Sale Date',
    'Order ID',
    'Order Value',
    'Discount Amount',
    'Shipping Discount',
    'Shipping',
    'Sales Tax',
    'Order Total',
    'Card Processing Fees',
    'Order Net'
]

### The same can be said for the original Monthly Statement. statement_columns_keep serves the same purpose as
### summary_columns_keep but designed for the second dataset.
statement_columns_keep = [
    'Date',
    'Type',
    'Title',
    'Info',
    'Amount',
    'Fees & Taxes'
]

### In order to clean dataframe columns via the DataFrame class method, each column to be passed must have its type
### specified. summary_schema stores these specifications for the first dataset.
summary_schema = {
    "Sale Date": "date",
    "Order ID": "string",
    "Order Value": "float",
    "Discount Amount": "float",
    "Shipping Discount": "float",
    "Shipping": "float",
    "Sales Tax": "float",
    "Order Total": "float",
    "Card Processing Fees": "float",
    "Order Net": "float",
    "Adjusted Order Total": "float",
    "Adjusted Card Processing Fees": "float",
    "Adjusted Net Order Amount": "float"
}

### The same can be said for the Monthly Statement import. statement_schema serves the same purpose as summary_schema
### but designed for the second dataset.
statement_schema = {
    "Date": "date",
    "Amount": "float",
    "Fees & Taxes": "float",
    "Net": "float",
    "Deposit": "float"
}

### Pairing journaling details to each order line requires mapping. This dictionary contains the values to be mapped.
orders_map = {
    'Order Value': [
        {'AccountName': '4000 Product Sales',
         'Name': 'Etsy Customer',
         'Side': 'Credit',
         'TempDesc': 'Sale Credit'}
    ],
    'Shipping': [
        {'AccountName': '4100 Shipping Income',
         'Name': 'Etsy Customer',
         'Side': 'Credit',
         'TempDesc': 'Shipping Paid by Buyer'}
    ],
    'Discount Amount': [
        {'AccountName': '4200 Sales Discounts',
         'Name': 'Etsy',
         'Side': 'Debit',
         'TempDesc': 'Discount'}
    ],
    'Offsite Ad Fee': [
        {'AccountName': '6000 Advertising & Marketing',
         'Name': 'Etsy Ads',
         'Side': 'Debit',
         'TempDesc': 'Offsite Ads Fee'}
    ],
    'Transaction Fees': [
        {'AccountName': '5300 Merchant Fees',
         'Name': 'Etsy',
         'Side': 'Debit',
         'TempDesc': 'Transaction Fees'}
    ],
    'Sales Tax': [  # Two entries — One for collection, one for remittance
        {'AccountName': '2100 Sales Tax Payable',
         'Name': 'Etsy Customer',
         'Side': 'Credit',
         'TempDesc': 'Sales Tax Paid by Buyer'},
        {'AccountName': '2100 Sales Tax Payable',
         'Name': 'Etsy',
         'Side': 'Debit',
         'TempDesc': 'Sales Tax Remitted by Etsy'}
    ],
    'Colorado Retail Fee': [  # Two entries — One for collection, one for remittance
        {'AccountName': '2100 Sales Tax Payable',
         'Name': 'Etsy Customer',
         'Side': 'Credit',
         'TempDesc': 'Colorado Retail Tax Paid by Buyer'},
        {'AccountName': '2100 Sales Tax Payable',
         'Name': 'Etsy',
         'Side': 'Debit',
         'TempDesc': 'Colorado Retail Tax Remitted by Etsy'}
    ],
    'Card Processing Fees': [
        {'AccountName': '5300 Merchant Fees',
         'Name': 'Etsy',
         'Side': 'Debit',
         'TempDesc': 'Payment Processing Fee'}
    ],
    'Earned on Order': [
        {'AccountName': '1200 Etsy Balance',
         'Name': 'Etsy Customer',
         'Side': 'Debit',
         'TempDesc': 'Earned on Order'}
    ]
}

# A worthwhile addition for ease of future analyses on the database is to group transactions by category. As they are
# already assigned a "subcategory" type, this list helps map categorical values to 'Ledger Type' in processor.py.
category_label_rules = [
    (lambda df: df['Ledger Type'] == 'Sale of Product', 'Sale'),
    (lambda df: df['Ledger Type'] == 'Shipping paid by Buyer', 'Shipping'),
    (lambda df: df['Ledger Type'] == 'Discount Amount', 'Discount'),
    (lambda df: df['Ledger Type'] == 'Sales Tax', 'Tax'),
    (lambda df: df['Ledger Type'] == 'Colorado Retail Tax', 'Tax'),
    (lambda df: df['Ledger Type'] == 'Offsite Ad Fee', 'Fee'),
    (lambda df: df['Ledger Type'] == 'Payment Processing Fee', 'Fee'),
    (lambda df: df['Ledger Type'] == 'Transaction Fees', 'Fee'),
    (lambda df: df['Ledger Type'] == 'Earned on Order', 'Net')
]

# Prior to effectively pairing a transaction map to the non-order data, transactions must be specified at a higher level
# of detail than what is contained within the "Account Statement"'s 'Type' column. This specification label is created
# using np.select() in processor.py. Below is the conditions and choices list used for said np.select() use.
transaction_label_rules = [
    (lambda df: df['Type'] == 'Deposit', 'Deposit'),
    (lambda df: (df['Type'] == 'Fee') & (df['Title'] == 'Listing fee'), 'Listing Fee'),
    (lambda df: (df['Type'] == 'Marketing') & (df['Title'] == 'Etsy Ads'), 'Etsy Ads'),
    (lambda df: df['Type'].isin(['Shipping', 'Shipping label']), 'Shipping through Etsy'),
    (lambda df: (df['Type'] == 'Marketing') & (df['Title'] == 'Etsy Plus subscription fee'), 'Etsy Plus Subscription'),
    (lambda df: df['Type'] == 'Payment', 'Charge for Refund'),
    (lambda df: df['Type'] == 'Refund', 'Refund'),
    (lambda df: df['Title'].str.contains('Refund to buyer for sales tax', na=False), 'Sales Tax Refunded'),
    (lambda df: (df['Type'] == 'Marketing') & df['Title'].str.contains('Credit for Offsite Ads fee', na=False),
     'Credit for Offsite Ads Fee'),
    (lambda df: (df['Type'] == 'Fee') & df['Title'].str.contains('Credit for listing fee', na=False),
     'Credit for Listing Fee'),
    (lambda df: (df['Type'] == 'Fee') & df['Title'].str.contains('Credit for Etsy Ads fee', na=False),
     'Credit for Etsy Ads Fee'),
    (lambda df: (df['Type'] == 'Fee') & df['Info'].str.contains('Order #', na=False),
     'Credit for Fee on Refunded Order'),
]

# To most effectively pair the necessary journaling details to each transaction line, mapping is the best option. This
# dictionary contains the values that are intended to be mapped and what is to be mapped ot them.
transactions_map = {
    'Deposit': [  # Credit to clearing acc / Debit to checking acc
        {'AccountName': '1200 Etsy Balance',
         'Name': 'Etsy',
         'Side': 'Credit'},
        {'AccountName': '1100 Payment Clearing',
         'Name': 'Etsy',
         'Side': 'Debit'}
    ],
    'Listing Fee': [  # Debit to Merchant Fees / Credit to clearing acc
        {'AccountName': '5300 Merchant Fees',
         'Name': 'Etsy',
         'Side': 'Debit'},
        {'AccountName': '1200 Etsy Balance',
         'Name': 'Etsy',
         'Side': 'Credit'}
    ],
    'Etsy Ads': [  # Debit to Advertising / Credit to clearing acc
        {'AccountName': '6000 Advertising & Marketing',
         'Name': 'Etsy Ads',
         'Side': 'Debit'},
        {'AccountName': '1200 Etsy Balance',
         'Name': 'Etsy',
         'Side': 'Credit'}
    ],
    'Shipping through Etsy': [  # Debit to Shipping Fees / Credit to clearing acc
        {'AccountName': '5200 Shipping Fees',
         'Name': 'Etsy',
         'Side': 'Debit'},
        {'AccountName': '1200 Etsy Balance',
         'Name': 'Etsy',
         'Side': 'Credit'}
    ],
    'Etsy Plus Subscription': [  # Debit to Subscriptions / Credit to clearing acc
        {'AccountName': '6100 Subscriptions & Software',
         'Name': 'Etsy',
         'Side': 'Debit'},
        {'AccountName': '1200 Etsy Balance',
         'Name': 'Etsy',
         'Side': 'Credit'}
    ],
    'Charge for Refund': [  # Credit Charges income acc / Debit clearing acc
        {'AccountName': '4400 Other Income',
         'Name': 'Etsy Customer',
         'Side': 'Credit'},
        {'AccountName': '1200 Etsy Balance',
         'Name': 'Etsy',
         'Side': 'Debit'}
    ],
    'Refund': [  # Debit to Sales Refunds / Credit to clearing acc
        {'AccountName': '4300 Sales Refunds',
         'Name': 'Etsy',
         'Side': 'Debit'},
        {'AccountName': '1200 Etsy Balance',
         'Name': 'Etsy',
         'Side': 'Credit'}
    ],
    'Sales Tax Refunded': [  # Debit to Sales Refunds / Credit to clearing acc
        {'AccountName': '4400 Sales Refunds', 'Name': 'Etsy',
         'Side': 'Credit'},
        {'AccountName': '1200 Etsy Balance',
         'Name': 'Etsy',
         'Side': 'Debit'}
    ],
    'Credit for Offsite Ads Fee': [  # Debit to clearing acc / Credit to Advertising
        {'AccountName': '1200 Etsy Balance',
         'Name': 'Etsy',
         'Side': 'Debit'},
        {'AccountName': '6000 Advertising & Marketing',
         'Name': 'Etsy',
         'Side': 'Credit'}
    ],
    'Credit for Listing Fee': [  # Credit to Merchant Fees / Debit to clearing acc
        {'AccountName': '5300 Merchant Fees',
         'Name': 'Etsy',
         'Side': 'Credit'},
        {'AccountName': '1200 Etsy Balance',
         'Name': 'Etsy',
         'Side': 'Debit'}
    ],
    'Credit for Fee on Refunded Order': [
        {'AccountName': '5300 Merchant Fees',
         'Name': 'Etsy',
         'Side': 'Credit'},
        {'AccountName': '1200 Etsy Balance',
         'Name': 'Etsy',
         'Side': 'Debit'}
    ],
    'Credit for Etsy Ads Fee': [  # Credit to Advertising & Marketing / Debit to clearing acc
        {'AccountName': '6000 Advertising & Marketing',
         'Name': 'Etsy',
         'Side': 'Credit'},
        {'AccountName': '1200 Etsy Balance',
         'Name': 'Etsy',
         'Side': 'Debit'}
    ],
}

### After mapping is complete, the temporary columns can be dropped (by keeping only columns specified in
### journal_columns_keep).
journal_columns_keep = [
    'JournalNo',
    'JournalDate',
    'AccountName',
    'Name',
    'Description',
    'Debit',
    'Credit'
]