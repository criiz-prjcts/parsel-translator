import streamlit as st

# Diccionario Parsel
TO_PARSEL = {
    'A': 'esh',  'B': 'ch',   'C': 'eish',
    'D': 'shi',  'E': 'ash',  'F': 'asha',
    'G': 'ei',   'H': 'shis', 'I': 'osh',
    'J': 'xim',  'K': 'ss',   'L': 'suh',
    'M': 'xan',  'N': 'sh',   'O': 'ush',
    'P': 'cah',  'Q': 'xii',  'R': 'in',
    'S': 'shs',  'T': 'cass', 'U': 'ish',
    'V': 'aus',  'W': 'xi',   'X': 'shh',
    'Y': 'sss',  'Z': 'xiy'
}

# Trie
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

TRIE_ROOT = build_trie(TO_PARSEL)

def decode_parsel(text):
    text = text.lower()
    decoded = ''
    i = 0
    while i < len(text):
        node = TRIE_ROOT
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

# Interfaz web
st.title("🔓 Parsel → Español")
st.write("Pega tu texto en Parsel abajo y obtendrás la traducción alfabética en español.")

entrada = st.text_area("Texto en Parsel", height=150)

if st.button("Traduce"):
    if entrada.strip():
        resultado = decode_parsel(entrada)
        st.success("Resultado:")
        st.code(resultado, language="text")
    else:
        st.warning("Por favor, introduce texto para traducir.")
