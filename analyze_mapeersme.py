import pandas as pd
import re
from datetime import datetime
import json

def analyze_mapeers_data(file_path):
    """
    Parse and analyze the multi-table CSV file from MaPeers database export
    """
    
    print("=" * 70)
    print("MAPEERS DATABASE ANALYSIS")
    print("=" * 70)
    
    # Read the entire file as text
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Split by the pattern that indicates a new table header
    # Table headers start with "id","name" or "id","token" etc.
    
    lines = content.split('\n')
    
    # Find all table start positions
    tables = []
    current_table = []
    current_header = None
    
    for line in lines:
        line = line.strip()
        if not line:
            continue
            
        # Check if this is a new table header
        is_header = False
        header_match = re.match(r'^"id","(\w+)"', line)
        if header_match:
            is_header = True
        
        if is_header and current_table:
            # Save previous table
            if current_header and current_table:
                tables.append({
                    'header': current_header,
                    'data': current_table
                })
            current_table = []
            current_header = line
        else:
            current_table.append(line)
    
    # Add the last table
    if current_header and current_table:
        tables.append({
            'header': current_header,
            'data': current_table
        })
    
    # Parse each table
    parsed_tables = {}
    
    for i, table in enumerate(tables):
        header = table['header']
        data_lines = table['data']
        
        # Parse header to get column names
        # Remove quotes and split
        header_clean = header.replace('"', '')
        columns = header_clean.split(',')
        
        # Parse data rows
        rows = []
        for line in data_lines:
            if not line.strip():
                continue
            
            # Parse CSV line (handling quoted fields)
            row = parse_csv_line(line)
            if len(row) == len(columns):
                rows.append(row)
            else:
                # Try to fix mismatched row length
                if len(row) < len(columns):
                    row.extend([''] * (len(columns) - len(row)))
                    rows.append(row)
                elif len(row) > len(columns):
                    rows.append(row[:len(columns)])
        
        if rows:
            df = pd.DataFrame(rows, columns=columns)
            # Store with a name based on columns
            table_name = identify_table_name(columns)
            parsed_tables[table_name] = df
            print(f"\n✓ Found table: {table_name} ({len(df)} rows, {len(columns)} columns)")
    
    return parsed_tables

def parse_csv_line(line):
    """Parse a CSV line handling quoted fields properly"""
    result = []
    current = ''
    in_quotes = False
    
    i = 0
    while i < len(line):
        char = line[i]
        
        if char == '"':
            if in_quotes and i + 1 < len(line) and line[i + 1] == '"':
                # Escaped quote
                current += '"'
                i += 1
            else:
                # Toggle quotes
                in_quotes = not in_quotes
        elif char == ',' and not in_quotes:
            # End of field
            result.append(current)
            current = ''
        else:
            current += char
        i += 1
    
    # Add last field
    result.append(current)
    
    # Remove surrounding quotes from each field
    result = [field.strip('"') for field in result]
    
    return result

def identify_table_name(columns):
    """Identify table name based on its columns"""
    
    table_patterns = {
        'users': ['email', 'password', 'avatar', 'fcm'],
        'admins': ['admin_id', 'role_id'],
        'appointments': ['appointment_date', 'health_expert_id', 'code', 'status'],
        'articles': ['category_id', 'video_link', 'body'],
        'categories': ['icon', 'status'],
        'health_experts': ['expert_title', 'expert_description', 'phone'],
        'sos_reports': ['report_name', 'value', 'resolved'],
        'sos_danger_types': ['description'],
        'fcm_tokens': ['token', 'last_used'],
        'migrations': ['migration', 'batch'],
        'sessions': ['payload', 'last_activity']
    }
    
    for table_name, pattern_cols in table_patterns.items():
        if any(col in columns for col in pattern_cols):
            return table_name
    
    # Default name based on first column
    if columns:
        return f"table_{columns[0]}"
    return "unknown_table"

