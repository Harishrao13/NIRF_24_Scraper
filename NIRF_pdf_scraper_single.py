import pandas as pd
import pdfplumber
import re

def main():
    serial = pd.read_csv('rankings/nirf_university_rankings.csv')
    i = 1
    for Id in serial['Institute ID']:
        print(f'{i}. {Id} currently scanning...')
        i += 1
        
        with pdfplumber.open(f'nirf_pdf_files/nirf_university_rankings/{Id}.pdf') as pdf:
            strength_df = process_strength_data(pdf)
            
            # Add 'Institute ID' to the DataFrame
            strength_df['Institute ID'] = Id
            
            # Save the DataFrame to CSV in append mode
            strength_df.to_csv('test.csv', index=False, mode='a', header=not pd.io.common.file_exists('test.csv'))


def process_strength_data(pdf):
    data = []
    for page in pdf.pages:
        tables = page.extract_tables()
        filtered_tables = [table for table in tables if len(table) > 1]
        data.extend(filtered_tables)

    # Assuming the table of interest is the second one, index 1
    student_strength_data = data[1]
    df = pd.DataFrame(student_strength_data[1:], columns=[col.replace('\n', ' ') for col in student_strength_data[0]])
    df.columns = df.columns.str.replace('\n', ' ')

    # Exclude PG-Integrated and calculate sums
    df_ug = df[df['(All programs of all years)'].str.contains('UG')]
    df_pg = df[df['(All programs of all years)'].str.contains('PG') & ~df['(All programs of all years)'].str.contains('Integrated')]

    # Calculate the required sums
    total_male_ug = df_ug['No. of Male Students'].astype(int).sum()
    total_female_ug = df_ug['No. of Female Students'].astype(int).sum()
    total_male_pg = df_pg['No. of Male Students'].astype(int).sum()
    total_female_pg = df_pg['No. of Female Students'].astype(int).sum()

    total_strength_ug = df_ug['Total Students'].astype(int).sum()
    total_strength_pg = df_pg['Total Students'].astype(int).sum()

    total_same_state_strength_ug = df_ug['Within State (Including male & female)'].astype(int).sum()
    total_same_state_strength_pg = df_pg['Within State (Including male & female)'].astype(int).sum()

    total_different_state_strength_ug = df_ug['Outside State (Including male & female)'].astype(int).sum()
    total_different_state_strength_pg = df_pg['Outside State (Including male & female)'].astype(int).sum()

    total_different_country_strength_ug = df_ug['Outside Country (Including male & female)'].astype(int).sum()
    total_different_country_strength_pg = df_pg['Outside Country (Including male & female)'].astype(int).sum()

    total_economically_backward_strength_ug = df_ug['Economically Backward (Including male & female)'].astype(int).sum()
    total_economically_backward_strength_pg = df_pg['Economically Backward (Including male & female)'].astype(int).sum()

    total_socially_challenged_strength_ug = df_ug['Socially Challenged (SC+ST+OBC Including male & female)'].astype(int).sum()
    total_socially_challenged_strength_pg = df_pg['Socially Challenged (SC+ST+OBC Including male & female)'].astype(int).sum()

    total_tuition_fee_strength_ug_from_govt = df_ug['No. of students receiving full tuition fee reimbursement from the State and Central Government'].astype(int).sum()
    total_tuition_fee_strength_pg_from_govt = df_pg['No. of students receiving full tuition fee reimbursement from the State and Central Government'].astype(int).sum()

    total_tuition_fee_strength_ug_from_institute = df_ug['No. of students receiving full tuition fee reimbursement from Institution Funds'].astype(int).sum()
    total_tuition_fee_strength_pg_from_institute = df_pg['No. of students receiving full tuition fee reimbursement from Institution Funds'].astype(int).sum()

    total_tuition_fee_strength_ug_from_private = df_ug['No. of students receiving full tuition fee reimbursement from the Private Bodies'].astype(int).sum()
    total_tuition_fee_strength_pg_from_private = df_pg['No. of students receiving full tuition fee reimbursement from the Private Bodies'].astype(int).sum()

    no_tuition_fee_strength_ug = df_ug['No. of students who are not receiving full tuition fee reimbursement'].astype(int).sum()
    no_tuition_fee_strength_pg = df_pg['No. of students who are not receiving full tuition fee reimbursement'].astype(int).sum()


    # Creating a result DataFrame for selected columns
    strength_df = pd.DataFrame({
        'Total Male UG': [total_male_ug],
        'Total Female UG': [total_female_ug],
        'Total Male PG': [total_male_pg],
        'Total Female PG': [total_female_pg],
        'Total Strength UG': [total_strength_ug],
        'Total Strength PG': [total_strength_pg],
        'Total Same State Strength UG': [total_same_state_strength_ug],
        'Total Same State Strength PG': [total_same_state_strength_pg],
        'Total Different State Strength UG': [total_different_state_strength_ug],
        'Total Different State Strength PG': [total_different_state_strength_pg],
        'Total Different Country Strength UG': [total_different_country_strength_ug],
        'Total Different Country Strength PG': [total_different_country_strength_pg],
        'Total Economically Backward Strength UG': [total_economically_backward_strength_ug],
        'Total Economically Backward Strength PG': [total_economically_backward_strength_pg],
        'Total Socially Challenged Strength UG': [total_socially_challenged_strength_ug],
        'Total Socially Challenged Strength PG': [total_socially_challenged_strength_pg],
        'Total Tuition Fee Reimbursed from govt UG': [total_tuition_fee_strength_ug_from_govt],
        'Total Tuition Fee Reimbursed from govt PG': [total_tuition_fee_strength_pg_from_govt],
        'Total Tuition Fee Reimbursed from Institute Funds UG': [total_tuition_fee_strength_ug_from_institute],
        'Total Tuition Fee Reimbursed from Institute Funds PG': [total_tuition_fee_strength_pg_from_institute],
        'Total Tuition Fee Reimbursed from Private Bodies UG': [total_tuition_fee_strength_ug_from_private],
        'Total Tuition Fee Reimbursed from Private Bodies PG': [total_tuition_fee_strength_pg_from_private],
        'Students who are not receiving full tuition fee reimbursement UG': [no_tuition_fee_strength_ug],
        'Students who are not receiving full tuition fee reimbursement PG': [no_tuition_fee_strength_pg]
    })

    return strength_df  # Return the DataFrame to be used in main()

if __name__ == "__main__":
    main()
