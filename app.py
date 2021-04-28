from flask import Flask, render_template, request, session
from werkzeug.utils import redirect
import secrets, json

app = Flask(__name__)
app.secret_key = secrets.token_hex(16)
app.run(debug=True)

with open('usuarios.json') as f:
    diccionario_usuarios = json.load(f)

@app.route('/')
def index():
    if 'username' in session:
        user = session['username']
        return render_template('index.html',username=user)
    return render_template('index.html')

@app.route('/logout') #falta confirmar el cierre
def logout():
    if 'username' in session:
        session.pop('username',None)
        return redirect('/')

@app.route('/register', methods=['GET','POST']) #falta poder modificar datos de usuario
def register():                                
    error = None
    if request.method == 'POST':
        if (request.form['username'] not in diccionario_usuarios):
            username, email, password = request.form['username'], request.form['email'], request.form['password']
            diccionario_usuarios[username] = {}
            diccionario_usuarios[username]['password'] = password
            diccionario_usuarios[username]['email'] = email
            diccionario_usuarios[username]['frases'] = []
            with open('usuarios.json', 'w') as fp:
                json.dump(diccionario_usuarios, fp)
            session['username'] = username
            return redirect('/')
        else:
            return render_template('register.html', error='Usuario ya registrado, inicie sesión')
    else:   
        return render_template('register.html', error=None)      

@app.route('/login', methods=['GET','POST']) 
def login():                                
    error = None
    if request.method == 'POST':

        if (request.form['username'] in diccionario_usuarios):
            username = request.form['username']
            diccionario = diccionario_usuarios[username]
            password = diccionario['password']
            if (request.form['password'] == password):
                session['username'] = request.form['username']
                return redirect('/')
            else:
                return render_template('login.html', error='Password incorrecto')
        else:
                return render_template('login.html', error='Username incorrecto')
    else:   
        return render_template('login.html', error=None)

if __name__ == "__main__":
    app.run(debug=True)