def extract_users_table(tables):
    """Extract the main users table (the first one with name, email, password)"""
    
    for name, df in tables.items():
        # Look for the main users table (has password column and created_at)
        if 'password' in df.columns and 'created_at' in df.columns and 'email' in df.columns:
            return df
    return None

def extract_appointments_table(tables):
    """Extract appointments table"""
    
    for name, df in tables.items():
        if 'appointment_date' in df.columns and 'health_expert_id' in df.columns:
            return df
    return None

def extract_articles_table(tables):
    """Extract articles table"""
    
    for name, df in tables.items():
        if 'body' in df.columns and 'title' in df.columns and 'category_id' in df.columns:
            return df
    return None

def extract_categories_table(tables):
    """Extract categories table"""
    
    for name, df in tables.items():
        if 'icon' in df.columns and 'name' in df.columns:
            return df
    return None

def extract_health_experts_table(tables):
    """Extract health experts table"""
    
    for name, df in tables.items():
        if 'expert_title' in df.columns and 'phone' in df.columns:
            return df
    return None

def print_analysis_results(tables):
    """Print detailed analysis results"""
    
    print("\n" + "=" * 70)
    print("DETAILED ANALYSIS RESULTS")
    print("=" * 70)
    
    # 1. Users Table
    users_df = extract_users_table(tables)
    if users_df is not None and not users_df.empty:
        print(f"\n👥 USERS TABLE")
        print(f"   Total users: {len(users_df)}")
        print(f"   Columns: {', '.join(users_df.columns)}")
        print(f"\n   User list:")
        for idx, row in users_df.iterrows():
            user_id = row.get('id', 'N/A')
            name = row.get('name', 'N/A')
            email = row.get('email', 'N/A')
            created = row.get('created_at', 'N/A')
            print(f"     • ID {user_id}: {name} ({email}) - Joined: {created[:10] if created != 'N/A' else 'N/A'}")
    
    # 2. Appointments Table
    appointments_df = extract_appointments_table(tables)
    if appointments_df is not None and not appointments_df.empty:
        print(f"\n📅 APPOINTMENTS TABLE")
        print(f"   Total appointments: {len(appointments_df)}")
        
        if 'status' in appointments_df.columns:
            print(f"\n   Status breakdown:")
            for status, count in appointments_df['status'].value_counts().items():
                print(f"     • {status}: {count}")
        
        print(f"\n   Appointment list:")
        for idx, row in appointments_df.iterrows():
            title = row.get('title', 'N/A')[:40]
            status = row.get('status', 'N/A')
            date = row.get('appointment_date', 'N/A')
            code = row.get('code', 'N/A')
            print(f"     • {title} - {status} - {date[:10] if date != 'N/A' else 'N/A'} (Code: {code})")
    
    # 3. Articles Table
    articles_df = extract_articles_table(tables)
    if articles_df is not None and not articles_df.empty:
        print(f"\n📝 ARTICLES TABLE")
        print(f"   Total articles: {len(articles_df)}")
        print(f"\n   Article list:")
        for idx, row in articles_df.iterrows():
            title = row.get('title', 'N/A')
            category = row.get('category_id', 'N/A')
            created = row.get('created_at', 'N/A')
            print(f"     • {title} (Category: {category}) - Created: {created[:10] if created != 'N/A' else 'N/A'}")
    
    # 4. Categories Table
    categories_df = extract_categories_table(tables)
    if categories_df is not None and not categories_df.empty:
        print(f"\n🏷️ CATEGORIES TABLE")
        print(f"   Total categories: {len(categories_df)}")
        print(f"\n   Category list:")
        for idx, row in categories_df.iterrows():
            name = row.get('name', 'N/A')
            desc = row.get('description', 'N/A')[:50]
            print(f"     • {name}: {desc}...")
    
    # 5. Health Experts Table
    experts_df = extract_health_experts_table(tables)
    if experts_df is not None and not experts_df.empty:
        print(f"\n👨‍⚕️ HEALTH EXPERTS TABLE")
        print(f"   Total health experts: {len(experts_df)}")
        print(f"\n   Expert list:")
        for idx, row in experts_df.iterrows():
            name = row.get('name', 'N/A')
            title = row.get('expert_title', 'N/A')
            phone = row.get('phone', 'N/A')
            print(f"     • {name} - {title} ({phone})")
    
    # 6. Additional Statistics
    print(f"\n📊 SUMMARY STATISTICS")
    
    # Count unique users from appointments
    if appointments_df is not None and 'user_id' in appointments_df.columns:
        unique_users = appointments_df['user_id'].nunique()
        print(f"   • Unique users with appointments: {unique_users}")
    
    # Count unique health experts from appointments
    if appointments_df is not None and 'health_expert_id' in appointments_df.columns:
        unique_experts = appointments_df['health_expert_id'].nunique()
        print(f"   • Unique health experts assigned: {unique_experts}")
    
    # Check for articles with images
    if articles_df is not None and 'image' in articles_df.columns:
        articles_with_images = articles_df[articles_df['image'].notna() & (articles_df['image'] != 'NULL')].shape[0]
        print(f"   • Articles with images: {articles_with_images}")

