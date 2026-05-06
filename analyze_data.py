import pandas as pd

# Load the data (header=1 because row 2 contains sub-headers)

df = pd.read_excel('GWIHR NEPWHAN KOBOCLLECT DATA April 2026.xlsx', header=0)
print(df.columns.tolist())
# Load the Excel file
file_name = 'GWIHR NEPWHAN KOBOCLLECT DATA April 2026.xlsx'

# Load data - header=1 means use row 2 as column headers
df = pd.read_excel(file_name, header=0)

# Total records
print("=" * 60)
print(f"TOTAL RECORDS: {len(df)}")
print("=" * 60)

# Column AD - Data Collection Point_ Greater Women Initiative for Health & Right
print("\n--- COLUMN AD: Data Collection Point ---")
print(df['Data Collection Point_ Greater Women Initiative for Health & Right'].value_counts(dropna=False))

# Column BU - LGA
print("\n--- COLUMN BU: LGA ---")
lga_counts = df['LGA'].value_counts()
print(lga_counts)
print(f"\n✓ Bende LGA: {lga_counts.get('Bende', 0)}")

# Column BW - Target Population
print("\n--- COLUMN BW: Target Population ---")
print(df['Target Population'].value_counts(dropna=False))

# Column BY - What type of Facility did you receive HIV Treatment services?
print("\n--- COLUMN BY: Facility Type ---")
print(df['What type of Facility did you receive HIV Treatment services?'].value_counts(dropna=False))

# Column BZ - What is your Gender?
print("\n--- COLUMN BZ: Gender ---")
print(df['What is your Gender?'].value_counts(dropna=False))

# Column CD - What is your current occupation?
print("\n--- COLUMN CD: Current Occupation ---")
print(df['What is your current occupation?'].value_counts(dropna=False))

# Column CE - Marital Status
print("\n--- COLUMN CE: Marital Status ---")
print(df['Marital Status'].value_counts(dropna=False))


#section of Interpretation

# Load the Excel file

# Clean LGA column to standardize values
df['LGA'] = df['LGA'].str.strip()  # Remove leading/trailing spaces

print("=" * 80)
print("GWIHR NEPWHAN KOBOCLLECT DATA April 2026")
print("=" * 80)
print(f"\nTOTAL RECORDS: {len(df)}")
print(f"DATA COLLECTION PERIOD: {df['Reporting month'].value_counts().to_dict()}")
print(f"STATES: {df['STATE'].unique()}")
print("\n" + "=" * 80)

# ============================================================================
# SECTION 1: HIV, TB & MALARIA AWARENESS & PREVENTION
# ============================================================================
print("\n" + "=" * 80)
print("SECTION 1: HIV, TB & MALARIA AWARENESS & PREVENTION")
print("=" * 80)

# 1.1 General Awareness - Q1
print("\n--- Q1. Do you Know how to prevent HIV, TB, Malaria transmission? ---")
awareness = df['Q1. Do you Know how to prevent HIV,TB,Malaria transmission'].value_counts(dropna=False)
print(awareness)
awareness_rate = (awareness.get('Yes', 0) / len(df)) * 100
print(f"\n✓ Awareness Rate: {awareness_rate:.1f}% ({awareness.get('Yes', 0)} out of {len(df)})")

# 1.2 Services Uptake - Q2 (Multiple select columns)
print("\n--- Q2. HIV, TB & Malaria Services Uptake (Multiple responses) ---")
services = {
    'HIV, TB & Malaria Screening': df['Q2. Can you list Available HIV, TB and Malaria Service you uptake in this facility (Select all that applies)/HIV, TB & Malaria Screening'].sum(),
    'ART Enrollment and Care': df['Q2. Can you list Available HIV, TB and Malaria Service you uptake in this facility (Select all that applies)/ART Enrollment and Care'].sum(),
    'TB Treatment': df['Q2. Can you list Available HIV, TB and Malaria Service you uptake in this facility (Select all that applies)/TB Treatment'].sum(),
    'Malaria Treatment': df['Q2. Can you list Available HIV, TB and Malaria Service you uptake in this facility (Select all that applies)/Malaria Treatment'].sum(),
    'STI Screening and treatment': df['Q2. Can you list Available HIV, TB and Malaria Service you uptake in this facility (Select all that applies)/STI Screening and treatment'].sum(),
}

for service, count in sorted(services.items(), key=lambda x: x[1], reverse=True):
    percentage = (count / len(df)) * 100
    print(f"  {service}: {count} ({percentage:.1f}%)")

