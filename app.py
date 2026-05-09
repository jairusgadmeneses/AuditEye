import streamlit as st
import pandas as pd
import base64


st.set_page_config(page_title="AuditEye | Sovereign Transparency", page_icon="", layout="wide")

def get_base64(bin_file):
    try:
        with open(bin_file, 'rb') as f:
            data = f.read()
        return base64.b64encode(data).decode()
    except FileNotFoundError:
        return "" 

logo_base64 = get_base64("logo.png")

minimal_css = f"""
<style>
    /* Pushes the logo up to the top of the sidebar */
    [data-testid="stSidebar"] .stMarkdown {{ padding-top: 0px; }}
    
    /* Clean Side-by-Side Layout */
    .logo-container {{
        display: flex;
        align-items: center;
        gap: 15px;
        margin-top: 5px;
        margin-bottom: 25px;
    }}
    
    /* The Logo Glow */
    .glowing-logo {{
        width: 100px; 
        height: auto;
        filter: drop-shadow(0px 0px 10px rgba(255, 70, 0, 0.8));
    }}
    
    /* The Text Glow */
    .glowing-title {{
        color: #FAFAFA;
        font-size: 58px;
        font-weight: 900;
        margin: 0;
        white-space: nowrap; 
        text-shadow: 0px 0px 12px rgba(255, 70, 0, 0.9);
    }}
</style>
"""
st.markdown(minimal_css, unsafe_allow_html=True)


with st.sidebar:
    if logo_base64:
        custom_logo_html = f"""
        <div class="logo-container">
            <img src="data:image/png;base64,{logo_base64}" class="glowing-logo" alt="AuditEye Logo">
            <p class="glowing-title">Sovereign Transparency Engine</p>
        </div>
        """
        st.markdown(custom_logo_html, unsafe_allow_html=True)
    else:
        st.error("⚠️ logo.png not found.")
    
    st.divider()
    
    st.markdown("### 🖥️ Hardware Telemetry")
    st.info("AMD MI300X Cloud Instance")
    st.progress(85, text="GPU/NPU Utilization")
    st.caption("🟢 Online | Region: ATL1")
    
    st.divider()
    
    st.markdown("### Agentic Settings")
    web_baselining = st.toggle("Enable Autonomous Web Baselining", value=True)
    st.caption("Agents dynamically search the web to establish real-time market prices.")
    
    st.slider("Anomaly Sensitivity", min_value=1, max_value=10, value=7)



st.title("Autonomous Forensic Auditor")
st.markdown("*Powered by LangChain & Qwen on AMD Compute Stack*")

uploaded_file = st.file_uploader("Drop CSV or XLSX files here", type=["csv", "xlsx"])

if uploaded_file:
    df = pd.read_csv(uploaded_file)
    st.success(f"Successfully ingested {uploaded_file.name} - {len(df)} rows found.")
    
    st.markdown("### Audit Overview")
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric(label="Total Budget Scanned", value="₱4.2B")
    with col2:
        st.metric(label="Red Flags Detected", value="--") 
    with col3:
        st.metric(label="Estimated Inflation", value="--")
        
    st.divider()

    col_map, col_feed = st.columns([6, 4]) 
    
    with col_map:
        st.markdown("### Dataset Context")
        with st.expander("View Raw Ingested Data", expanded=True):
            st.dataframe(df.head(10), use_container_width=True)
            
    with col_feed:
        st.markdown("### Audit Alert Feed")
        if st.button("Initialize Forensic Audit", type="primary", use_container_width=True):
            st.warning("Agentic Workflow Initiated. Initializing AI Brain...")
            st.info("The UI is ready. Awaiting LangChain integration.")
            
else:
    st.info("Waiting for dataset ingestion. Please upload a dummy CSV file to begin.")