def export_to_excel(tables, output_file='mapeers_analysis.xlsx'):
    """Export all tables to an Excel file with separate sheets"""
    
    try:
        with pd.ExcelWriter(output_file, engine='openpyxl') as writer:
            for table_name, df in tables.items():
                if df is not None and not df.empty:
                    # Clean sheet name (max 31 chars, no special chars)
                    sheet_name = re.sub(r'[^\w]', '_', table_name)[:31]
                    df.to_excel(writer, sheet_name=sheet_name, index=False)
        print(f"\n✅ Data exported to '{output_file}'")
        return True
    except Exception as e:
        print(f"\n⚠️ Could not export to Excel: {e}")
        return False

def get_basic_stats(tables):
    """Get basic statistics from all tables"""
    
    stats = {}
    
    users_df = extract_users_table(tables)
    if users_df is not None:
        stats['total_users'] = len(users_df)
        if 'created_at' in users_df.columns:
            users_df['created_date'] = pd.to_datetime(users_df['created_at'], errors='coerce')
            stats['users_joined_by_month'] = users_df['created_date'].dt.to_period('M').value_counts().to_dict()
    
    appointments_df = extract_appointments_table(tables)
    if appointments_df is not None:
        stats['total_appointments'] = len(appointments_df)
        if 'status' in appointments_df.columns:
            stats['appointment_statuses'] = appointments_df['status'].value_counts().to_dict()
    
    articles_df = extract_articles_table(tables)
    if articles_df is not None:
        stats['total_articles'] = len(articles_df)
    
    categories_df = extract_categories_table(tables)
    if categories_df is not None:
        stats['total_categories'] = len(categories_df)
    
    experts_df = extract_health_experts_table(tables)
    if experts_df is not None:
        stats['total_health_experts'] = len(experts_df)
    
    return stats

# Main execution
if __name__ == "__main__":
    file_path = 'db_mapeers.csv'
    
    # Parse all tables
    print("Parsing database file...")
    tables = analyze_mapeers_data(file_path)
    
    # Print detailed analysis
    print_analysis_results(tables)
    
    # Export to Excel
    export_to_excel(tables)
    
    # Get and print basic stats
    stats = get_basic_stats(tables)
    print(f"\n📈 QUICK STATS:")
    for key, value in stats.items():
        if not isinstance(value, dict):
            print(f"   • {key}: {value}")
    
    # Display any tables that weren't captured by the main extractors
    print(f"\n📋 ALL TABLES FOUND:")
    for table_name, df in tables.items():
        print(f"   • {table_name}: {len(df)} rows")


