import streamlit as st
import pandas as pd


def render_streamlit_panel(placeholder, state: dict) -> None:
    """左カラム: Streamlit Cloud の状態を描画"""
    with placeholder.container():
        if state["is_crashed"]:
            st.markdown(
                """
                <div style="background:#ff4b4b;color:white;padding:20px;border-radius:8px;
                            text-align:center;animation:blink 0.5s step-start infinite;">
                    <h2 style="margin:0;">⚡ SYSTEM CRASH ⚡</h2>
                    <p style="font-size:1.2em;margin:8px 0;">503 Service Unavailable</p>
                    <p style="margin:0;">大量アクセスによりサーバーが停止しました</p>
                </div>
                """,
                unsafe_allow_html=True,
            )
            st.metric("CPU使用率", "100%")
            st.progress(1.0)
            st.metric("応答時間", "タイムアウト")
            st.metric("現在のアクセス数", f"{state['current_users']:,}人")
            st.error("スケールアウト不可のため復旧できません")
        else:
            cpu = state["cpu"]
            mem = state["memory"]
            rt = state["response_time"]

            col1, col2 = st.columns(2)
            with col1:
                st.metric("CPU使用率", f"{cpu:.0f}%")
                st.progress(min(cpu / 100, 1.0))
            with col2:
                st.metric("メモリ使用率", f"{mem:.0f}%")
                st.progress(min(mem / 100, 1.0))

            st.metric("応答時間", f"{rt:.1f}秒")
            st.metric("現在のアクセス数", f"{state['current_users']:,}人")

            if cpu >= 90:
                st.error("CPU使用率が危険域！もうすぐクラッシュします")
            elif cpu >= 70:
                st.warning("CPU使用率が高くなっています（スケールアウト不可）")
            else:
                st.success("正常稼働中")


def render_aws_panel(placeholder, state: dict) -> None:
    """右カラム: AWS / Azure の状態を描画"""
    with placeholder.container():
        # ロードバランサー
        st.markdown(
            """
            <div style="background:#fff3cd;border:2px solid #ffc107;padding:10px 16px;
                        border-radius:8px;text-align:center;margin-bottom:12px;">
                🔀 <strong>ロードバランサー</strong>　リクエストを自動で振り分け
            </div>
            """,
            unsafe_allow_html=True,
        )

        # スケールアウトイベント通知
        if state.get("scale_event"):
            st.toast(f"🚀 オートスケール: {state['scale_event']}", icon="🚀")

        # EC2インスタンス表示（最大4台まで横並び、超過分は別表示）
        instances = state["instances"]
        display_count = min(instances, 4)
        cols = st.columns(display_count)
        cpu_i = state["cpu_per_instance"]
        color = "#d4edda" if cpu_i < 70 else "#fff3cd"

        for i, col in enumerate(cols):
            with col:
                st.markdown(
                    f"""
                    <div style="background:{color};border:1px solid #aaa;padding:10px 6px;
                                border-radius:6px;text-align:center;font-size:0.85em;">
                        <strong>EC2-{i+1}</strong><br>
                        CPU: {cpu_i:.0f}%
                    </div>
                    """,
                    unsafe_allow_html=True,
                )

        if instances > 4:
            st.caption(f"+ {instances - 4}台 稼働中（合計 {instances}台）")

        st.metric("応答時間", f"{state['response_time']:.1f}秒")
        st.metric("現在のアクセス数", f"{state['current_users']:,}人")
        st.metric("稼働インスタンス数", f"{instances}台")
        st.success(f"安定稼働中（{instances}台でロードバランシング）")


def render_chart(placeholder, chart_data: pd.DataFrame) -> None:
    """応答時間の推移グラフを描画"""
    with placeholder.container():
        if chart_data.empty or chart_data.dropna(how="all").empty:
            return
        st.line_chart(
            chart_data,
            color=["#ff4b4b", "#1f77b4"],
        )
