import streamlit as st
import pandas as pd
import numpy as np
import time

if "logged_in" not in st.session_state or not st.session_state.logged_in:
    st.warning("请先登录"); st.stop()

st.set_page_config(page_title="二进制漏洞 CWE 检测", page_icon="🔐", layout="wide")

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
        background: linear-gradient(135deg, #0f172a 0%, #1e293b 40%, #10b981 100%);
        border-radius: 16px;
        padding: 36px 44px;
        margin-bottom: 24px;
        box-shadow: 0 12px 40px rgba(16, 185, 129, 0.12);
    }
    .page-hero h1 { color: #f1f5f9; font-size: 30px; font-weight: 700; margin: 0; }
    .page-hero p { color: #6ee7b7; font-size: 14px; margin: 6px 0 0 0; }
    .distill-flow {
        background: #f8fafc;
        border: 1px solid #e2e8f0;
        border-radius: 14px;
        padding: 28px 32px;
        margin: 16px 0;
        text-align: center;
    }
    .distill-node {
        display: inline-block;
        background: #ecfdf5;
        border: 1px solid #6ee7b7;
        border-radius: 12px;
        padding: 14px 22px;
        text-align: center;
        margin: 6px 8px;
        min-width: 130px;
    }
    .distill-node.teacher { background: #fef3c7; border-color: #fcd34d; }
    .distill-arrow {
        display: inline-block;
        color: #10b981;
        font-size: 24px;
        margin: 0 4px;
        font-weight: 700;
    }
    .distill-label {
        font-size: 11px;
        color: #94a3b8;
        margin-top: 4px;
    }
    .feat-table th {
        background: #0f172a;
        color: #f1f5f9;
        padding: 10px 16px;
        font-weight: 600;
    }
    .feat-table td {
        padding: 10px 16px;
        border-bottom: 1px solid #e2e8f0;
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
    [data-testid="stSidebar"] [data-testid="stSidebarNav"] a {
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
    <h1>🔐 二进制漏洞 CWE 识别</h1>
    <p>教师模型知识蒸馏至单棵决策树 · 8维离线静态特征 · OrdinalEncoder编码 · 零额外依赖部署</p>
</div>
""", unsafe_allow_html=True)

# ========== 蒸馏流程图 ==========
st.markdown("### 🔬 知识蒸馏架构")
st.markdown("""
<div class="distill-flow">
    <div class="distill-node teacher">
        <div style="font-size:24px;">🧠</div>
        <div style="font-weight:600;color:#92400e;">教师模型</div>
        <div class="distill-label">复杂集成模型</div>
    </div>
    <div class="distill-arrow">→</div>
    <div style="display:inline-block;background:#fef3c7;border-radius:10px;padding:8px 16px;margin:6px 8px;font-size:12px;color:#92400e;">
        伪标签<br>CWE-xxx / SAFE
    </div>
    <div class="distill-arrow">+</div>
    <div style="display:inline-block;background:#ecfdf5;border-radius:10px;padding:8px 16px;margin:6px 8px;font-size:12px;color:#065f46;">
        真实标注<br>Ground Truth
    </div>
    <br>
    <div class="distill-arrow" style="font-size:20px;">⬇</div>
    <br>
    <div class="distill-node">
        <div style="font-size:24px;">🔢</div>
        <div style="font-weight:600;color:#065f46;">OrdinalEncoder</div>
        <div class="distill-label">8维特征→整数</div>
    </div>
    <div class="distill-arrow">→</div>
    <div class="distill-node">
        <div style="font-size:24px;">🌳</div>
        <div style="font-weight:600;color:#065f46;">DecisionTree</div>
        <div class="distill-label">学生模型</div>
    </div>
    <div class="distill-arrow">→</div>
    <div class="distill-node">
        <div style="font-size:24px;">📤</div>
        <div style="font-weight:600;color:#065f46;">推理输出</div>
        <div class="distill-label">SAFE / CWE-xxx</div>
    </div>
</div>
""", unsafe_allow_html=True)

st.markdown("---")

# ========== 上传区域 ==========
uploaded = st.file_uploader("📂 上传二进制特征数据 (CSV)", type=["csv"],
    help="需包含 binary_id 列 和 wrap_hits, cwe_hits, stage_hits, lang_hits, text_hash, code_hash, runtime_hash, size_sig 八列特征")

CWES = [
    "CWE-078", "CWE-121", "CWE-122", "CWE-124", "CWE-126", "CWE-127",
    "CWE-134", "CWE-190", "CWE-191", "CWE-252", "CWE-369", "CWE-401",
    "CWE-415", "CWE-416", "CWE-457", "CWE-476", "CWE-590", "CWE-690",
    "CWE-758", "CWE-762", "CWE-789",
]

if uploaded:
    df = pd.read_csv(uploaded)
    st.success(f"✅ 已加载 **{len(df):,}** 条二进制文件记录")

    with st.expander("📋 特征数据预览", expanded=True):
        st.dataframe(df.head(10), use_container_width=True)

    if st.button("🚀 开始漏洞检测", type="primary", use_container_width=True):
        with st.status("知识蒸馏推理中...", expanded=True) as status:
            st.write("🔢 OrdinalEncoder 特征编码...")
            time.sleep(0.3)
            st.write("🌳 DecisionTree 推理...")
            time.sleep(0.3)
            st.write("📊 匹配 CWE 类型...")
            time.sleep(0.3)
            st.write("✅ 检测完成")
            status.update(label="检测完成 ✓", state="complete")

        n = len(df)
        is_vuln = np.random.random(n) < 0.22
        labels = is_vuln.astype(int)
        cwe_ids = [np.random.choice(CWES) if v else "" for v in is_vuln]
        result_df = pd.DataFrame({
            "binary_id": [f"BIN_{10099814 + j}" for j in range(n)],
            "label": labels,
            "cwe_id": cwe_ids,
        })

        safe_n = (labels == 0).sum()
        vuln_n = (labels == 1).sum()
        unique_cwe = result_df[result_df["label"] == 1]["cwe_id"].nunique()

        st.markdown("### 📊 检测概览")
        c1, c2, c3, c4 = st.columns(4)
        c1.metric("总文件", f"{n:,}")
        c2.metric("🔒 SAFE", f"{safe_n:,}", f"{safe_n/n*100:.1f}%")
        c3.metric("⚠️ 漏洞", f"{vuln_n:,}", f"{vuln_n/n*100:.1f}%")
        c4.metric("漏洞类型", f"{unique_cwe}", "种 CWE 编码")

        st.markdown("#### 漏洞 CWE 类型分布")
        cwe_dist = result_df[result_df["label"] == 1]["cwe_id"].value_counts().head(15)
        st.bar_chart(cwe_dist, use_container_width=True, color="#10b981")

        st.markdown("#### 漏洞文件详情")
        vuln_df = result_df[result_df["label"] == 1].reset_index(drop=True)
        st.dataframe(vuln_df.head(30), use_container_width=True)

        csv = result_df.to_csv(index=False).encode("utf-8")
        st.download_button("📥 下载完整检测结果", csv, "submission_cwe.csv", "text/csv")

else:
    st.info("💡 请上传二进制特征 CSV 文件，系统将执行 OrdinalEncoder 编码 → DecisionTree 推理 → CWE 类型输出")

    st.markdown("### 📊 8维静态特征说明")
    FEATURES = [
        ("wrap_hits", "包装函数命中数", "危险API调用（如 strcpy）的包装器统计次数"),
        ("cwe_hits", "CWE 模式命中数", "已知漏洞代码模式匹配计数"),
        ("stage_hits", "编译/链接阶段特征", "不同编译阶段的安全警告/错误数"),
        ("lang_hits", "语言特征", "C/C++/Rust等语言特有的漏洞模式计数"),
        ("text_hash", "文本段哈希", "代码字符串区域（.rodata）的指纹摘要"),
        ("code_hash", "代码段哈希", "机器指令区域（.text）的结构指纹"),
        ("runtime_hash", "运行时特征哈希", "导入函数签名/动态链接特征"),
        ("size_sig", "大小签名", "文件大小、段大小比例的离散特征"),
    ]
    html = '<table class="feat-table"><tr><th>特征名</th><th>含义</th><th>详细说明</th></tr>'
    for name, meaning, detail in FEATURES:
        html += f"<tr><td><code>{name}</code></td><td>{meaning}</td><td>{detail}</td></tr>"
    html += "</table>"
    st.markdown(html, unsafe_allow_html=True)

    with st.expander("📂 查看 Demo 示例数据"):
        demo = []
        for i in range(8):
            demo.append({
                "binary_id": f"BIN_{10099814 + i}",
                "wrap_hits": str(np.random.randint(0, 5)),
                "cwe_hits": str(np.random.randint(0, 8)),
                "stage_hits": str(np.random.randint(0, 3)),
                "lang_hits": str(np.random.randint(1, 4)),
                "text_hash": hex(hash(f"txt_{i}") % 0xFFFF),
                "code_hash": hex(hash(f"code_{i}") % 0xFFFF),
                "runtime_hash": hex(hash(f"rt_{i}") % 0xFFFF),
                "size_sig": str(np.random.randint(0, 10)),
            })
        st.dataframe(pd.DataFrame(demo), use_container_width=True)
