#DUEÑAS SALMAN AYDIN BERENICE
#CAZARES GALLEGOS ULISES VIDAL

#INSTRUCCIONES:
#En la terminal del ambiente de desarrollo4, dirigirse a la carpeta del archivo mediante el comando cd (ejemplo: cd proyecto-final)
#Exportar el proyecto mediante el comando export FLASK_APP=app.py
#Correr flask mediante el comando flask run
#Copiar la dirección que resulta (http://127.0.0.1:5000) y pegarla en el navegador, lo que dirigirá al index del sitio del proyecto final

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

resultados_busqueda=[]

@app.route('/')
def index():
    if 'username' in session:
        user = session['username']
        return render_template('index.html',username=user)
    return render_template('index.html')

@app.route('/confirm') #CONFIRMA SI TE VAS A SALIR
def confirm():
    return render_template('confirm.html')

@app.route('/logout') 
def logout():
    if 'username' in session:
        session.pop('username',None)
        return redirect('/')

@app.route('/register', methods=['GET','POST'])
def register():                                
    error = None
    if 'username' in session:
        user = session['username']
        if request.method == 'POST':
            username, email, password = request.form['username'], request.form['email'], request.form['password']
            if (username not in diccionario_usuarios): #si cambiaron el usuario
                if diccionario_usuarios[user]['email'] == email and diccionario_usuarios[user]['password'] == password: #checar que los datos coincidan con los de la cuenta
                    diccionario_usuarios[username] = diccionario_usuarios.pop(user)
                    with open('usuarios.json', 'w') as fp:
                        json.dump(diccionario_usuarios, fp)
                    session['username'] = username
                    return redirect('/')
                return render_template('register.html', error='No se puede cambiar el usuario si el correo y contraseña no coinciden con los de tu cuenta.', username=user)
            else:
                if (username == user):
                    diccionario_usuarios[user]['password'] = password
                    diccionario_usuarios[user]['email'] = email
                    with open('usuarios.json', 'w') as fp:
                        json.dump(diccionario_usuarios, fp)
                    return redirect('/')
                return render_template('register.html', error='No se puede cambiar el correo y contraseña si el usuario no coincide con el de tu cuenta.', username=user)
        else:   
            return render_template('register.html', error=None, username=user)
    else:
        if request.method == 'POST':
            username, email, password = request.form['username'], request.form['email'], request.form['password']
            if (username not in diccionario_usuarios): #checar que el usuario no esté registrado
                for user in diccionario_usuarios:
                    if diccionario_usuarios[user]['email'] == email: #checar que el correo no esté registrado
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
    error = None
    if request.method == 'POST':
        valor = request.form['boton']
        if(valor=="Buscar"):
            frase, similitud = request.form['frase'], float(request.form['similitud'])
            buscar_frases = frases.Buscador(frases_celebres,frase,similitud)
            resultados_busqueda = buscar_frases.buscar()
            longitud = len(resultados_busqueda)
            if (longitud == 0):
                return render_template('search.html', error='No se encontraron resultados para esa frase')
            diccionario_usuarios['busqueda']=resultados_busqueda
            with open('usuarios.json', 'w') as fp:
                json.dump(diccionario_usuarios, fp)
            if 'username' in session:
                user = session['username']
                return render_template('search.html', resultados=resultados_busqueda, frase = frase, len = longitud, username=user)
            return render_template('search.html', resultados=resultados_busqueda, frase = frase, len = longitud) 
        if(valor=="Agregar a favoritos"):
            frasesnuevas = []
            frasesfavs = []
            peliculas = request.form.getlist("indice")
            if 'username' in session:
                user = session['username']
                for item in peliculas:
                    frasesnuevas = diccionario_usuarios['busqueda'][int(item)]
                    frasesfavs = diccionario_usuarios[user]['frases']
                diccionario_usuarios[user]['frases'] = [x for x in frasesnuevas if x not in frasesfavs]
                del diccionario_usuarios['busqueda']
                with open('usuarios.json', 'w') as fp:
                    json.dump(diccionario_usuarios, fp)
                return redirect('/')
            del diccionario_usuarios['busqueda']
            return render_template('search.html', error='Debes iniciar sesión para guardar frases favoritas.') 
        del diccionario_usuarios['busqueda']
        return render_template('search.html', error='No se q está pasando.') 
    else:   
        return render_template('search.html', resultados=None)

@app.route('/frases', methods=['GET','POST']) #FRASES FAVORITAS
def frases_fav():
    user = session['username']
    resultados = None
    error = None
    if request.method == 'POST':
        frases_borradas=[]
        frases_favs=[]
        frases = request.form.getlist("indice")
        if user in diccionario_usuarios:
            frases_favs = diccionario_usuarios[user]['frases']
            for item in frases:
                frases_borradas.append(diccionario_usuarios[user]['frases'][int(item)])
            diccionario_usuarios[user]['frases'] = [x for x in frases_favs if x not in frases_borradas]
            with open('usuarios.json', 'w') as fp:
                json.dump(diccionario_usuarios, fp)
            favs = diccionario_usuarios[user]['frases']
            longitud = len(favs)
            return render_template('frases.html', frases=favs, len=longitud, username=user)
        return render_template('frases.html', error='Inicia sesión.') 
    else:
        if user in diccionario_usuarios:
            favs = diccionario_usuarios[user]['frases']
            longitud = len(favs)
            return render_template('frases.html', frases=favs, len=longitud, username=user)
        return render_template('frases.html', frases=None, len=0)   

if __name__ == "__main__":
    app.run(debug=True)