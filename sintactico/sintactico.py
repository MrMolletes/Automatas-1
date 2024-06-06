import ply.lex as lex
import ply.yacc as yacc
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

# Precedencia de operadores
precedence = (
    ('left', 'PLUS', 'MINUS'),
    ('left', 'TIMES', 'DIVIDE'),
)

# Definición de la gramática
def p_program(p):
    '''program : PROGRAM ID SEMI declarations BEGIN stmt_list END DOT'''
    p[0] = ('program', p[2], p[4], p[6])

def p_declarations(p):
    '''declarations : VAR var_declarations
                    | empty'''
    p[0] = p[2] if len(p) > 2 else None

def p_var_declarations(p):
    '''var_declarations : var_declarations var_declaration
                        | var_declaration'''
    if len(p) == 3:
        p[0] = p[1] + [p[2]]
    else:
        p[0] = [p[1]]

def p_var_declaration(p):
    '''var_declaration : ID_list COLON ID SEMI'''
    p[0] = ('var_decl', p[1], p[3])

def p_ID_list(p):
    '''ID_list : ID
               | ID_list COMMA ID'''
    if len(p) == 2:
        p[0] = [p[1]]
    else:
        p[0] = p[1] + [p[3]]

def p_stmt_list(p):
    '''stmt_list : stmt_list stmt
                 | stmt'''
    if len(p) == 3:
        p[0] = p[1] + [p[2]]
    else:
        p[0] = [p[1]]

def p_stmt(p):
    '''stmt : ID ASSIGN expr SEMI
            | block
            | WHILE expr DO stmt
            | IF expr THEN stmt ELSE stmt
            | IF expr THEN stmt'''
    if p[1] == 'while':
        p[0] = ('while', p[2], p[4])
    elif p[1] == 'if':
        if len(p) == 8:
            p[0] = ('if', p[2], p[4], p[6])
        else:
            p[0] = ('if', p[2], p[4], None)
    elif len(p) == 5:
        p[0] = ('assign', p[1], p[3])
    else:
        p[0] = p[1]

def p_block(p):
    '''block : BEGIN stmt_list END'''
    p[0] = ('block', p[2])

def p_expr(p):
    '''expr : expr PLUS term
            | expr MINUS term
            | expr LT term
            | expr GT term
            | expr LE term
            | expr GE term
            | expr EQ term
            | expr NEQ term
            | term'''
    if len(p) == 4:
        p[0] = ('binop', p[2], p[1], p[3])
    else:
        p[0] = p[1]

def p_term(p):
    '''term : term TIMES factor
            | term DIVIDE factor
            | factor'''
    if len(p) == 4:
        p[0] = ('binop', p[2], p[1], p[3])
    else:
        p[0] = p[1]

def p_factor(p):
    '''factor : NUMBER
              | ID
              | LPAREN expr RPAREN'''
    if isinstance(p[1], int):
        p[0] = ('number', p[1])
    elif isinstance(p[1], str):
        p[0] = ('id', p[1])
    else:
        p[0] = p[2]

def p_empty(p):
    'empty :'
    p[0] = None

def p_error(p):
    if p:
        print(f"Error de sintaxis en '{p.value}' en la línea {p.lineno}")
    else:
        print("Error de sintaxis en EOF")

# Construcción del parser
parser = yacc.yacc()

# Función para analizar el código
def analyze_code():
    code = text.get("1.0", "end-1c")
    try:
        result = parser.parse(code)
        result_output = str(result) if result else "No se pudo generar el árbol de análisis sintáctico."
    except Exception as e:
        result_output = f"Error al analizar: {str(e)}"

    parser_output.config(state=tk.NORMAL)
    parser_output.delete(1.0, tk.END)
    parser_output.insert(tk.END, result_output)
    parser_output.config(state=tk.DISABLED)

# Configuración de la interfaz gráfica
root = tk.Tk()
root.title("Pascal Syntax Analyzer")

# Área de texto para entrada de código
text = tk.Text(root, height=20, width=60)
text.pack()

# Botón para analizar el código
analyze_button = tk.Button(root, text="Analyze", command=analyze_code)
analyze_button.pack()

# Etiqueta y área de texto para salida sintáctica
parser_label = tk.Label(root, text="Sintáctico:")
parser_label.pack()

parser_output = scrolledtext.ScrolledText(root, height=10, width=60, state=tk.DISABLED)
parser_output.pack()

root.mainloop()

