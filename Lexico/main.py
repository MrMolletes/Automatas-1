import ply.lex as lex
import tkinter as tk
from tkinter import scrolledtext

# Palabras clave de Pascal
reserved = {
    'begin': 'BEGIN',
    'end': 'END',
    'if': 'IF',
    'then': 'THEN',
    'else': 'ELSE',
    'while': 'WHILE',
    'do': 'DO',
    'var': 'VAR',
    'procedure': 'PROCEDURE',
    'function': 'FUNCTION',
    'program': 'PROGRAM'
}

# Lista de tokens
tokens = [
    'ID', 'NUMBER', 'PLUS', 'MINUS', 'TIMES', 'DIVIDE', 'LPAREN', 'RPAREN',
    'SEMI', 'COLON', 'COMMA', 'DOT', 'ASSIGN', 'EQ', 'NEQ', 'LT', 'GT',
    'LE', 'GE'
] + list(reserved.values())

# Expresiones regulares para tokens simples
t_PLUS = r'\+'
t_MINUS = r'-'
t_TIMES = r'\*'
t_DIVIDE = r'/'
t_LPAREN = r'\('
t_RPAREN = r'\)'
t_SEMI = r';'
t_COLON = r':'
t_COMMA = r','
t_DOT = r'\.'
t_ASSIGN = r':='
t_EQ = r'='
t_NEQ = r'<>'
t_LT = r'<'
t_GT = r'>'
t_LE = r'<='
t_GE = r'>='

# Expresión regular para números
def t_NUMBER(t):
    r'\d+'
    t.value = int(t.value)
    return t

# Identificadores y palabras clave
def t_ID(t):
    r'[a-zA-Z_][a-zA-Z_0-9]*'
    t.type = reserved.get(t.value.lower(), 'ID')
    return t

# Contador de líneas
def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)

# Caracteres ignorados (espacios y tabuladores)
t_ignore = ' \t'

# Manejador de errores
def t_error(t):
    print(f"Carácter ilegal '{t.value[0]}'")
    t.lexer.skip(1)

# Construcción del lexer
lexer = lex.lex()

# Función para analizar el código
def analyze_code():
    code = text.get("1.0", "end-1c")
    lexer.input(code)
    tokens_output = []
    while True:
        tok = lexer.token()
        if not tok:
            break
        tokens_output.append(f'{tok.type} -> {tok.value}')

    lexer_output.config(state=tk.NORMAL)
    lexer_output.delete(1.0, tk.END)
    lexer_output.insert(tk.END, '\n'.join(tokens_output))
    lexer_output.config(state=tk.DISABLED)

# Configuración de la interfaz gráfica
root = tk.Tk()
root.title("Pascal Lexer")

# Área de texto para entrada de código
text = tk.Text(root, height=20, width=60)
text.pack()

# Botón para analizar el código
analyze_button = tk.Button(root, text="Analyze", command=analyze_code)
analyze_button.pack()

# Etiqueta y área de texto para salida léxica
lexer_label = tk.Label(root, text="Léxico:")
lexer_label.pack()

lexer_output = scrolledtext.ScrolledText(root, height=10, width=60, state=tk.DISABLED)
lexer_output.pack()

root.mainloop()

