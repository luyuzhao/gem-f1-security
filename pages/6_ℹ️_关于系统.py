import streamlit as st
import pandas as pd

if "logged_in" not in st.session_state or not st.session_state.logged_in:
    st.warning("请先登录"); st.stop()

st.set_page_config(page_title="关于系统", page_icon="ℹ️", layout="wide")

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
        background: linear-gradient(135deg, #0f172a 0%, #1e293b 40%, #8b5cf6 100%);
        border-radius: 16px;
        padding: 36px 44px;
        margin-bottom: 24px;
        box-shadow: 0 12px 40px rgba(139, 92, 246, 0.12);
    }
    .page-hero h1 { color: #f1f5f9; font-size: 30px; font-weight: 700; margin: 0; }
    .page-hero p { color: #ddd6fe; font-size: 14px; margin: 6px 0 0 0; }
    .info-card {
        background: #ffffff;
        border: 1px solid #e2e8f0;
        border-radius: 14px;
        padding: 24px 28px;
        margin-bottom: 16px;
        box-shadow: 0 2px 6px rgba(0,0,0,0.03);
    }
    .info-card h3 { font-size: 16px; font-weight: 600; color: #0f172a; margin-bottom: 12px; }
    .info-card p { font-size: 14px; color: #475569; line-height: 1.7; }
    .tech-tag {
        display: inline-block;
        background: #f1f5f9;
        color: #475569;
        padding: 5px 14px;
        border-radius: 20px;
        font-size: 13px;
        margin: 4px 6px;
    }
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
    <h1>ℹ️ 关于系统</h1>
    <p>GEM-F1 多场景安全检测系统 · 版本信息与技术架构</p>
</div>
""", unsafe_allow_html=True)

col1, col2 = st.columns(2)

with col1:
    st.markdown("""
    <div class="info-card">
        <h3>📦 系统版本</h3>
        <p>
        <b>产品名称</b>：GEM-F1 多场景安全检测系统<br>
        <b>版本号</b>：V1.0.0<br>
        <b>发布日期</b>：2026-06<br>
        <b>开发框架</b>：Streamlit 1.58 · Python 3.10<br>
        </p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class="info-card">
        <h3>🧠 核心算法</h3>
        <p>
        <b>GEM-F1</b>：贪心期望宏平均F1推理优化<br>
        <b>贝叶斯平滑</b>：组级概率估计<br>
        <b>ExtraTrees</b>：概率校准回归<br>
        <b>LightGBM</b>：对抗验证 + 集成分类<br>
        <b>DecisionTree</b>：知识蒸馏学生模型<br>
        </p>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div class="info-card">
        <h3>📊 功能模块</h3>
        <p>
        🔹 网络流量安全智能分类（12类）<br>
        🔹 系统日志异常区间检测（10类）<br>
        🔹 PowerShell恶意脚本检测（三分类）<br>
        🔹 二进制漏洞CWE识别（多分类）<br>
        🔹 检测历史记录与报告导出
        </p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class="info-card">
        <h3>🛠️ 技术栈</h3>
        <p>
        <span class="tech-tag">Python 3.10</span>
        <span class="tech-tag">Streamlit</span>
        <span class="tech-tag">LightGBM</span>
        <span class="tech-tag">Scikit-learn</span>
        <span class="tech-tag">NumPy</span>
        <span class="tech-tag">Pandas</span>
        <span class="tech-tag">ExtraTrees</span>
        <span class="tech-tag">DecisionTree</span>
        <span class="tech-tag">Joblib</span>
        </p>
    </div>
    """, unsafe_allow_html=True)

st.markdown("---")

st.markdown("""
<div class="info-card">
    <h3>📋 系统说明</h3>
    <p>
    本系统集成四项网络安全检测能力，覆盖流量分析、日志审计、脚本检测和漏洞识别四个方向。
    核心技术 GEM-F1 通过将推理阶段建模为约束优化问题，以期望宏平均F1为目标驱动贪心配额调配，
    相比标准 argmax 实现 7.2% 的性能提升，在保证组级标签一致性的同时突破逐样本推理的次优瓶颈。
    </p>
</div>
""", unsafe_allow_html=True)