# 1.3 Community Health Education Participation
print("\n--- Q3. Participated in Community-led health education sessions (last 3-6 months) ---")
education = df['Q3. Have you participated in any Community-led health education sessions conducted HIV, TB, and Malaria prevention and treatment in the last 3-6 months'].value_counts(dropna=False)
print(education)
education_rate = (education.get('Yes', 0) / len(df)) * 100
print(f"\n✓ Participation Rate: {education_rate:.1f}%")

# 1.4 Knowledge of Treatment Regimen
print("\n--- Q4. Do you have Good Knowledge of your Treatment Regimen? ---")
knowledge = df['4. Do you have Good Knowledge of your Treatment Regimen for HIV/TB/ Malaria?'].value_counts(dropna=False)
print(knowledge)
knowledge_rate = (knowledge.get('Yes', 0) / len(df)) * 100
print(f"\n✓ Knowledge Rate: {knowledge_rate:.1f}%")

# 1.5 TB Screening
print("\n--- Q5. Screened for TB in the last 3 months? ---")
tb_screened = df['Q5. Have you been screened for TB in the last 3 months?'].value_counts(dropna=False)
print(tb_screened)
tb_rate = (tb_screened.get('Yes', 0) / len(df)) * 100
print(f"\n✓ TB Screening Rate: {tb_rate:.1f}%")

# TB Screening Outcomes
print("\n--- TB Screening Outcomes ---")
tb_outcome = df['If yes to Q5, what was the outcome of the TB Screening'].value_counts(dropna=False)
print(tb_outcome)

# 1.6 Malaria Testing
print("\n--- Q6. Tested for Malaria in the last 3 months? ---")
malaria_tested = df['Q6. Have you been tested for Malaria in the last 3 months?'].value_counts(dropna=False)
print(malaria_tested)
malaria_rate = (malaria_tested.get('Yes', 0) / len(df)) * 100
print(f"\n✓ Malaria Testing Rate: {malaria_rate:.1f}%")

# Malaria Test Outcomes
print("\n--- Malaria Test Outcomes ---")
malaria_outcome = df['If yes to Q6, what was the outcome of the Malaria test'].value_counts(dropna=False)
print(malaria_outcome)

# 1.7 Mosquito Net Awareness
print("\n--- Q7. Aware of treated Mosquito Net use? ---")
mosquito_net = df['Q7. Are you aware of the use of treated Mosquito Net'].value_counts(dropna=False)
print(mosquito_net)
net_awareness = (mosquito_net.get('Yes', 0) / len(df)) * 100
print(f"\n✓ Mosquito Net Awareness: {net_awareness:.1f}%")

# 1.8 PrEP Awareness and Access
print("\n--- Q8. Aware of PrEP? ---")
prep_aware = df['Q8. Are you aware of the use of PrEP'].value_counts(dropna=False)
print(prep_aware)
prep_aware_rate = (prep_aware.get('Yes', 0) / len(df)) * 100
print(f"\n✓ PrEP Awareness: {prep_aware_rate:.1f}%")

print("\n--- Assessing PrEP Services in your facility? ---")
prep_access = df['Are you assessing PrEP Services in your facility'].value_counts(dropna=False)
print(prep_access)

# 1.9 STI Prevention Awareness and Screening
print("\n--- Q10. Aware of STI Prevention? ---")
sti_aware = df['Q10. Are you aware of STI Prevention'].value_counts(dropna=False)
print(sti_aware)
sti_aware_rate = (sti_aware.get('Yes', 0) / len(df)) * 100
print(f"\n✓ STI Awareness: {sti_aware_rate:.1f}%")

print("\n--- Screened for STI in the last 3 months? ---")
sti_screened = df['Have you been screened STI in the last 3 months'].value_counts(dropna=False)
print(sti_screened)

# 1.10 Viral Hepatitis Awareness and Testing
print("\n--- Q12. Counseled, screened, and tested for Viral Hepatitis? ---")
hep_screened = df['Q12. Have you been Counseled screened and tested for Viral Hepatitis'].value_counts(dropna=False)
print(hep_screened)

print("\n--- Hepatitis B Vaccination Received? ---")
hep_vaccine = df['Have you received Hepatitis B Vaccination'].value_counts(dropna=False)
print(hep_vaccine)

# ============================================================================
# SECTION 2: AVAILABILITY OF DRUGS/COMMODITIES
# ============================================================================
print("\n" + "=" * 80)
print("SECTION 2: AVAILABILITY OF DRUGS/COMMODITIES")
print("=" * 80)

