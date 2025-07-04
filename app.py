import streamlit as st

# Diccionarios para Parsel, Troll y Sirenio
CODES = {
    "Parsel": {
        'A': 'esh',  'B': 'ch',   'C': 'eish',
        'D': 'shi',  'E': 'ash',  'F': 'asha',
        'G': 'ei',   'H': 'shis', 'I': 'osh',
        'J': 'xim',  'K': 'ss',   'L': 'suh',
        'M': 'xan',  'N': 'sh',   'O': 'ush',
        'P': 'cah',  'Q': 'xii',  'R': 'in',
        'S': 'shs',  'T': 'cass', 'U': 'ish',
        'V': 'aus',  'W': 'xi',   'X': 'shh',
        'Y': 'sss',  'Z': 'xiy'
    },
    "Troll": {
        'A': 'oet',  'B': 'lool', 'C': 'cad',
        'D': 'tuu',  'E': 'fno',  'F': 'oll',
        'G': 'cawl', 'H': 'tel',  'I': 'lot',
        'J': 'tro',  'K': 'ojt',  'L': 'rew',
        'M': 'pit',  'N': 'graw', 'O': 'ietg',
        'P': 'zit',  'Q': 'vlq',  'R': 'pos',
        'S': 'velf', 'T': 'insl', 'U': 'dil',
        'V': 'grig', 'W': 'bet',  'X': 'rot',
        'Y': 'etss', 'Z': 'sor'
    },
    "Sirenio": {
        'A': 'ogl',   'B': 'jig',   'C': 'sul',
        'D': 'fyg',   'E': 'igl',   'F': 'tigl',
        'G': 'fegl',  'H': 'sug',   'I': 'ugl',
        'J': 'leg',   'K': 'jhul',  'L': 'wag',
        'M': 'poh',   'N': 'pluh',  'Ñ': 'peeg',
        'O': 'agl',   'P': 'degl',  'Q': 'zel',
        'R': 'tig',   'S': 'xuu',   'T': 'geg',
        'U': 'egl',   'V': 'dafh',  'W': 'dufh',
        'X': 'lhh',   'Y': 'xieh',  'Z': 'welg'
    }
}

# Trie universal
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
        node.letter = letter
    return root

def decode_text(text, mapping):
    trie_root = build_trie(mapping)
    text = text.lower()
    decoded = ''
    i = 0
    while i < len(text):
        node = trie_root
        j = i
        match = None
        while j < len(text) and text[j] in node.children:
            node = node.children[text[j]]
            j += 1
            if node.letter:
                match = (node.letter, j)
        if match:
            decoded += match[0]
            i = match[1]
        else:
            decoded += text[i]
            i += 1
    return decoded

def encode_text(text, mapping):
    result = ''
    text = text.upper()
    for char in text:
        if char in mapping:
            result += mapping[char]
        else:
            result += char  # conserva espacios y signos
    return result

# Interfaz Streamlit
st.title("🔄 Traductor de Lenguajes Fantásticos")
st.write("Selecciona un idioma mágico y el modo que deseas utilizar.")

idioma = st.selectbox("Idioma", list(CODES.keys()))
modo = st.radio("Modo", ["Codificar (Español → Idioma mágico)", "Decodificar (Idioma mágico → Español)"])
entrada = st.text_area("Texto de entrada", height=150)

if st.button("Traducir"):
    if not entrada.strip():
        st.warning("Por favor, introduce algún texto.")
    else:
        if modo.startswith("Codificar"):
            resultado = encode_text(entrada, CODES[idioma])
        else:
            resultado = decode_text(entrada, CODES[idioma])
        st.success("Resultado:")
        st.code(resultado, language="text")
