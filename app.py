import streamlit as st

NOTE_NAMES_SHARP = ['C', 'C#', 'D', 'D#', 'E', 'F',
                    'F#', 'G', 'G#', 'A', 'A#', 'B']

# 各コードタイプとそのインターバル
CHORD_FORMULAS = {
    "maj": [0, 4, 7],
    "m": [0, 3, 7],
    "7": [0, 4, 7, 10],
    "m7": [0, 3, 7, 10],
    "maj7": [0, 4, 7, 11],
}

# チューニング（6弦〜1弦）
OPEN_STRINGS = ['E', 'A', 'D', 'G', 'B', 'E']

# 指板の各音を取得
def generate_fretboard():
    fretboard = []
    for string_note in OPEN_STRINGS:
        string = []
        start_index = NOTE_NAMES_SHARP.index(string_note)
        for fret in range(0, 22 + 1):
            note = NOTE_NAMES_SHARP[(start_index + fret) % 12]
            string.append(note)
        fretboard.append(string)
    return fretboard

# コード構成音の取得
def get_chord_notes(root, chord_type):
    root_index = NOTE_NAMES_SHARP.index(root)
    intervals = CHORD_FORMULAS[chord_type]
    return [NOTE_NAMES_SHARP[(root_index + i) % 12] for i in intervals]

# HTML/CSS 指板描画
def render_fretboard_html(fretboard, chord_notes):
    html = """
    <style>
        .fretboard { display: grid; grid-template-columns: repeat(23, 40px); gap: 1px; }
        .string-row { display: contents; }
        .fret {
            height: 30px;
            display: flex;
            align-items: center;
            justify-content: center;
            border: 1px solid #aaa;
            font-family: monospace;
            font-size: 14px;
        }
        .note-normal { background: #eee; color: #666; }
        .note-highlight { background: orange; color: white; font-weight: bold; }
        .note-root { background: crimson; color: white; font-weight: bold; }
    </style>
    <div class="fretboard">
    """
    for string in fretboard:
        for fret, note in enumerate(string):
            if note == chord_notes[0]:
                cell_class = "note-root"
            elif note in chord_notes:
                cell_class = "note-highlight"
            else:
                cell_class = "note-normal"
            html += f"<div class='fret {cell_class}'>{note}</div>"
    html += "</div>"
    return html

# ---------------- Streamlit UI ---------------- #

st.set_page_config(layout="wide")
st.title("🎸 ギター指板コード構成音ビジュアライザー")

# コード入力
col1, col2 = st.columns(2)
with col1:
    root_note = st.selectbox("ルート音", NOTE_NAMES_SHARP)
with col2:
    chord_type = st.selectbox("コードタイプ", list(CHORD_FORMULAS.keys()))

# 構成音表示
chord_notes = get_chord_notes(root_note, chord_type)
st.markdown(f"**{root_note}{chord_type}** の構成音: {', '.join(chord_notes)}")

# フレットボード生成
fretboard = generate_fretboard()

# 指板表示
st.markdown("### 指板ビュー（22フレット）")
fretboard = generate_fretboard()
fretboard_html = render_fretboard_html(fretboard, chord_notes)
st.markdown(fretboard_html, unsafe_allow_html=True)