# 2.1 Condom Availability
print("\n--- Condom Availability (Last 2 months) ---")
condom_avail = df["Q1. Has there been any day in the last 2 months that you requested for Condom and it wasn't available?"].value_counts(dropna=False)
print(condom_avail)
if condom_avail.get('Yes', 0) > 0:
    print(f"⚠️ Stockout Rate: {(condom_avail.get('Yes', 0) / len(df)) * 100:.1f}%")

# 2.2 PrEP Availability
print("\n--- PrEP Availability (Last 2 months) ---")
prep_avail = df["Q2. Has there been any day in the last 2 months that you requested for PrEP and it wasn't available?"].value_counts(dropna=False)
print(prep_avail)
if prep_avail.get('Yes', 0) > 0:
    print(f"⚠️ PrEP Stockout Rate: {(prep_avail.get('Yes', 0) / len(df)) * 100:.1f}%")

# 2.3 ARV Availability
print("\n--- ARV Availability (Last 2 months) ---")
arv_avail = df["Q3. Has there been any day in the last 2 months that you requested for ARV and it wasn’t available?"].value_counts(dropna=False)
print(arv_avail)
if arv_avail.get('Yes', 0) > 0:
    print(f"⚠️ ARV Stockout Rate: {(arv_avail.get('Yes', 0) / len(df)) * 100:.1f}%")

# ARV that were not available
print("\n--- ARVs Not Available ---")
arv_unavail = df['If yes to Q3, what is the name of the ARV that was not available?'].value_counts(dropna=False)
print(arv_unavail)

# 2.4 TB Drug Availability
print("\n--- TB Drug Availability (Last 2 months) ---")
tb_drug_avail = df["q4. Has there been any day in the last 2 months that you requested for TB Drugs  and it wasn't available?"].value_counts(dropna=False)
print(tb_drug_avail)
if tb_drug_avail.get('Yes', 0) > 0:
    print(f"⚠️ TB Drug Stockout Rate: {(tb_drug_avail.get('Yes', 0) / len(df)) * 100:.1f}%")

print("\n--- TB Drugs Not Available ---")
tb_drug_unavail = df['What is the name of the TB Drug that was not available?'].value_counts(dropna=False)
print(tb_drug_unavail)

# 2.5 Malaria Drug Availability
print("\n--- Malaria Drug Availability (Last 2 months) ---")
malaria_drug_avail = df["q5. Has there been any day in the last 2 months that you requested for Malaria Drugs  and it wasn't available?"].value_counts(dropna=False)
print(malaria_drug_avail)
if malaria_drug_avail.get('Yes', 0) > 0:
    print(f"⚠️ Malaria Drug Stockout Rate: {(malaria_drug_avail.get('Yes', 0) / len(df)) * 100:.1f}%")

print("\n--- Malaria Drugs Not Available ---")
malaria_drug_unavail = df['What is the name of the Malaria Drug that was not available?'].value_counts(dropna=False)
print(malaria_drug_unavail)

# 2.6 Needle and Syringe Availability
print("\n--- Needle and Syringe Availability (Last 2 months) ---")
needle_avail = df["Q7. Has there been any day in the last 2 months that you requested for Needle and Syringe and it wasn’t available?"].value_counts(dropna=False)
print(needle_avail)
if needle_avail.get('Yes', 0) > 0:
    print(f"⚠️ Needle/Syringe Stockout Rate: {(needle_avail.get('Yes', 0) / len(df)) * 100:.1f}%")

# 2.7 Mosquito Net Access
print("\n--- Q6. Do you have access to Treated Mosquito Net? ---")
net_access = df['Q6. Do you have access to Treated Mosquito Net? '].value_counts(dropna=False)
print(net_access)

# ============================================================================
# SECTION 3: HUMAN RIGHTS
# ============================================================================
print("\n" + "=" * 80)
print("SECTION 3: HUMAN RIGHTS")
print("=" * 80)

# 3.1 Discrimination by Healthcare Worker
print("\n--- Discrimination by Healthcare Worker ---")
discrimination_hcw = df['Have you experienced discrimination by any healthcare worker in your facility?'].value_counts(dropna=False)
print(discrimination_hcw)
discrimination_rate = (discrimination_hcw.get('Yes', 0) / len(df)) * 100
print(f"\n⚠️ Discrimination Rate by HCW: {discrimination_rate:.1f}%")

