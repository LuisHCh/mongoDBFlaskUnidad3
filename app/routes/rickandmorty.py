from flask import Blueprint, render_template, url_for, flash, redirect, request
from app.forms import RickandmortyForm
from app.db import db
from app.models.rickandmorty import RickandMorty

rickandmorty_router = Blueprint('rickandmorty_router',__name__)

@rickandmorty_router.route("/")
def index():
    personajes = db.rickandmorty.find()
    return render_template("indexRM.html",personajes=personajes)


@rickandmorty_router.route("/obtenerPersonajes")
def obtenerPersonajes():
    personajesTotales = RickandMorty.obtenerPersonajes()        # [personajesPagina1][personajesPagina2][personajesPagina3][personajesPagina4][][]
    for personajeXpagina in personajesTotales:                  # [personajesPagina1] = [personajeID1][personajeID2][personajeID3][]
        for personaje in personajeXpagina:                      # [personajeID1] 
            new_personaje = RickandMorty(
                id=str(personaje['id']),
                name=personaje['name'],
                status=personaje['status'],
                species=personaje['species'],
                location=personaje['location'],
                image=personaje['image']
            )
            db.rickandmorty.insert_one(new_personaje.to_json())
    
    personajesDB = db.rickandmorty.find()
    return render_template("indexRM.html",personajes=personajesDB)

# Detalle del personaje
@rickandmorty_router.route("/detail/<id>",methods=['GET','POST'])
def detail_personaje(id):
    personaje = db.rickandmorty.find({"id": int(id)})
    personaje_detail = list(personaje)
    return render_template("detailRM.html",personaje=personaje_detail[0])

# Eliminar personaje
@rickandmorty_router.route("/eliminar/<id>")
def delete_personaje(id):
  db.rickandmorty.delete_one({"name": id})

  flash("Personaje eliminado", "success")

  return redirect(url_for('rickandmorty_router.index'))

# Actualizar personaje
@rickandmorty_router.route('/actualizar/<int:id>', methods=['GET', 'POST'])
def vista_actualizar(id):
    personaje = db.rickandmorty.find({"id": int(id)})
    personaje_detail = list(personaje)
    print(personaje_detail)

    if request.method == 'POST':
        updated_personaje = {
            'name': request.form["name"], 
            'status': request.form["status"],
            'species': request.form["species"] 
            , 'location.name': request.form["location"]
            }
        db.rickandmorty.update_one({'_id': personaje_detail[0]["_id"]}, {"$set": updated_personaje})
        return redirect(url_for('rickandmorty_router.index'))

    return render_template("actualizarPersonaje.html", personaje=personaje_detail[0])