### dataframe.py
### Introduces a DataFrame class to streamline processing and transformation steps shared across platforms.

import pandas as pd
import numpy as np

class DataFrame:

### Constructor - instantiates a class object
    def __init__(self, df, platform):
        self.df = df
        self.platform = platform

###.clean() standardizes data and handles null values
    def clean(self, schema, date_format="%m/%d/%Y"):
        for col, dtype in schema.items():
            ### Optional safety
            if col not in self.df.columns:
                continue
            ### Cleaning for float values
            if dtype == "float":
                self.df[col] = (
                    self.df[col]
                    .astype(str)
                    .str.replace(',', '', regex=False)
                    .str.replace('$', '', regex=False)
                    .str.replace('(', '', regex=False)
                    .str.replace(')', '', regex=False)
                    .str.replace('-', '', regex=False)
                    .str.replace('--', '0', regex=False)
                    .str.strip()
                )
                self.df[col] = pd.to_numeric(
                    self.df[col], errors='coerce'
                ).fillna(0)
            ### Cleaning for data values
            elif dtype == "date":
                parsed = pd.to_datetime(
                    self.df[col],
                    format="mixed",
                    errors="coerce"
                )
                self.df[col] = parsed.dt.strftime(date_format)
            ### Cleaning for string values
            else:
                self.df[col] = (
                    self.df[col]
                    .astype(str)
                    .str.strip()
                    .fillna("None")
                )
        return self

### .number() handles the assignment of journal numbers
    def number(self, current_journal_no):
        self.df['JournalNo'] = range(
            current_journal_no,
            current_journal_no + len(self.df)
        )

# .journal() transforms the data into an accounting format
    def journal(self, account_maps, label_rules=None, label_column=None, orders_data=False):

        if label_rules is not None:
            conditions, choices = zip(*[
                (rule(self.df), label)
                for rule, label in label_rules
            ])
            self.df['Label'] = np.select(conditions, choices, default='Other')
            mapping_key = 'Label'

        elif label_column is not None:
            mapping_key = label_column

        else:
            raise ValueError("Either label_rules or label_column must be provided.")
        # Apply mapping
        self.df['Mapping'] = self.df[mapping_key].map(account_maps)
        self.df = self.df.explode('Mapping', ignore_index=True)
        # Cleanly expand the dictionaries into columns
        self.df = self.df.join(
            self.df['Mapping'].apply(pd.Series)
        )

        ###
        if orders_data:
            self.df['Description'] = (self.platform + " Order #" + self.df['Order ID'] + " " + self.df['TempDesc'])

        # Handle Debit and Credit columns
        self.df['Debit'] = self.df['Value'].where(self.df['Side'] == 'Debit', 0)
        self.df['Credit'] = self.df['Value'].where(self.df['Side'] == 'Credit', 0)
        # Drop empty rows
        self.df = self.df[~((self.df['Debit'] == 0) & (self.df['Credit'] == 0))]
        # Return the result
        return self

### .format()
    def format(self):
        self.df[['Debit', 'Credit']] = self.df[['Debit', 'Credit']].replace(0, '')
        self.df = self.df.sort_values(by=['JournalDate', 'JournalNo', 'Debit'],
                              ascending=[False, True, False])
        return self