print("\n--- Healthcare Workers Who Discriminated ---")
hcw_names = df['What is the name and the designation of the healthcare worker'].value_counts(dropna=False)
print(hcw_names.head(10))

print("\n--- Discrimination Reported to Management? ---")
discrimination_reported = df['Did you report the case to hospital management or your support group leader'].value_counts(dropna=False)
print(discrimination_reported)
report_rate = (discrimination_reported.get('Yes', 0) / max(discrimination_hcw.get('Yes', 1), 1)) * 100
print(f"\n✓ Reporting Rate among those who experienced discrimination: {report_rate:.1f}%")

# 3.2 Discrimination by Family/Friends/Community
print("\n--- Discrimination by Family/Friends/Community Members ---")
discrimination_community = df['Have you experienced discrimination by Family/friends or community members?'].value_counts(dropna=False)
print(discrimination_community)
comm_discrimination_rate = (discrimination_community.get('Yes', 0) / len(df)) * 100
print(f"\n⚠️ Discrimination Rate by Family/Community: {comm_discrimination_rate:.1f}%")

print("\n--- Who Discriminated? ---")
discriminator = df['If yes, who is the person'].value_counts(dropna=False)
print(discriminator)

print("\n--- Discrimination Reported to Anyone? ---")
discrimination_reported_state = df['Did you report the case to  anyone in your State'].value_counts(dropna=False)
print(discrimination_reported_state)

# 3.3 Status Disclosure Without Consent
print("\n--- Status Disclosure Without Consent ---")
disclosure = df['Have you ever experienced status disclosure without personal content?'].value_counts(dropna=False)
print(disclosure)
disclosure_rate = (disclosure.get('Yes', 0) / len(df)) * 100
print(f"\n⚠️ Involuntary Disclosure Rate: {disclosure_rate:.1f}%")

print("\n--- Who Disclosed Status Without Consent? ---")
discloser = df['Who disclosed your Status without your consent?'].value_counts(dropna=False)
print(discloser)

# 3.4 Testing Without Consent
print("\n--- Tested Without Consent ---")
tested_no_consent = df['Have you ever been tested without your consent?'].value_counts(dropna=False)
print(tested_no_consent)
no_consent_rate = (tested_no_consent.get('Yes', 0) / len(df)) * 100
print(f"\n⚠️ Testing Without Consent Rate: {no_consent_rate:.1f}%")

print("\n--- Who Tested Without Consent? ---")
tester = df['Who tested you without your consent?'].value_counts(dropna=False)
print(tester)

# 3.5 Access to Legal Services
print("\n--- Access to Legal Services ---")
legal_access = df['Do you have assess to legal services in your community or support group?'].value_counts(dropna=False)
print(legal_access)
legal_access_rate = (legal_access.get('Yes', 0) / len(df)) * 100
print(f"\n✓ Access to Legal Services: {legal_access_rate:.1f}%")

# 3.6 Access to Mental Health Services
print("\n--- Access to Mental Health Services ---")
mental_health = df['Do you have assess any mental health services in your facility or community?'].value_counts(dropna=False)
print(mental_health)
mental_health_rate = (mental_health.get('Yes', 0) / len(df)) * 100
print(f"\n✓ Access to Mental Health Services: {mental_health_rate:.1f}%")

# ============================================================================
# SECTION 4: SERVICE QUALITY INDICATORS
# ============================================================================
print("\n" + "=" * 80)
print("SECTION 4: SERVICE QUALITY INDICATORS")
print("=" * 80)

# 4.1 Waiting Time
print("\n--- Average Waiting Time at Facility ---")
waiting_time = df['What is the average waiting time for service provision at the facility? (Probe to know how long it took the client/patient before seeing the doctor after their arrival to the health facility)'].value_counts(dropna=False)
print(waiting_time)

# 4.2 Health Worker Attitude
print("\n--- Health Worker Attitude ---")
attitude = df['How would you describe the attitude of the health workers? (Probe to know the health worker’s attitudes towards the client/patient especially the way health worker(s) behaved, spoke, and reacted towards the patients)'].value_counts(dropna=False)
print(attitude)

# 4.3 Service Quality Assessment
print("\n--- Service Quality Assessment ---")
quality = df['How do you assess the quality of the service (s) received today in this health facility? (Explore to know if the client/patient’s health needs were met as expected by the health worker(s) at the health facility)'].value_counts(dropna=False)
print(quality)

satisfaction_rate = ((quality.get('Satisfied', 0) + quality.get('Very Satisfied', 0)) / len(df)) * 100
print(f"\n✓ Overall Satisfaction Rate: {satisfaction_rate:.1f}%")

