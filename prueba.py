import json

f = open('usuarios.json',)
data = json.load(f)
frase = data['ranita']['frases'][0][1]
pelicula = data['ranita']['frases'][0][2]
print(frase + ' de '+ pelicula)