import pandas as pd

# Load the exported Excel file
file_path = 'mapeers_analysis.xlsx'

# Read all sheets
users_df = pd.read_excel(file_path, sheet_name='users')
appointments_df = pd.read_excel(file_path, sheet_name='appointments')
fcm_tokens_df = pd.read_excel(file_path, sheet_name='fcm_tokens')
sessions_df = pd.read_excel(file_path, sheet_name='sessions')

print("=" * 80)
print("USERS TABLE")
print("=" * 80)
print(f"Total Users: {len(users_df)}")
print(f"\nColumns: {', '.join(users_df.columns)}")
print("\nFirst 20 users:")
# Display available columns
display_cols = ['id', 'name', 'email', 'created_at'] if 'created_at' in users_df.columns else ['id', 'name', 'email']
print(users_df[display_cols].head(20).to_string(index=False))

print("\n" + "=" * 80)
print("APPOINTMENTS TABLE - COLUMN CHECK")
print("=" * 80)
print(f"Total Appointments: {len(appointments_df)}")
print(f"\nAvailable Columns: {', '.join(appointments_df.columns)}")
print("\nFirst 5 rows of appointments:")
print(appointments_df.head(5).to_string(index=False))

print("\n" + "=" * 80)
print("FCM TOKENS TABLE")
print("=" * 80)
print(f"Total FCM Tokens: {len(fcm_tokens_df)}")
print(f"\nColumns: {', '.join(fcm_tokens_df.columns)}")
print("\nFirst 20 FCM tokens:")
# Display available columns for FCM
fcm_display_cols = ['id', 'token', 'created_at'] if 'created_at' in fcm_tokens_df.columns else ['id', 'token']
if 'admin_id' in fcm_tokens_df.columns:
    fcm_display_cols.append('admin_id')
if 'user_id' in fcm_tokens_df.columns:
    fcm_display_cols.append('user_id')
print(fcm_tokens_df[fcm_display_cols].head(20).to_string(index=False))

print("\n" + "=" * 80)
print("SESSIONS TABLE")
print("=" * 80)
print(f"Total Sessions: {len(sessions_df)}")
print(f"\nColumns: {', '.join(sessions_df.columns)}")
print("\nFirst 20 sessions:")
# Display available columns for sessions
session_display_cols = ['id', 'user_id', 'ip_address', 'last_activity'] if 'last_activity' in sessions_df.columns else sessions_df.columns[:5]
print(sessions_df[session_display_cols].head(20).to_string(index=False))

# Additional statistics
print("\n" + "=" * 80)
print("ADDITIONAL STATISTICS")
print("=" * 80)

# User statistics by age range
if 'age_range' in users_df.columns:
    print("\nUsers by Age Range:")
    age_counts = users_df['age_range'].value_counts()
    for age, count in age_counts.items():
        print(f"  • {age}: {count}")

# User statistics by gender
if 'gender' in users_df.columns:
    print("\nUsers by Gender:")
    gender_counts = users_df['gender'].value_counts()
    for gender, count in gender_counts.items():
        print(f"  • {gender}: {count}")

# User statistics by description (population type)
if 'description' in users_df.columns:
    print("\nUsers by Population Type (Top 10):")
    desc_counts = users_df['description'].value_counts().head(10)
    for desc, count in desc_counts.items():
        desc_display = desc if desc and desc != 'NULL' and desc != 'nan' else 'Not specified'
        print(f"  • {desc_display}: {count}")

# Appointment statistics (using available columns)
print("\nAppointment Statistics:")
print(f"  • Total appointments: {len(appointments_df)}")

if 'status' in appointments_df.columns:
    print("\n  Appointment Status Breakdown:")
    status_counts = appointments_df['status'].value_counts()
    for status, count in status_counts.items():
        print(f"    - {status}: {count}")

