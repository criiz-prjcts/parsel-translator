import streamlit as st
from collections import defaultdict

# Emojis por idioma
LANG_EMOJIS = {
    "Parsel": "🐍",
    "Troll": "🏏",
    "Sirenio": "🧜‍♀️",
    "Duendigonza": "🧌",
    "Draconis": "🐉",
    "Veela": "🧚‍♀️",
    "Finofaudio": "🦖"
}

# Diccionarios de codificación (abreviado por brevedad, reemplazar por los completos)
CODES = {
    "Finofaudio": {
        'A': 'fi', 'B': 'fgh', 'C': 'fjd', 'D': 'fsa', 'E': 'fa', 'F': 'fre',
        'G': 'fes', 'H': 'fag', 'I': 'fu', 'J': 'feg', 'K': 'fo', 'L': 'fffg',
        'M': 'fur', 'N': 'fot', 'O': 'fe', 'P': 'for', 'Q': 'fafe', 'R': 'faer',
        'S': 'fiuf', 'T': 'ful', 'U': 'fo', 'V': 'feik', 'W': 'fyw', 'X': 'feg',
        'Y': 'feh', 'Z': 'fff'
    },
    # Agrega los demás idiomas aquí...
}

class TrieNode:
    def __init__(self):
        self.children = {}
        self.letter = None

def build_trie(mapping):
    root = TrieNode()
    for letter, code in mapping.items():
        node = root
        for char in code:
            node = node.children.setdefault(char, TrieNode())
        if node.letter is None:
            node.letter = letter  # prioriza la primera letra en caso de colisión
    return root

def get_ambiguous_codes(mapping):
    code_map = defaultdict(list)
    for k, v in mapping.items():
        code_map[v].append(k)
    return {code: letters for code, letters in code_map.items() if len(letters) > 1}

def decode_text_with_notes(text, mapping):
    trie_root = build_trie(mapping)
    ambiguous_codes = get_ambiguous_codes(mapping)
    inverted_map = defaultdict(list)
    for letter, code in mapping.items():
        inverted_map[code].append(letter)

    text = text.lower()
    decoded = ''
    i = 0
    used_codes = []
    while i < len(text):
        node = trie_root
        j = i
        match = None
        current_code = ''
        while j < len(text) and text[j] in node.children:
            node = node.children[text[j]]
            current_code += text[j]
            j += 1
            if node.letter:
                match = (node.letter, j, current_code)
        if match:
            letter, new_i, code = match
            decoded += letter
            if code in ambiguous_codes:
                used_codes.append(code)
            i = new_i
        else:
            decoded += text[i]
            i += 1

    notes = []
    for code in set(used_codes):
        letters = inverted_map[code]
        if len(letters) > 1:
            notes.append(f'- Código "{code}" puede ser {" o ".join(letters)} → se usó {letters[0]}')

    return decoded, notes

def encode_text(text, mapping):
    result = ''
    text = text.upper()
    for char in text:
        if char in mapping:
            result += mapping[char]
        else:
            result += char
    return result

# Interfaz
st.set_page_config(page_title="Traductor de Lenguajes Fantásticos", page_icon="✨")
st.title("✨ Traductor de Lenguajes Fantásticos")

modo = st.radio("Modo", ["Codificar (Español → Idioma mágico)", "Decodificar (Idioma mágico → Español)"])
idiomas_ordenados = list(LANG_EMOJIS.keys())
idioma_seleccionado = st.selectbox("Idioma mágico", [f"{LANG_EMOJIS[n]} {n}" for n in idiomas_ordenados])
idioma_nombre = idioma_seleccionado.split(" ", 1)[1]

entrada = st.text_area("Texto de entrada", height=150)

if st.button("Traducir"):
    if not entrada.strip():
        st.warning("Por favor, introduce algún texto.")
    else:
        if modo.startswith("Codificar"):
            resultado = encode_text(entrada, CODES[idioma_nombre])
            st.success("Resultado:")
            st.code(resultado, language="text")
        else:
            resultado, notas = decode_text_with_notes(entrada, CODES[idioma_nombre])
            st.success("Resultado:")
            st.code(resultado, language="text")
            if notas:
                st.warning("\n".join(["Posibles ambigüedades encontradas:"] + notas))
