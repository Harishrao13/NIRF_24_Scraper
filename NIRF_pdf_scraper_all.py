import pandas as pd
import pdfplumber
import re

def extract_numeric_value(text):
    match = re.search(r'\d+', text)
    return match.group() if match else '0'

def find_table_by_title(page, title):
    text = page.extract_text()
    if title in text:
        # Find the position of the title
        lines = text.split('\n')
        for i, line in enumerate(lines):
            if title in line:
                title_index = i
                break
        # Extract tables and check which one follows the title
        tables = page.extract_tables()
        for table in tables:
            if title_index < len(lines):
                title_line = lines[title_index]
                if any(title_line in row for row in table):
                    # print(table)
                    return table

    return None

def process_strength_data(table):
    # Processing logic as before
    df = pd.DataFrame(table[1:], columns=[col.replace('\n', ' ') for col in table[0]])
    df.columns = df.columns.str.replace('\n', ' ')
    df.columns = df.columns.str.strip().str.replace('\n', ' ', regex=True)

    # Exclude PG-Integrated and calculate sums
    df_ug = df[df['(All programs of all years)'].str.contains('UG')]
    df_pg = df[df['(All programs of all years)'].str.contains('PG') & ~df['(All programs of all years)'].str.contains('Integrated')]

    # Calculate the required sums
    totals = {
        'Total Male UG': df_ug['No. of Male Students'].astype(int).sum(),
        'Total Female UG': df_ug['No. of Female Students'].astype(int).sum(),
        'Total Male PG': df_pg['No. of Male Students'].astype(int).sum(),
        'Total Female PG': df_pg['No. of Female Students'].astype(int).sum(),
        'Total Strength UG': df_ug['Total Students'].astype(int).sum(),
        'Total Strength PG': df_pg['Total Students'].astype(int).sum(),
        'Total Same State Strength UG': df_ug['Within State (Including male & female)'].astype(int).sum(),
        'Total Same State Strength PG': df_pg['Within State (Including male & female)'].astype(int).sum(),
        'Total Different State Strength UG': df_ug['Outside State (Including male & female)'].astype(int).sum(),
        'Total Different State Strength PG': df_pg['Outside State (Including male & female)'].astype(int).sum(),
        'Total Different Country Strength UG': df_ug['Outside Country (Including male & female)'].astype(int).sum(),
        'Total Different Country Strength PG': df_pg['Outside Country (Including male & female)'].astype(int).sum(),
        'Total Economically Backward Strength UG': df_ug['Economically Backward (Including male & female)'].astype(int).sum(),
        'Total Economically Backward Strength PG': df_pg['Economically Backward (Including male & female)'].astype(int).sum(),
        'Total Socially Challenged Strength UG': df_ug['Socially Challenged (SC+ST+OBC Including male & female)'].astype(int).sum(),
        'Total Socially Challenged Strength PG': df_pg['Socially Challenged (SC+ST+OBC Including male & female)'].astype(int).sum(),
        'Total Tuition Fee Reimbursed from govt UG': df_ug['No. of students receiving full tuition fee reimbursement from the State and Central Government'].astype(int).sum(),
        'Total Tuition Fee Reimbursed from govt PG': df_pg['No. of students receiving full tuition fee reimbursement from the State and Central Government'].astype(int).sum(),
        'Total Tuition Fee Reimbursed from Institute Funds UG': df_ug['No. of students receiving full tuition fee reimbursement from Institution Funds'].astype(int).sum(),
        'Total Tuition Fee Reimbursed from Institute Funds PG': df_pg['No. of students receiving full tuition fee reimbursement from Institution Funds'].astype(int).sum(),
        'Total Tuition Fee Reimbursed from Private Bodies UG': df_ug['No. of students receiving full tuition fee reimbursement from the Private Bodies'].astype(int).sum(),
        'Total Tuition Fee Reimbursed from Private Bodies PG': df_pg['No. of students receiving full tuition fee reimbursement from the Private Bodies'].astype(int).sum(),
        'Students who are not receiving full tuition fee reimbursement UG': df_ug['No. of students who are not receiving full tuition fee reimbursement'].astype(int).sum(),
        'Students who are not receiving full tuition fee reimbursement PG': df_pg['No. of students who are not receiving full tuition fee reimbursement'].astype(int).sum()
    }
    print(totals)
    return pd.DataFrame(totals, index=[0])

