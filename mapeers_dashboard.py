import streamlit as st
import pandas as pd
import os
import random
from datetime import datetime, timedelta
import plotly.express as px
import plotly.graph_objects as go

# ========== PAGE CONFIGURATION ==========
st.set_page_config(
    page_title="MaPeers Dashboard",
    page_icon="⚕️",
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
    </style>
""", unsafe_allow_html=True)

# ========== FILE PATH HELPER ==========
def get_file_path(filename):
    """Get correct file path whether running locally or on Streamlit Cloud"""
    if os.path.exists(filename):
        return filename
    for root, dirs, files in os.walk('.'):
        if filename in files:
            return os.path.join(root, filename)
    return None

# ========== CREATE SAMPLE DATA IF NEEDED ==========
def create_sample_appointments():
    """Create sample appointment data with dates from Nov 2025 to April 2026"""
    start_date = datetime(2025, 11, 1)
    end_date = datetime(2026, 4, 30)
    
    sample_data = []
    first_names = [
        "Idorenyin", "Mfoniso", "Iniobong", "Aniedi", "Ubong", "Nsikak", "Ime", "Emem", "Usoro", "Abasifreke",
        "Udeme", "Ifiok", "Imeobong", "Mfon", "Unyime", "Imaobong", "Ekaette", "Ngozi", "Uduak", "Nneka",
        "Iquo", "Aniekeme", "Ima", "Ekaete", "Udodirim", "Abasi", "Iboro", "Ufomba", "Emediong", "Mfonobong"
    ]
    
    last_names = ["John", "Jane", "Mike", "Sarah", "David", "Lisa", "Paul", "Mary", "James", "Patricia"]
    facilities = ["GWIHR Clinic", "General Hospital", "Care Center", "Unity Health Center", "Mercy Hospital"]
    statuses = ["Scheduled", "Pending", "Completed", "Cancelled"]
    genders = ["Male", "Female"]
    marital_statuses = ["Single", "Married", "Divorced"]
    services = ["HIV Testing", "Consultation", "Medication Refill", "Counseling", "Lab Test"]
    scheduled_by_list = ["Dr. Emeka", "Nurse Grace", "Dr. Chinasa", "Dr. Okon", "Nurse Blessing"]
    
    for i in range(100):  # Create 100 sample appointments
        random_days = random.randint(0, (end_date - start_date).days)
        appointment_date = start_date + timedelta(days=random_days)
        
        first_name = random.choice(first_names)
        last_name = random.choice(last_names)
        full_name = f"{first_name} {last_name}"
        
        sample_data.append({
            'S/N': i + 1,
            'USER_NAME': full_name,
            'Phone_Number': f"080{random.randint(10000000, 99999999)}",
            'AGE': random.randint(15, 24),
            'FACILITY': random.choice(facilities),
            'FACILITY_ADDRESS': f"{random.randint(1, 999)} Health Street, Uyo",
            'SCHEDULED_BY': random.choice(scheduled_by_list),
            'GENDER': random.choice(genders),
            'MARITAL_STATUS': random.choice(marital_statuses),
            'SERVICES_NEEDED': random.choice(services),
            'APPOINTMENT_DATE': appointment_date.strftime('%Y-%m-%d'),
            'APPOINTMENT STATUS': random.choice(statuses)
        })
    
    df = pd.DataFrame(sample_data)
    df.to_excel("MaPeer_Appointments.xlsx", index=False)
    return df

# ========== LOAD APPOINTMENTS ==========
@st.cache_data
def load_appointments():
    """Load appointments from Excel file, create sample if not exists"""
    file_path = get_file_path("MaPeer_Appointments.xlsx")
    
    if file_path is None:
        st.info("📝 Creating sample appointment data with dates from Nov 2025 - April 2026...")
        df = create_sample_appointments()
        return df, None
    
    try:
        df = pd.read_excel(file_path, engine='openpyxl')
        df = df.fillna('')
        
        # Convert APPOINTMENT_DATE to datetime
        if 'APPOINTMENT_DATE' in df.columns:
            df['APPOINTMENT_DATE'] = pd.to_datetime(df['APPOINTMENT_DATE'], errors='coerce')
        else:
            for col in df.columns:
                if 'date' in str(col).lower():
                    df[col] = pd.to_datetime(df[col], errors='coerce')
                    break
        
        return df, None
    except Exception as e:
        return None, str(e)

@st.cache_data
def load_users_from_csv():
    """Load users from CSV if exists"""
    csv_path = get_file_path("db_mapeers.csv")
    
    if csv_path is None:
        sample_users = pd.DataFrame({
            'name': ['Idorenyin John', 'Mfoniso Jane', 'Iniobong Mike', 'Aniedi Sarah', 'Ubong David'],
            'email': ['idorenyin@example.com', 'mfoniso@example.com', 'iniobong@example.com', 'aniedi@example.com', 'ubong@example.com'],
            'phone': ['08012345678', '08087654321', '08011223344', '08099887766', '08055667788']
        })
        return sample_users, None
    
    try:
        df = pd.read_csv(csv_path)
        df = df.fillna('')
        return df, None
    except Exception as e:
        return None, str(e)

@st.cache_data
def load_notifications():
    """Load notifications from Excel if exists"""
    file_path = get_file_path("notifications.xlsx")
    
    if file_path is None:
        return None, "No notifications file found"
    
    try:
        df = pd.read_excel(file_path, engine='openpyxl')
        df = df.fillna('')
        return df, None
    except Exception as e:
        return None, str(e)

# ========== LOAD ALL DATA ==========
appointments_df, apt_error = load_appointments()
users_df, users_error = load_users_from_csv()
notifications_df, notif_error = load_notifications()

# ========== PROCESS APPOINTMENTS BY STATUS ==========
scheduled_appointments = pd.DataFrame()
pending_appointments = pd.DataFrame()
completed_appointments = pd.DataFrame()
cancelled_appointments = pd.DataFrame()
all_appointments = pd.DataFrame()

status_column = None
date_column = None

if appointments_df is not None and not appointments_df.empty:
    all_appointments = appointments_df.copy()
    
    for col in all_appointments.columns:
        if 'status' in str(col).lower():
            status_column = col
            break
    
    for col in all_appointments.columns:
        if 'date' in str(col).lower():
            date_column = col
            break
    
    if status_column:
        status_series = all_appointments[status_column].astype(str).str.strip()
        
        scheduled_appointments = all_appointments[status_series == 'Scheduled']
        if len(scheduled_appointments) == 0:
            scheduled_appointments = all_appointments[status_series.str.lower() == 'scheduled']
        
        pending_appointments = all_appointments[status_series == 'Pending']
        if len(pending_appointments) == 0:
            pending_appointments = all_appointments[status_series.str.lower() == 'pending']
        
        completed_appointments = all_appointments[status_series == 'Completed']
        if len(completed_appointments) == 0:
            completed_appointments = all_appointments[status_series.str.lower() == 'completed']
        
        cancelled_appointments = all_appointments[status_series == 'Cancelled']
        if len(cancelled_appointments) == 0:
            cancelled_appointments = all_appointments[status_series.str.lower() == 'cancelled']
        
        st.sidebar.success(f"✅ Status Column: '{status_column}'")
        st.sidebar.write(f"📊 Total Appointments: {len(all_appointments)}")
    else:
        st.sidebar.warning("⚠️ No status column found")
else:
    st.sidebar.error("❌ Could not load appointments")

# ========== MERGE USERS ==========
def get_merged_users():
    all_users = {}
    
    if users_df is not None and not users_df.empty:
        for idx, user in users_df.iterrows():
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
    
    if appointments_df is not None and not appointments_df.empty and status_column:
        name_col = None
        for col in appointments_df.columns:
            if 'name' in str(col).lower() or 'user' in str(col).lower():
                name_col = col
                break
        
        if name_col:
            for idx, apt in appointments_df.iterrows():
                name = apt.get(name_col, '')
                if name and name != '' and name != 'nan':
                    key = str(name).strip().lower()
                    apt_status = apt.get(status_column, 'Unknown')
                    
                    if key in all_users:
                        all_users[key]['has_appointment'] = True
                        all_users[key]['appointment_status'] = apt_status
                        all_users[key]['source'] = 'Both'
                    else:
                        all_users[key] = {
                            'name': name,
                            'email': f"{name.lower().replace(' ', '.')}@mapeer.com",
                            'phone': apt.get('Phone_Number', '') if 'Phone_Number' in apt else '',
                            'source': 'Appointments Only',
                            'has_appointment': True,
                            'appointment_status': apt_status
                        }
    
    return pd.DataFrame(list(all_users.values())) if all_users else pd.DataFrame()

merged_users_df = get_merged_users()
total_users = len(merged_users_df)

# ========== HELPER FUNCTIONS ==========
def filter_by_date(df, year=None, month=None):
    if df.empty or date_column is None or date_column not in df.columns:
        return df
    
    filtered_df = df.copy()
    
    if not pd.api.types.is_datetime64_any_dtype(filtered_df[date_column]):
        filtered_df[date_column] = pd.to_datetime(filtered_df[date_column], errors='coerce')
    
    if year and year != "All" and year is not None:
        try:
            filtered_df = filtered_df[filtered_df[date_column].dt.year == int(year)]
        except:
            pass
    
    if month and month != "All" and month is not None:
        try:
            filtered_df = filtered_df[filtered_df[date_column].dt.month == int(month)]
        except:
            pass
    
    return filtered_df

def get_available_years(df):
    if df.empty or date_column is None or date_column not in df.columns:
        return ["All"]
    try:
        years = df[date_column].dt.year.dropna().unique()
        years = sorted([str(int(y)) for y in years if pd.notna(y)])
        return ["All"] + years if years else ["All"]
    except:
        return ["All"]

def get_available_months():
    return ["All", "1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "11", "12"]

def get_month_name(month_num):
    months = {"1": "January", "2": "February", "3": "March", "4": "April", "5": "May", "6": "June",
              "7": "July", "8": "August", "9": "September", "10": "October", "11": "November", "12": "December"}
    return months.get(str(month_num), "")

# ========== SIDEBAR ==========
with st.sidebar:
    st.markdown("### ⚕️ MaPeers Dashboard")
    st.markdown("---")
    st.markdown("### 📊 Navigation")
    
    menu_options = ["Dashboard", "Users", "Scheduled Appointments", "Pending Appointments", 
                   "Completed Appointments", "All Appointments", "Push Reminders"]
    
    if 'current_page' not in st.session_state:
        st.session_state.current_page = "Dashboard"
    
    for option in menu_options:
        if st.button(option, use_container_width=True, key=f"menu_{option}"):
            st.session_state.current_page = option
            st.rerun()
    
    st.markdown("---")
    st.markdown("### 📊 Data Summary")
    st.write(f"📊 Total Appointments: {len(all_appointments) if not all_appointments.empty else 0}")
    st.write(f"🟢 Scheduled: {len(scheduled_appointments)}")
    st.write(f"🟡 Pending: {len(pending_appointments)}")
    st.write(f"✅ Completed: {len(completed_appointments)}")
    st.write(f"👥 Total Users: {total_users}")

# ========== HEADER ==========
col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    st.markdown('<h1 class="main-header">⚕️ MaPeers Dashboard</h1>', unsafe_allow_html=True)

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
            <div class="stat-number">{len(all_appointments) if not all_appointments.empty else 0}</div>
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
                fig = px.pie(status_df, values='Count', names='Status', title="Status Distribution")
                st.plotly_chart(fig, use_container_width=True)

# ========== USERS PAGE ==========
elif st.session_state.current_page == "Users":
    st.markdown("### 👥 User Management")
    
    if merged_users_df.empty:
        st.info("No user data found")
    else:
        search = st.text_input("🔍 Search users", placeholder="Name or email...")
        filtered = merged_users_df.copy()
        if search:
            filtered = filtered[filtered['name'].str.contains(search, case=False, na=False)]
        st.write(f"**Showing {len(filtered)} of {len(merged_users_df)} users**")
        st.dataframe(filtered, use_container_width=True)

# ========== SCHEDULED APPOINTMENTS PAGE ==========
elif st.session_state.current_page == "Scheduled Appointments":
    st.markdown("### 🟢 Scheduled Appointments")
    if scheduled_appointments.empty:
        st.info("No scheduled appointments found.")
    else:
        st.metric("Total Scheduled", len(scheduled_appointments))
        st.markdown("---")
        st.dataframe(scheduled_appointments, use_container_width=True)

# ========== PENDING APPOINTMENTS PAGE ==========
elif st.session_state.current_page == "Pending Appointments":
    st.markdown("### 🟡 Pending Appointments")
    if pending_appointments.empty:
        st.info("No pending appointments found.")
    else:
        st.metric("Total Pending", len(pending_appointments))
        st.dataframe(pending_appointments, use_container_width=True)

# ========== COMPLETED APPOINTMENTS PAGE ==========
elif st.session_state.current_page == "Completed Appointments":
    st.markdown("### ✅ Completed Appointments")
    if completed_appointments.empty:
        st.info("No completed appointments found.")
    else:
        st.metric("Total Completed", len(completed_appointments))
        st.dataframe(completed_appointments, use_container_width=True)

# ========== ALL APPOINTMENTS PAGE ==========
elif st.session_state.current_page == "All Appointments":
    st.markdown("### 📅 All Appointments")
    if all_appointments.empty:
        st.warning("No appointments found.")
    else:
        st.dataframe(all_appointments, use_container_width=True)

# ========== PUSH REMINDERS PAGE ==========
elif st.session_state.current_page == "Push Reminders":
    st.markdown("### 🔔 Push Reminders")
    if notifications_df is None or notifications_df.empty:
        st.info("No notifications file found.")
    else:
        st.dataframe(notifications_df, use_container_width=True)

# ========== FOOTER ==========
st.markdown("---")
st.markdown(f"<div style='text-align: center; color: #888;'>MaPeers Dashboard | {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</div>", unsafe_allow_html=True)
