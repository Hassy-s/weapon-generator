import streamlit as st
import pyperclip

# ジョブデータ（必ず「未選択」を先頭に）
jobs = ["未選択", "戦士", "ナイト", "暗黒", "ガンブレ", "白魔", "学者", "占星", "賢者",
        "モンク", "竜", "忍者", "侍", "リーパー", "ヴァイパー", "詩人", 
        "機工士", "踊り子", "黒魔", "召喚", "赤魔", "ピクマ"]

# 完全な初期化関数
def initialize_state():
    st.session_state.clear()  # 全セッション状態をクリア
    st.session_state.update({
        'pt_members': ["未選択"] * 8,
        'wish_weapons': ["未選択"] * 8
    })

# 初回実行時 or リセット時に初期化
if 'pt_members' not in st.session_state:
    initialize_state()

# ページ設定
st.set_page_config(page_title="希望武器生成ツール", layout="wide")
st.title("⚔️ 希望武器マクロ生成ツール⚔️")

# リセットボタン（ページ最上部に配置）
if st.button("🔄 リセット", type="primary"):
    initialize_state()
    st.rerun()

# メインUI
col1, col2 = st.columns(2)

with col1:
    st.header("PTメンバー")
    for i in range(8):
        # 現在の選択値を安全に取得
        current_value = st.session_state.pt_members[i]
        safe_index = jobs.index(current_value) if current_value in jobs else 0
        
        # Selectboxを作成
        selected = st.selectbox(
            f"PTメンバー {i+1}",
            jobs,
            index=safe_index,
            key=f"pt_select_{i}"  # ユニークなkeyを設定
        )
        st.session_state.pt_members[i] = selected

with col2:
    st.header("希望武器")
    for i in range(8):
        current_value = st.session_state.wish_weapons[i]
        safe_index = jobs.index(current_value) if current_value in jobs else 0
        
        selected = st.selectbox(
            f"希望武器 {i+1}",
            jobs,
            index=safe_index,
            key=f"wish_select_{i}"
        )
        st.session_state.wish_weapons[i] = selected

# 生成処理
output = "\n".join(
    f"/p {pt}さん→{wish}" 
    for pt, wish in zip(st.session_state.pt_members, st.session_state.wish_weapons)
    if pt != "未選択" and wish != "未選択"
)

if output:
    st.code(output)
    
    # クリップボードコピー
    if st.button("📋 クリップボードにコピー"):
        try:
            pyperclip.copy(output)
            st.success("クリップボードにコピーしました！")
            st.balloons()  # 成功アニメーション
        except Exception as e:
            st.error(f"コピー失敗: {e}\n生成されたテキストを手動でコピーしてください")

# デバッグ用（必要に応じて表示）
# with st.expander("デバッグ情報"):
#    st.write("PTメンバー:", st.session_state.pt_members)
#    st.write("希望武器:", st.session_state.wish_weapons)