import streamlit as st
import streamlit.components.v1 as components

# ページ設定（必ず最初に記述）
st.set_page_config(page_title="武器希望制マクロ生成ツール", layout="centered")

# CSSカスタマイズ（中央寄せ＆コンパクト化）
st.markdown(
    """
    <style>
    /* メインコンテナ */
    .main-container {
        display: flex;
        justify-content: center;
        max-width: 1200px;
        margin: 0 auto;
        padding: 0 20px;
    }
    
    /* カラムコンテナ */
    .columns-container {
        display: flex;
        justify-content: center;
        width: 100%;
        gap: 20px;
    }
    
    /* セレクトボックス */
    div[data-baseweb="select"] {
        width: 200px !important;
    }
    
    /* ラベル */
    .stSelectbox > label {
        min-width: 70px;
        max-width: 70px;
        font-size: 14px;
    }
    
    /* 警告エリア */
    .warning-area {
        border-left: 2px solid #ff4b4b;
        padding: 15px;
        margin-left: 15px;
        min-width: 300px;
        background-color: var(--background-color);
        border-radius: 8px;
    }
    
    /* コードブロック */
    .stCodeBlock {
        background-color: var(--background-color) !important;
        border-radius: 8px;
        padding: 10px;
        margin-bottom: 10px;
    }
    
    /* カラム調整 */
    .stColumn {
        padding: 0 5px !important;
    }
    
    /* タイトル中央寄せ */
    .stTitle {
        text-align: center !important;
    }
    
    /* カスタムボタン */
    .copy-btn {
        background-color: #1f77b4 !important;
        border: none !important;
        color: white !important;
        padding: 0.5rem 1rem !important;
        text-align: center !important;
        text-decoration: none !important;
        display: inline-block !important;
        font-size: 14px !important;
        margin: 4px 0 !important;
        cursor: pointer !important;
        border-radius: 0.25rem !important;
        width: 100% !important;
        font-family: inherit !important;
        line-height: 1.5 !important;
        transition: all 0.2s ease-in-out !important;
    }
    
    .copy-btn:hover {
        background-color: #1668a7 !important;
    }
    
    /* ボタンコンテナ */
    .copy-btn-container {
        background-color: var(--background-color);
        padding: 0;
        margin: 0;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# ジョブデータ
jobs = ["未選択", "戦士", "ナイト", "暗黒", "ガンブレ", "白魔", "学者", "占星", "賢者",
        "モンク", "竜", "忍者", "侍", "リーパー", "ヴァイパー", "詩人", 
        "機工士", "踊り子", "黒魔", "召喚", "赤魔", "ピクマ"]

# 初期化関数
def initialize_state():
    st.session_state.clear()
    st.session_state.update({
        'pt_members': ["未選択"] * 8,
        'wish_weapons': ["未選択"] * 8
    })

# 初回初期化
if 'pt_members' not in st.session_state:
    initialize_state()

# タイトル（中央寄せ）
st.markdown('<div class="stTitle">', unsafe_allow_html=True)
st.title("⚔️ 武器希望制マクロ生成ツール⚔️")
st.markdown('</div>', unsafe_allow_html=True)

# リセットボタン（中央寄せ）
col_btn, _ = st.columns([1, 3])
with col_btn:
    if st.button("🔄 リセット", type="primary"):
        initialize_state()
        st.rerun()

# メインコンテンツ - 3列レイアウト（中央寄せ）
st.markdown('<div class="main-container"><div class="columns-container">', unsafe_allow_html=True)

# 第1カラム（PTメンバー）
col1, col2, col3 = st.columns([1.3, 1.3, 1.9], gap="medium")

with col1:
    st.header("PTリスト")
    for i in range(8):
        current_value = st.session_state.pt_members[i]
        safe_index = jobs.index(current_value) if current_value in jobs else 0
        selected = st.selectbox(
            f"メンバー {i+1}",
            jobs,
            index=safe_index,
            key=f"pt_select_{i}"
        )
        st.session_state.pt_members[i] = selected

# 第2カラム（希望武器）
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

# 第3カラム（チェック結果 & マクロ）
with col3:
    st.header("警告＆マクロ")
    st.markdown('<div class="warning-area">', unsafe_allow_html=True)
    
    # チェック処理
    pt_jobs = [j for j in st.session_state.pt_members if j != "未選択"]
    wish_list = [w for w in st.session_state.wish_weapons if w != "未選択"]
    
    # 重複チェック
    pt_duplicates = [j for j in set(pt_jobs) if pt_jobs.count(j) > 1]
    if pt_duplicates:
        st.warning(f"⚠️ PTジョブ重複: {', '.join(pt_duplicates)}")

    wish_duplicates = [w for w in set(wish_list) if wish_list.count(w) > 1]
    if wish_duplicates:
        st.warning(f"⚠️ 武器重複: {', '.join(wish_duplicates)}")

    # 未選択チェック
    if len(pt_jobs) < 8:
        st.warning("⚠️ PTに未選択あり")
    if len(wish_list) < 8:
        st.warning("⚠️ 武器に未選択あり")

    # マクロ生成
    output = "\n".join(
        f"/p {pt}さん→{wish}" 
        for pt, wish in zip(st.session_state.pt_members, st.session_state.wish_weapons)
        if pt != "未選択" and wish != "未選択"
    )

    if output:
        output += "\n/p 希望武器に間違いなければRC◯下さい<wait.3>\n/readycheck"
        st.code(output)
        
        # クリップボードコピー用のJavaScript
        copy_script = f"""
        <script>
        function copyToClipboard() {{
            const text = `{output}`;
            navigator.clipboard.writeText(text)
                .then(() => {{
                    const copyBtn = document.getElementById('copyBtn');
                    copyBtn.textContent = '✅ コピー完了！';
                    setTimeout(() => {{
                        copyBtn.textContent = '📋 クリップボードにコピー';
                    }}, 2000);
                }})
                .catch(err => {{
                    alert('クリップボードへのコピーに失敗しました: ' + err);
                }});
        }}
        </script>
        """
        
        # ボタンの作成
        components.html(
            f"""
            <div class="copy-btn-container">
                {copy_script}
                <button id="copyBtn" onclick="copyToClipboard()" class="copy-btn">
                    📋 クリップボードにコピー
                </button>
            </div>
            """,
            height=50
        )
    
    st.markdown('</div>', unsafe_allow_html=True)

st.markdown('</div></div>', unsafe_allow_html=True)
