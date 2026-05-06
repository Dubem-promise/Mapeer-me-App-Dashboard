import streamlit as st
import pandas as pd
import os
from datetime import datetime
import plotly.express as px
import plotly.graph_objects as go

# ========== PAGE CONFIGURATION ==========
st.set_page_config(
    page_title="MaPeers Dashboard",
    page_icon="logo.png" if os.path.exists("logo.png") else "⚕️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ========== CUSTOM CSS ==========
st.markdown("""
    <style>
    .main-header {
        font-size: 2rem;
        font-weight: 700;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin: 0;
        display: inline-block;
        margin-left: 15px;
    }
    .stat-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 1.2rem;
        border-radius: 15px;
        text-align: center;
        color: white;
        box-shadow: 0 4px 15px rgba(0,0,0,0.1);
    }
    .stat-number {
        font-size: 2rem;
        font-weight: 700;
    }
    .stat-label {
        font-size: 0.85rem;
        opacity: 0.9;
    }
    .filter-container {
        background: #f8f9fa;
        padding: 1rem;
        border-radius: 12px;
        margin-bottom: 1rem;
    }
    .data-table-container {
        background: white;
        border-radius: 12px;
        padding: 1rem;
        box-shadow: 0 2px 8px rgba(0,0,0,0.05);
        overflow-x: auto;
    }
    </style>
""", unsafe_allow_html=True)

# ========== CSV PARSING FUNCTIONS ==========
def smart_csv_parse(file_path):
    """Parse the multi-table CSV file"""
    with open(file_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    
    tables = {}
    current_table = []
    current_headers = None
    
    for line in lines:
        line = line.strip()
        if not line:
            continue
        
        if line.startswith('"id","') and line.count('","') >= 2:
            if current_headers and current_table:
                df = parse_table_data(current_headers, current_table)
                if df is not None and not df.empty:
                    table_name = identify_table(df)
                    tables[table_name] = df
            
            current_headers = parse_csv_line(line)
            current_table = []
        else:
            current_table.append(line)
    
    if current_headers and current_table:
        df = parse_table_data(current_headers, current_table)
        if df is not None and not df.empty:
            table_name = identify_table(df)
            tables[table_name] = df
    
    return tables

def parse_csv_line(line):
    """Parse CSV line into fields"""
    fields = []
    current = ''
    in_quotes = False
    
    for char in line:
        if char == '"':
            in_quotes = not in_quotes
        elif char == ',' and not in_quotes:
            fields.append(current.strip('"').strip())
            current = ''
        else:
            current += char
    fields.append(current.strip('"').strip())
    
    return fields

def parse_table_data(headers, data_lines):
    """Parse table data rows into DataFrame"""
    rows = []
    for line in data_lines:
        if line.strip():
            values = parse_csv_line(line)
            if len(values) == len(headers):
                rows.append(values)
    
    if rows:
        return pd.DataFrame(rows, columns=headers)
    return None

def identify_table(df):
    """Identify table type based on columns"""
    cols = [c.lower() for c in df.columns]
    
    if 'email' in cols and 'password' in cols and 'name' in cols:
        return 'users'
    elif 'token' in cols:
        return 'fcm_tokens'
    elif 'report_name' in cols:
        return 'sos_reports'
    else:
        return f'table_{len(df.columns)}'

def load_mapeer_appointments():
    """Load appointments from MaPeer Appointments.xlsx"""
    file_path = "MaPeer Appointments.xlsx"
    try:
        if not os.path.exists(file_path):
            # Create sample with various dates and statuses
            sample_df = pd.DataFrame({
                'S/N': [1, 2, 3, 4, 5, 6],
                'USER NAME': ['John Doe', 'Jane Smith', 'Mike Johnson', 'Sarah Williams', 'David Brown', 'Lisa Wong'],
                'Phone-Number': ['08012345678', '08087654321', '08011223344', '08099887766', '08055667788', '08044556677'],
                'AGE': [28, 32, 25, 35, 42, 29],
                'FACILITY': ['GWIHR Clinic', 'General Hospital', 'Care Center', 'GWIHR Clinic', 'General Hospital', 'Care Center'],
                'FACILITY_ADDRESS': ['123 Health Way', '456 Hospital Road', '789 Care Street', '123 Health Way', '456 Hospital Road', '789 Care Street'],
                'SCHEDULED_BY': ['Dr. Emeka', 'Nurse Grace', 'Dr. Chinasa', 'Dr. Emeka', 'Nurse Grace', 'Dr. Chinasa'],
                'GENDER': ['Male', 'Female', 'Male', 'Female', 'Male', 'Female'],
                'MARITAL_STATUS': ['Single', 'Married', 'Single', 'Married', 'Divorced', 'Single'],
                'SERVICES_NEEDED': ['HIV Testing', 'Consultation', 'Medication Refill', 'HIV Testing', 'Consultation', 'Counseling'],
                'APPOINTMENT_DATE': [
                    '2024-01-15', '2024-01-20', '2024-02-10', '2024-02-25', '2024-03-05', '2024-03-18'
                ],
                'APPOINTMENT STATUS': ['Completed', 'Pending', 'Scheduled', 'Completed', 'Scheduled', 'Completed']
            })
            sample_df.to_excel(file_path, index=False)
            st.info("Sample appointments file created. Please add your data and refresh.")
            return sample_df, None
        
        df = pd.read_excel(file_path)
        df = df.fillna('')
        
        # Convert APPOINTMENT_DATE to datetime if exists
        for col in df.columns:
            if 'date' in str(col).lower():
                df[col] = pd.to_datetime(df[col], errors='coerce')
                break
        
        return df, None
    except Exception as e:
        return None, str(e)

def load_notifications():
    """Load notifications from notifications.xlsx"""
    file_path = "notifications.xlsx"
    try:
        if not os.path.exists(file_path):
            return None, "File not found"
        df = pd.read_excel(file_path)
        df = df.fillna('')
        return df, None
    except Exception as e:
        return None, str(e)

# ========== LOAD DATA ==========
@st.cache_data
def load_all_data(csv_path='db_mapeers.csv'):
    """Load and parse all data from CSV"""
    if not os.path.exists(csv_path):
        return None, f"File not found: {csv_path}"
    
    try:
        tables = smart_csv_parse(csv_path)
        return tables, None
    except Exception as e:
        return None, str(e)

# Load data
tables, error = load_all_data()
excel_appointments, apt_error = load_mapeer_appointments()
notifications_df, notif_error = load_notifications()

# Extract CSV users
csv_users = tables.get('users', pd.DataFrame()) if tables else pd.DataFrame()

# ========== FIND COLUMNS ==========
# Find date column
date_column = None
if excel_appointments is not None and not excel_appointments.empty:
    for col in excel_appointments.columns:
        if 'date' in str(col).lower():
            date_column = col
            break

# Find status column - check multiple possible names
status_column = None
status_column_original = None
if excel_appointments is not None and not excel_appointments.empty:
    possible_status_names = ['APPOINTMENT STATUS', 'Appointment Status', 'appointment status', 'STATUS', 'Status', 'status']
    for col in excel_appointments.columns:
        if col in possible_status_names or str(col).lower() in ['appointment status', 'status']:
            status_column = col
            status_column_original = col
            break
    
    # If still not found, try any column with 'status' in name
    if status_column is None:
        for col in excel_appointments.columns:
            if 'status' in str(col).lower():
                status_column = col
                status_column_original = col
                break

# ========== PROCESS APPOINTMENTS BY STATUS ==========
# Initialize all DataFrames
scheduled_appointments = pd.DataFrame()
pending_appointments = pd.DataFrame()
completed_appointments = pd.DataFrame()
cancelled_appointments = pd.DataFrame()
all_appointments = pd.DataFrame()

if excel_appointments is not None and not excel_appointments.empty:
    all_appointments = excel_appointments.copy()
    
    if status_column:
        # Create a clean status series
        status_series = excel_appointments[status_column].astype(str).str.strip()
        
        # Match each status
        scheduled_appointments = excel_appointments[status_series == 'Scheduled']
        if len(scheduled_appointments) == 0:
            scheduled_appointments = excel_appointments[status_series.str.lower() == 'scheduled']
        
        pending_appointments = excel_appointments[status_series == 'Pending']
        if len(pending_appointments) == 0:
            pending_appointments = excel_appointments[status_series.str.lower() == 'pending']
        
        completed_appointments = excel_appointments[status_series == 'Completed']
        if len(completed_appointments) == 0:
            completed_appointments = excel_appointments[status_series.str.lower() == 'completed']
        
        cancelled_appointments = excel_appointments[status_series == 'Cancelled']
        if len(cancelled_appointments) == 0:
            cancelled_appointments = excel_appointments[status_series.str.lower() == 'cancelled']
        
        # Show debug info
        st.sidebar.success(f"✅ Status Column Found: '{status_column}'")
        st.sidebar.write(f"📊 Status Values: {excel_appointments[status_column].unique().tolist()}")
        st.sidebar.write(f"🟢 Scheduled: {len(scheduled_appointments)}")
        st.sidebar.write(f"✅ Completed: {len(completed_appointments)}")
        st.sidebar.write(f"🟡 Pending: {len(pending_appointments)}")
    else:
        st.sidebar.error("❌ No status column found in Excel file")
        st.sidebar.write("Available columns:", list(excel_appointments.columns))
else:
    st.sidebar.warning("No appointments data loaded")

# ========== MERGE USERS ==========
def get_merged_users():
    """Merge users from CSV and appointments"""
    all_users = {}
    
    if not csv_users.empty:
        for idx, user in csv_users.iterrows():
            name = user.get('name', '')
            if name and name != '' and name != 'nan':
                key = str(name).strip().lower()
                all_users[key] = {
                    'name': name,
                    'email': user.get('email', ''),
                    'phone': user.get('phone', ''),
                    'source': 'CSV Database',
                    'has_appointment': False,
                    'appointment_status': 'None'
                }
    
    if excel_appointments is not None and not excel_appointments.empty and status_column:
        name_col = None
        phone_col = None
        
        for col in excel_appointments.columns:
            col_lower = str(col).lower()
            if 'name' in col_lower or 'user' in col_lower:
                name_col = col
            if 'phone' in col_lower:
                phone_col = col
        
        if name_col:
            for idx, apt in excel_appointments.iterrows():
                name = apt.get(name_col, '')
                if name and name != '' and name != 'nan':
                    key = str(name).strip().lower()
                    apt_status = apt.get(status_column, 'Unknown')
                    
                    if key in all_users:
                        all_users[key]['has_appointment'] = True
                        all_users[key]['appointment_status'] = apt_status
                        all_users[key]['source'] = 'Both'
                        if phone_col and apt.get(phone_col):
                            all_users[key]['phone'] = apt.get(phone_col, '')
                    else:
                        all_users[key] = {
                            'name': name,
                            'email': f"{name.lower().replace(' ', '.')}@mapeer.com",
                            'phone': apt.get(phone_col, '') if phone_col else '',
                            'source': 'Appointments Only',
                            'has_appointment': True,
                            'appointment_status': apt_status
                        }
    
    return pd.DataFrame(list(all_users.values()))

merged_users_df = get_merged_users()
total_users = len(merged_users_df)
active_users = len(merged_users_df[merged_users_df['has_appointment'] == True]) if not merged_users_df.empty else 0

# ========== HELPER FUNCTIONS FOR DATE FILTERING ==========
def filter_by_date(df, year=None, month=None):
    """Filter dataframe by year and month based on date column"""
    if df.empty or date_column is None:
        return df
    
    filtered_df = df.copy()
    
    if date_column in filtered_df.columns:
        # Convert to datetime if not already
        if not pd.api.types.is_datetime64_any_dtype(filtered_df[date_column]):
            filtered_df[date_column] = pd.to_datetime(filtered_df[date_column], errors='coerce')
        
        # Filter by year
        if year and year != "All" and year is not None:
            try:
                filtered_df = filtered_df[filtered_df[date_column].dt.year == int(year)]
            except:
                pass
        
        # Filter by month
        if month and month != "All" and month is not None:
            try:
                filtered_df = filtered_df[filtered_df[date_column].dt.month == int(month)]
            except:
                pass
    
    return filtered_df

def get_available_years(df):
    """Get available years from date column"""
    if df.empty or date_column is None or date_column not in df.columns:
        return ["All"]
    
    try:
        years = df[date_column].dt.year.dropna().unique()
        years = sorted([str(int(y)) for y in years if pd.notna(y)])
        return ["All"] + years
    except:
        return ["All"]

def get_available_months():
    """Get list of months"""
    return ["All", "1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "11", "12"]

def get_month_name(month_num):
    """Convert month number to name"""
    months = {
        "1": "January", "2": "February", "3": "March", "4": "April",
        "5": "May", "6": "June", "7": "July", "8": "August",
        "9": "September", "10": "October", "11": "November", "12": "December"
    }
    return months.get(str(month_num), "")

# ========== SIDEBAR ==========
with st.sidebar:
    # Logo
    if os.path.exists("logo.png"):
        st.image("logo.png", width=120)
    else:
        st.markdown("### ⚕️ MaPeers")
    
    st.markdown("---")
    st.markdown("### 📊 Navigation")
    
    menu_options = ["Dashboard", "Users", "Scheduled Appointments", "Pending Appointments", "Completed Appointments", "All Appointments", "Push Reminders"]
    
    if 'current_page' not in st.session_state:
        st.session_state.current_page = "Dashboard"
    
    for option in menu_options:
        if st.button(option, use_container_width=True, key=f"menu_{option}"):
            st.session_state.current_page = option
            st.rerun()
    
    st.markdown("---")
    st.markdown("### 📊 Data Summary")
    st.write(f"📁 CSV Users: {len(csv_users)}")
    st.write(f"📊 Total Appointments: {len(excel_appointments) if excel_appointments is not None else 0}")
    st.write(f"🟢 Scheduled: {len(scheduled_appointments)}")
    st.write(f"🟡 Pending: {len(pending_appointments)}")
    st.write(f"✅ Completed: {len(completed_appointments)}")
    st.write(f"👥 Merged Users: {total_users}")

# ========== HEADER ==========
col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    logo_col, text_col = st.columns([1, 5])
    with logo_col:
        if os.path.exists("logo.png"):
            st.image("logo.png", width=60)
        else:
            st.markdown("### ⚕️")
    with text_col:
        st.markdown('<h1 class="main-header">MaPeers Dashboard</h1>', unsafe_allow_html=True)

# ========== DASHBOARD PAGE ==========
if st.session_state.current_page == "Dashboard":
    st.markdown("### 📈 Overview")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown(f"""
        <div class="stat-card">
            <div class="stat-number">{total_users}</div>
            <div class="stat-label">Total Users</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
        <div class="stat-card">
            <div class="stat-number">{len(excel_appointments) if excel_appointments is not None else 0}</div>
            <div class="stat-label">Total Appointments</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown(f"""
        <div class="stat-card">
            <div class="stat-number">{len(completed_appointments)}</div>
            <div class="stat-label">Completed</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        st.markdown(f"""
        <div class="stat-card">
            <div class="stat-number">{len(scheduled_appointments)}</div>
            <div class="stat-label">Scheduled</div>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Status Distribution Chart
    if status_column and not all_appointments.empty:
        st.markdown("### 📊 Appointment Status Distribution")
        
        status_counts = {
            'Scheduled': len(scheduled_appointments),
            'Pending': len(pending_appointments),
            'Completed': len(completed_appointments),
            'Cancelled': len(cancelled_appointments)
        }
        
        status_df = pd.DataFrame(list(status_counts.items()), columns=['Status', 'Count'])
        status_df = status_df[status_df['Count'] > 0]
        
        if not status_df.empty:
            col1, col2 = st.columns(2)
            with col1:
                fig = px.bar(status_df, x='Status', y='Count', title="Appointments by Status",
                            color='Status', color_discrete_sequence=['#17a2b8', '#ffc107', '#28a745', '#dc3545'])
                st.plotly_chart(fig, use_container_width=True)
            with col2:
                fig = px.pie(status_df, values='Count', names='Status', title="Status Distribution",
                            color_discrete_sequence=['#17a2b8', '#ffc107', '#28a745', '#dc3545'])
                st.plotly_chart(fig, use_container_width=True)

# ========== USERS PAGE ==========
elif st.session_state.current_page == "Users":
    st.markdown("### 👥 User Management")
    
    if merged_users_df.empty:
        st.info("No user data found")
    else:
        search = st.text_input("🔍 Search users", placeholder="Name or email...")
        status_filter = st.selectbox("Filter by Status", ["All", "Active", "Inactive"])
        
        filtered = merged_users_df.copy()
        if search:
            filtered = filtered[filtered['name'].str.contains(search, case=False, na=False)]
        if status_filter == "Active":
            filtered = filtered[filtered['has_appointment'] == True]
        elif status_filter == "Inactive":
            filtered = filtered[filtered['has_appointment'] == False]
        
        st.write(f"**Showing {len(filtered)} of {len(merged_users_df)} users**")
        st.dataframe(filtered, use_container_width=True)

# ========== SCHEDULED APPOINTMENTS PAGE ==========
elif st.session_state.current_page == "Scheduled Appointments":
    st.markdown("### 🟢 Scheduled Appointments")
    
    if scheduled_appointments.empty:
        st.info("No scheduled appointments found.")
        if status_column:
            st.write(f"Status column '{status_column}' contains: {all_appointments[status_column].unique().tolist() if not all_appointments.empty else 'No data'}")
    else:
        st.metric("Total Scheduled", len(scheduled_appointments))
        st.markdown("---")
        
        # Date Filter Section
        st.markdown("### 📅 Filter by Date")
        col1, col2 = st.columns(2)
        
        available_years = get_available_years(scheduled_appointments)
        with col1:
            selected_year = st.selectbox("Select Year", available_years, key="scheduled_year")
        
        with col2:
            selected_month = st.selectbox("Select Month", get_available_months(), key="scheduled_month", 
                                         format_func=lambda x: get_month_name(x) if x != "All" else "All")
        
        # Apply date filter
        filtered_appointments = filter_by_date(scheduled_appointments, selected_year, selected_month)
        
        st.write(f"**Showing {len(filtered_appointments)} scheduled appointments**")
        
        # Sort by date
        if date_column and not filtered_appointments.empty and date_column in filtered_appointments.columns:
            filtered_appointments = filtered_appointments.sort_values(date_column, ascending=True)
        
        # Display the data
        st.dataframe(filtered_appointments, use_container_width=True)

# ========== PENDING APPOINTMENTS PAGE ==========
elif st.session_state.current_page == "Pending Appointments":
    st.markdown("### 🟡 Pending Appointments")
    
    if pending_appointments.empty:
        st.info("No pending appointments found.")
    else:
        st.metric("Total Pending", len(pending_appointments))
        st.markdown("---")
        
        st.markdown("### 📅 Filter by Date")
        col1, col2 = st.columns(2)
        
        available_years = get_available_years(pending_appointments)
        with col1:
            selected_year = st.selectbox("Select Year", available_years, key="pending_year")
        
        with col2:
            selected_month = st.selectbox("Select Month", get_available_months(), key="pending_month",
                                         format_func=lambda x: get_month_name(x) if x != "All" else "All")
        
        filtered_appointments = filter_by_date(pending_appointments, selected_year, selected_month)
        
        st.write(f"**Showing {len(filtered_appointments)} pending appointments**")
        
        if date_column and not filtered_appointments.empty and date_column in filtered_appointments.columns:
            filtered_appointments = filtered_appointments.sort_values(date_column, ascending=True)
        
        st.dataframe(filtered_appointments, use_container_width=True)

# ========== COMPLETED APPOINTMENTS PAGE ==========
elif st.session_state.current_page == "Completed Appointments":
    st.markdown("### ✅ Completed Appointments")
    
    if completed_appointments.empty:
        st.info("No completed appointments found.")
        if status_column:
            st.write(f"Status column '{status_column}' contains: {all_appointments[status_column].unique().tolist() if not all_appointments.empty else 'No data'}")
    else:
        col1, col2 = st.columns(2)
        with col1:
            st.metric("Total Completed", len(completed_appointments))
        with col2:
            name_col = None
            for col in completed_appointments.columns:
                if 'name' in str(col).lower():
                    name_col = col
                    break
            unique_users = completed_appointments[name_col].nunique() if name_col else 0
            st.metric("Unique Users", unique_users)
        
        st.markdown("---")
        
        st.markdown("### 📅 Filter by Date")
        col1, col2 = st.columns(2)
        
        available_years = get_available_years(completed_appointments)
        with col1:
            selected_year = st.selectbox("Select Year", available_years, key="completed_year")
        
        with col2:
            selected_month = st.selectbox("Select Month", get_available_months(), key="completed_month",
                                         format_func=lambda x: get_month_name(x) if x != "All" else "All")
        
        filtered_appointments = filter_by_date(completed_appointments, selected_year, selected_month)
        
        st.write(f"**Showing {len(filtered_appointments)} completed appointments**")
        
        if date_column and not filtered_appointments.empty and date_column in filtered_appointments.columns:
            filtered_appointments = filtered_appointments.sort_values(date_column, ascending=True)
        
        st.dataframe(filtered_appointments, use_container_width=True)

# ========== ALL APPOINTMENTS PAGE ==========
elif st.session_state.current_page == "All Appointments":
    st.markdown("### 📅 All Appointments")
    
    if all_appointments.empty:
        st.warning("No appointments found.")
        st.info("Please make sure 'MaPeer Appointments.xlsx' exists in the same directory")
    else:
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("Total", len(all_appointments))
        with col2:
            st.metric("Scheduled", len(scheduled_appointments))
        with col3:
            st.metric("Pending", len(pending_appointments))
        with col4:
            st.metric("Completed", len(completed_appointments))
        
        st.markdown("---")
        
        # Date Filter Section
        st.markdown("### 📅 Filter by Date")
        col1, col2 = st.columns(2)
        
        available_years = get_available_years(all_appointments)
        with col1:
            selected_year = st.selectbox("Select Year", available_years, key="all_year")
        
        with col2:
            selected_month = st.selectbox("Select Month", get_available_months(), key="all_month",
                                         format_func=lambda x: get_month_name(x) if x != "All" else "All")
        
        # Status Filter
        status_options = ["All", "Scheduled", "Pending", "Completed", "Cancelled"]
        selected_status = st.selectbox("Filter by Status", status_options)
        
        # Show column info
        if status_column:
            st.info(f"📋 Status column: '{status_column}'")
        
        # Apply filters
        filtered = all_appointments.copy()
        filtered = filter_by_date(filtered, selected_year, selected_month)
        
        if selected_status != "All":
            if status_column:
                status_vals = filtered[status_column].astype(str).str.strip()
                filtered = filtered[status_vals == selected_status]
                if len(filtered) == 0:
                    filtered = filtered[status_vals.str.lower() == selected_status.lower()]
        
        # Search
        search = st.text_input("🔍 Search", placeholder="Search by name or phone...")
        if search:
            for col in filtered.columns:
                if 'name' in str(col).lower() or 'phone' in str(col).lower():
                    filtered = filtered[filtered[col].astype(str).str.contains(search, case=False, na=False)]
                    break
        
        st.write(f"**Showing {len(filtered)} appointments**")
        
        # Sort by date
        if date_column and not filtered.empty and date_column in filtered.columns:
            filtered = filtered.sort_values(date_column, ascending=True)
        
        st.dataframe(filtered, use_container_width=True)
        
        # Monthly Summary
        if date_column and not filtered.empty and date_column in filtered.columns:
            st.markdown("### 📊 Monthly Summary")
            filtered['Month'] = filtered[date_column].dt.strftime('%Y-%m')
            monthly_counts = filtered.groupby('Month').size().reset_index(name='Count')
            if not monthly_counts.empty:
                fig = px.bar(monthly_counts, x='Month', y='Count', title="Appointments by Month",
                            color_discrete_sequence=['#667eea'])
                st.plotly_chart(fig, use_container_width=True)

# ========== PUSH REMINDERS PAGE ==========
elif st.session_state.current_page == "Push Reminders":
    st.markdown("### 🔔 User Push Reminders")
    
    if notifications_df is None or notifications_df.empty:
        st.warning("No notifications file found.")
        
        if st.button("📝 Create Sample Template"):
            sample_df = pd.DataFrame({
                'date': [datetime.now().strftime('%Y-%m-%d')],
                'time': ['10:00 AM'],
                'message': ['Welcome to MaPeers! New health resources available.']
            })
            sample_df.to_excel('notifications.xlsx', index=False)
            st.success("Sample template created! Refresh the page.")
    else:
        st.success(f"✅ Loaded {len(notifications_df)} push reminders")
        
        search = st.text_input("🔍 Search reminders", placeholder="Search by message...")
        
        filtered = notifications_df.copy()
        if search:
            for col in filtered.columns:
                if 'message' in str(col).lower():
                    filtered = filtered[filtered[col].astype(str).str.contains(search, case=False, na=False)]
                    break
        
        st.write(f"**Showing {len(filtered)} reminders**")
        st.dataframe(filtered, use_container_width=True)

# ========== FOOTER ==========
st.markdown("---")
st.markdown(
    f"<div style='text-align: center; color: #888;'>MaPeers Dashboard | {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</div>",
    unsafe_allow_html=True
)