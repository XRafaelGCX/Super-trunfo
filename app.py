import random 
 
from flask import Flask, redirect, render_template, request
 
app = Flask(__name__)

cartas = {
    "cebolo" : {
                    "nome" : "Cebolo",
                    "img" : "Cebolinha.jpg",
                    "raridade" : "rara",
                    "viralidade" : 25,
                    "resenha" : 100,
                    "aura" : 70
                },
    "calado" : {
                    "nome" : "Calado beta",
                    "img" : "calado beta.jpg",
                    "raridade" : "lendaria",
                    "viralidade" : 75,
                    "resenha" : 80,
                    "aura" : 80
                },
    "burro" : {
                    "nome" : "Burro carente",
                    "img" : "burro.jpg",
                    "raridade" : "Incomum",
                    "viralidade" : 75,
                    "resenha" : 55,
                    "aura" : 60
                },    
}


@app.route("/")
def index():
    return render_template("index.html", cartas=cartas)


@app.route("/regras")
def regras():
    return render_template("regras.html")


# Pacotinho: sorteia uma carta e vai direto para o duelo
@app.route("/pacotinho")
def pacotinho():
    carta = random.choice(list(cartas))
    return redirect("/duelo/" + carta)


# Duelo, passo 1: escolher o atributo
@app.route("/duelo/<carta>")
def escolher_atributo(carta):
    if carta not in cartas:          # apelido errado? volta para a coleção
        return redirect("/")
    return render_template("atributo.html", carta=carta, minha=cartas[carta])


# Duelo, passo 2: comparar com uma carta sorteada
@app.route("/duelo/<carta>/<atributo>")
def resultado(carta, atributo):
    if carta not in cartas:
        return redirect("/")
    minha = cartas[carta]
    if atributo not in minha:        # atributo errado? volta para a escolha
        return redirect("/duelo/" + carta)

    outras = [c for c in cartas if c != carta]
    if len(outras) == 0:             # só tem uma carta? duela com ela mesma
        outras = [carta]
    adversaria = cartas[random.choice(outras)]

    if minha[atributo] > adversaria[atributo]:
        resultado = "Você venceu!"
    elif minha[atributo] < adversaria[atributo]:
        resultado = "Você perdeu!"
    else:
        resultado = "Empate!"

    poder_total = minha["viralidade"] + minha["resenha"] + minha["aura"]

    return render_template("resultado.html",
                           atributo=atributo,
                           minha=minha,
                           adversaria=adversaria,
                           resultado=resultado,
                           poder_total=poder_total)

#Rota para criar rota

@app.route("/criar")
def criar():
    return render_template("criar.html")

@app.route("/carta_criada", methods=["POST"])
def carta_criada():
    nome = request.form["nome"]
    imagem = request.form["imagem"]
    raridade = request.form["raridade"]
    viralidade = int(request.form["viralidade"])
    resenha = int(request.form["resenha"])
    aura = int(request.form["aura"])

    # A carta nova também entra no duelo (até o servidor reiniciar!)
    chave = nome.lower().replace(" ", "-")
    cartas[chave] = {"nome": nome, "img": imagem, "raridade": raridade,
                     "viralidade": viralidade, "resenha": resenha, "aura": aura}

    poder_total = viralidade + resenha + aura
    return render_template("carta_criada.html",
                           chave=chave, nome=nome, imagem=imagem, raridade=raridade,
                           viralidade=viralidade, resenha=resenha, aura=aura,
                           poder_total=poder_total)

if __name__ == "__main__":
    app.run(debug=True)