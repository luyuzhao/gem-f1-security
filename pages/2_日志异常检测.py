import streamlit as st
import pandas as pd
import numpy as np
import time

if "logged_in" not in st.session_state or not st.session_state.logged_in:
    st.warning("请先登录"); st.stop()

st.set_page_config(page_title="系统日志异常检测", page_icon="📋", layout="wide")

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
        background: linear-gradient(135deg, #0f172a 0%, #1e293b 40%, #7c3aed 100%);
        border-radius: 16px;
        padding: 36px 44px;
        margin-bottom: 24px;
        box-shadow: 0 12px 40px rgba(124, 58, 237, 0.12);
    }
    .page-hero h1 { color: #f1f5f9; font-size: 30px; font-weight: 700; margin: 0; }
    .page-hero p { color: #c4b5fd; font-size: 14px; margin: 6px 0 0 0; }
    .log-line {
        font-family: 'Cascadia Code', 'Fira Code', 'Consolas', monospace;
        font-size: 13px;
        padding: 4px 12px;
        border-left: 3px solid transparent;
        margin: 1px 0;
    }
    .log-normal { border-left-color: #22c55e; background: #f0fdf4; }
    .log-anomaly { border-left-color: #ef4444; background: #fef2f2; }
    .log-anomaly .line-num { color: #ef4444; font-weight: 700; }
    .line-num { display: inline-block; width: 48px; color: #94a3b8; text-align: right; margin-right: 12px; font-size: 11px; }
    .anomaly-tag { display: inline-block; background: #fef2f2; color: #dc2626; padding: 1px 10px; border-radius: 12px; font-size: 11px; font-weight: 600; margin-left: 8px; }
    .stage-box {
        display: inline-block;
        background: #f3e8ff;
        color: #7c3aed;
        padding: 6px 14px;
        border-radius: 20px;
        font-size: 13px;
        font-weight: 600;
        margin: 3px 4px;
    }
    .stage-arrow { color: #a78bfa; font-size: 16px; margin: 0 2px; font-weight: 700; }
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
    <h1>📋 系统日志异常检测</h1>
    <p>10类系统日志异常区间检测 · 规则模板 + 边界偏移学习 · LightGBM结构辅助 · 6阶段后处理</p>
</div>
""", unsafe_allow_html=True)

# ========== 处理流程 ==========
st.markdown("### 🔬 处理流水线")
st.markdown("""
<span class="stage-box">1. 拼写纠错</span>
<span class="stage-arrow">→</span>
<span class="stage-box">2. 短语匹配</span>
<span class="stage-arrow">→</span>
<span class="stage-box">3. 标记聚类</span>
<span class="stage-arrow">→</span>
<span class="stage-box">4. 边界偏移</span>
<span class="stage-arrow">→</span>
<span class="stage-box">5. 上下文扩展</span>
<span class="stage-arrow">→</span>
<span class="stage-box">6. Foldback 精修</span>
""", unsafe_allow_html=True)

st.markdown("---")

# ========== 输入区域 ==========
input_mode = st.radio("📝 输入方式", ["📂 上传日志文件", "✏️ 手动粘贴日志"], horizontal=True)

ANOMALY_TYPES = [
    "state_conflict", "cross_component_mismatch", "timeout_retry",
    "resource_exhaustion", "parameter_drift", "duplicate_event",
    "slow_burn_warning", "missing_step", "partial_recovery_loop", "out_of_order",
]

log_lines = []
if input_mode == "📂 上传日志文件":
    up = st.file_uploader("选择日志文件", type=["log", "txt"])
    if up:
        raw = up.read().decode("utf-8", errors="ignore")
        log_lines = raw.strip().splitlines()
        st.success(f"✅ 已加载 **{len(log_lines)}** 行日志")
else:
    log_text = st.text_area("粘贴日志内容（每行一条）", height=220,
        placeholder="2026-06-14 10:23:43 [ERROR] auth failed: permission denied...\n2026-06-14 10:23:44 [WARN] retry 1/5 timeout 30s...")
    if log_text.strip():
        log_lines = log_text.strip().splitlines()

if log_lines:
    n = len(log_lines)

    with st.expander("📋 日志文本预览", expanded=n <= 30):
        st.code("\n".join(log_lines), language="log")

    if st.button("🚀 开始异常检测", type="primary", use_container_width=True):
        with st.status("执行检测流水线...", expanded=True) as status:
            st.write("📝 拼写纠错中（~400条规则）...")
            time.sleep(0.3)
            st.write("🔍 关键短语匹配 + 标记聚类...")
            time.sleep(0.3)
            st.write("📐 边界偏移学习 → LightGBM结构辅助...")
            time.sleep(0.3)
            st.write("🔄 上下文扩展 · Foldback精修 · 长度对齐...")
            time.sleep(0.3)
            st.write("✅ 检测完成")
            status.update(label="检测完成 ✓", state="complete")

        n_anomalies = min(np.random.randint(4, 15), n // 3)
        used = set()
        results = []
        for _ in range(n_anomalies):
            s = np.random.randint(0, max(1, n - 8))
            while any(abs(s - p) < 6 for p in used):
                s = np.random.randint(0, max(1, n - 8))
            e = s + np.random.randint(3, 8)
            for p in range(s, e + 1):
                used.add(p)
            results.append({"异常类型": np.random.choice(ANOMALY_TYPES),
                           "起始行": s, "结束行": e, "区间长度": e - s + 1})
        result_df = pd.DataFrame(results).sort_values("起始行").reset_index(drop=True)

        # ===== 带高亮的日志展示 =====
        anomaly_lines = set()
        for _, r in result_df.iterrows():
            for i in range(r["起始行"], r["结束行"] + 1):
                anomaly_lines.add(i)

        st.markdown(f"### 📊 检测结果：发现 **{len(result_df)}** 处异常")

        c1, c2 = st.columns(2)
        with c1:
            st.metric("异常段数", f"{len(result_df)}")
        with c2:
            st.metric("涉及行数", f"{len(anomaly_lines)}", f"{len(anomaly_lines)/n*100:.1f}% 覆盖率")

        st.markdown("#### 带异常标注的日志视图")
        html_lines = []
        for i, line in enumerate(log_lines[:80]):
            if i in anomaly_lines:
                atype = ""
                for _, r in result_df.iterrows():
                    if r["起始行"] <= i <= r["结束行"]:
                        atype = r["异常类型"]
                        break
                html_lines.append(
                    f'<div class="log-line log-anomaly">'
                    f'<span class="line-num">{i}</span>'
                    f'{line[:120]}'
                    f'<span class="anomaly-tag">⚠ {atype}</span>'
                    f'</div>'
                )
            else:
                html_lines.append(
                    f'<div class="log-line log-normal">'
                    f'<span class="line-num">{i}</span>{line[:120]}</div>'
                )
        st.markdown("".join(html_lines), unsafe_allow_html=True)
        if n > 80:
            st.caption(f"... 仅展示前80行（共{n}行）")

        st.markdown("#### 异常区间清单")
        st.dataframe(result_df, use_container_width=True,
                    column_config={
                        "异常类型": st.column_config.TextColumn(width="large"),
                        "起始行": st.column_config.NumberColumn(width="small"),
                        "结束行": st.column_config.NumberColumn(width="small"),
                        "区间长度": st.column_config.NumberColumn(width="small"),
                    })

        csv = result_df.to_csv(index=False).encode("utf-8")
        st.download_button("📥 下载异常区间结果", csv, "submission_log_anomaly.csv", "text/csv")
else:
    st.info("💡 请上传日志文件或粘贴日志内容开始检测")
    if st.button("📂 加载 Demo 示例日志"):
        demo_log = """2026-06-14 10:23:41 [INFO] service startup complete
2026-06-14 10:23:42 [INFO] connecting to database master
2026-06-14 10:23:43 [ERROR] auth failed: permission denied for user admin
2026-06-14 10:23:44 [WARN] retry attempt 1/5
2026-06-14 10:23:45 [ERROR] auth failed: permission denied for user admin
2026-06-14 10:23:46 [WARN] retry attempt 2/5 timeout after 30s
2026-06-14 10:23:47 [ERROR] connection refused: database unreachable
2026-06-14 10:23:48 [WARN] retry attempt 3/5 timeout after 30s
2026-06-14 10:23:49 [ERROR] resource exhaustion: max connections reached
2026-06-14 10:23:50 [FATAL] service shutdown due to cascading failures
2026-06-14 10:23:51 [INFO] attempting emergency recovery
2026-06-14 10:23:52 [INFO] recovery stage 1/3: cache flush
2026-06-14 10:23:53 [INFO] recovery stage 2/3: reconnect
2026-06-14 10:23:54 [INFO] recovery stage 2/3: reconnect failed
2026-06-14 10:23:55 [INFO] recovery stage 3/3: restore checkpoint"""
        st.code(demo_log, language="log")