if 'created_at' in appointments_df.columns:
    print(f"\n  Appointment date range: {appointments_df['created_at'].min()} to {appointments_df['created_at'].max()}")

# Users with FCM tokens
users_with_fcm = users_df[users_df['fcm'].notna() & (users_df['fcm'] != 'NULL')].shape[0]
print(f"\nUsers with FCM tokens: {users_with_fcm} / {len(users_df)} ({users_with_fcm/len(users_df)*100:.1f}%)")

# SOS reports
try:
    sos_df = pd.read_excel(file_path, sheet_name='sos_reports')
    print(f"\nTotal SOS Reports: {len(sos_df)}")
    if 'report_name' in sos_df.columns:
        print("\nSOS Report Types:")
        report_counts = sos_df['report_name'].value_counts().head(10)
        for report, count in report_counts.items():
            print(f"  • {report}: {count}")
except:
    print("\nSOS Reports sheet not found or couldn't be loaded")

# Migrations table
try:
    migrations_df = pd.read_excel(file_path, sheet_name='migrations')
    print(f"\nTotal Migrations: {len(migrations_df)}")
    print(f"Latest migration batch: {migrations_df['batch'].max() if 'batch' in migrations_df.columns else 'N/A'}")
except:
    pass

# Save detailed views to separate Excel files
print("\n" + "=" * 80)
print("SAVING DETAILED VIEWS")
print("=" * 80)

# Create a detailed users report
with pd.ExcelWriter('mapeers_detailed_users.xlsx') as writer:
    users_df.to_excel(writer, sheet_name='All_Users', index=False)
    
    # Filter by population type
    if 'description' in users_df.columns:
        sex_workers = users_df[users_df['description'].str.contains('Sex worker', na=False)]
        drug_users = users_df[users_df['description'].str.contains('injecting drugs', na=False)]
        lgbtq = users_df[users_df['description'].str.contains('GBMSM|LBQ|trans', na=False)]
        
        if not sex_workers.empty:
            sex_workers.to_excel(writer, sheet_name='Sex_Workers', index=False)
        if not drug_users.empty:
            drug_users.to_excel(writer, sheet_name='Drug_Users', index=False)
        if not lgbtq.empty:
            lgbtq.to_excel(writer, sheet_name='LGBTQ', index=False)
    
    # Users by age range
    if 'age_range' in users_df.columns:
        for age in users_df['age_range'].dropna().unique():
            if age and age != 'NULL' and age != 'nan':
                age_group = users_df[users_df['age_range'] == age]
                if not age_group.empty:
                    sheet_name = f'Age_{age}'.replace('+', 'plus').replace('-', '_to')
                    age_group.to_excel(writer, sheet_name=sheet_name[:31], index=False)

print("✅ Detailed user reports saved to 'mapeers_detailed_users.xlsx'")

# Create appointments detailed view
with pd.ExcelWriter('mapeers_detailed_appointments.xlsx') as writer:
    appointments_df.to_excel(writer, sheet_name='All_Appointments', index=False)
    
    # Group by status if available
    if 'status' in appointments_df.columns:
        for status in appointments_df['status'].dropna().unique():
            status_group = appointments_df[appointments_df['status'] == status]
            if not status_group.empty:
                sheet_name = f'Status_{status}'
                status_group.to_excel(writer, sheet_name=sheet_name[:31], index=False)

print("✅ Detailed appointments report saved to 'mapeers_detailed_appointments.xlsx'")

# Create FCM tokens report
with pd.ExcelWriter('mapeers_fcm_tokens.xlsx') as writer:
    fcm_tokens_df.to_excel(writer, sheet_name='All_FCM_Tokens', index=False)
    
    # Tokens by admin/user
    if 'admin_id' in fcm_tokens_df.columns:
        admin_tokens = fcm_tokens_df[fcm_tokens_df['admin_id'].notna()]
        if not admin_tokens.empty:
            admin_tokens.to_excel(writer, sheet_name='Admin_Tokens', index=False)
    
    if 'user_id' in fcm_tokens_df.columns:
        user_tokens = fcm_tokens_df[fcm_tokens_df['user_id'].notna()]
        if not user_tokens.empty:
            user_tokens.to_excel(writer, sheet_name='User_Tokens', index=False)

