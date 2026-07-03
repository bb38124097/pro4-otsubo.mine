from datetime import date
import sqlite3
import streamlit as st

# あなたが作った「Control(司令塔)」と「Entity(データ)」のクラスをインポート
from control.meal_schedule_manager import MealScheduleManager
from entity.group_calendar import GroupCalendar

# ページの初期設定
st.set_page_config(
    page_title="おうちのご飯管理アプリ（正式版）", page_icon="🏠", layout="wide"
)

# --- シーケンス図の登場人物（オブジェクト）を準備 ---
if "meal_manager" not in st.session_state:
    st.session_state.meal_manager = MealScheduleManager()

if "group_calendar" not in st.session_state:
    st.session_state.group_calendar = GroupCalendar(
        group_id="g_001", group_name="大坪・三根家"
    )

manager = st.session_state.meal_manager
my_group_cal = st.session_state.group_calendar


# --- 画面レイアウト ---
st.title(f"🏠 {my_group_cal.group_name} のご飯管理システム")
st.write("【正式設計準拠】Boundary ➔ Control ➔ Entity の連携アプリです。")

# 画面を左（各自の入力）と右（全員の確認）に分割
col_input, col_view = st.columns([1, 1])


# --- 👥 左側：各ユーザーの入力エリア（Boundaryの役割） ---
with col_input:
    st.header("📝 自分の予定を登録")

    # テスト用のユーザースイッチ
    selected_user = st.selectbox(
        "あなたのお名前は？", ["選択してください", "user_father", "user_sister"]
    )

    if selected_user != "選択してください":
        target_date = st.date_input("対象の日付", date.today())
        date_str = str(target_date)  # DB検索用に文字列に変換

        st.markdown(f"**{selected_user}** さんの **{date_str}** の予定を入力中...")

        # フォームの作成
        with st.form(key="input_form"):
            needs_meal = st.radio("今日の夕飯は？", ("必要", "不要"))
            return_