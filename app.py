from flask import Flask, render_template, request, session
from werkzeug.utils import redirect
import secrets, json
import frases
import os

app = Flask(__name__)
app.secret_key = secrets.token_hex(16)
app.run(debug=True)

with open('usuarios.json') as f:
    diccionario_usuarios = json.load(f)

THIS_FOLDER = os.path.dirname(os.path.abspath(__file__))
frases_celebres = os.path.join(THIS_FOLDER, 'frases_celebres.csv')

@app.route('/')
def index():
    if 'username' in session:
        user = session['username']
        return render_template('index.html',username=user)
    return render_template('index.html')

@app.route('/logout') #FALTA CONFIRMAR CIERRE
def logout():
    if 'username' in session:
        session.pop('username',None)
        return redirect('/')

@app.route('/register', methods=['GET','POST']) #FALTA PODER MODIFICAR DATOS DE USUARIO
def register():                                
    error = None
    if request.method == 'POST':
        username, email, password = request.form['username'], request.form['email'], request.form['password']
        if (username not in diccionario_usuarios): #checar que el usuario no esté registrado
            for username in diccionario_usuarios:
                if diccionario_usuarios[username]['email'] == email: #checar que el correo no esté registrado
                    return render_template('register.html', error='Correo ya registrado.')
            diccionario_usuarios[username] = {}
            diccionario_usuarios[username]['password'] = password
            diccionario_usuarios[username]['email'] = email
            diccionario_usuarios[username]['frases'] = []
            with open('usuarios.json', 'w') as fp:
                json.dump(diccionario_usuarios, fp)
            session['username'] = username
            return redirect('/')
        else:
            return render_template('register.html', error='Usuario ya registrado.')
    else:   
        return render_template('register.html', error=None)      

@app.route('/login', methods=['GET','POST']) 
def login():                                
    error = None
    if request.method == 'POST':
        for user in diccionario_usuarios:
            if diccionario_usuarios[user]['email'] == request.form['email']:
                if diccionario_usuarios[user]['password'] == request.form['password']:
                    session['username'] = user
                    return redirect('/')
                else:
                    return render_template('login.html', error='Password incorrecto')
        return render_template('login.html', error='Email incorrecto')
    else:   
        return render_template('login.html', error=None)

@app.route('/search', methods=['GET','POST']) 
def search():                             
    resultados = None
    if request.method == 'POST':
        frase, similitud = request.form['frase'], float(request.form['similitud'])
        buscar_frases = frases.Buscador(frases_celebres,frase,similitud)
        resultados_busqueda = buscar_frases.buscar()
        longitud = len(resultados_busqueda)
        return render_template('search.html', resultados=resultados_busqueda, frase = frase, len = longitud)
    else:   
        return render_template('search.html', resultados=None)

if __name__ == "__main__":
    app.run(debug=True)