print("✅ FCM tokens report saved to 'mapeers_fcm_tokens.xlsx'")

# Create sessions report
with pd.ExcelWriter('mapeers_sessions.xlsx') as writer:
    sessions_df.to_excel(writer, sheet_name='All_Sessions', index=False)

print("✅ Sessions report saved to 'mapeers_sessions.xlsx'")

print("\n" + "=" * 80)
print("SUMMARY")
print("=" * 80)

# Calculate date range for users
user_date_range = "N/A"
if 'created_at' in users_df.columns:
    users_df['created_date'] = pd.to_datetime(users_df['created_at'], errors='coerce')
    min_date = users_df['created_date'].min()
    max_date = users_df['created_date'].max()
    user_date_range = f"{min_date.date() if min_date else 'N/A'} to {max_date.date() if max_date else 'N/A'}"

print(f"""
Database Statistics:
• Total Users: {len(users_df)}
• Total Appointments: {len(appointments_df)}
• Total FCM Tokens: {len(fcm_tokens_df)}
• Total Sessions: {len(sessions_df)}

Key Findings:
• Users joined from: {user_date_range}
• Users with push notifications: {users_with_fcm} / {len(users_df)} ({users_with_fcm/len(users_df)*100:.1f}%)
• Total appointments: {len(appointments_df)}
• Total FCM tokens registered: {len(fcm_tokens_df)}

Files Created:
1. mapeers_analysis.xlsx - Complete database export
2. mapeers_detailed_users.xlsx - Users grouped by demographics
3. mapeers_detailed_appointments.xlsx - Appointments by status
4. mapeers_fcm_tokens.xlsx - Push notification tokens
5. mapeers_sessions.xlsx - User session data
""")

# Optional: Display sample of each table in console
print("\n" + "=" * 80)
print("SAMPLE DATA - APPOINTMENTS (First 5 rows)")
print("=" * 80)
print(appointments_df.head().to_string(index=False))

print("\n" + "=" * 80)
print("SAMPLE DATA - FCM TOKENS (First 5 rows)")
print("=" * 80)
print(fcm_tokens_df.head().to_string(index=False))

print("\n" + "=" * 80)
print("SAMPLE DATA - SESSIONS (First 5 rows)")
print("=" * 80)
print(sessions_df.head().to_string(index=False))

import pandas as pd
import json

# Load the exported Excel file
file_path = 'mapeers_analysis.xlsx'

# Read all sheets
users_df = pd.read_excel(file_path, sheet_name='users')
appointments_df = pd.read_excel(file_path, sheet_name='appointments')
fcm_tokens_df = pd.read_excel(file_path, sheet_name='fcm_tokens')

print("=" * 80)
print("USERS WITH APPOINTMENTS")
print("=" * 80)

