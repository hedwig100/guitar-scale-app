import streamlit.components.v1 as components
import streamlit as st

NOTE_NAMES_SHARP = ['C', 'C#', 'D', 'D#', 'E', 'F',
                    'F#', 'G', 'G#', 'A', 'A#', 'B']

CHORD_FORMULAS = {
    "maj": [0, 4, 7],
    "m": [0, 3, 7],
    "7": [0, 4, 7, 10],
    "m7": [0, 3, 7, 10],
    "maj7": [0, 4, 7, 11],
    "dim": [0, 3, 6],  
    "dim7": [0, 3, 6, 9], 
}

OPEN_STRINGS = ['E', 'B', 'G', 'D', 'A', 'E']  # 1弦→6弦

def generate_fretboard():
    fretboard = []
    for string_note in OPEN_STRINGS:
        string = []
        start_index = NOTE_NAMES_SHARP.index(string_note)
        for fret in range(0, 23):
            note = NOTE_NAMES_SHARP[(start_index + fret) % 12]
            string.append(note)
        fretboard.append(string)
    return fretboard

def get_chord_notes(root, chord_type):
    root_index = NOTE_NAMES_SHARP.index(root)
    intervals = CHORD_FORMULAS[chord_type]
    return [NOTE_NAMES_SHARP[(root_index + i) % 12] for i in intervals]

# 🆕 指板をリアル風にHTML+CSSで描画
def render_fretboard_html(fretboard, chord_notes):
    html = """
    <style>
        .fretboard-container {
            overflow-x: auto;
            padding: 10px;
        }
        .fretboard {
            position: relative;
            width: calc(40px * 23);
            height: calc(30px * 6);
            border-top: 4px solid #444;
            border-bottom: 4px solid #444;
        }
        .string {
            position: absolute;
            height: 2px;
            background: #666;
            left: 0;
            right: 0;
        }
        .fret {
            position: absolute;
            width: 2px;
            background: #aaa;
            top: 0;
            bottom: 0;
        }
        .note-dot {
            position: absolute;
            width: 18px;
            height: 18px;
            border-radius: 50%;
            transform: translate(-50%, -50%);
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 10px;
            font-weight: bold;
            color: white;
            z-index: 2;
        }
        .note-root { background: crimson; }
        .note-highlight { background: orange; }
        .fret-labels {
            display: flex;
            gap: 38px;
            margin-left: 20px;
            margin-bottom: 6px;
            font-size: 12px;
            color: #444;
        }
    </style>
    """

    # フレット番号
    html += "<div class='fret-labels'>"
    for fret in range(23):
        html += f"<div>{fret}</div>"
    html += "</div>"

    html += "<div class='fretboard-container'><div class='fretboard'>"

    # 弦（6本）
    for i in range(6):
        y = (i + 0.5) * 30
        html += f"<div class='string' style='top: {y}px'></div>"

    # フレット線（0〜22）
    for f in range(23):
        x = f * 40
        html += f"<div class='fret' style='left: {x}px'></div>"

    # 構成音ドット
    for string_idx, string in enumerate(fretboard):
        for fret_idx, note in enumerate(string):
            if note in chord_notes:
                y = (string_idx + 0.5) * 30
                x = fret_idx * 40 + 20
                note_class = "note-root" if note == chord_notes[0] else "note-highlight"
                html += f"""
                    <div class='note-dot {note_class}' style='top: {y}px; left: {x}px'>
                        {note}
                    </div>
                """

    html += "</div></div>"
    return html

# -------- Streamlit UI --------
st.set_page_config(layout="wide")
st.title("🎸 ギター指板コード構成音ビジュアライザー")

col1, col2 = st.columns(2)
with col1:
    root_note = st.selectbox("ルート音", NOTE_NAMES_SHARP)
with col2:
    chord_type = st.selectbox("コードタイプ", list(CHORD_FORMULAS.keys()))

chord_notes = get_chord_notes(root_note, chord_type)
st.markdown(f"**{root_note}{chord_type}** の構成音: {', '.join(chord_notes)}")

fretboard = generate_fretboard()
fretboard_html = render_fretboard_html(fretboard, chord_notes)
st.markdown("### 指板ビュー")
components.html(fretboard_html, height=250, scrolling=True)
