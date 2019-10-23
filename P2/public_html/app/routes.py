#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from app import app
from flask import render_template, request, url_for, redirect, session, make_response
import json
import os
import sys
import hashlib
from random import randrange
from flask import flash
import ast


@app.route('/', methods=['POST', 'GET', 'PUT'])
@app.route('/index', methods=['POST', 'GET', 'PUT'])
def index():
    catalogue_data = open(os.path.join(app.root_path,'catalogue/catalogo.json'), encoding="utf-8").read()
    catalogue = json.loads(catalogue_data)

    if request.method == 'POST':
        if 'Busqueda' in request.form:
            pelicula = request.form['Busqueda']
            return render_template('index.html', title = "Home", movies=catalogue['peliculas'], pelicula=pelicula, busqueda = 'si', session=session)
        else:
            pelicula = request.form['Filtrado']
            if (pelicula != 'Filtrar por'):
                return render_template('index.html', title = "Home", movies=catalogue['peliculas'], pelicula=pelicula, busqueda = 'filtro', session=session)

    return render_template('index.html', title = "Home", movies=catalogue['peliculas'], busqueda='no', session=session)

@app.route('/<titulo>')
def detalle(titulo):
    catalogue_data = open(os.path.join(app.root_path,'catalogue/catalogo.json'), encoding="utf-8").read()
    catalogue = json.loads(catalogue_data)
    movies = catalogue['peliculas']
    return render_template('detail.html', selection=next((item for item in movies if item["titulo"] == titulo), False))


@app.route('/sesion')
def sesion():
    last_user = request.cookies.get('username')
    if last_user:
        return render_template('sesion.html', title = "Sesion", last_user=last_user)
    return render_template('sesion.html', title = "Sesion")


@app.route('/registrar', methods=['GET', 'POST'] )
def registrar():   
    if request.method == "POST":
        usuario = { "username" : request.form['usuario'],
                    "password" :  hashlib.md5(request.form['password'].encode('utf-8')).hexdigest(),
                    "email" : request.form['email'],
                    "genero" : request.form['genero'],
                    "edad" : request.form['edad'],
                    "tarjeta" : request.form['tarjeta'], 
                    "saldo" :  randrange(101)}

        directorio = os.path.join(app.root_path, 'usuarios', request.form['usuario'])
        try:
            os.makedirs(directorio)
        except OSError:
            flash('¡El usuario ya existe!')
            return redirect(url_for('sesion'))        

        directorio = os.path.join(app.root_path, 'usuarios', request.form['usuario'], 'datos.dat')
        data_file = open(directorio,"w")
        data_file.write(str(usuario))
        data_file.close()

        directorio = os.path.join(app.root_path, 'usuarios', request.form['usuario'], 'historial.json')
        historial = open(directorio,"w")
        historial.close()

    return redirect(url_for('index'))


@app.route('/login', methods=['GET', 'POST'] )
def login():   
    if request.method == "POST":
        usuario = request.form['usuario']
        password =  hashlib.md5(request.form['password'].encode('utf-8')).hexdigest()                  

        directorio = os.path.join(app.root_path, 'usuarios', usuario, 'datos.dat')
        try:
            with open(directorio, "r") as data_file:
                data_dictionary = ast.literal_eval(data_file.read())
        except IOError:
            flash('¡El usuario no existe!')
            flash('Puedes registrarte en esta misma página.')
            return redirect(url_for('sesion'))       

        if( password != data_dictionary.get('password') ):
            flash('¡Contraseña errónea!')
            return redirect(url_for('sesion')) 

        session['logged_in'] = True
        session['usuario'] = request.form['usuario']
        session.modified=True

        resp = make_response(redirect(url_for('index')))
        resp.set_cookie('username', usuario)
        return resp

        # return redirect(url_for('index')) 
    else:
        flash('Error en el login, pruebe otra vez.')
        return redirect(url_for('sesion')) 

@app.route('/logout/<user>')
def logout(user):   
    if 'logged_in' in session:
        session.pop('usuario', None)
        session.pop('cart', None)
        session.pop('logged_in', None)
        session.modified=True
    else:
        flash('Hubo un error al cerrar sesión')

    return redirect(url_for('index'))

@app.route("/carrito")
def carrito():
    catalogue_data = open(os.path.join(app.root_path,'catalogue/catalogo.json'), encoding="utf-8").read()
    catalogue = json.loads(catalogue_data)
    
    ids_in_cart = session.get('cart',[])
    movies = []
    precio = 0
    
    for x in catalogue['peliculas']:
        if x['id'] in ids_in_cart:
            movies.append(x)
            precio += x['precio']
            


    return render_template("carrito.html", movies=movies, precio=precio)


@app.route("/add_to_cart/<id>")
def add_to_cart(id):
    if 'cart' not in session:
        session['cart'] = []

    session['cart'].append(int(id))

    flash('Elemento añadido al carrito')
    
    catalogue_data = open(os.path.join(app.root_path,'catalogue/catalogo.json'), encoding="utf-8").read()
    catalogue = json.loads(catalogue_data)
    for x in catalogue['peliculas']:
        if x['id'] == int(id):
            return redirect("/" + x['titulo'])
    
    return redirect("/carrito")
     
@app.route('/borrarCarrito')
def borrarCarrito():   
    session.pop('cart', None)
    session.modified=True

    return redirect(url_for('carrito'))

@app.route('/borrarElemento/<id>')
def borrarElemento(id):   
    session['cart'].remove(int(id))
    session.modified=True

    return redirect(url_for('carrito'))
