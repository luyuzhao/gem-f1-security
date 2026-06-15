import streamlit as st
import time

st.set_page_config(
    page_title="GEM-F1 多场景安全检测系统",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ========== Session State ==========
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "username" not in st.session_state:
    st.session_state.username = ""

# ========== CSS ==========
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');
    * { font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif; }
    .main > div { padding-top: 1rem; }

    /* ========== Login Page ========== */
    .login-container {
        display: flex;
        justify-content: center;
        align-items: center;
        min-height: 80vh;
    }
    .login-box {
        background: #ffffff;
        border: 1px solid #e2e8f0;
        border-radius: 20px;
        padding: 48px 44px;
        width: 420px;
        box-shadow: 0 20px 60px rgba(0,0,0,0.06);
    }
    .login-logo {
        text-align: center;
        font-size: 40px;
        margin-bottom: 8px;
    }
    .login-title {
        text-align: center;
        font-size: 22px;
        font-weight: 700;
        color: #0f172a;
        margin-bottom: 4px;
    }
    .login-subtitle {
        text-align: center;
        font-size: 13px;
        color: #94a3b8;
        margin-bottom: 32px;
    }
    .login-input {
        margin-bottom: 16px;
    }
    .login-input label {
        font-size: 13px;
        font-weight: 500;
        color: #475569;
        display: block;
        margin-bottom: 6px;
    }
    .login-hint {
        text-align: center;
        font-size: 12px;
        color: #94a3b8;
        margin-top: 20px;
    }

    /* ========== Hero Banner ========== */
    .hero-banner {
        background: linear-gradient(135deg, #0f172a 0%, #1e293b 40%, #0ea5e9 100%);
        border-radius: 20px;
        padding: 48px 52px;
        margin-bottom: 32px;
        position: relative;
        overflow: hidden;
        box-shadow: 0 20px 60px rgba(14, 165, 233, 0.15);
    }
    .hero-banner::after {
        content: '';
        position: absolute;
        top: -50%;
        right: -10%;
        width: 500px;
        height: 500px;
        background: radial-gradient(circle, rgba(14,165,233,0.12) 0%, transparent 70%);
        border-radius: 50%;
    }
    .hero-title {
        font-size: 38px;
        font-weight: 700;
        color: #f1f5f9;
        margin-bottom: 8px;
        position: relative;
        z-index: 1;
    }
    .hero-subtitle {
        font-size: 16px;
        color: #94a3b8;
        font-weight: 400;
        position: relative;
        z-index: 1;
    }

    /* ========== KPI Cards ========== */
    .kpi-card {
        background: linear-gradient(135deg, #ffffff 0%, #f8fafc 100%);
        border: 1px solid #e2e8f0;
        border-radius: 16px;
        padding: 24px 28px;
        box-shadow: 0 2px 8px rgba(0,0,0,0.04);
        transition: all 0.3s ease;
    }
    .kpi-card:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 24px rgba(0,0,0,0.08);
        border-color: #0ea5e9;
    }
    .kpi-icon { font-size: 32px; margin-bottom: 10px; }
    .kpi-label { font-size: 13px; color: #64748b; font-weight: 500; text-transform: uppercase; letter-spacing: 0.5px; }
    .kpi-value { font-size: 28px; font-weight: 700; color: #0f172a; margin-top: 2px; }
    .kpi-desc { font-size: 12px; color: #94a3b8; margin-top: 4px; }

    /* ========== Feature Grid ========== */
    .feature-item {
        background: #f8fafc;
        border: 1px solid #e2e8f0;
        border-radius: 12px;
        padding: 20px 24px;
        transition: all 0.2s;
    }
    .feature-item:hover { border-color: #0ea5e9; background: #f0f9ff; }
    .feature-item .icon { font-size: 28px; margin-bottom: 8px; }
    .feature-item .title { font-size: 15px; font-weight: 600; color: #0f172a; }
    .feature-item .desc { font-size: 13px; color: #64748b; margin-top: 4px; line-height: 1.6; }

    /* ========== Innovation Highlight ========== */
    .innovation-box {
        background: linear-gradient(135deg, #eff6ff 0%, #dbeafe 100%);
        border: 1px solid #93c5fd;
        border-radius: 16px;
        padding: 28px 32px;
        margin-bottom: 24px;
    }
    .innovation-box .title { font-size: 16px; font-weight: 700; color: #1e40af; margin-bottom: 12px; }
    .innovation-box .bullet { font-size: 14px; color: #1e3a5f; line-height: 1.8; padding-left: 8px; }

    .section-title {
        font-size: 18px; font-weight: 600; color: #0f172a;
        margin-bottom: 16px; display: flex; align-items: center; gap: 10px;
    }
    .section-title .dot { width: 8px; height: 8px; border-radius: 50%; background: #0ea5e9; }

    .footer {
        text-align: center; padding: 24px; color: #94a3b8;
        font-size: 12px; border-top: 1px solid #e2e8f0; margin-top: 40px;
    }

    /* ========== Sidebar ========== */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #0f172a 0%, #1e293b 100%);
    }
    [data-testid="stSidebar"] * { color: #e2e8f0 !important; }
    [data-testid="stSidebar"] .stMarkdown,
    [data-testid="stSidebar"] .stRadio label,
    [data-testid="stSidebar"] [data-testid="stSidebarNav"] span,
    [data-testid="stSidebar"] [data-testid="stSidebarNav"] p,
    [data-testid="stSidebar"] [data-testid="stSidebarNav"] a,
    [data-testid="stSidebar"] .st-emotion-cache-1v0mbdj,
    [data-testid="stSidebar"] .st-emotion-cache-1rtdyuf {
        color: #f8fafc !important; font-weight: 500;
    }
    [data-testid="stSidebar"] hr { border-color: #334155; }
    [data-testid="stSidebar"] .st-ec .st-bo,
    [data-testid="stSidebar"] .st-emotion-cache-1rsc3kj { background: transparent; }
    [data-testid="stSidebar"] button {
        background: #334155 !important;
        color: #f8fafc !important;
        border: 1px solid #475569 !important;
    }
    [data-testid="stSidebar"] button:hover {
        background: #475569 !important;
        border-color: #64748b !important;
    }
</style>
""", unsafe_allow_html=True)

# ========== Login Gate ==========
if not st.session_state.logged_in:
    st.markdown('<div class="login-container">', unsafe_allow_html=True)

    col_space, col_form, _ = st.columns([1, 1.2, 1])

    with col_form:
        st.markdown("""
        <div class="login-box">
            <div class="login-logo">🛡️</div>
            <div class="login-title">GEM-F1 安全检测系统</div>
            <div class="login-subtitle">多场景网络安全智能检测平台</div>
        """, unsafe_allow_html=True)

        username = st.text_input("用户名", placeholder="请输入用户名", key="login_user",
                                  label_visibility="collapsed")
        st.markdown('<div style="height:8px"></div>', unsafe_allow_html=True)
        password = st.text_input("密码", placeholder="请输入密码", type="password", key="login_pass",
                                  label_visibility="collapsed")

        st.markdown('<div style="height:12px"></div>', unsafe_allow_html=True)

        if st.button("🔓 登 录", type="primary", use_container_width=True):
            if username and password:
                with st.spinner("验证中..."):
                    time.sleep(0.6)
                st.session_state.logged_in = True
                st.session_state.username = username
                st.rerun()
            else:
                st.error("请输入用户名和密码")

        st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)
    st.stop()

# ========== Sidebar (logged in) ==========
with st.sidebar:
    st.markdown(f"👤 {st.session_state.username}")
    if st.button("退出登录", use_container_width=True):
        st.session_state.logged_in = False
        st.session_state.username = ""
        st.rerun()
    st.divider()

# ========== Hero Banner ==========
st.markdown("""
<div class="hero-banner">
    <div class="hero-title">🛡️ GEM-F1 多场景安全检测系统</div>
    <div class="hero-subtitle">基于贪心期望宏平均F1推理优化的网络安全智能检测平台</div>
</div>
""", unsafe_allow_html=True)

# ========== KPI Row ==========
c1, c2, c3, c4 = st.columns(4)
with c1:
    st.markdown('<div class="kpi-card"><div class="kpi-icon">🌐</div><div class="kpi-label">网络流量分类</div><div class="kpi-value">0.708</div><div class="kpi-desc">Macro F1 · 12类威胁</div></div>', unsafe_allow_html=True)
with c2:
    st.markdown('<div class="kpi-card"><div class="kpi-icon">📋</div><div class="kpi-label">日志异常检测</div><div class="kpi-value">0.913</div><div class="kpi-desc">IoU · 10类异常区间</div></div>', unsafe_allow_html=True)
with c3:
    st.markdown('<div class="kpi-card"><div class="kpi-icon">⚡</div><div class="kpi-label">PowerShell 检测</div><div class="kpi-value">0.680</div><div class="kpi-desc">Macro F1 · GEM-F1 优化</div></div>', unsafe_allow_html=True)
with c4:
    st.markdown('<div class="kpi-card"><div class="kpi-icon">🔐</div><div class="kpi-label">漏洞 CWE 识别</div><div class="kpi-value">轻量</div><div class="kpi-desc">决策树 · 知识蒸馏</div></div>', unsafe_allow_html=True)

# ========== GEM-F1 核心创新 ==========
st.markdown("""
<div class="innovation-box">
    <div class="title">💡 核心创新：GEM-F1 贪心期望宏平均F1推理优化框架</div>
    <div class="bullet">
        🔹 <b>问题建模</b>：将分类推理形式化为以期望 Macro F1 为目标函数的约束优化问题，突破传统逐样本 argmax 与评估指标不一致的次优性<br>
        🔹 <b>组级一致性约束</b>：将特征完全相同的样本归为同一决策单元，既保证"同特征→同标签"的语义一致性，又大幅压缩搜索空间<br>
        🔹 <b>贪心全局优化</b>：以组级配额为决策变量，从 argmax 初始解出发，在最多5000步贪心搜索中调配标签配额<br>
        🔹 <b>实测效果</b>：Macro F1 从 0.6346 提升至 <b>0.6802</b>，相对提升 <b>7.2%</b>，优化742步收敛
    </div>
</div>
""", unsafe_allow_html=True)

# ========== 四大功能模块 ==========
st.markdown('<div class="section-title"><span class="dot"></span>功能模块</div>', unsafe_allow_html=True)

m1, m2 = st.columns(2)
with m1:
    st.markdown('<div class="feature-item"><div class="icon">🌐</div><div class="title">网络流量安全智能分类</div><div class="desc">对抗验证驱动的样本加权 + 5种子LightGBM集成 + 对数空间Bias校准 · 12类威胁分类</div></div>', unsafe_allow_html=True)
    st.markdown('<div class="feature-item"><div class="icon">⚡</div><div class="title">PowerShell 恶意脚本检测</div><div class="desc">核心模块 · GEM-F1贪心推理框架 · 组合键概率回归 · 三分类（正常/一般恶意/混淆恶意）</div></div>', unsafe_allow_html=True)
with m2:
    st.markdown('<div class="feature-item"><div class="icon">📋</div><div class="title">系统日志异常区间检测</div><div class="desc">规则模板+边界偏移学习 · 400条拼写纠错 · LightGBM结构特征 · 6阶段后处理精修</div></div>', unsafe_allow_html=True)
    st.markdown('<div class="feature-item"><div class="icon">🔐</div><div class="title">二进制漏洞 CWE 识别</div><div class="desc">教师模型知识蒸馏至单棵决策树 · 8维静态特征 · OrdinalEncoder编码 · 零额外依赖部署</div></div>', unsafe_allow_html=True)

# ========== Footer ==========
st.markdown('<div class="footer">GEM-F1 Multi-Scenario Security Detection System &copy; 2026 · Built with Streamlit<br>请从左侧导航栏选择功能模块开始检测</div>', unsafe_allow_html=True)
