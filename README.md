# 👁️ AuditEye: Sovereign AI Procurement Auditor

![Hackathon](https://img.shields.io/badge/Hackathon-AMD_AI_Global-red?style=for-the-badge)
![Hardware](https://img.shields.io/badge/Hardware-AMD_Instinct™_MI300X-black?style=for-the-badge)
![LLM](https://img.shields.io/badge/Model-Qwen_2.5-blue?style=for-the-badge)
![Status](https://img.shields.io/badge/Status-Working_Prototype-success?style=for-the-badge)

**AuditEye** is a 100% sovereign, locally hosted AI auditing system designed to detect price bloat, anomalies, and corruption in government and enterprise procurement.

## 🛑 The Problem
Traditional SaaS auditing tools require uploading highly sensitive financial data to third-party clouds, creating massive security and privacy risks. Furthermore, manual auditing is slow, expensive, and prone to human error, allowing overpriced items to slip through the cracks.

## 💡 The Solution
AuditEye brings the AI to the data, not the data to the AI. Powered by **Alibaba Qwen 2.5** running locally on an **AMD Instinct™ MI300X** compute node, AuditEye acts as a tireless forensic accountant. It cross-references requested budgets against internal price lists or live market baselines, instantly flagging anomalies—all without your data ever leaving the hardware.

---

## ⚙️ Tech Stack & Architecture

* **The Brain:** Alibaba Qwen 2.5 (Direct PyTorch Inference)
* **The Hardware:** AMD Instinct™ MI300X GPU (ROCm™ Enabled)
* **The Orchestration:** LangGraph / LangChain for deterministic, tool-based agentic workflows.
* **The Frontend:** Streamlit (Real-time telemetry and dynamic dashboards)
* **Web Baselining:** DuckDuckGo Search API for live market pricing context.

---

## 🚀 Key Features

1. **Secure Data Ingestion:** Process bulk CSV and Excel procurement logs securely on-premise.
2. **Autonomous Web Baselining:** The agent autonomously searches the web for current market prices to compare against listed prices.
3. **Internal RAG Priority:** Force the AI to cross-reference prices against an internal, approved vendor catalog first.
4. **Vendor Risk Dashboard:** A dynamic leaderboard that tracks historical vendor data to flag repeatedly malicious or overcharging vendors.
5. **Hardware-Accelerated:** Leverages AMD ROCm for lightning-fast local LLM inference on massive document sets.

---

## 🏆 Hackathon Context
Built as a solo project by an 18-year-old 1st-year CS student for the **AMD AI Hackathon**. The goal of this project was to prove that Sovereign, Enterprise-Grade AI is highly viable at the edge using AMD hardware. Please refer to the submitted video presentation for the full system demonstration and UI walkthrough.
