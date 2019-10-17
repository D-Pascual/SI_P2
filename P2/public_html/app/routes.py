#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from app import app
from flask import render_template, request, url_for, redirect, session
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
            return render_template('index.html', title = "Home", movies=catalogue['peliculas'], pelicula=pelicula, busqueda = 'si')
        else:
            pelicula = request.form['Filtrado']
            if (pelicula != 'Filtrar por'):
                return render_template('index.html', title = "Home", movies=catalogue['peliculas'], pelicula=pelicula, busqueda = 'filtro')
    return render_template('index.html', title = "Home", movies=catalogue['peliculas'], busqueda='no')

@app.route('/<titulo>')
def detalle(titulo):
    catalogue_data = open(os.path.join(app.root_path,'catalogue/catalogo.json'), encoding="utf-8").read()
    catalogue = json.loads(catalogue_data)
    movies = catalogue['peliculas']
    return render_template('detail.html', selection=next((item for item in movies if item["titulo"] == titulo), False))


@app.route('/sesion')
def sesion():
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

    catalogue_data = open(os.path.join(app.root_path,'catalogue/catalogo.json'), encoding="utf-8").read()
    catalogue = json.loads(catalogue_data)
    return render_template('index.html', title = "Home", movies=catalogue['peliculas'])


