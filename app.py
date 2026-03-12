import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd
import datetime
import plotly.express as px
from datetime import date


import streamlit as st

# ==========================================
# ✨ SIDEBAR KA PREMIUM CSS STYLING ✨
# ==========================================
st.markdown("""
<style>
    /* 1. Dark Gradient Background aur Glowing Border */
    [data-testid="stSidebar"] {
        background: linear-gradient(145deg, #11141e 0%, #0a0b10 100%) !important;
        border-right: 2px solid #ff7b00 !important;
        box-shadow: 3px 0px 20px rgba(255, 123, 0, 0.4) !important;
    }

    /* 2. Main heading (Kahan jana hai?) */
    [data-testid="stSidebar"] .stRadio > label {
        background: transparent !important;
        border: none !important;
        padding: 0px !important;
        color: #ff7b00 !important; 
        font-size: 18px !important;
        font-weight: bold !important;
        margin-bottom: 15px !important;
    }

    /* 3. Sirf OPTIONS (Radio buttons) ko styling dena */
    [data-testid="stSidebar"] div[role="radiogroup"] label {
        padding: 12px 15px !important;
        border-radius: 12px !important;
        transition: all 0.3s ease !important;
        margin-bottom: 10px !important;
        border: 1px solid rgba(255, 255, 255, 0.1) !important;
        background: rgba(255, 255, 255, 0.03) !important;
    }

    /* 4. Options ke andar ke Text ka color */
    [data-testid="stSidebar"] div[role="radiogroup"] p {
        color: #ffffff !important;
        font-size: 16px !important;
        font-weight: 500 !important;
    }

    /* 5. ✨ Hover Animation */
    [data-testid="stSidebar"] div[role="radiogroup"] label:hover {
        background: rgba(255, 123, 0, 0.15) !important;
        border: 1px solid #ff7b00 !important;
        box-shadow: 0px 0px 15px rgba(255, 123, 0, 0.6) !important;
        transform: translateX(8px) !important;
        cursor: pointer;
    }

    /* 6. 🚨 Saari Headings (h1 se h6 tak) ko Crisp White karna */
    [data-testid="stSidebar"] h1, 
    [data-testid="stSidebar"] h2, 
    [data-testid="stSidebar"] h3, 
    [data-testid="stSidebar"] h4, 
    [data-testid="stSidebar"] h5, 
    [data-testid="stSidebar"] h6 {
        color: #ffffff !important;
        font-weight: 600 !important;
    }

    /* 7. 🚨 st.caption ko Faded se Chamkadar banana */
    [data-testid="stSidebar"] small {
        color: #e2e8f0 !important;
        opacity: 1 !important;
        font-size: 14px !important;
        font-weight: 500 !important;
        letter-spacing: 0.5px !important;
    }

    /* Caption container fix */
    [data-testid="stCaptionContainer"] {
        opacity: 1 !important;
    }

    /* 8. 🚨 ALL TEXT ELEMENTS PERFECT VISIBILITY */
    [data-testid="stSidebar"] p,
    [data-testid="stSidebar"] span,
    [data-testid="stSidebar"] em,
    [data-testid="stSidebar"] div p,
    [data-testid="stSidebar"] .stMarkdown p {
        color: #e2e8f0 !important;
        opacity: 1 !important;
        font-weight: 500 !important;
    }
</style>
""", unsafe_allow_html=True)


# ==========================================
# ⚙️ PAGE SETUP
# ==========================================
st.set_page_config(page_title="Smart Electricity Billing", page_icon="⚡", layout="centered") # Centered mobile ke liye best hai
# 🔥 HERO SECTION (No Revenue)
st.markdown("""
<div style="background: linear-gradient(135deg, #FF6B35 0%, #4ECDC4 100%); 
            padding:2rem; border-radius:15px; margin-bottom:2rem; color:white; text-align:center">
    <h1 style="margin:0">⚡ Nehru Nagar Smart Billing</h1>
    <p style="margin:0; opacity:0.9">Modern • Fast • Accurate</p>
</div>
""", unsafe_allow_html=True)
st.divider()

# ==========================================
# 🔗 ULTRA-FAST DATABASE CONNECTION 
# ==========================================
# YAHAN APNI SHEET KA LINK DAALNA
SHEET_URL = "https://docs.google.com/spreadsheets/d/1frzmMjaKIdCip5VNyvcafzneQMwoqaRmpf4eWqEfvzk/edit?usp=sharing"
conn = st.connection("gsheets", type=GSheetsConnection)

