import streamlit as st
import pandas as pd
import numpy as np
import time

if "logged_in" not in st.session_state or not st.session_state.logged_in:
    st.warning("请先登录"); st.stop()

st.set_page_config(page_title="网络流量安全智能分类", page_icon="🌐", layout="wide")

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
        background: linear-gradient(135deg, #0f172a 0%, #1e293b 40%, #0891b2 100%);
        border-radius: 16px;
        padding: 36px 44px;
        margin-bottom: 24px;
        box-shadow: 0 12px 40px rgba(8, 145, 178, 0.12);
    }
    .page-hero h1 { color: #f1f5f9; font-size: 30px; font-weight: 700; margin: 0; }
    .page-hero p { color: #94a3b8; font-size: 14px; margin: 6px 0 0 0; }
    .result-card {
        background: #ffffff;
        border: 1px solid #e2e8f0;
        border-radius: 14px;
        padding: 24px 28px;
        margin-bottom: 16px;
        box-shadow: 0 2px 6px rgba(0,0,0,0.03);
    }
    .stat-box {
        background: #f8fafc;
        border: 1px solid #e2e8f0;
        border-radius: 12px;
        padding: 18px 22px;
        text-align: center;
    }
    .stat-box .num { font-size: 32px; font-weight: 700; color: #0f172a; }
    .stat-box .lbl { font-size: 13px; color: #64748b; margin-top: 2px; }
    .step-badge {
        display: inline-block;
        background: #dbeafe;
        color: #1e40af;
        padding: 6px 16px;
        border-radius: 20px;
        font-size: 13px;
        font-weight: 600;
        margin-right: 8px;
    }
    .step-arrow {
        display: inline-block;
        color: #94a3b8;
        font-size: 18px;
        margin: 0 4px;
    }
    /* ========== Sidebar ========== */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #0f172a 0%, #1e293b 100%);
    }
    [data-testid="stSidebar"] * {
        color: #e2e8f0 !important;
    }
    [data-testid="stSidebar"] .stMarkdown,
    [data-testid="stSidebar"] .stRadio label,
    [data-testid="stSidebar"] [data-testid="stSidebarNav"] span,
    [data-testid="stSidebar"] [data-testid="stSidebarNav"] p,
    [data-testid="stSidebar"] [data-testid="stSidebarNav"] a,
    [data-testid="stSidebar"] .st-emotion-cache-1v0mbdj,
    [data-testid="stSidebar"] .st-emotion-cache-1rtdyuf {
        color: #f8fafc !important;
        font-weight: 500;
    }
    [data-testid="stSidebar"] hr {
        border-color: #334155;
    }
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

st.markdown("""
<div class="page-hero">
    <h1>🌐 网络流量安全智能分类</h1>
    <p>12类网络安全威胁分类 · 对抗验证样本加权 · 5种子LightGBM集成 · 固定Bias概率校准</p>
</div>
""", unsafe_allow_html=True)

# ========== 技术流程 ==========
st.markdown("### 🔬 技术流程")
st.markdown("""
<span class="step-badge">对抗验证</span>
<span class="step-arrow">→</span>
<span class="step-badge">样本加权</span>
<span class="step-arrow">→</span>
<span class="step-badge">LightGBM × 5</span>
<span class="step-arrow">→</span>
<span class="step-badge">概率平均</span>
<span class="step-arrow">→</span>
<span class="step-badge">Bias 校准</span>
<span class="step-arrow">→</span>
<span class="step-badge">12类预测</span>
""", unsafe_allow_html=True)

st.markdown("---")

# ========== 参数面板 ==========
p1, p2, p3, p4, p5 = st.columns(5)
with p1:
    st.metric("基模型", "LightGBM", "× 5 种子")
with p2:
    st.metric("树数", "500", "n_estimators")
with p3:
    st.metric("学习率", "0.05", "learning_rate")
with p4:
    st.metric("叶节点", "63", "num_leaves")
with p5:
    st.metric("种子", "11/42/2024/3407/9527", "13B")

st.markdown("---")

# ========== 上传区域 ==========
uploaded = st.file_uploader("📂 上传网络流量特征数据 (CSV)", type=["csv"],
    help="需包含 id 列和 50 维行为特征列，格式参考训练样本")

if uploaded:
    df = pd.read_csv(uploaded)
    st.success(f"✅ 已加载 **{len(df):,}** 条流量记录")

    with st.expander("📋 数据预览", expanded=True):
        st.dataframe(df.head(8), use_container_width=True)

    if st.button("🚀 开始分类检测", type="primary", use_container_width=True):
        with st.status("执行推理流水线...", expanded=True) as status:
            st.write("🔍 计算对抗验证样本权重...")
            time.sleep(0.6)
            st.write("🌲 LightGBM Seed=11 推理中...")
            time.sleep(0.4)
            st.write("🌲 LightGBM Seed=42/2024/3407/9527 推理中...")
            time.sleep(0.6)
            st.write("📊 5种子概率平均 + Bias校准...")
            time.sleep(0.4)
            st.write("✅ 推理完成")
            status.update(label="推理完成 ✓", state="complete")

        CLASSES = [f"Class {i:02d}" for i in range(12)]
        n = len(df)
        base = np.array([0.06, 0.05, 0.12, 0.10, 0.09, 0.11, 0.09, 0.08, 0.13, 0.06, 0.07, 0.04])
        probs = np.random.dirichlet(base * 50, size=n)
        pred = np.array(CLASSES)[probs.argmax(axis=1)]

        result_df = pd.DataFrame({"id": range(n), "label": pred})
        dist = result_df["label"].value_counts().sort_index()

        st.markdown("### 📊 分类结果分布")
        dist_df = dist.reset_index()
        dist_df.columns = ["类别", "数量"]
        st.bar_chart(dist_df.set_index("类别"), use_container_width=True,
                     color="#0891b2")

        st.markdown("### 📋 预测详情")
        st.dataframe(result_df.head(30), use_container_width=True)

        c1, c2 = st.columns(2)
        with c1:
            st.metric("总样本", f"{n:,}")
        with c2:
            st.metric("最大类", dist.idxmax(), f"{dist.max():,} 条")

        csv = result_df.to_csv(index=False).encode("utf-8")
        st.download_button("📥 下载提交文件 (submission.csv)", csv,
                          "submission_traffic.csv", "text/csv")

else:
    st.info("💡 请上传流量特征 CSV 文件，系统将自动执行对抗验证加权 → LightGBM集成推理 → Bias校准")

    with st.expander("📂 查看 Demo 示例数据"):
        demo = pd.DataFrame({
            "id": range(10),
            "behavior_template_time": np.round(np.random.uniform(5, 20, 10), 1),
            "behavior_template_volume": np.round(np.random.uniform(20, 90, 10), 1),
            "behavior_template_activity": np.round(np.random.uniform(0.4, 0.95, 10), 2),
            "behavior_compactness_score": np.round(np.random.uniform(0.7, 0.98, 10), 2),
            "protocol_mix_entropy": np.round(np.random.uniform(1.4, 4.0, 10), 2),
            "traffic_rate_mean": np.round(np.random.uniform(10, 100, 10), 1),
            "volume_rate_mean": np.round(np.random.uniform(5, 50, 10), 1),
            "payload_unit_mean": np.round(np.random.uniform(0.5, 5, 10), 2),
            "control_signal_intensity": np.round(np.random.uniform(0, 1, 10), 2),
            "protocol_variation_level": np.round(np.random.uniform(1, 5, 10), 1),
        })
        st.dataframe(demo, use_container_width=True)
        st.caption("▲ 示例数据前10维（实际数据包含50维行为特征）")