def process_capital_expenditure(table):
    capital_df = pd.DataFrame(table[2:], columns=table[0])
    capital_df.columns = ['Expenditure Type', '2022-23', '2021-22', '2020-21']

    capital_df['Expenditure Type'] = capital_df['Expenditure Type'].str.replace('\n', ' ', regex=True).str.strip()

    expenditure_types = [
        'Library',
        'New Equipment for Laboratories',
        'Engineering Workshops',
        'Studios',
        'Other expenditure on creation of Capital Assets (excluding expenditure on Land and Building)'
    ]
    years = ['2022-23', '2021-22', '2020-21']

    expenditure_dict = {f'{expenditure}_{year}': [] for expenditure in expenditure_types for year in years}

    for year in years:
        for expenditure in expenditure_types:
            escaped_expenditure = re.escape(expenditure)
            value = capital_df[capital_df['Expenditure Type'].str.contains(escaped_expenditure, case=False, na=False, regex=True)][year].values
            key = f'{expenditure}_{year}'
            expenditure_dict[key] = [extract_numeric_value(value[0]) if len(value) > 0 else '0']

    return pd.DataFrame(expenditure_dict)

def process_operational_expenditure(table):
    operational_capital_df = pd.DataFrame(table[2:], columns=table[0])
    operational_capital_df.columns = ['Expenditure Type', '2022-23', '2021-22', '2020-21']

    operational_capital_df['Expenditure Type'] = operational_capital_df['Expenditure Type'].str.replace('\n', ' ', regex=True).str.strip()

    operational_expenditure_types = [
        'Salaries (Teaching and Non Teaching staff)',
        'Maintenance of Academic Infrastructure or consumables and other running expenditures(excluding maintenance of hostels and allied services,rent of the building, depreciation cost, etc)',
        'Seminars/Conferences/Workshops'
    ]
    years = ['2022-23', '2021-22', '2020-21']

    operational_expenditure_dict = {f'{opexpenditure}_{year}': [] for opexpenditure in operational_expenditure_types for year in years}

    for year in years:
        for opexpenditure in operational_expenditure_types:
            escaped_expenditure = re.escape(opexpenditure)
            value = operational_capital_df[operational_capital_df['Expenditure Type'].str.contains(escaped_expenditure, case=False, na=False, regex=True)][year].values
            key = f'{opexpenditure}_{year}'
            operational_expenditure_dict[key] = [extract_numeric_value(value[0]) if len(value) > 0 else '0']

    return pd.DataFrame(operational_expenditure_dict)

def main():
    i = 1
    serial = pd.read_csv('rankings_copy/nirf_university_rankings.csv')
    write_header = True

    for Id in serial['Institute ID']:
        print(f'{i}. {Id} currently scanning...')
        i += 1
        
        with pdfplumber.open(f'nirf_pdf_files/nirf_university_rankings/{Id}.pdf') as pdf:
            pages = pdf.pages
            
            strength_df = pd.DataFrame()
            capital_df = pd.DataFrame()
            operational_expenditure_df = pd.DataFrame()

            for page in pages:
                # strength_table = page.extract_table()[1] 
                capital_table = find_table_by_title(page, 'Annual Capital Expenditure on Academic Activities and Resources (excluding expenditure on buildings)')
                operational_table = find_table_by_title(page, 'Annual Operational Expenditure')

                if capital_table:
                    capital_df = process_capital_expenditure(capital_table)
                    # print(f'Capital Data Success')

                if operational_table:
                    operational_expenditure_df = process_operational_expenditure(operational_table)
                    # print(f'Operational Data Success')

                combined_df = pd.concat([capital_df, operational_expenditure_df], axis=1)

                combined_df['Institute ID'] = Id 

                combined_df.to_csv('rankin.csv', mode='a', index=False, header=False)

if __name__ == "__main__":
    main()