# Get unique user IDs from appointments
if 'user_id' in appointments_df.columns:
    users_with_appointments = appointments_df['user_id'].unique()
    print(f"\nTotal users who have appointments: {len(users_with_appointments)}")
    
    # Get user details for those with appointments
    users_with_appointments_data = users_df[users_df['id'].astype(str).isin(users_with_appointments.astype(str))]
    
    print("\nDetailed list of users with appointments:")
    print("-" * 80)
    
    # Merge appointments with user data
    merged_data = appointments_df.merge(
        users_df[['id', 'name', 'email', 'phone', 'created_at']], 
        left_on='user_id', 
        right_on='id', 
        how='left'
    )
    
    # Display each appointment with user info
    display_cols = ['title', 'user_id', 'name', 'email', 'appointment_date', 'status', 'code']
    available_cols = [col for col in display_cols if col in merged_data.columns]
    
    for idx, row in merged_data.iterrows():
        print(f"\nAppointment #{idx+1}:")
        print(f"  • Title: {row.get('title', 'N/A')}")
        print(f"  • User ID: {row.get('user_id', 'N/A')}")
        print(f"  • User Name: {row.get('name', 'N/A')}")
        print(f"  • User Email: {row.get('email', 'N/A')}")
        print(f"  • Date: {row.get('appointment_date', 'N/A')}")
        print(f"  • Status: {row.get('status', 'N/A')}")
        print(f"  • Code: {row.get('code', 'N/A')}")
    
    # Summary by user
    print("\n" + "=" * 80)
    print("SUMMARY BY USER")
    print("=" * 80)
    
    user_appointment_counts = merged_data['user_id'].value_counts()
    for user_id, count in user_appointment_counts.items():
        user_name = users_df[users_df['id'].astype(str) == str(user_id)]['name'].values
        user_name = user_name[0] if len(user_name) > 0 else 'Unknown'
        print(f"  • User {user_id} ({user_name}): {count} appointment(s)")
else:
    print("No user_id column found in appointments table")
    print(f"Available columns: {appointments_df.columns.tolist()}")

print("\n" + "=" * 80)
print("PUSH NOTIFICATIONS (ADMIN TO USERS)")
print("=" * 80)

# Check for notifications or push notifications table
try:
    # Try to read push_notifications table if it exists
    push_notifications_df = pd.read_excel(file_path, sheet_name='push_notifications')
    print(f"\nTotal push notifications: {len(push_notifications_df)}")
    print(f"\nColumns: {push_notifications_df.columns.tolist()}")
    print("\nSample push notifications:")
    print(push_notifications_df.head(10).to_string(index=False))
except:
    print("No 'push_notifications' sheet found. Looking for notification data...")

# Check admin_device_tokens table for admin push tokens
try:
    admin_tokens_df = pd.read_excel(file_path, sheet_name='admin_device_tokens')
    print(f"\nAdmin Device Tokens: {len(admin_tokens_df)}")
    print(admin_tokens_df.head().to_string(index=False))
except:
    pass

# Check for notifications table
try:
    notifications_df = pd.read_excel(file_path, sheet_name='notifications')
    print(f"\nNotifications Table: {len(notifications_df)} rows")
    print(f"Columns: {notifications_df.columns.tolist()}")
    
    if not notifications_df.empty:
        print("\nSample notifications:")
        print(notifications_df.head(10).to_string(index=False))
        
        # Parse notification data if it contains JSON
        if 'data' in notifications_df.columns:
            print("\nParsed notification messages:")
            for idx, row in notifications_df.head(10).iterrows():
                try:
                    data = json.loads(row['data']) if isinstance(row['data'], str) else row['data']
                    message = data.get('message', 'No message') if isinstance(data, dict) else str(data)
                    print(f"  • {message}")
                except:
                    print(f"  • {row['data'][:100]}..." if len(str(row['data'])) > 100 else f"  • {row['data']}")
except:
    pass

# Check for admin_push_notification_models
try:
    admin_push_df = pd.read_excel(file_path, sheet_name='admin_push_notification_models')
    print(f"\nAdmin Push Notifications: {len(admin_push_df)} rows")
    print(admin_push_df.head().to_string(index=False))
except:
    pass

# Analyze FCM tokens to see who can receive push notifications
print("\n" + "=" * 80)
print("PUSH NOTIFICATION CAPABILITY")
print("=" * 80)

# Users with FCM tokens (can receive push notifications)
users_with_fcm = users_df[users_df['fcm'].notna() & (users_df['fcm'] != 'NULL')]
print(f"\nUsers with FCM tokens (can receive push): {len(users_with_fcm)}")
print("\nUsers who can receive push notifications:")
for idx, row in users_with_fcm.head(20).iterrows():
    print(f"  • ID {row['id']}: {row['name']} - {row['email']}")

