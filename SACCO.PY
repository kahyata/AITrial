import sqlite3
import csv
import os

# Define the path to the SQLite database
db_path = r'C:\Users\User\Desktop\Database projects\sqlite\sqlite-tools-win-x64-3460000\Sacco\src\sacco.db'

# Define the directory for CSV files
csv_dir = r'C:\Users\User\Desktop\Database projects\sqlite\sqlite-tools-win-x64-3460000\Sacco\src\csvs'

# Ensure the CSV directory exists
os.makedirs(csv_dir, exist_ok=True)

# Connect to the SQLite database
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

# Create tables
tables_creation_queries = {
    'Businesses': '''
        CREATE TABLE IF NOT EXISTS Businesses (
            BusinessID INTEGER PRIMARY KEY AUTOINCREMENT,
            BusinessName VARCHAR(255) NOT NULL,
            Industry VARCHAR(100),
            OwnerName VARCHAR(255),
            ContactEmail VARCHAR(255),
            ContactPhone VARCHAR(50),
            StartDate DATE
        );
    ''',
    'Transactions': '''
        CREATE TABLE IF NOT EXISTS Transactions (
            TransactionID INTEGER PRIMARY KEY AUTOINCREMENT,
            BusinessID INTEGER,
            Date DATE NOT NULL,
            Type VARCHAR(50),
            Category VARCHAR(100),
            Amount DECIMAL(10, 2) NOT NULL,
            Description TEXT,
            FOREIGN KEY (BusinessID) REFERENCES Businesses(BusinessID)
        );
    ''',
    'Accounts': '''
        CREATE TABLE IF NOT EXISTS Accounts (
            AccountID INTEGER PRIMARY KEY AUTOINCREMENT,
            BusinessID INTEGER,
            AccountName VARCHAR(255),
            AccountType VARCHAR(50),
            Balance DECIMAL(10, 2),
            Currency VARCHAR(10),
            LastUpdated DATE,
            FOREIGN KEY (BusinessID) REFERENCES Businesses(BusinessID)
        );
    ''',
    'Invoices': '''
        CREATE TABLE IF NOT EXISTS Invoices (
            InvoiceID INTEGER PRIMARY KEY AUTOINCREMENT,
            BusinessID INTEGER,
            InvoiceNumber VARCHAR(50) NOT NULL,
            DateIssued DATE,
            DueDate DATE,
            Amount DECIMAL(10, 2) NOT NULL,
            Status VARCHAR(50),
            FOREIGN KEY (BusinessID) REFERENCES Businesses(BusinessID)
        );
    ''',
    'Expenses': '''
        CREATE TABLE IF NOT EXISTS Expenses (
            ExpenseID INTEGER PRIMARY KEY AUTOINCREMENT,
            BusinessID INTEGER,
            ExpenseType VARCHAR(100),
            Amount DECIMAL(10, 2) NOT NULL,
            DateIncurred DATE,
            Recurring BOOLEAN,
            Description TEXT,
            FOREIGN KEY (BusinessID) REFERENCES Businesses(BusinessID)
        );
    ''',
    'Revenue': '''
        CREATE TABLE IF NOT EXISTS Revenue (
            RevenueID INTEGER PRIMARY KEY AUTOINCREMENT,
            BusinessID INTEGER,
            Source VARCHAR(100),
            Amount DECIMAL(10, 2) NOT NULL,
            DateReceived DATE,
            Description TEXT,
            FOREIGN KEY (BusinessID) REFERENCES Businesses(BusinessID)
        );
    ''',
    'Assets': '''
        CREATE TABLE IF NOT EXISTS Assets (
            AssetID INTEGER PRIMARY KEY AUTOINCREMENT,
            BusinessID INTEGER,
            AssetName VARCHAR(255),
            AssetType VARCHAR(100),
            Value DECIMAL(10, 2),
            PurchaseDate DATE,
            Depreciation DECIMAL(10, 2),
            FOREIGN KEY (BusinessID) REFERENCES Businesses(BusinessID)
        );
    ''',
    'Liabilities': '''
        CREATE TABLE IF NOT EXISTS Liabilities (
            LiabilityID INTEGER PRIMARY KEY AUTOINCREMENT,
            BusinessID INTEGER,
            LiabilityName VARCHAR(255),
            LiabilityType VARCHAR(100),
            AmountOwed DECIMAL(10, 2),
            DueDate DATE,
            FOREIGN KEY (BusinessID) REFERENCES Businesses(BusinessID)
        );
    ''',
    'FinancialSummary': '''
        CREATE TABLE IF NOT EXISTS FinancialSummary (
            SummaryID INTEGER PRIMARY KEY AUTOINCREMENT,
            BusinessID INTEGER,
            PeriodStart DATE NOT NULL,
            PeriodEnd DATE NOT NULL,
            TotalRevenue DECIMAL(10, 2),
            TotalExpenses DECIMAL(10, 2),
            NetIncome DECIMAL(10, 2),
            TotalAssets DECIMAL(10, 2),
            TotalLiabilities DECIMAL(10, 2),
            FOREIGN KEY (BusinessID) REFERENCES Businesses(BusinessID)
        );
    ''',
    'Receipts': '''
        CREATE TABLE IF NOT EXISTS Receipts (
            ReceiptID INTEGER PRIMARY KEY AUTOINCREMENT,
            BusinessID INTEGER,
            TransactionID INTEGER,
            ReceiptNumber VARCHAR(50) NOT NULL,
            DateIssued DATE NOT NULL,
            Amount DECIMAL(10, 2) NOT NULL,
            PaymentMethod VARCHAR(50),
            IssuedBy VARCHAR(255),
            Description TEXT,
            ReceiptImage BLOB,
            FOREIGN KEY (BusinessID) REFERENCES Businesses(BusinessID),
            FOREIGN KEY (TransactionID) REFERENCES Transactions(TransactionID)
        );
    '''
}

