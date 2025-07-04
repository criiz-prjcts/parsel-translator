import streamlit as st

# Diccionarios para Parsel y Troll
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

# Interfaz Streamlit
st.title("🔓 Decodificador de Lenguajes Mágicos")
st.write("Selecciona un idioma y pega el texto para decodificarlo al alfabeto latino.")

idioma = st.selectbox("Idioma", list(CODES.keys()))
entrada = st.text_area("Texto cifrado", height=150)

if st.button("Decodificar"):
    if entrada.strip():
        resultado = decode_text(entrada, CODES[idioma])
        st.success("Texto decodificado:")
        st.code(resultado, language="text")
    else:
        st.warning("Por favor, introduce algún texto.")