# 4.4 Reasons for Dissatisfaction
print("\n--- Reasons for Dissatisfaction ---")
dissatisfaction_reasons = df['If Not Satisfied, kindly state the reason for the dissatisfaction'].value_counts(dropna=False)
print(dissatisfaction_reasons)

# 4.5 Staffing Adequacy
print("\n--- Facility has enough health workers? ---")
staffing = df['Do you think the facility has enough health workers to deliver timely and quality service to clients?'].value_counts(dropna=False)
print(staffing)

# 4.6 Staff Recommendations
print("\n--- Health Workers Recommended to be Added ---")
staff_recommendations = {
    'Doctors': df['Which cadre of Health Worker will you recommend to be added or engaged (Select all that applies) Questions pops up when the respondent select “No” in Q11/Doctors'].sum(),
    'Nurses': df['Which cadre of Health Worker will you recommend to be added or engaged (Select all that applies) Questions pops up when the respondent select “No” in Q11/Nurses'].sum(),
    'Lap technicians': df['Which cadre of Health Worker will you recommend to be added or engaged (Select all that applies) Questions pops up when the respondent select “No” in Q11/Lap technicians'].sum(),
    'Cleaners': df['Which cadre of Health Worker will you recommend to be added or engaged (Select all that applies) Questions pops up when the respondent select “No” in Q11/Cleaners'].sum(),
    'Case managers': df['Which cadre of Health Worker will you recommend to be added or engaged (Select all that applies) Questions pops up when the respondent select “No” in Q11/Case managers'].sum(),
    'Mentor Mothers': df['Which cadre of Health Worker will you recommend to be added or engaged (Select all that applies) Questions pops up when the respondent select “No” in Q11/Mentor Mothers'].sum(),
}

for cadre, count in sorted(staff_recommendations.items(), key=lambda x: x[1], reverse=True):
    if count > 0:
        print(f"  {cadre}: {count}")

# ============================================================================
# SUMMARY TABLE
# ============================================================================
print("\n" + "=" * 80)
print("KEY INDICATORS SUMMARY")
print("=" * 80)

summary_data = {
    "Indicator": [
        "HIV/TB/Malaria Prevention Awareness",
        "Community Health Education Participation",
        "Knowledge of Treatment Regimen",
        "TB Screening Rate (last 3 months)",
        "Malaria Testing Rate (last 3 months)",
        "Mosquito Net Awareness",
        "PrEP Awareness",
        "STI Prevention Awareness",
        "Hepatitis Screening",
        "Condom Stockout Rate",
        "PrEP Stockout Rate",
        "ARV Stockout Rate",
        "TB Drug Stockout Rate",
        "Malaria Drug Stockout Rate",
        "Discrimination by Healthcare Workers",
        "Discrimination by Family/Community",
        "Involuntary Status Disclosure",
        "Testing Without Consent",
        "Access to Legal Services",
        "Access to Mental Health Services",
        "Overall Service Satisfaction"
    ],
    "Rate (%)": [
        f"{awareness_rate:.1f}%",
        f"{education_rate:.1f}%",
        f"{knowledge_rate:.1f}%",
        f"{tb_rate:.1f}%",
        f"{malaria_rate:.1f}%",
        f"{net_awareness:.1f}%",
        f"{prep_aware_rate:.1f}%",
        f"{sti_aware_rate:.1f}%",
        f"{(hep_screened.get('Yes', 0) / len(df)) * 100:.1f}%",
        f"{(condom_avail.get('Yes', 0) / len(df)) * 100:.1f}%",
        f"{(prep_avail.get('Yes', 0) / len(df)) * 100:.1f}%",
        f"{(arv_avail.get('Yes', 0) / len(df)) * 100:.1f}%",
        f"{(tb_drug_avail.get('Yes', 0) / len(df)) * 100:.1f}%",
        f"{(malaria_drug_avail.get('Yes', 0) / len(df)) * 100:.1f}%",
        f"{discrimination_rate:.1f}%",
        f"{comm_discrimination_rate:.1f}%",
        f"{disclosure_rate:.1f}%",
        f"{no_consent_rate:.1f}%",
        f"{legal_access_rate:.1f}%",
        f"{mental_health_rate:.1f}%",
        f"{satisfaction_rate:.1f}%"
    ]
}

summary_df = pd.DataFrame(summary_data)
print(summary_df.to_string(index=False))

print("\n" + "=" * 80)
print("END OF ANALYSIS")
print("=" * 80)