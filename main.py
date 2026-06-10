import streamlit as st
import re
import unicodedata

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

    /* ─── 全テキストを白系に強制 ─── */
    .stApp p,
    .stApp span,
    .stApp label,
    .stApp div,
    .stApp li,
    .stApp h1, .stApp h2, .stApp h3, .stApp h4,
    .stMarkdown p,
    .stMarkdown li,
    .stMarkdown td,
    .stMarkdown th {
        color: #f1f5f9 !important;
    }

    /* radio / checkbox ラベル */
    div[data-testid="stRadio"] label,
    div[data-testid="stRadio"] label p,
    div[data-testid="stCheckbox"] label {
        color: #f1f5f9 !important;
        font-size: 1rem !important;
    }

    /* radio 選択済マーカー */
    div[data-testid="stRadio"] [data-testid="stMarkdownContainer"] p {
        color: #f1f5f9 !important;
    }

    /* expander ラベル */
    details summary p,
    div[data-testid="stExpander"] summary span {
        color: #e2e8f0 !important;
        font-size: 1rem !important;
    }

    /* テーブルヘッダー */
    .stMarkdown table th {
        background: rgba(167,139,250,0.2);
        color: #f1f5f9 !important;
    }
    .stMarkdown table td {
        color: #e2e8f0 !important;
    }

    /* ヘッダー */
    .hero-header {
        text-align: center;
        padding: 2.5rem 1rem 1.5rem;
        margin-bottom: 0.5rem;
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
        color: #cbd5e1 !important;
        font-weight: 400;
    }


    /* テキストエリア */
    textarea {
        background: rgba(15,12,41,0.8) !important;
        border: 1px solid rgba(167,139,250,0.4) !important;
        border-radius: 10px !important;
        color: #f1f5f9 !important;
        font-family: 'Noto Sans JP', monospace !important;
        font-size: 0.95rem !important;
        line-height: 1.7 !important;
        resize: vertical;
    }
    textarea::placeholder {
        color: #64748b !important;
    }
    textarea:focus {
        border-color: rgba(167,139,250,0.8) !important;
        box-shadow: 0 0 0 3px rgba(167,139,250,0.15) !important;
    }

    /* ボタン */
    div[data-testid="stButton"] > button {
        background: linear-gradient(90deg, #7c3aed, #2563eb) !important;
        color: #fff !important;
        border: none !important;
        border-radius: 10px !important;
        font-size: 1.05rem !important;
        font-weight: 600 !important;
        padding: 0.65rem 2.2rem !important;
        cursor: pointer;
        transition: all 0.25s ease;
        box-shadow: 0 4px 15px rgba(124,58,237,0.35) !important;
        width: 100%;
        letter-spacing: 0.04em;
    }
    div[data-testid="stButton"] > button:hover {
        background: linear-gradient(90deg, #6d28d9, #1d4ed8) !important;
        transform: translateY(-2px);
        box-shadow: 0 8px 24px rgba(124,58,237,0.5) !important;
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
        color: #86efac !important;
        font-size: 0.95rem;
        margin-bottom: 0.8rem;
    }
    .success-banner strong {
        color: #86efac !important;
    }

    /* 統計バッジ */
    .stat-badge {
        display: inline-block;
        background: rgba(167,139,250,0.18);
        border: 1px solid rgba(167,139,250,0.35);
        border-radius: 20px;
        padding: 0.25rem 0.9rem;
        font-size: 0.82rem;
        color: #ddd6fe !important;
        margin-right: 0.5rem;
        margin-top: 0.3rem;
    }

    /* セパレータ */
    hr {
        border: none;
        border-top: 1px solid rgba(255,255,255,0.1);
        margin: 1.5rem 0;
    }

    /* フッター */
    .footer {
        text-align: center;
        color: #64748b !important;
        font-size: 0.8rem;
        padding: 2rem 0 1rem;
    }

    /* hint テキスト */
    .hint-text {
        color: #94a3b8 !important;
        font-size: 0.83rem;
        margin-top: 0.4rem;
    }
    .hint-excel {
        color: #7dd3fc !important;
        font-size: 0.85rem;
    }

    /* placeholder 中央揃え */
    .placeholder-center {
        text-align: center;
        padding: 4rem 0;
        color: #475569 !important;
    }
    .placeholder-center .icon {
        font-size: 3rem;
        margin-bottom: 1rem;
    }
    .placeholder-center .msg {
        font-size: 1rem;
        color: #64748b !important;
    }

    /* warning / alert 内テキスト */
    div[data-testid="stAlert"] p {
        color: #1e293b !important;
    }

    /* Streamlit デフォルト要素を隠す */
    #MainMenu, footer, header { visibility: hidden; }

    /* empty element（空divなど）を非表示 */
    .element-container:empty { display: none !important; }
    </style>
    """,
    unsafe_allow_html=True,
)

# ─────────────────────────────────────────────
# 見出し（ラベル）専用の CSS 定義
# ─────────────────────────────────────────────
st.markdown(
    """
    <style>
    .section-title {
        font-size: 2.2rem !important;
        font-weight: 800 !important;
        color: #a78bfa !important;
        letter-spacing: 0.04em;
        margin-bottom: 0.6rem;
        padding-bottom: 0.4rem;
        border-bottom: 1px solid rgba(167,139,250,0.3);
        display: block;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# ─────────────────────────────────────────────
# ユーティリティ関数
# ─────────────────────────────────────────────

ZENKAKU_SPACE = "\u3000"
HANKAKU_SPACE = " "


def clean_text(text: str) -> str:
    """
    目に見えない制御文字・ゴミ文字を除去する。
    除去対象：
      - C0制御文字（\x00-\x08, \x0b, \x0c, \x0e-\x1f）※改行\x0a・タブ\x09は保持
      - C1制御文字（\x7f-\x9f）
      - Unicode「Cc」カテゴリ（制御文字）
      - バックスペース（\x08）
      - ゼロ幅文字（U+200B, U+200C, U+200D, U+FEFF, U+2028, U+2029 等）
      - 不正なサロゲートペア
    """
    # ゼロ幅・不可視文字・制御文字を除去（改行 \n とタブ \t は維持）
    cleaned = re.sub(
        r'[\x00-\x08\x0b\x0c\x0e-\x1f\x7f-\x9f'
        r'\u200b\u200c\u200d\u200e\u200f'
        r'\u2028\u2029\u202a-\u202e'
        r'\u2060-\u2064\uFEFF\uFFF9-\uFFFB]',
        '',
        text
    )
    # unicodedata で Cc カテゴリ（制御文字）を念のため追加除去
    result = []
    for ch in cleaned:
        cat = unicodedata.category(ch)
        if cat == 'Cc' and ch not in ('\n', '\t', '\r'):
            continue  # 制御文字をスキップ
        result.append(ch)
    return ''.join(result)


def normalize_spaces(text: str, mode: str) -> str:
    """
    ゴミ文字除去 → スペース変換を実施。
    mode:
      'half'   → 全角・半角スペースを半角1つに統一（連続も1つに圧縮）
      'delete' → 全角・半角スペースをすべて削除
      'tab'    → 全角・半角スペースをタブ区切りに変換（Excel2列貼付用）
    """
    # まずゴミ文字を除去
    text = clean_text(text)

    lines = text.splitlines()
    result_lines = []

    for line in lines:
        if mode == "half":
            converted = line.replace(ZENKAKU_SPACE, HANKAKU_SPACE)
            converted = re.sub(r"[ \t]+", " ", converted).strip()
        elif mode == "delete":
            converted = line.replace(ZENKAKU_SPACE, "").replace(HANKAKU_SPACE, "")
            converted = re.sub(r"\t", "", converted)
        elif mode == "tab":
            converted = line.replace(ZENKAKU_SPACE, HANKAKU_SPACE)
            converted = re.sub(r"[ \t]+", "\t", converted).strip()
        else:
            converted = line
        result_lines.append(converted)

    return "\n".join(result_lines)


def count_stats(original: str):
    """入力テキストの統計を返す"""
    orig_lines = [l for l in original.splitlines() if l.strip()]
    orig_half = original.count(HANKAKU_SPACE)
    orig_zen = original.count(ZENKAKU_SPACE)
    return len(orig_lines), orig_half, orig_zen


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

# ─── 左カラム：入力 ────────────────────────────────────────────
with col_left:

    st.markdown(
        '<p class="section-title">📋 名簿を貼り付け</p>',
        unsafe_allow_html=True,
    )

    input_text = st.text_area(
        label="名簿入力",
        placeholder=(
            "ここに名簿をコピペしてください。\n"
            "例：\n"
            "山田　太郎\n"
            "佐藤 花子\n"
            "田中　 次郎"
        ),
        height=300,
        key="input_roster",
        label_visibility="collapsed",
    )

    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown(
        '<p class="section-title">⚙️ 変換モードを選択</p>',
        unsafe_allow_html=True,
    )

    MODE_OPTIONS = {
        "半角スペース1つに統一（連続も圧縮）": "half",
        "スペースをすべて削除": "delete",
        "タブ区切りに変換（Excel 2列貼付用）": "tab",
    }

    selected_label = st.radio(
        label="変換モード",
        options=list(MODE_OPTIONS.keys()),
        index=0,
        key="mode_select",
        label_visibility="collapsed",
    )
    selected_mode = MODE_OPTIONS[selected_label]

    st.markdown("<br>", unsafe_allow_html=True)
    convert_btn = st.button("🚀 変換する", key="convert_btn")

# ─── 右カラム：出力 ────────────────────────────────────────────
with col_right:

    st.markdown(
        '<p class="section-title">✅ 変換結果</p>',
        unsafe_allow_html=True,
    )

    if convert_btn:
        if not input_text.strip():
            st.warning("⚠️ 名簿が入力されていません。左側にテキストを貼り付けてください。")
        else:
            result = normalize_spaces(input_text, selected_mode)
            n_lines, n_half, n_zen = count_stats(input_text)

            # 結果テキストエリア
            st.text_area(
                label="変換結果",
                value=result,
                height=260,
                key="output_area",
                label_visibility="collapsed",
            )

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

            # コピーヒント
            st.markdown(
                '<p class="hint-text">💡 テキストエリアをクリック → Ctrl+A → Ctrl+C でコピーできます</p>',
                unsafe_allow_html=True,
            )

            # タブモード時の補足
            if selected_mode == "tab":
                st.markdown(
                    '<p class="hint-excel">📊 <strong>Excel貼付け手順：</strong> A列を選択 → Ctrl+V で2列に展開されます</p>',
                    unsafe_allow_html=True,
                )

    else:
        st.markdown(
            """
            <div class="placeholder-center">
                <div class="icon">🎯</div>
                <div class="msg">左側に名簿を貼り付けて<br>「変換する」を押してください</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

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
        | **半角スペース1つに統一** | 全角・半角スペースを半角1つに変換。連続するスペースも1つに圧縮 | 標準的な名簿整形、DBへの登録 |
        | **スペースをすべて削除** | 全角・半角スペースを完全に削除 | 姓名を1文字列として扱いたい場合 |
        | **タブ区切りに変換** | スペース（全角・半角・連続）をタブ1つに変換 | Excel に姓・名を別列で貼り付けたい場合 |

        ### ゴミ文字の自動除去
        変換前に以下の不正文字を自動的に除去します：
        - **制御文字**（バックスペース・NUL・ESCなど）
        - **ゼロ幅スペース**（U+200B など）
        - **不可視Unicode文字**（BOM・方向制御文字など）

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
