#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from app import app
from flask import render_template, request, url_for, redirect, session
import json
import os
import sys
import hashlib
from random import randrange


@app.route('/')
@app.route('/index')
def index():
    catalogue_data = open(os.path.join(app.root_path,'catalogue/catalogo.json'), encoding="utf-8").read()
    catalogue = json.loads(catalogue_data)
    return render_template('index.html', title = "Home", movies=catalogue['peliculas'])

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

        os.makedirs(os.path.join(app.root_path, 'usuarios/', request.form['usuario'], '/'),exist_ok=True)

        data_file = open(os.path.join(app.root_path, 'usuarios/', request.form['usuario'], '/datos.dat'),"w")
        data_file.write(usuario)
        data_file.close()

    return redirect(url_for('index'))