import streamlit as st
import re

# ─────────────────────────────────────────────
# ページ設定（必ず先頭に）
# ─────────────────────────────────────────────
st.set_page_config(
    page_title="名簿スペース一括成形ツール",
    page_icon="✏️",
    layout="wide",
)

# ─────────────────────────────────────────────
# カスタム CSS
# ─────────────────────────────────────────────
st.markdown(
    """
    <style>
    /* Google Fonts */
    @import url('https://fonts.googleapis.com/css2?family=Noto+Sans+JP:wght@400;500;700&family=Inter:wght@400;600;700&display=swap');

    html, body, [class*="css"] {
        font-family: 'Noto Sans JP', 'Inter', sans-serif;
    }

    /* 背景グラデーション */
    .stApp {
        background: linear-gradient(135deg, #0f0c29 0%, #302b63 50%, #24243e 100%);
        min-height: 100vh;
    }

    /* ヘッダー */
    .hero-header {
        text-align: center;
        padding: 2.5rem 1rem 1.5rem;
        margin-bottom: 1.5rem;
    }
    .hero-title {
        font-size: 2.8rem;
        font-weight: 700;
        background: linear-gradient(90deg, #a78bfa, #60a5fa, #34d399);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        letter-spacing: 0.02em;
        margin-bottom: 0.4rem;
    }
    .hero-sub {
        font-size: 1.05rem;
        color: #94a3b8;
        font-weight: 400;
    }

    /* カード */
    .glass-card {
        background: rgba(255,255,255,0.06);
        border: 1px solid rgba(255,255,255,0.12);
        border-radius: 16px;
        padding: 1.6rem 1.8rem;
        backdrop-filter: blur(12px);
        margin-bottom: 1.2rem;
        box-shadow: 0 8px 32px rgba(0,0,0,0.3);
    }
    .card-label {
        font-size: 0.85rem;
        font-weight: 600;
        letter-spacing: 0.08em;
        color: #a78bfa;
        text-transform: uppercase;
        margin-bottom: 0.6rem;
    }

    /* ラジオボタン */
    div[data-testid="stRadio"] label {
        color: #e2e8f0 !important;
        font-size: 1rem;
    }

    /* テキストエリア */
    textarea {
        background: rgba(15,12,41,0.7) !important;
        border: 1px solid rgba(167,139,250,0.3) !important;
        border-radius: 10px !important;
        color: #e2e8f0 !important;
        font-family: 'Noto Sans JP', monospace !important;
        font-size: 0.95rem !important;
        line-height: 1.7 !important;
        resize: vertical;
    }
    textarea:focus {
        border-color: rgba(167,139,250,0.8) !important;
        box-shadow: 0 0 0 3px rgba(167,139,250,0.15) !important;
    }

    /* ボタン */
    div[data-testid="stButton"] > button {
        background: linear-gradient(90deg, #7c3aed, #2563eb);
        color: #fff;
        border: none;
        border-radius: 10px;
        font-size: 1.05rem;
        font-weight: 600;
        padding: 0.6rem 2.2rem;
        cursor: pointer;
        transition: all 0.25s ease;
        box-shadow: 0 4px 15px rgba(124,58,237,0.35);
        width: 100%;
        letter-spacing: 0.04em;
    }
    div[data-testid="stButton"] > button:hover {
        background: linear-gradient(90deg, #6d28d9, #1d4ed8);
        transform: translateY(-2px);
        box-shadow: 0 8px 24px rgba(124,58,237,0.5);
    }
    div[data-testid="stButton"] > button:active {
        transform: translateY(0px);
    }

    /* 成功バナー */
    .success-banner {
        background: linear-gradient(90deg, rgba(52,211,153,0.15), rgba(96,165,250,0.15));
        border: 1px solid rgba(52,211,153,0.4);
        border-radius: 10px;
        padding: 0.8rem 1.2rem;
        color: #6ee7b7;
        font-size: 0.95rem;
        margin-bottom: 0.8rem;
        display: flex;
        align-items: center;
        gap: 0.5rem;
    }

    /* 統計バッジ */
    .stat-badge {
        display: inline-block;
        background: rgba(167,139,250,0.15);
        border: 1px solid rgba(167,139,250,0.3);
        border-radius: 20px;
        padding: 0.25rem 0.9rem;
        font-size: 0.82rem;
        color: #c4b5fd;
        margin-right: 0.5rem;
        margin-top: 0.3rem;
    }

    /* セパレータ */
    hr {
        border: none;
        border-top: 1px solid rgba(255,255,255,0.08);
        margin: 1.5rem 0;
    }

    /* フッター */
    .footer {
        text-align: center;
        color: #475569;
        font-size: 0.8rem;
        padding: 2rem 0 1rem;
    }

    /* Streamlit デフォルト要素を隠す */
    #MainMenu, footer, header { visibility: hidden; }
    </style>
    """,
    unsafe_allow_html=True,
)