@st.cache_data(ttl=600)
def load_data():
    raw = conn.read(spreadsheet=SHEET_URL, worksheet="meter_readings")
    history = conn.read(spreadsheet=SHEET_URL, worksheet="monthly_bills")
    
    if not history.empty and 'Payment_Status' not in history.columns:
        history['Payment_Status'] = "🔴 Not Paid"
        
    return raw, history

df_raw, df_history_live = load_data()

# ==========================================
# 🧭 SIDEBAR NAVIGATION (PERFECTLY ORGANIZED)
# ==========================================
with st.sidebar:
    # 1. GLOWING Profile Section
    st.markdown("""
    <div style='text-align:center; padding:1.5rem; 
                background: linear-gradient(145deg, rgba(255,123,0,0.15), rgba(255,123,0,0.05)); 
                border-radius:20px; border:2px solid rgba(255,123,0,0.4); margin:1rem 0.5rem'>
        <img src="https://cdn-icons-png.flaticon.com/512/3135/3135715.png" width=80 
             style='filter: drop-shadow(0 0 15px rgba(255,123,0,0.6)); border-radius:50%'>
        <h3 style='color:#ff7b00; margin:0.8rem 0; font-size:20px'>⚡ Admin Panel</h3>
        <p style='color:#e2e8f0; margin:0; font-size:13px'>Nehru Nagar</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.divider()
    
    # 2. Main Menu Section
    st.markdown("### 🎛️ **Main Menu**")
    app_mode = st.radio(
        "➤ Chuno:", 
        [
            "🧭 1. Nayi Meter Reading", 
            "🧾 2. Agle Mahine ka Bill Banao", 
            "📊 3. Purane Record aur Payment Dikhao"
        ]
    )
    
    # Active Page Indicator
    current_page = app_mode.split('.')[1].strip() if '.' in app_mode else app_mode
    st.markdown(f"✅ **{current_page} Active**")
    
    st.divider()
    
    # 3. Quick Actions Section
    st.markdown("### 🚀 **Quick Actions**")
    if st.button("🔄 Refresh Data", key="refresh_sidebar", use_container_width=True):
        st.cache_data.clear()
        st.rerun()
    
    st.divider()
    
    # 4. Status Section
    st.markdown("### 📊 **Status**")
    from datetime import date
    aaj_ki_tareekh = date.today().strftime('%d %B %Y')
    st.info(f"📅 Aaj: **{aaj_ki_tareekh}**")
    
    st.divider()
    
    # 5. Footer Section (PERFECTLY VISIBLE)
    st.markdown("""
        <div style='
            color: #FFFFFF !important;
            font-size: 18px !important;
            font-weight: 700 !important;
            text-shadow: 1px 1px 3px rgba(0,0,0,0.8) !important;
            opacity: 1 !important;
            text-align: center; 
            padding: 15px; 
            background: linear-gradient(145deg, rgba(16,20,30,0.95), rgba(10,11,16,0.95));
            border-radius: 15px; 
            border: 2px solid #ff7b00 !important;
            margin: 15px 8px 10px 8px;
            box-shadow: 0 6px 20px rgba(255,123,0,0.3);
        '>
            ✨ Made with ❤️ in Bhopal
        </div>
    """, unsafe_allow_html=True)

# ==========================================
# PAGE 1: FAST METER ENTRY
# ==========================================
if app_mode == "🧭 1. Nayi Meter Reading":
    st.subheader("📝 Nayi Meter Reading Daalein")
    st.markdown("Sirf nayi (current) reading daalein. Purani apne aap aa jayegi.")
    
    months_list = df_raw['Month'].dropna().unique()
    
    if len(months_list) > 0:
        last_month = months_list[-1]
        df_last_month = df_raw[df_raw['Month'] == last_month].copy()
        
        st.write("---")
        
        selected_date = st.date_input("📅 Reading ki Tareekh (Date)", datetime.date.today())
        new_month_name = selected_date.strftime("%d-%B-%Y")
        
        st.write(f"### 📟 **{new_month_name}** ki Readings:")
        
        with st.form("quick_entry_form"):
            new_readings_data = []
            
            for index, row in df_last_month.iterrows():
                tenant_name = row['Tenant']
                meter_type = row['Meter_Type']
                block = row['Block']
                auto_previous = float(row['Current']) 
                
                st.markdown(f"👤 **{tenant_name}** ({block})")
                
                c1, c2 = st.columns(2)
                c1.number_input("Pichli Reading", value=auto_previous, disabled=True, key=f"prev_{tenant_name}_{block}")
                new_current = c2.number_input("Nayi Reading", value=None, step=1.0, placeholder = "Enter Value", key=f"curr_{tenant_name}_{block}")
                
                new_readings_data.append({
                    "Month": new_month_name, "Tenant": tenant_name, "Meter_Type": meter_type,
                    "Block": block, "Previous": auto_previous, "Current": new_current
                })
                st.write("---")
                
            submit_btn = st.form_submit_button("💾 Sabki Reading Save Karein", type="primary")
            
            if submit_btn:
                df_new_entries = pd.DataFrame(new_readings_data)
                df_updated_readings = pd.concat([df_raw, df_new_entries], ignore_index=True)
                df_updated_readings = df_updated_readings.drop_duplicates(subset=['Month', 'Tenant', 'Meter_Type'], keep='last')
                try:
                    conn.update(spreadsheet=SHEET_URL, worksheet="meter_readings", data=df_updated_readings)
                    st.cache_data.clear()
                    st.success(f"✅ {new_month_name} ki saari readings save ho gayi!")
                except Exception as e:
                    st.error(f"❌ Error: {e}")

# ==========================================
# PAGE 2: BILL GENERATION 
# ==========================================
elif app_mode == "🧾 2. Agle Mahine ka Bill Banao":
    st.subheader("🧾 Final Bill Generate Karein")
    
    months_available = df_raw['Month'].dropna().unique()
    selected_month = st.selectbox("📅 Kis mahine ka bill banana hai?", options=reversed(months_available))
    st.write("---")
    
    df = df_raw[df_raw['Month'] == selected_month].copy()
    df['Current'] = pd.to_numeric(df['Current'], errors='coerce').fillna(0)
    df['Previous'] = pd.to_numeric(df['Previous'], errors='coerce').fillna(0)
    df['Meter_Type'] = df['Meter_Type'].astype(str).str.strip().str.lower()
    df['Block'] = df['Block'].astype(str).str.strip().str.upper()
    
    df['Raw_Units'] = df['Current'] - df['Previous']
    df['Final_Units'] = df['Raw_Units']
    
    for b_name in ['S774', 'S773']:
        mask = df['Block'] == b_name
        subs = df[mask & (df['Meter_Type'].str.contains('sub'))]['Raw_Units'].sum()
        main_idx = df[mask & (df['Meter_Type'].str.contains('main'))].index
        if not main_idx.empty: 
            df.loc[main_idx, 'Final_Units'] = df.loc[main_idx, 'Raw_Units'] - subs

    total_units_s774 = df[df['Block'] == 'S774']['Final_Units'].sum()
    total_units_s773 = df[df['Block'] == 'S773']['Final_Units'].sum()

    st.markdown(f"🔌 **Total Units:** S774 = **{total_units_s774:.2f}** | S773 = **{total_units_s773:.2f}**")
    
    st.write("---")
    st.markdown("⚡ **Bijli ka Rate (₹)**")
    colA, colB = st.columns(2)
    with colA:
        rate_s774 = st.number_input("Rate S774 ke liye", value=7.02, step=0.1)
    with colB:
        rate_s773 = st.number_input("Rate S773 ke liye", value=1.35, step=0.1)

    st.write("---")
    st.markdown("💧 **Paani aur Nagar Nigam Config**")
    cc1, cc2, cc3 = st.columns(3)
    total_tenants = cc1.number_input("Total Kirayedar", value=5, min_value=1)
    nagar_per_block = cc2.number_input("Nagar Nigam (Per Block)", value=330.0, step=10.0)
    water_override = cc3.number_input("Water Fixed Amount (₹)", value=None, placeholder ="Enter Amount")

    if st.button("🚀 Sabka Bill Calculate Karein", type="primary"):
        water_row = df[df['Tenant'].str.contains('Water', case=False, na=False)]
        water_units = water_row['Raw_Units'].values[0] if not water_row.empty else 0
        auto_water_cost = (water_units * rate_s773) / total_tenants
        final_water_share = water_override if water_override > 0 else auto_water_cost

        nagar_nigam_share = (nagar_per_block * 2) / total_tenants
        
        df_final = df[~df['Tenant'].str.contains('Water', case=False, na=False)].copy()
        df_final['Rate'] = df_final['Block'].apply(lambda x: rate_s774 if x == 'S774' else rate_s773).round(2)
        df_final['Electricity'] = round(df_final['Final_Units'] * df_final['Rate'], 2)
        df_final['Water'] = round(final_water_share, 2)
        df_final['Nagar_Nigam'] = round(nagar_nigam_share, 2)
        df_final['Total'] = round(df_final['Electricity'] + df_final['Water'] + df_final['Nagar_Nigam'])
        
        st.session_state['calculated_bill'] = df_final
        
    if 'calculated_bill' in st.session_state:
        df_preview = st.session_state['calculated_bill']
        st.dataframe(df_preview[['Tenant', 'Final_Units', 'Total']], use_container_width=True) # Mobile pe choti table dikhayenge
        
        if st.button("💾 Bill Save Karein (Google Sheet me)", type="secondary"):
            try:
                new_history = df_preview[['Month', 'Tenant', 'Final_Units', 'Rate', 'Electricity', 'Water', 'Nagar_Nigam', 'Total']]
                new_history = new_history.rename(columns={'Final_Units': 'Units'})
                new_history['Payment_Status'] = "🔴 Not Paid" 
                
                updated_history = pd.concat([df_history_live, new_history], ignore_index=True)
                updated_history = updated_history.drop_duplicates(subset=['Month', 'Tenant'], keep='last')
                
                conn.update(spreadsheet=SHEET_URL, worksheet="monthly_bills", data=updated_history)
                st.cache_data.clear() 
                st.success("🎉 Sabka bill save ho gaya! Ab 'Purane Record' me jaakar payment check karein.")
            except Exception as e:
                st.error(f"❌ Failed to save history: {e}")
                
        if st.button("🔄 Page Refresh Karein"):
            del st.session_state['calculated_bill']
            st.rerun()

# ==========================================
# PAGE 3: PAYMENT DASHBOARD & ANALYTICS
# ==========================================
elif app_mode == "📊 3. Purane Record aur Payment Dikhao":
    st.subheader("📊 Payment aur Analytics Dashboard")
    
    if not df_history_live.dropna(how='all').empty:
        # Total Revenue Calculations
        total_revenue = df_history_live['Total'].sum()
        
        if 'Payment_Status' in df_history_live.columns:
            pending_mask = df_history_live['Payment_Status'].str.contains('Not Paid', na=False)
            pending_amount = df_history_live[pending_mask]['Total'].sum()
            collected_amount = total_revenue - pending_amount
            pending_df = df_history_live[pending_mask] 
        else:
            pending_amount = total_revenue
            collected_amount = 0
            pending_df = df_history_live

        # 📱 TABS YAHAN SE SHURU HOTE HAIN
        tab1, tab2 = st.tabs(["📈 Dashboard & Pending", "📂 Pura Record (Excel jaisa)"])
        
        # ------------------------------------------
        # TAB 1: DASHBOARD AUR PENDING PAYMENTS
        # ------------------------------------------
        with tab1:
            # SABSE UPAR METRICS
            c1, c2 = st.columns(2)
            c1.metric("🟢 Total Mil Gaya", f"₹{collected_amount:,.0f}")
            c2.metric("🔴 Aana Baaki Hai", f"₹{pending_amount:,.0f}")
            
            st.divider()
            
            # USKE NEECCHE PENDING PAYMENTS
            st.markdown("### ⏳ Pending Payments (Paisa lena baaki hai)")
            
            if not pending_df.empty:
                for index, row in pending_df.iterrows():
                    with st.container(border=True):
                        card_col1, card_col2 = st.columns([2, 1])
                        
                        with card_col1:
                            st.markdown(f"**👤 {row['Tenant']}**")
                            st.caption(f"📅 {row['Month']} | ⚡ {row['Units']} Units")
                            st.markdown(f"#### 💰 ₹{row['Total']}")
                        
                        with card_col2:
                            if st.button("✅ Paisa Mil Gaya", key=f"pay_{index}"):
                                df_history_live.at[index, 'Payment_Status'] = "🟢 Paid"
                                try:
                                    conn.update(spreadsheet=SHEET_URL, worksheet="monthly_bills", data=df_history_live)
                                    st.cache_data.clear()
                                    st.success(f"{row['Tenant']} ka paisa update ho gaya!")
                                    st.rerun() 
                                except Exception as e:
                                    st.error(f"❌ Error: {e}")
            else:
                st.success("🎉 Kamaal hai! Sabka paisa aa gaya hai, koi pending nahi hai.")

            st.divider()
            
            # LAST ME CHARTS AND GRAPHS (TAB 1 KE SABSE NEECCHE)
            # 📈 SUNDAR PLOTLY GRAPHS (Dono side-by-side)
            col_chart1, col_chart2 = st.columns(2)
            
            with col_chart1:
                # 1. Paisa Aaya ya Baaki Hai? (Donut Chart)
                status_data = {'Status': ['Mil Gaya', 'Aana Baaki Hai'], 'Amount': [collected_amount, pending_amount]}
                # Agar koi entry nahi hai toh error se bachne ke liye check
                if total_revenue > 0:
                    fig_pie = px.pie(status_data, values='Amount', names='Status', 
                                     color='Status', color_discrete_map={'Mil Gaya':'#28a745', 'Aana Baaki Hai':'#dc3545'},
                                     hole=0.5, title="💰 Payment Status")
                    fig_pie.update_layout(margin=dict(t=40, b=0, l=0, r=0))
                    st.plotly_chart(fig_pie, use_container_width=True)
                else:
                    st.info("📊 Graph dekhne ke liye bills add karein.")

            with col_chart2:
                # 2. Kisne Kitni Bijli Jalayi? (Colorful Bar Chart)
                df_history_live['Units'] = pd.to_numeric(df_history_live['Units'], errors='coerce').fillna(0)
                tenant_units = df_history_live.groupby('Tenant')['Units'].sum().reset_index()
                
                if not tenant_units.empty and tenant_units['Units'].sum() > 0:
                    fig_bar = px.bar(tenant_units, x='Tenant', y='Units', text='Units', 
                                     color='Tenant', title="⚡ Bijli Kharch (Units)")
                    fig_bar.update_traces(textposition='outside')
                    fig_bar.update_layout(margin=dict(t=40, b=0, l=0, r=0), showlegend=False)
                    st.plotly_chart(fig_bar, use_container_width=True)
                else:
                    st.info("⚡ Bijli ka data graph ke liye available nahi hai.")

        # ------------------------------------------
        # TAB 2: PURA RECORD (EXCEL JAISA)
        # ------------------------------------------
        with tab2:
            # Filters ko side-by-side dikhane ke liye 2 columns banayein
            col1, col2 = st.columns(2)
    
            with col1:
                hist_months = df_history_live['Month'].dropna().unique()
                filter_month = st.selectbox(
                    "📅 Mahina chunein:", 
                    options=["All"] + list(reversed(hist_months))
                )
                
            with col2:
                hist_tenants = df_history_live['Tenant'].dropna().unique()
                filter_tenant = st.selectbox(
                    "👤 Tenant (Kirayedar) chunein:", 
                    options=["All"] + list(hist_tenants)
                )
            
            # Data ki ek copy banate hain taaki original data safe rahe
            display_df = df_history_live.copy()
            
            # Mahine ke hisaab se filter lagana
            if filter_month != "All":
                display_df = display_df[display_df['Month'] == filter_month]
                
            # Tenant ke hisaab se filter lagana
            if filter_tenant != "All":
                display_df = display_df[display_df['Tenant'] == filter_tenant]
                
            # Sirf zaroori columns dikhana
            cols_to_show = ['Month', 'Tenant', 'Units', 'Total', 'Payment_Status']
            
            # Total Amount dikhana, par check karna ki table khali toh nahi hai
            if not display_df.empty:
                st.dataframe(
                    display_df[cols_to_show], 
                    use_container_width=True, 
                    hide_index=True
                )
                try:
                    total_amount = display_df['Total'].sum()
                    st.success(f"**💰 Is list ka Total Bill Amount:** ₹ {total_amount:,.2f}")
                except:
                    pass
            else:
                st.warning("⚠️ Is filter combination ke hisaab se koi record nahi mila.")

    else:
        st.info("ℹ️ Abhi tak koi bill history save nahi hui hai. Pehle bill generate karein!")
