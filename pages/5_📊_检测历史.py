import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime, timedelta

if "logged_in" not in st.session_state or not st.session_state.logged_in:
    st.warning("请先登录"); st.stop()

st.set_page_config(page_title="检测历史记录", page_icon="📊", layout="wide")

with st.sidebar:
    st.markdown(f"👤 {st.session_state.username}")
    if st.button("退出登录", use_container_width=True):
        st.session_state.logged_in = False
        st.session_state.username = ""
        st.rerun()
    st.divider()

st.markdown("""
<style>
    .page-hero {
        background: linear-gradient(135deg, #0f172a 0%, #1e293b 40%, #6366f1 100%);
        border-radius: 16px;
        padding: 36px 44px;
        margin-bottom: 24px;
        box-shadow: 0 12px 40px rgba(99, 102, 241, 0.12);
    }
    .page-hero h1 { color: #f1f5f9; font-size: 30px; font-weight: 700; margin: 0; }
    .page-hero p { color: #c7d2fe; font-size: 14px; margin: 6px 0 0 0; }
    [data-testid="stSidebar"] { background: linear-gradient(180deg, #0f172a 0%, #1e293b 100%); }
    [data-testid="stSidebar"] * { color: #e2e8f0 !important; }
    [data-testid="stSidebar"] .stMarkdown,
    [data-testid="stSidebar"] .stRadio label,
    [data-testid="stSidebar"] [data-testid="stSidebarNav"] span,
    [data-testid="stSidebar"] [data-testid="stSidebarNav"] p,
    [data-testid="stSidebar"] [data-testid="stSidebarNav"] a { color: #f8fafc !important; font-weight: 500; }
    [data-testid="stSidebar"] hr { border-color: #334155; }
    [data-testid="stSidebar"] button { background: #334155 !important; color: #f8fafc !important; border: 1px solid #475569 !important; }
    [data-testid="stSidebar"] button:hover { background: #475569 !important; border-color: #64748b !important; }
</style>
""", unsafe_allow_html=True)

st.markdown("""
<div class="page-hero">
    <h1>📊 检测历史记录</h1>
    <p>所有检测任务的执行记录、结果统计与报告追溯</p>
</div>
""", unsafe_allow_html=True)

# ========== Demo History Data ==========
np.random.seed(42)
TASKS = ["网络流量分类", "日志异常检测", "PowerShell脚本检测", "漏洞CWE识别"]
STATUS = ["已完成", "已完成", "已完成", "已完成", "进行中"]

now = datetime.now()
records = []
for i in range(30):
    dt = now - timedelta(hours=np.random.randint(1, 168), minutes=np.random.randint(0, 60))
    task = np.random.choice(TASKS)
    status = np.random.choice(STATUS)
    files = np.random.randint(100, 5000)
    anomalies = np.random.randint(0, files // 3) if "异常" in task else None
    records.append({
        "时间": dt.strftime("%m-%d %H:%M"),
        "检测模块": task,
        "文件数": files,
        "检出量": anomalies if task == "日志异常检测" else (np.random.randint(0, files) if "漏洞" not in task else f"{np.random.randint(5,60)} 个CWE"),
        "状态": status,
        "操作人": st.session_state.get("username", "admin"),
        "耗时": f"{np.random.randint(1, 30)}s",
    })

df = pd.DataFrame(records).sort_values("时间", ascending=False).reset_index(drop=True)

# ========== Stats ==========
c1, c2, c3 = st.columns(3)
c1.metric("总检测次数", f"{len(df)}")
c2.metric("今日检测", f"{np.random.randint(3, 12)}")
c3.metric("累计处理文件", f"{df['文件数'].astype(int).sum():,}")

st.markdown("---")

# ========== History Table ==========
st.markdown("### 检测记录清单")
st.dataframe(df, use_container_width=True,
    column_config={
        "时间": st.column_config.TextColumn(width="small"),
        "检测模块": st.column_config.TextColumn(width="medium"),
        "文件数": st.column_config.NumberColumn(width="small"),
        "检出量": st.column_config.TextColumn(width="small"),
        "状态": st.column_config.TextColumn(width="small"),
        "操作人": st.column_config.TextColumn(width="small"),
        "耗时": st.column_config.TextColumn(width="small"),
    })

# ========== Export ==========
csv = df.to_csv(index=False).encode("utf-8")
st.download_button("📥 导出完整历史记录", csv, "detection_history.csv", "text/csv")