# ─────────────────────────────────────────────
# ユーティリティ関数
# ─────────────────────────────────────────────

ZENKAKU_SPACE = "\u3000"
HANKAKU_SPACE = " "

def normalize_spaces(text: str, mode: str) -> str:
    """
    mode:
      'half'   → 全角・半角スペースを半角1つに統一（連続も1つに圧縮）
      'delete' → 全角・半角スペースをすべて削除
      'tab'    → 全角・半角スペースをタブ区切りに変換（Excel2列貼付用）
    """
    lines = text.splitlines()
    result_lines = []

    for line in lines:
        if mode == "half":
            # 全角スペースを半角に置換し、連続する半角スペースを1つに
            converted = line.replace(ZENKAKU_SPACE, HANKAKU_SPACE)
            converted = re.sub(r" +", " ", converted).strip()
        elif mode == "delete":
            converted = line.replace(ZENKAKU_SPACE, "").replace(HANKAKU_SPACE, "")
        elif mode == "tab":
            # 全角スペースも半角に統一してからタブに変換（連続スペースは1タブ）
            converted = line.replace(ZENKAKU_SPACE, HANKAKU_SPACE)
            converted = re.sub(r" +", "\t", converted).strip()
        else:
            converted = line
        result_lines.append(converted)

    return "\n".join(result_lines)


def count_stats(original: str, converted: str):
    """変換前後の統計を返す"""
    orig_lines = [l for l in original.splitlines() if l.strip()]
    conv_lines = [l for l in converted.splitlines() if l.strip()]
    orig_half = original.count(HANKAKU_SPACE)
    orig_zen = original.count(ZENKAKU_SPACE)
    return len(orig_lines), orig_half, orig_zen, len(conv_lines)


# ─────────────────────────────────────────────
# メイン UI
# ─────────────────────────────────────────────

# ヒーローヘッダー
st.markdown(
    """
    <div class="hero-header">
        <div class="hero-title">✏️ 名簿スペース一括成形ツール</div>
        <div class="hero-sub">
            全角・半角スペースを瞬時に変換 ─ コピペするだけで即完了
        </div>
    </div>
    """,
    unsafe_allow_html=True,
)

# 2カラムレイアウト
col_left, col_right = st.columns([1, 1], gap="large")

# ─── 左カラム：入力 ───────────────────────────
with col_left:
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    st.markdown('<div class="card-label">📋 名簿を貼り付け</div>', unsafe_allow_html=True)

    input_text = st.text_area(
        label="",
        placeholder=(
            "ここに名簿をコピペしてください。\n"
            "例：\n"
            "山田　太郎\n"
            "佐藤 花子\n"
            "田中　 次郎"
        ),
        height=320,
        key="input_roster",
        label_visibility="collapsed",
    )
    st.markdown("</div>", unsafe_allow_html=True)

    # 変換モード選択
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    st.markdown('<div class="card-label">⚙️ 変換モードを選択</div>', unsafe_allow_html=True)

    MODE_OPTIONS = {
        "半角スペース1つに統一（連続も圧縮）": "half",
        "スペースをすべて削除": "delete",
        "タブ区切りに変換（Excel 2列貼付用）": "tab",
    }

    selected_label = st.radio(
        label="",
        options=list(MODE_OPTIONS.keys()),
        index=0,
        key="mode_select",
        label_visibility="collapsed",
    )
    selected_mode = MODE_OPTIONS[selected_label]
    st.markdown("</div>", unsafe_allow_html=True)

    convert_btn = st.button("🚀 変換する", key="convert_btn")

