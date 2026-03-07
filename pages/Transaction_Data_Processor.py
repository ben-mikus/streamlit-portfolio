### Transaction_Data_Processor.py
### Within this page lives the presentation of the e-commerce data processing engine project

import pandas as pd
import streamlit as st
import helper

st.set_page_config("Transaction Data Processor Demo", layout="wide")

### Custom page margins
col1, col2, col3 = st.columns([2, 9, 2])

with col2:

    ### Title section
    st.title("Transaction Data Processor Demo")
    st.markdown("<p style='font-size:18px;'>Data processing tool that transforms raw transaction data into "
                "structured datasets for accounting and analysis.</p>", unsafe_allow_html=True)
    st.markdown("""
    <div style="display:flex; gap:10px; flex-wrap:wrap;">
        <span style="background:#bfdbfe; padding:3px 5px; border-radius:6px;font-size:14px;">Processing Engine</span>
        <span style="background:#ddd6fe; padding:3px 5px; border-radius:6px;font-size:14px;">Python</span>
        <span style="background:#ddd6fe; padding:3px 5px; border-radius:6px;font-size:14px;">Pandas</span>
        <span style="background:#bbf7d0; padding:3px 5px; border-radius:6px;font-size:14px;">Streamlit</span>
    </div>
    """, unsafe_allow_html=True)

    ### Introduction
    st.space()
    st.space()
    helper.header("Problem/Motivation")
    st.write("Modern accounting software is quite efficient and features such as QuickBooks' bank feed make bookkeeping"
             " accessible even for business owners with little-to-no accounting knowledge. However, e-commerce "
             "business, who sell their products through platforms such as Amazon, Shopify, and Etsy, don't find "
             "bookkeeping as reasonable a task since these platforms don't easily integrate into accounting software, "
             " if at all. I've designed this processing engine to solve just that problem. At the click of a button "
             "the program transforms transaction data into journal entries, which can be mass-uploaded to QuickBooks "
             "in minutes.")
    st.space()

    ### Live Demo
    helper.header("Live Demo")
    with st.container(border=True):

        from project_one import processor

        helper.header("Journal Entry Generator")

        ### Builds a session state to aid with UI
        if "generated_journals" not in st.session_state:
            st.session_state.generated_journals = []
        if "next_journal_no" not in st.session_state:
            st.session_state.next_journal_no = None

        ### Receive journal number input from user
        with st.container(border=True, width="stretch"):
            starting_journal_no = st.number_input(
                label="Starting Journal Number",
                value=100,
            )
        with st.container(border=True):
            st.badge("Etsy")

            col1, col2 = st.columns(2, gap="medium")

            with col1:
                summary_file = st.file_uploader(
                    label="Order Summary",
                    type=["csv"],
                    key="order_summary"
                )
            with col2:
                statement_file = st.file_uploader(
                    label="Monthly Statement",
                    type=["csv"],
                    key="monthly_statement"
                )

        if st.button("Generate Journal Entries", type="primary"):

            configuration = {
                "name": "Bottle Corp.",
                "platform": "Etsy"
            }
            journal_entries, missing_orders, next_journal_no = processor.run(
                summary_file=summary_file,
                statement_file=statement_file,
                configuration=configuration,
                starting_journal_no=starting_journal_no
            )

            st.success("Journal entries generated successfully.")
            st.success(f"The following orders require manual inspection: {missing_orders}.")
            st.dataframe(journal_entries, hide_index=True)
            csv = journal_entries.to_csv(index=False).encode("utf-8")
            st.download_button(
                label=f"Download Journal Uploader",
                data=csv,
                file_name=f"january_journal_uploader.csv".replace(" ", "_"),
                mime="text/csv"
            )
            st.write("Next Journal Number:", st.session_state.next_journal_no)
    st.space()

    ### Breakdown
    helper.header("How it Works")
    st.write("The user interface was designed to require no more than the click of a few buttons. Then, the engine "
             "within the tool follows a 4-step procedure:")
    st.write(">1. Import raw CSV files\n\n"
             ">2. Clean and standardize data\n\n"
             ">3. Apply accounting logic and labeling\n\n"
             ">4. Export the result\n\n")
    st.space()

    ### Demo Instruction
    helper.header("Try it For Yourself")
    st.write("Without diving into the code, this tool can be best understood by trying it out for yourself. Below, is "
             "some sample data from Etsy. Take a look at the notes, then download the files and run them through the "
             "processing engine.")

    tab1, tab2 = st.tabs(["Etsy Order Summary", "Etsy Monthly Statement"])
    with tab1:
        st.write("_Etsy provides its users with a handful of different CSV types. We're interested in two. The first_ "
                 "_stores all sales recorded in a selected time period. The numeric columns are quite clean, hardly_ "
                 "_ever containing commas and such. The net values, however, aren't calculated in a way that agrees_ "
                 "_with accounting principles. Then, sales tax and other fees are missing_.")
        df1 = pd.read_csv("data/Etsy_Order_Summary.csv")
        st.dataframe(df1, hide_index=True)
    with tab2:
        st.write("_The second dataset of interest covers all transactions affecting a business's deposit account_. "
                 "_It is here that the missing fees can be found, as well as information on non-order-related_ "
                 "_transactions, such as withdrawals and marketing fees. Because the data reads like a bank_ "
                 "_statement, numeric fields are riddled with non-numeric values and even stored within strings._")
        df2 = pd.read_csv("data/Etsy_Monthly_Statement.csv")
        st.dataframe(df2, hide_index=True)
    st.space()

    ### Broad application of skills
    helper.header("So What?")
    st.write("While this data tool was designed to solve a very specific problem, the underlying approach is broadly "
             "applicable. This project makes use of pre-processing methods that are applied to almost all real-world "
             "analyses. It demonstrates how data systems can be designed to address even highly specific business "
             "challenges. And, it shows how valuable a deep understanding of data is when tackling building workflows.")
    st.space()

    ### Reflection
    helper.header("Developer Notes")
    st.write("Deployed versions of this processing engine handle multiple sales channels, and even multiple business "
             "units, without issue. However, no project is perfect. QuickBooks limits CSV uploads to 1000 rows, "
             "so a good next step would be to implement more precise output handling. Additionally, general sales "
             "analyses on the transaction data would be easier performed if it were stored in a true database. "
             "Building an element to handle that could be interesting.")
    st.space()

    ### Repository link
    helper.header("TL;DR, just give me the code!")
    st.write("To get a better understanding the interworkings of the program and see some of the decisions that I made "
             "about the data, view the source code on my [GitHub](https://github.com/ben-mikus).")