# Admins with FCM tokens
if 'admin_id' in fcm_tokens_df.columns:
    admin_tokens = fcm_tokens_df[fcm_tokens_df['admin_id'].notna()]
    print(f"\nAdmins with FCM tokens: {len(admin_tokens)}")
    for idx, row in admin_tokens.head(10).iterrows():
        print(f"  • Admin ID {row['admin_id']}: Token: {row['token'][:50]}...")

# Create a comprehensive report
print("\n" + "=" * 80)
print("CREATING COMPREHENSIVE REPORT")
print("=" * 80)

with pd.ExcelWriter('mapeers_push_notification_report.xlsx') as writer:
    # Users with appointments
    if 'user_id' in appointments_df.columns:
        users_with_appointments_data.to_excel(writer, sheet_name='Users_With_Appointments', index=False)
        
        # Appointment details by user
        appointment_details = appointments_df.merge(
            users_df[['id', 'name', 'email']], 
            left_on='user_id', 
            right_on='id', 
            how='left'
        )
        appointment_details.to_excel(writer, sheet_name='Appointment_Details', index=False)
    
    # Users who can receive push notifications
    users_with_fcm.to_excel(writer, sheet_name='Users_With_Push_Capability', index=False)
    
    # All FCM tokens
    fcm_tokens_df.to_excel(writer, sheet_name='All_FCM_Tokens', index=False)
    
    # Users without push capability
    users_without_fcm = users_df[users_df['fcm'].isna() | (users_df['fcm'] == 'NULL')]
    users_without_fcm.to_excel(writer, sheet_name='Users_Without_Push', index=False)

print("✅ Report saved to 'mapeers_push_notification_report.xlsx'")

# Summary statistics
print("\n" + "=" * 80)
print("SUMMARY STATISTICS")
print("=" * 80)

print(f"""
Push Notification & Appointment Summary:
=========================================
• Total Users: {len(users_df)}
• Users with Appointments: {len(users_with_appointments) if 'users_with_appointments' in dir() else 'N/A'}
• Total Appointments: {len(appointments_df)}
• Users with Push Capability: {len(users_with_fcm)}
• Users without Push Capability: {len(users_df) - len(users_with_fcm)}
• FCM Tokens Registered: {len(fcm_tokens_df)}

Push Coverage: {len(users_with_fcm)/len(users_df)*100:.1f}% of users can receive notifications

Recommendations:
• {len(users_df) - len(users_with_fcm)} users cannot receive push notifications
• Consider encouraging users to enable notifications
• Use alternative communication (SMS/Email) for users without FCM tokens
""")

# Display users who need attention (have appointments but no push capability)
if 'user_id' in appointments_df.columns:
    users_with_appointments_list = appointments_df['user_id'].unique()
    users_with_appointments_but_no_push = users_df[
        (users_df['id'].astype(str).isin(users_with_appointments_list.astype(str))) & 
        (users_df['fcm'].isna() | (users_df['fcm'] == 'NULL'))
    ]
    
    if not users_with_appointments_but_no_push.empty:
        print("\n" + "=" * 80)
        print("⚠️ USERS WITH APPOINTMENTS BUT NO PUSH CAPABILITY")
        print("=" * 80)
        print("These users have scheduled appointments but cannot receive push notifications:")
        for idx, row in users_with_appointments_but_no_push.iterrows():
            print(f"  • {row['name']} ({row['email']}) - User ID: {row['id']}")
            # Find their appointments
            user_appointments = appointments_df[appointments_df['user_id'].astype(str) == str(row['id'])]
            for _, apt in user_appointments.iterrows():
                print(f"    - Appointment: {apt.get('title', 'N/A')} on {apt.get('appointment_date', 'N/A')} (Status: {apt.get('status', 'N/A')})")