# Execute table creation queries
for table_name, query in tables_creation_queries.items():
    cursor.execute(query)

# Insert sample data into tables
insert_data_queries = {
    'Businesses': '''
        INSERT INTO Businesses (BusinessName, Industry, OwnerName, ContactEmail, ContactPhone, StartDate)
        VALUES
        ('Mulioko Trading', 'Retail', 'Mwansa Chileshe', 'mwansa@muliokotrading.zm', '0976123456', '2020-03-15'),
        ('Chisungu Services', 'Service', 'Chileshe Mutale', 'chileshe@chisungu.zm', '0967876543', '2018-07-01'),
        ('Nsofwa Agro', 'Agriculture', 'Mutale Banda', 'mutale@nsofwaagro.zm', '0956789321', '2019-09-10');
    ''',
    'Transactions': '''
        INSERT INTO Transactions (BusinessID, Date, Type, Category, Amount, Description)
        VALUES
        (1, '2024-08-01', 'Income', 'Sales', 15000.00, 'Sales of goods'),
        (1, '2024-08-05', 'Expense', 'Rent', 3000.00, 'Monthly rent payment'),
        (2, '2024-08-03', 'Income', 'Consulting', 8000.00, 'Consulting service fee'),
        (3, '2024-08-06', 'Expense', 'Supplies', 2000.00, 'Purchase of farming supplies');
    ''',
    'Accounts': '''
        INSERT INTO Accounts (BusinessID, AccountName, AccountType, Balance, Currency, LastUpdated)
        VALUES
        (1, 'Zanaco Main Account', 'Asset', 50000.00, 'ZMW', '2024-08-07'),
        (2, 'Savings Account', 'Asset', 20000.00, 'ZMW', '2024-08-07'),
        (3, 'Liability Account', 'Liability', 10000.00, 'ZMW', '2024-08-07');
    ''',
    'Expenses': '''
        INSERT INTO Expenses (BusinessID, ExpenseType, Amount, DateIncurred, Recurring, Description)
        VALUES
        (1, 'Rent', 3000.00, '2024-08-05', 1, 'Monthly rent payment'),
        (2, 'Salaries', 7000.00, '2024-08-03', 1, 'Staff salaries for August'),
        (3, 'Supplies', 2000.00, '2024-08-06', 0, 'Purchase of farming supplies');
    ''',
    'Revenue': '''
        INSERT INTO Revenue (BusinessID, Source, Amount, DateReceived, Description)
        VALUES
        (1, 'Sales', 15000.00, '2024-08-01', 'Sales revenue for August'),
        (2, 'Consulting', 8000.00, '2024-08-03', 'Consulting service revenue'),
        (3, 'Farm Produce', 10000.00, '2024-08-10', 'Sale of farm produce');
    ''',
    'Assets': '''
        INSERT INTO Assets (BusinessID, AssetName, AssetType, Value, PurchaseDate, Depreciation)
        VALUES
        (1, 'Office Building', 'Property', 250000.00, '2020-03-15', 20000.00),
        (2, 'Computers', 'Equipment', 50000.00, '2018-07-01', 5000.00),
        (3, 'Tractor', 'Machinery', 120000.00, '2019-09-10', 10000.00);
    ''',
    'Liabilities': '''
        INSERT INTO Liabilities (BusinessID, LiabilityName, LiabilityType, AmountOwed, DueDate)
        VALUES
        (1, 'Bank Loan', 'Loan', 50000.00, '2024-12-31'),
        (2, 'Credit Card', 'Credit Line', 15000.00, '2024-11-15'),
        (3, 'Equipment Lease', 'Lease', 30000.00, '2024-10-20');
    ''',
    'FinancialSummary': '''
        INSERT INTO FinancialSummary (BusinessID, PeriodStart, PeriodEnd, TotalRevenue, TotalExpenses, NetIncome, TotalAssets, TotalLiabilities)
        VALUES
        (1, '2024-08-01', '2024-08-31', 15000.00, 3000.00, 12000.00, 50000.00, 50000.00),
        (2, '2024-08-01', '2024-08-31', 8000.00, 7000.00, 1000.00, 20000.00, 15000.00),
        (3, '2024-08-01', '2024-08-31', 10000.00, 2000.00, 8000.00, 120000.00, 30000.00);
    ''',
    'Receipts': '''
        INSERT INTO Receipts (BusinessID, TransactionID, ReceiptNumber, DateIssued, Amount, PaymentMethod, IssuedBy, Description)
        VALUES
        (1, 1, 'R001', '2024-08-01', 15000.00, 'Bank Transfer', 'Mwansa Chileshe', 'Receipt for sales'),
        (2, 2, 'R002', '2024-08-03', 8000.00, 'Bank Transfer', 'Chileshe Mutale', 'Receipt for consulting services'),
        (3, 3, 'R003', '2024-08-06', 10000.00, 'Cash', 'Mutale Banda', 'Receipt for farm produce');
    '''
}

# Execute insert data queries
for table_name, query in insert_data_queries.items():
    cursor.executescript(query)

# Function to export a table to CSV
def export_to_csv(table_name, filename):
    cursor = conn.cursor()
    cursor.execute(f"SELECT * FROM {table_name}")
    rows = cursor.fetchall()
    column_names = [description[0] for description in cursor.description]

    file_path = os.path.join(csv_dir, filename)
    with open(file_path, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(column_names)
        writer.writerows(rows)

# Dictionary of tables and their corresponding CSV filenames
tables_to_export = {
    'Businesses': 'Businesses.csv',
    'Transactions': 'Transactions.csv',
    'Accounts': 'Accounts.csv',
    'Invoices': 'Invoices.csv',
    'Expenses': 'Expenses.csv',
    'Revenue': 'Revenue.csv',
    'Assets': 'Assets.csv',
    'Liabilities': 'Liabilities.csv',
    'FinancialSummary': 'FinancialSummary.csv',
    'Receipts': 'Receipts.csv'
}

# Export each table to a CSV file
for table, filename in tables_to_export.items():
    export_to_csv(table, filename)

# Close the connection
conn.close()

print("CSV files have been exported to:", csv_dir)
