import random 
from flask import Flask
 
app = Flask(__name__)

cartas = ["Cebolo", "Calado beta", "burro carente"]

@app.route("/")
def index():
    return '''
        <h1>Bem-vindo ao Trunfo de Memes!</h1>
        <p>Abra um pacotinho e descubra a sua carta.</p>
        <a href="/pack">Abrir pacotinho</a>
        <a href="/rules">Ver regras</a>
        

    '''

@app.route("/pack")
def open_pack():
    carta = random.choice(cartas)
    
    return f'''
        <h1>Você desbloqueou.... {carta}</h1>
        <p>Atualize a página para abrir outro pacotinho!</p>
        <a href="/">Voltar</a>
    '''

@app.route("/rules")
def rules():
    return "<p>Cara você quer mesmo saber as regras???</p>"
    
app.run(debug=True)