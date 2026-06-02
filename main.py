# ============================================
# APRIORI ALGORITHM - MENU DRIVEN PROGRAM
# Using Excel File Input
#
# Required Libraries:
# pip install pandas mlxtend openpyxl
# ============================================

import pandas as pd
from mlxtend.preprocessing import TransactionEncoder
from mlxtend.frequent_patterns import apriori, association_rules

# ---------- Global Variables ----------
transactions = []
df = None
frequent_itemsets = None


# ---------- Utility Function ----------
def pause():
    input("\nPress Enter to continue...")


# ---------- Load Excel File ----------
def load_excel():
    global transactions

    file_path = "data.xlsx"

    try:
        # Read Excel file
        data = pd.read_excel(file_path, engine="openpyxl")

        print("\nExcel File Loaded Successfully!\n")
        print(data.head())

        # Clear old transactions
        transactions.clear()

        # Convert rows into transaction lists
        for _, row in data.iterrows():
            items = []

            for item in row:
                if pd.notna(item):
                    items.append(str(item))

            if items:
                transactions.append(items)

        print("\nTransactions Created Successfully!")

    except FileNotFoundError:
        print("\nError: 'data.xlsx' file not found!")

    except Exception as e:
        print("\nError:", e)


# ---------- Show Transactions ----------
def show_transactions():

    if not transactions:
        print("\nNo transactions available!")
        return

    print("\n========== TRANSACTIONS ==========")

    for i, transaction in enumerate(transactions, start=1):
        print(f"T{i} : {transaction}")


# ---------- Convert to One-Hot Encoded Data ----------
def convert_to_dataframe():
    global df

    if not transactions:
        print("\nLoad Excel data first!")
        return

    # Transaction Encoding
    te = TransactionEncoder()
    te_array = te.fit(transactions).transform(transactions)

    # Create DataFrame
    df = pd.DataFrame(te_array, columns=te.columns_)

    print("\n====== ONE-HOT ENCODED DATA ======")
    print(df)


# ---------- Run Apriori Algorithm ----------
def run_apriori():
    global df, frequent_itemsets

    if df is None:
        print("\nConvert transactions into dataframe first!")
        return

    try:
        min_support = float(
            input("\nEnter Minimum Support (Example: 0.3): ")
        )

        frequent_itemsets = apriori(
            df,
            min_support=min_support,
            use_colnames=True
        )

        if frequent_itemsets.empty:
            print("\nNo frequent itemsets found!")

        else:
            print("\n====== FREQUENT ITEMSETS ======")
            print(frequent_itemsets)

    except ValueError:
        print("\nInvalid support value!")


# ---------- Generate Association Rules ----------
def generate_rules():
    global frequent_itemsets

    if frequent_itemsets is None:
        print("\nRun Apriori Algorithm first!")
        return

    try:
        min_confidence = float(
            input("\nEnter Minimum Confidence (Example: 0.6): ")
        )

        rules = association_rules(
            frequent_itemsets,
            metric="confidence",
            min_threshold=min_confidence
        )

        if rules.empty:
            print("\nNo association rules found!")

        else:
            print("\n====== ASSOCIATION RULES ======\n")

            print(
                rules[
                    [
                        "antecedents",
                        "consequents",
                        "support",
                        "confidence",
                        "lift"
                    ]
                ]
            )

    except ValueError:
        print("\nInvalid confidence value!")


# ---------- Main Menu ----------
while True:

    print("\n================================")
    print("   APRIORI ALGORITHM PROGRAM")
    print("================================")

    print("1. Load Data from Excel")
    print("2. Show Transactions")
    print("3. Convert to One-Hot Data")
    print("4. Run Apriori Algorithm")
    print("5. Generate Association Rules")
    print("6. Exit")

    choice = input("\nEnter Your Choice: ")

    # ---------- Menu Operations ----------
    if choice == "1":
        load_excel()
        pause()

    elif choice == "2":
        show_transactions()
        pause()

    elif choice == "3":
        convert_to_dataframe()
        pause()

    elif choice == "4":
        run_apriori()
        pause()

    elif choice == "5":
        generate_rules()
        pause()

    elif choice == "6":
        print("\nProgram Exited Successfully!")
        break

    else:
        print("\nInvalid Choice! Please try again.")
        pause()