# ─── 右カラム：出力 ───────────────────────────
with col_right:
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    st.markdown('<div class="card-label">✅ 変換結果</div>', unsafe_allow_html=True)

    if convert_btn:
        if not input_text.strip():
            st.warning("⚠️ 名簿が入力されていません。左側にテキストを貼り付けてください。")
        else:
            result = normalize_spaces(input_text, selected_mode)
            n_lines, n_half, n_zen, n_out = count_stats(input_text, result)

            # 統計バッジ
            st.markdown(
                f"""
                <div style="margin-bottom:0.8rem;">
                    <span class="stat-badge">📄 {n_lines} 行</span>
                    <span class="stat-badge">半角スペース {n_half} 個</span>
                    <span class="stat-badge">全角スペース {n_zen} 個</span>
                </div>
                """,
                unsafe_allow_html=True,
            )

            # 成功バナー
            st.markdown(
                f'<div class="success-banner">✓ 変換完了 ─ <strong>{selected_label}</strong> で処理しました</div>',
                unsafe_allow_html=True,
            )

            # 結果テキストエリア
            st.text_area(
                label="",
                value=result,
                height=260,
                key="output_area",
                label_visibility="collapsed",
            )

            # コピーヒント
            st.markdown(
                "<p style='color:#64748b; font-size:0.82rem; margin-top:0.4rem;'>"
                "💡 テキストエリアをクリック → Ctrl+A → Ctrl+C でコピーできます</p>",
                unsafe_allow_html=True,
            )

            # タブモード時の補足
            if selected_mode == "tab":
                st.markdown(
                    "<p style='color:#7dd3fc; font-size:0.85rem;'>"
                    "📊 <strong>Excel貼付け手順：</strong> A列を選択 → Ctrl+V で2列に展開されます</p>",
                    unsafe_allow_html=True,
                )

    else:
        st.markdown(
            """
            <div style="text-align:center; padding: 5rem 0; color:#334155;">
                <div style="font-size:3rem; margin-bottom:1rem;">🎯</div>
                <div style="font-size:1rem;">左側に名簿を貼り付けて<br>「変換する」を押してください</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    st.markdown("</div>", unsafe_allow_html=True)

# ─────────────────────────────────────────────
# 使い方セクション
# ─────────────────────────────────────────────
st.markdown("<hr>", unsafe_allow_html=True)

with st.expander("📖 使い方 / 変換モードの詳細"):
    st.markdown(
        """
        ### 変換モード一覧

        | モード | 動作 | 用途 |
        |--------|------|------|
        | **半角スペース1つに統一** | 全角・半角スペースをすべて半角1つに変換し、連続するスペースも1つに圧縮 | 標準的な名簿整形、DBへの登録 |
        | **スペースをすべて削除** | 全角・半角スペースを完全に削除 | 姓名を1文字列として扱いたい場合 |
        | **タブ区切りに変換** | スペース（全角・半角・連続）をタブ1つに変換 | Excel に姓・名を別列で貼り付けたい場合 |

        ### 操作手順
        1. 名簿をコピー（Ctrl+C）
        2. 左の入力欄に貼り付け（Ctrl+V）
        3. 変換モードを選択
        4. 「変換する」ボタンをクリック
        5. 右の結果欄からコピー（Ctrl+A → Ctrl+C）

        ### 対応スペース
        - **全角スペース**（`　` U+3000）
        - **半角スペース**（` ` U+0020）
        - **連続スペース**（複数個）→ 1つに圧縮または1タブに変換
        """
    )

# フッター
st.markdown(
    '<div class="footer">名簿スペース一括成形ツール ─ Powered by Streamlit</div>',
    unsafe_allow_html=True,
)
