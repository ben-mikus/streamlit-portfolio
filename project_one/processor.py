### processor.py
### Handles the transformation of transaction data from Etsy into journal entry format.

import pandas as pd
from project_one.dataframe import DataFrame
from project_one import mapping


### The transformation process is called through the run() function.
def run(summary_file, statement_file, configuration, starting_journal_no):
    # business_unit = configuration['name']
    platform = configuration['platform']

    ### Etsy provides two datasets that are required to satisfy accounting requirements. The Order Summary
    ### (summary_import) is the first dataset, and it contains order-focused data.
    raw_summary_data = pd.read_csv(summary_file)
    summary_import = raw_summary_data.loc[:, mapping.summary_columns_keep]

    ### Instantiate summary_import as DataFrame class object -> clean columns -> return to pandas object
    summary_import = DataFrame(df=summary_import, platform=platform)
    summary_import.clean(schema=mapping.summary_schema)
    summary_import = summary_import.df

    ### The second dataset required for the journaling process contains transaction-focused data through the Monthly
    ### statement (statement_import).
    raw_statement_data = pd.read_csv(statement_file)
    statement_import = raw_statement_data.loc[:, mapping.statement_columns_keep]

    ### Dataset-specific: Deposit amounts are stored within strings, and must be extracted to be cleaned. Order IDs are
    ### more easily indexable if stored in their own column. Null values in 'Info' are filled with 'Title' values.
    statement_import['Deposit'] = statement_import['Title'].where(
        statement_import['Title'].astype(str).str.contains("sent to your bank account", na=False))
    statement_import['Order ID'] = (
        statement_import['Info'].where(statement_import['Info'].astype(str).str.startswith('Order')))
    statement_import['Order ID'] = statement_import['Order ID'].str.replace('Order #', '', regex=False).str.strip()
    statement_import['Info'] = statement_import['Info'].fillna(statement_import['Title'])

    ### Instantiate statement_import as DataFrame class object -> clean columns -> return to pandas object
    statement_import = DataFrame(df=statement_import, platform=platform)
    statement_import.clean(schema=mapping.statement_schema)
    statement_import = statement_import.df

    ### Cancelled orders (orders paid for but not fulfilled) do not appear in the summary data. They must still be
    ### recorded as sales though since the refunds appear in the data, so at this point they are pulled aside and
    ### noted as requiring to be manually journaling adjustments.
    missing_orders = list((set(statement_import['Order ID'].dropna())) - (set(summary_import['Order ID'].dropna())))

    ### Prior to journaling, summary_import requires dataset-specific adjustments. To achieve this, values from the
    ### Monthly Statement dataset are filtered into individual dataframes and then layered in as columns.
    sales_tax = statement_import[statement_import['Title'] == 'Sales tax paid by buyer']
    summary_import['Sales Tax'] = (summary_import['Order ID'].map(
        dict(zip(sales_tax['Order ID'], sales_tax['Fees & Taxes']))).fillna(0).astype(float))

    colorado_retail_tax = statement_import[statement_import['Title'] == 'Colorado Retail Delivery Fee (paid by buyer)']
    summary_import['Colorado Retail Fee'] = (summary_import['Order ID'].map(
        dict(zip(colorado_retail_tax['Order ID'], colorado_retail_tax['Fees & Taxes']))).fillna(0).astype(float))

    offsite_ad_fee = statement_import[statement_import['Title'] == 'Fee for sale made through Offsite Ads']
    summary_import['Offsite Ad Fee'] = (summary_import['Order ID'].map(
        dict(zip(offsite_ad_fee['Order ID'], offsite_ad_fee['Fees & Taxes']))).fillna(0).astype(float))

    transaction_fees = statement_import[statement_import['Title'].str.startswith('Transaction fee:')]
    summary_import['Transaction Fees'] = round(
        summary_import['Order ID'].map(
            transaction_fees.groupby('Order ID')['Fees & Taxes'].sum()), 2).fillna(0).astype(float)

    ### Dataset-specific: The earned on order column is adjusted to reflect the net earned per order by the business.
    summary_import['Earned on Order'] = round(
            (summary_import['Order Total'] - summary_import[['Sales Tax', 'Colorado Retail Fee', 'Offsite Ad Fee',
                                                    'Card Processing Fees', 'Transaction Fees']].sum(axis=1)), 2)

    ### Re-instantiate statement_import as DataFrame class object -> assign journal numbers -> return to pandas object
    summary_import = DataFrame(df=summary_import, platform=platform)
    summary_import.number(current_journal_no=starting_journal_no)
    summary_import = summary_import.df

    ### With the proper adjustments made, the data is converted to a long format
    summary_long = summary_import.melt(
        id_vars=['JournalNo', 'Sale Date', 'Order ID'],
        value_vars=['Order Value', 'Shipping', 'Discount Amount', 'Offsite Ad Fee', 'Transaction Fees',
                    'Sales Tax', 'Colorado Retail Fee', 'Card Processing Fees', 'Earned on Order' ],
        var_name='Ledger Type',
        value_name='Value')

    ### Instantiate summary_long as DataFrame class object -> apply accounting logic -> return to pandas object
    summary_long = DataFrame(df=summary_long, platform=platform)
    summary_long.journal(account_maps=mapping.orders_map, label_column='Ledger Type', orders_data=True)
    summary_long = summary_long.df

    ### Revisit the second dataset to transform non-order-related transactions. Sales are indexed within the Monthly
    ### Statement data via sales labels or description containing order.
    statement_import = statement_import[
        ~(statement_import['Info'].str.contains("Order #", na=False) &
                ~(statement_import['Title'].str.startswith("Credit for", na=False) |
                statement_import['Title'].str.startswith("Refund to buyer", na=False) |
                statement_import['Title'].str.contains("refund", na=False, case=False))) &
        ~(statement_import['Type'] == 'Sale')]

    ### All values must be joined into one column (values are stored in multiple columns but none of them overlap)
    statement_import['Value'] = statement_import[['Amount', 'Fees & Taxes', 'Deposit']].sum(axis=1)

    ### Instantiate statement_import as DataFrame class object -> assign journal numbers -> apply accounting logic ->
    ### return to pandas object
    statement_import = DataFrame(df=statement_import, platform=platform)
    statement_import.number(current_journal_no=summary_long['JournalNo'].max() + 1)
    statement_import.journal(account_maps=mapping.transactions_map, label_rules=mapping.transaction_label_rules)
    statement_import = statement_import.df

    ### Journaling adjustments
    mask1 = ((statement_import['Title'].str.startswith("Credit for") |
            statement_import['Title'].str.contains("Refund to buyer for sales tax"))
            & statement_import['Info'].str.startswith("Order #"))
    statement_import.loc[mask1, 'Info'] = statement_import.loc[mask1, 'Title']
    mask2 = (statement_import['Title'].str.contains('Credit for listing fee'))
    statement_import.loc[mask2, 'Info'] = statement_import.loc[mask2, 'Title']

    ### Nearly ready for export, final adjustments are made to ensure proper concatenation of the two datasets.
    summary_long.rename(columns={'Sale Date':'JournalDate'}, inplace=True)
    summary_long = summary_long.loc[:, mapping.journal_columns_keep]
    statement_import.rename(columns={'Date':'JournalDate', 'Info': 'Description'}, inplace=True)
    journal_entries = pd.concat([summary_long, statement_import], join="inner", ignore_index=True)

    ### Instantiate journal_entries as DataFrame class object -> export
    journal_entries = DataFrame(df=journal_entries, platform=platform)
    journal_entries.format()

    next_journal_no = journal_entries.df['JournalNo'].max() + 1
    return journal_entries.df, missing_orders, next_journal_no