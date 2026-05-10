# app.py
import streamlit as st
import pandas as pd
import base64
import torch
import re
from audit_agent import create_audit_agent

st.set_page_config(page_title="AuditEye | Sovereign Transparency", layout="wide")

# 🔁 Initialize Dynamic Session States
if "chart_data" not in st.session_state:
    st.session_state.chart_data = pd.DataFrame({
        "Source": ["Baseline", "Web Avg", "Your Price"],
        "Price (PHP)": [0, 0, 0]
    }).set_index("Source")

if "vendor_risk_db" not in st.session_state:
    st.session_state.vendor_risk_db = pd.DataFrame(columns=[
        "Vendor Name", "Items Audited", "Anomalies Flagged",
        "Total Overcharge (PHP)", "Risk Level"
    ])

if "ai_report" not in st.session_state:
    st.session_state.ai_report = ""

# === CSS & LOGO ===
def get_base64(bin_file):
    try:
        with open(bin_file, 'rb') as f:
            return base64.b64encode(f.read()).decode()
    except FileNotFoundError:
        return ""

logo_base64 = get_base64("logo.png")
minimal_css = """
<style>
[data-testid="stSidebar"] .stMarkdown { padding-top: 0px; }
.logo-container { display: flex; align-items: center; gap: 15px; margin-top: 5px; margin-bottom: 25px; }
.glowing-logo { width: 100px; height: auto; filter: drop-shadow(0px 0px 10px rgba(255, 70, 0, 0.8)); }
.glowing-title { color: #FAFAFA; font-size: 32px; font-weight: 900; margin: 0; }
.stButton>button { background: linear-gradient(90deg, #ff4b4b 0%, #ff6b6b 100%); color: white; border: none; }
</style>
"""
st.markdown(minimal_css, unsafe_allow_html=True)

# === SIDEBAR ===
with st.sidebar:
    if logo_base64:
        st.markdown(f'<div class="logo-container"><img src="image/png;base64,{logo_base64}" class="glowing-logo" alt="Logo"><p class="glowing-title">AuditEye Engine</p></div>', unsafe_allow_html=True)
    st.divider()

    # 🔁 DYNAMIC TELEMETRY (Real PyTorch/ROCm)
    st.markdown("### 🖥️ Hardware Telemetry")
    if torch.cuda.is_available():
        gpu_name = torch.cuda.get_device_name(0)
        used_vram = torch.cuda.memory_allocated(0) / (1024**3)
        total_vram = torch.cuda.get_device_properties(0).total_memory / (1024**3)
        usage_pct = used_vram / total_vram if total_vram > 0 else 0
        st.info(gpu_name)
        st.progress(usage_pct, text=f"VRAM: {used_vram:.1f}GB / {total_vram:.1f}GB")
        st.caption("🟢 Online | PyTorch + ROCm Active")
    else:
        st.warning("⚠️ GPU Not Detected")
        st.progress(0.0, text="ROCm: Offline")

    st.divider()
    st.markdown("### 📂 Data Ingestion")
    primary_file = st.file_uploader("1. Audit Target (CSV, Excel)", type=["csv", "xlsx", "xls"])
    ref_file = st.file_uploader("2. Internal Price List (Optional)", type=["csv", "xlsx", "xls"], key="ref")

    st.divider()
    st.markdown("### ⚙️ Agentic Settings")
    rag_priority = st.toggle("Prioritize Internal Price List", value=True)
    web_baselining = st.toggle("Enable Autonomous Web Search", value=True)
    markup_threshold = st.slider("Anomaly Threshold (%)", min_value=10, max_value=200, value=50, step=5)

# === MAIN DASHBOARD ===
st.title("Autonomous Forensic Auditor")
st.markdown("Powered by Direct PyTorch Inference & Qwen 2.5 on AMD ROCm™")
tab1, tab2 = st.tabs(["🔍 Live Audit & Red Flags", "🏢 Vendor Risk Dashboard"])

