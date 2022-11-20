from tkinter import END, Tk, Menu, Text, messagebox
from tkinter.filedialog import asksaveasfilename, askopenfilename
import subprocess
from pygments.lexers import PythonLexer
from pygments.token import Token
import webbrowser
from sys import exit


def set_file_path(path):
	global file_path
	file_path = path


def open_file():
	try:
		path = askopenfilename(filetypes=[('Python Files', '*.py')])
		with open(path, 'r', encoding="utf-8") as file:
			code = file.read()
			editor.delete('1.0', END)
			editor.insert('1.0', code)
			set_file_path(path)
	except Exception:
		messagebox.showerror("Помилка", 'Відкрийте не битий файл.')


def save_as():
	if file_path == '':
		path = asksaveasfilename(filetypes=[('Python Files', '*.py')])
	else:
		path = file_path
	with open(path, 'w') as file:
		code = editor.get('1.0', END)
		file.write(code)
		set_file_path(path)


def run():
	if file_path == '':
		messagebox.showerror("Помилка", 'Збережіть код перед стартом.')
		return
	command = f'python {file_path}'
	process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
	output, error = process.communicate()
	code_output.delete('1.0', END)
	code_output.insert('1.0', output)
	code_output.insert('1.0', error)


def docs():
	webbrowser.open_new(r"https://www.python.org/doc/")


def theme_changer():
	if editor["bg"] == "#696969" and code_output["bg"] == "#696969":
		editor["bg"] = "white"
		code_output["bg"] = "white"
		editor["fg"] = "#696969"
		code_output["fg"] = "#696969"
	else:
		editor["bg"] = "#696969"
		code_output["bg"] = "#696969"
		editor["fg"] = "white"
		code_output["fg"] = "white"


def get_editor_cord(s: str, i: int):
	for row_number, line in enumerate(s.splitlines(keepends=True), 1):
		if i < len(line):
			return f'{row_number}.{i}'

		i -= len(line)


def on_edit(event):
	for tag in editor.tag_names():
		editor.tag_remove(tag, 1.0, END)

	for tag in code_output.tag_names():
		code_output.tag_remove(tag, 1.0, END)

	edit = editor.get(1.0, END)
	tokens = lexer.get_tokens_unprocessed(edit)

	for i, token_type, token in tokens:
		j = i + len(token)
		if token_type in token_type_to_tag:
			editor.tag_add(token_type_to_tag[token_type], get_editor_cord(edit, i), get_editor_cord(edit, j))

	editor.edit_modified(0)

	for tag in code_output.tag_names():
		code_output.tag_remove(tag, 1.0, END)

	output = code_output.get(1.0, END)
	tokens = lexer.get_tokens_unprocessed(output)

	for i, token_type, token in tokens:
		j = i + len(token)
		if token_type in token_type_to_tag:
			code_output.tag_add(token_type_to_tag[token_type], get_editor_cord(output, i), get_editor_cord(output, j))

	code_output.edit_modified(0)


root = Tk()
root.title('IDE.py')

try:
	root.iconbitmap('icon.ico')
except:
	pass

file_path = ''

menu_bar = Menu(root)

file_menu = Menu(menu_bar, tearoff=0)
file_menu.add_command(label='Відкрити', command=open_file)
file_menu.add_command(label='Зберегти', command=save_as)
file_menu.add_command(label='Вийти', command=exit)
menu_bar.add_cascade(label='Файл', menu=file_menu)

ide_menu = Menu(menu_bar, tearoff=0)
ide_menu.add_command(label='Старт', command=run)
ide_menu.add_command(label="Документація Python", command=docs)
ide_menu.add_command(label="Зміна теми(світла/нічна)", command=theme_changer)
menu_bar.add_cascade(label='IDE', menu=ide_menu)

root.config(menu=menu_bar)

editor = Text()
editor.pack()
code_output = Text(height=10)
code_output.pack()

lexer = PythonLexer()
editor.tag_config("orange", foreground='#b57007')
editor.tag_config("green", foreground='#80a35f')
editor.tag_config("gray", foreground='gray')
editor.tag_config("blue", foreground='#0abbcf')
editor.tag_config("yellow", foreground='#87830b')
editor.tag_config("purple", foreground='#b386f7')
code_output.tag_config("red", foreground='red')
code_output.tag_config("orange", foreground='#b57007')
code_output.tag_config("green", foreground='#80a35f')
code_output.tag_config("gray", foreground='gray')
code_output.tag_config("blue", foreground='#0abbcf')
code_output.tag_config("yellow", foreground='#87830b')
code_output.tag_config("purple", foreground='#b386f7')

token_type_to_tag = {
	Token.Keyword: "orange",
	Token.Operator: 'orange',
	Token.Operator.Word: "orange",
	Token.Name.Builtin: "purple",
	Token.Name.Attribute: "yellow",
	Token.Name.Decorator: "yellow",
	Token.Name.Entity: "orange",
	Token.Name.Label: "orange",
	Token.Name.Class: "yellow",
	Token.Name.Function: "yellow",
	Token.Name.Tag: "yellow",
	Token.Name.Exception: "red",
	Token.Name.Builtin.Pseudo: "purple",
	Token.Name.Variable.Class: "yellow",
	Token.Name.Variable.Instance: "yellow",
	Token.Name.Variable.Magic: "yellow",
	Token.Name.Variable.Global: "orange",
	Token.Punctuation: 'orange',
	Token.Punctuation.Marker: 'orange',
	Token.Comment.Single: "gray",
	Token.Literal.String.Single: "green",
	Token.Literal.String.Double: "green",
	Token.Literal.Number.Integer: "blue",
	Token.Literal.Number.Bin: "blue",
	Token.Literal.Number.Float: "blue",
	Token.Literal.Number.Integer.Long: "blue",
}

editor.bind('<<Modified>>', on_edit)
code_output.bind('<<Modified>>', on_edit)

root.mainloop()