with tab1:
    if not primary_file:
        st.info("👈 Upload a spreadsheet to begin.")
    else:
        st.success("✅ Data Ingested. Ready for HPC analysis.")
        
        st.markdown("### Audit Overview")
        col1, col2, col3 = st.columns(3)
        
        # 🔁 DYNAMIC BUDGET CALCULATION
        primary_ext = primary_file.name.split('.')[-1].lower()
        df = None
        total_budget = 0
        try:
            if primary_ext == 'csv':
                try:
                    df = pd.read_csv(primary_file, encoding='cp1252')
                except UnicodeDecodeError:
                    primary_file.seek(0)
                    df = pd.read_csv(primary_file, encoding='utf-8')
            elif primary_ext in ['xlsx', 'xls']:
                df = pd.read_excel(primary_file, engine='openpyxl' if primary_ext=='xlsx' else 'xlrd')
            
            if df is not None:
                # Find amount column dynamically
                amount_col = next((c for c in df.columns if any(k in c.lower() for k in ['amount', 'price', 'cost', 'total'])), None)
                if amount_col and pd.api.types.is_numeric_dtype(df[amount_col]):
                    total_budget = pd.to_numeric(df[amount_col], errors='coerce').sum()
        except Exception:
            pass
        
        col1.metric("Total Budget Scanned", f"₱{total_budget:,.2f}")
        col2.metric("Red Flags Detected", "--")
        col3.metric("Estimated Overspend", "--")
        st.divider()

        col_visuals, col_alerts = st.columns([6, 4])

        with col_visuals:
            st.markdown("### 📄 Dataset Context")
            
            if df is not None:
                st.dataframe(df.head(), width="stretch")
            else:
                st.warning("Unsupported file format for preview.")

            if ref_file:
                ref_ext = ref_file.name.split('.')[-1].lower()
                if ref_ext in ['csv', 'xlsx', 'xls']:
                    st.markdown("#### 📋 Internal Catalog")
                    ref_df = pd.read_csv(ref_file) if ref_ext == 'csv' else pd.read_excel(ref_file, engine='openpyxl' if ref_ext=='xlsx' else 'xlrd')
                    st.dataframe(ref_df.head(), width="stretch")

            # 🔁 DYNAMIC MARKET CHART
            st.markdown("### 📈 Live Market Analysis")
            st.bar_chart(st.session_state.chart_data, color="#ff4b4b", height=300)

        with col_alerts:
            st.markdown("### 🚨 Audit Alert Feed")
            
            # ✅ Download Button with actual report content
            st.download_button(
                "📥 Download Report", 
                data=st.session_state.get('ai_report', "Run audit first."), 
                file_name="AuditEye_Report.txt", 
                mime="text/plain", 
                width="stretch"
            )
            st.divider()
            
            if st.button("🔍 Initialize Forensic Audit", type="primary", width="stretch"):
                with st.spinner("🧠 Running Qwen 2.5 directly on AMD MI300X..."):
                    try:
                        auditor = create_audit_agent()
                        if df is not None:
                            # Dynamically find the Item and Price columns
                            item_col = next((c for c in df.columns if 'item' in c.lower()), df.columns[0])
                            price_col = next((c for c in df.columns if any(k in c.lower() for k in ['amount', 'price', 'cost', 'total'])), df.columns[1])
                            item = str(df.iloc[0][item_col])
                            price = float(df.iloc[0][price_col])
                        else:
                            item, price = "Unknown", 0

                        # 🔥 Send ONLY data to agent (Rules are in audit_agent.py)
                        prompt = f"Item: {item} | Listed Price: ₱{price} | Threshold: {markup_threshold}%"
                        ai_report = auditor(prompt, use_web_search=web_baselining)
                        
                        # Save report for download
                        st.session_state.ai_report = ai_report

                        st.markdown("#### 📝 AI Executive Summary")
                        with st.container(border=True):
                            st.write(ai_report)

                        # 🔁 UPDATE DYNAMIC CHART & VENDOR DB
                        try:
                            listed = price
                            m_b = re.search(r"Baseline:.*?([\d,]+\.?\d*)", ai_report)
                            baseline = float(m_b.group(1).replace(",","")) if m_b else 0
                            
                            # The AI doesn't output "Market Price", so we mirror Baseline for the chart to keep it clean
                            market = baseline 
                            
                            st.session_state.chart_data = pd.DataFrame({
                                "Source": ["Baseline", "Web Avg", "Your Price"],
                                "Price (PHP)": [baseline, market, listed]
                            }).set_index("Source")
                            
                            # Calculate Overcharge in Python instead of asking the AI!
                            is_anomaly = "TRUE" in ai_report.upper()
                            overcharge = (listed - baseline) if (is_anomaly and baseline > 0) else 0
                            
                            vendor_col = [c for c in df.columns if "vendor" in c.lower()]
                            vendor_name = df.iloc[0][vendor_col[0]] if vendor_col else "Unknown Vendor"

                            existing = st.session_state.vendor_risk_db[st.session_state.vendor_risk_db["Vendor Name"] == vendor_name]
                            if not existing.empty:
                                idx = existing.index[0]
                                st.session_state.vendor_risk_db.at[idx, "Items Audited"] += 1
                                if is_anomaly:
                                    st.session_state.vendor_risk_db.at[idx, "Anomalies Flagged"] += 1
                                    st.session_state.vendor_risk_db.at[idx, "Total Overcharge (PHP)"] += overcharge
                                    anomalies = st.session_state.vendor_risk_db.at[idx, "Anomalies Flagged"]
                                    st.session_state.vendor_risk_db.at[idx, "Risk Level"] = "🔴 EXTREME" if anomalies >= 5 else "🟡 MEDIUM" if anomalies >= 2 else "🟢 LOW"
                            else:
                                risk = "🔴 EXTREME" if is_anomaly else "🟢 LOW"
                                new_row = pd.DataFrame({"Vendor Name": [vendor_name], "Items Audited": [1], "Anomalies Flagged": [1 if is_anomaly else 0], "Total Overcharge (PHP)": [overcharge if is_anomaly else 0], "Risk Level": [risk]})
                                st.session_state.vendor_risk_db = pd.concat([st.session_state.vendor_risk_db, new_row], ignore_index=True)
                        except: pass

                    except Exception as e:
                        st.error(f"⚠️ Engine Failure: {e}")
                        st.exception(e)

with tab2:
    st.markdown("### 🏢 High-Risk Vendor Leaderboard")
    st.write("Real-time intelligence accumulated from procurement audits.")
    if st.session_state.vendor_risk_db.empty:
        st.info("📊 No audits completed yet. Run audits to populate the risk database.")
    else:
        sorted_df = st.session_state.vendor_risk_db.sort_values("Anomalies Flagged", ascending=False)
        st.dataframe(sorted_df, width="stretch", hide_index=True)
        col1, col2, col3 = st.columns(3)
        col1.metric("Total Vendors", len(st.session_state.vendor_risk_db))
        col2.metric("High-Risk", len(st.session_state.vendor_risk_db[st.session_state.vendor_risk_db["Risk Level"] == "🔴 EXTREME"]))
        col3.metric("Total Overcharge", f"₱{st.session_state.vendor_risk_db['Total Overcharge (PHP)'].sum():,.0f}")
