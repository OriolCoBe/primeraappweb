from flask import Flask, render_template, request, redirect, url_for, flash, session
import db
from models import (Administradores, Usuarios, Peliculas, Peliculas_vistas, Peliculas_favoritas, Series, Series_vistas,
                    Series_favoritas)

app = Flask(__name__)  # Creamos el servidor en app
app.secret_key = "prueva"  # Creo la clave


# -------------------- Página principal --------------------
@app.route("/")  # Creo la ruta de la página principal
def home():
    return render_template("index.html")  # Lo conecto con el formato definido en "index.html"


# -------------------- Formulario para crear un nuevo usuari@ --------------------
@app.route("/registro-usuario")  # Esta primera ruta me redirecciona a la pagina para crear un/a nuev@ usuari@
def redireccionar_registro():
    return render_template("registro_usuario.html")


@app.route("/registro-usuario", methods=["POST"])  # En esta ruta registro el/la nuev@ usuari@
def nuevo_usuario():  # El nombre y contraseña entran por formulario, los otros atributos los inicializo en 0
    usuario = Usuarios(nombre_usuario=request.form["nombre_usuario"],
                       contrasena_usuario=request.form["contrasena"],
                       pelis_vistas=0,
                       series_vistas=0)

    # Compruevo si el nombre de usuario ya existe en la base de datos y lo guardo en la variable
    nombre_usuario_existe = db.session.query(Usuarios).filter_by(nombre_usuario=usuario.nombre_usuario).first()
    # Compruevo si la contraseña ya existe en la base de datos y lo guardo en la variable
    contrasena_existe = db.session.query(Usuarios).filter_by(contrasena_usuario=usuario.contrasena_usuario).first()

    if nombre_usuario_existe:  # Si el nombre de usuario ya se està usando lanzo el mensaje flash y lo redirecciono a la
        flash("Nombre de usuari@ en uso, prueve con otra opción")  # a la misma pàgina
        return render_template("registro_usuario.html")
    elif contrasena_existe:  # Si la contraseña ya se està usando lanzo el mensaje flash y lo redirecciono a la misma
        flash("Contraseña en uso, prueve con otra opción")  # pàgina
        return render_template("registro_usuario.html")
    else:  # Si no existe ni el nombre ni la contraseña
        db.session.add(usuario)  # Añado el objeto de usuario a la base de datos
        db.session.commit()  # Realizo los cambios
        print("""Usuari@ creado correctamente
                            - Nombre:""", usuario.nombre_usuario,
                           "- Contraseña:", usuario.contrasena_usuario)

        flash("Usuari@ cread@ correctamente")  # Lanzo el mensaje flash

        return render_template("index.html")  # Una vez cread@ el/la usuari@ vuelvo a la página principal


# -------------------- Acceso de usuari@s --------------------
@app.route("/acceso-usuario")  # Esta ruta me redirecciona a la pagina para iniciar sessión
def acceso_usuario():
    return render_template("acceso_usuario.html")


@app.route("/acceso-usuario", methods=["POST", "GET"])
def iniciar_session_usuario():  # Filtro para encontrar el usuario que se quiere logear
                                # (en base a su nombre de usuario y contraseña)
    nombre = request.form["acceso_nombre"]  # La información que viene por el formulario "acceso_nombre" la guardo en la
                                            # variable nombre
    contrasena = request.form["acceso_contrasena"]  # La información que viene por el formulario "acceso_contrasena" la
                                                    # guardo en la variable contraseña
    # Hago la busqueda en la base de datos
    usuario = db.session.query(Usuarios).filter_by(nombre_usuario=str(nombre),
                                                   contrasena_usuario=str(contrasena)).first()

    session["id"] = usuario.id_usuario  # En session almaceno el id del usuario que ha iniciado session
    if usuario is not None:  # Si el usuario existe en la base de datos (coinciden nombre de usuario y contraseña)
        return render_template("zona_usuario.html", usuario=usuario)  # Lo redirecciono a esta pàgina,
    # también envio el usuario para que me permita ver en todo momento cuantas películas y/o series ha visualizado (este
    # procedimiento se repite a lo largo de todo el programa)
    else:  # Si el usuario no existe en la base de datos
        flash("Nombre de usuari@ o contraseña incorrectos. Por favor inténtelo de nuevo")  # lanzo el mensaje flash
        return render_template("acceso_usuario.html")  # y lo redirecciono a la misma pàgina


# -------------------- Acceso de administrador@s --------------------
@app.route("/acceso-admin")  # Esta ruta me redirecciona a la pagina para iniciar sessión
def acceso_admin():
    return render_template("acceso_admin.html")


@app.route("/acceso-admin", methods=["POST"])
def iniciar_session_admin():  # Filtro para encontrar el administrador que se quiere logear
                              # (en base a su nombre de usuario y contraseña)
    nombre = request.form["acceso_nombre_admin"]  # La información que viene por el formulario "acceso_nombre_admin"
                                                  # la guardo en la variable nombre
    contrasena = request.form["acceso_contrasena_admin"]  # La información que viene por el formulario
                                                        # "acceso_contrasena_admin" la guardo en la variable contraseña
    # Hago la busqueda en la base de datos
    admin = db.session.query(Administradores).filter_by(nombre_admin=str(nombre),
                                                        contrasena_admin=str(contrasena)).first()
    if admin is not None:  # Si el administrador existe en la base de datos (coinciden nombre de usuario y contraseña)
        return render_template("zona_admin.html")  # Lo redirecciono a esta pàgina
    else:  # Si el administrador no existe en la base de datos lanzo el mensaje flash
        flash("Nombre de adminstrador/a o contraseña incorrectos. Por favor inténtelo de nuevo")
        return render_template("acceso_admin.html")  # y lo redirecciono a la misma pàgina


# -------------------- Usuari@s --------------------
@app.route("/ver-usuarios")  # Esta  ruta me muestra todos los usuarios de la base de datos
def ver_usuarios():
    todos_usuarios = db.session.query(Usuarios).all()  # Consulto y almaceno todos los usuarios
    print(todos_usuarios)
    if todos_usuarios is not None:  # Si hay usuario en la db redirecciono y cargo los usuarios en la pàgina
        return render_template("zona_admin.html", lista_usuarios=todos_usuarios)  # "usuarios.html"
    else:  # Si no hay usuarios en la db lanzo el mensaje flash y lo redirecciono a la misma pàgina
        flash("Actualmente no hay usuari@s registrad@s")
        return render_template("zona_admin.html")


@app.route("/crear-usuario")  # Esta ruta me redirecciona a la pagina para crear un/a nuev@ usuari@
def redireccionar_crear_usuario():
    return render_template("crear_usuario.html")


@app.route("/crear-usuario", methods=["POST"])  # En esta ruta registro el/la nuev@ usuari@
def crear_usuario():
    usuario = Usuarios(nombre_usuario=request.form["nombre_usuario"],
                       contrasena_usuario=request.form["contrasena"],
                       pelis_vistas=0,
                       series_vistas=0)

    # Compruevo si el nombre de usuario ya existe en la base de datos y lo guardo en la variable
    nombre_usuario_existe = db.session.query(Usuarios).filter_by(nombre_usuario=usuario.nombre_usuario).first()
    # Compruevo si la contraseña ya existe en la base de datos y lo guardo en la variable
    contrasena_existe = db.session.query(Usuarios).filter_by(contrasena_usuario=usuario.contrasena_usuario).first()

    if nombre_usuario_existe:  # Si el nombre de usuario ya se està usando
        flash("Nombre de usuario en uso, prueve con otra opción")  # lanzo el mensaje flash y lo redirecciono
        return render_template("crear_usuario.html")  # a la misma pàgina
    elif contrasena_existe:  # Si la contraseña ya se està usando
        flash("Contraseña en uso, prueve con otra opción")  # lanzo el mensaje flash
        return render_template("crear_usuario.html")  # y lo redirecciono a la misma pàgina
    else:
        db.session.add(usuario)  # Añado el objeto de usuario a la base de datos
        db.session.commit()  # Realizo los cambios
        db.session.close()  # Cierro la base de datos
        flash("Usuari@ cread@ correctamente")
        return render_template("zona_admin.html")  # Una vez cread@ el/la usuari@ vuelvo a la página principal


@app.route("/eliminar-usuario/<id>")  # Esta ruta me permite eliminar el usuario y todas las acciones que ha hecho
def eliminar_usuario(id):  # Hago una consulta en la db en base al id, cuando lo encuentra lo elimina
        usuario = db.session.query(Usuarios).filter_by(id_usuario=int(id)).delete()
        pelis_vistas = db.session.query(Peliculas_vistas).filter_by(id_usuario=int(id)).delete()
        pelis_favoritas = db.session.query(Peliculas_favoritas).filter_by(id_usuario=int(id)).delete()
        serie_vista = db.session.query(Series_vistas).filter_by(id_usuario=int(id)).delete()
        series_favoritas = db.session.query(Series_favoritas).filter_by(id_usuario=int(id)).delete()
        db.session.commit()  # Ejecuto las operaciónes
        db.session.close()  # Cierro la base de datos
        return redirect(url_for("ver_usuarios"))  # Me redirecciona a la función "ver_usuario()"


@app.route("/editar-usuario/<id>")  # Esta ruta selecciona el usuario a editar (en base al id) y redirecciona a la
def editar_usuario(id):             # pàgina donde está el formulario para editarlo
    usuario = db.session.query(Usuarios).filter_by(id_usuario=int(id)).first()  # Busco al usuario en base al id y lo
    return render_template("editar_usuario.html", usuario=usuario)  # "envió" a "editar_usuario.html"


@app.route("/modificar-usuario/<id>", methods=["POST", "GET"])  # Esta ruta recive el id del usuario y realiza los
def modificar_usuario(id):                                           # canvios pertinentes
    usuario = db.session.query(Usuarios).filter_by(id_usuario=id).first()  # Busco al usuario en base al id y realizo la
    usuario.nombre_usuario = request.form["editar-nombre-usuario"]         # actualización
    usuario.contrasena_usuario = request.form["editar-contrasena-usuario"]
    db.session.commit()  # Se realizan los canvios en la base de datos
    db.session.close()   # Se cierra la base de datos
    return redirect(url_for("ver_usuarios"))  # Volvemos a "usuarios" dónde ya podemos visualizar los cambios realizados


# -------------------- Administrador@s --------------------
@app.route("/ver-administradores")  # Esta  ruta me muestra todos l@s administrador@s de la base de datos
def ver_administradores():
    todos_admins = db.session.query(Administradores).all()  # Consulto y almaceno tod@s l@s administrador@s
    print(todos_admins)
    if todos_admins is not None:  # Si hay administrador@s en la db redirecciono y los cargo en la pàgina
        return render_template("zona_admin.html", lista_admin=todos_admins)  # "zona_admin.html"
    else:  # Si no hay usuarios en la db lanzo el mensaje flash y lo redirecciono a la misma pàgina
        flash("Actualmente no hay administrador@s registrad@s")
        return render_template("zona_admin.html")


@app.route("/crear-administrador")  # Esta  ruta me redirecciona a la pagina para crear un/a nuev@ administrador/a
def redireccionar_crear_administrador():
    return render_template("crear_administrador.html")


@app.route("/crear-administrador", methods=["POST"])  # En esta ruta registro el/la nuev@ administrador/a
def crear_administrador():
    administrador = Administradores(nombre_admin=request.form["nombre_admin"],
                                    contrasena_admin=request.form["contrasena"])

    # Compruevo si el nombre de administrador ya existe en la base de datos y lo guardo en la variable
    nombre_admin_existe = db.session.query(Administradores).filter_by(nombre_admin=administrador.nombre_admin).first()
    # Compruevo si la contraseña ya existe en la base de datos y lo guardo en la variable
    contrasena_existe = db.session.query(Administradores).filter_by(contrasena_admin=administrador.contrasena_admin).first()

    if nombre_admin_existe:  # Si el nombre de admin ya se està usando
        flash("Nombre de administrador/a en uso, prueve con otra opción")  # lanzo el mensaje flash y lo redirecciono
        return render_template("crear_administrador.html")  # a la misma pàgina
    elif contrasena_existe:  # Si la contraseña ya se està usando
        flash("Contraseña en uso, prueve con otra opción")  # lanzo el mensaje flash
        return render_template("crear_administrador.html")  # y lo redirecciono a la misma pàgina
    else:
        db.session.add(administrador)  # Añado el objeto administrador a la base de datos
        db.session.commit()  # Realizo los cambios
        db.session.close()  # Cierro la base de datos
        flash("Administrador/a cread@ correctamente")
        return render_template("zona_admin.html")  # Una vez cread@ el/la administrador/a vuelvo a la página principal


@app.route("/eliminar-admin/<id>")  # Esta ruta me permite eliminar el/la admnistrador/a de la base de datos
def eliminar_admin(id):  # Hago una consulta en la db en base al id, cuando lo encuentra lo elimina
        admin = db.session.query(Administradores).filter_by(id_admin=int(id)).delete()
        db.session.commit()  # Ejecuto la operación
        db.session.close()
        return redirect(url_for("ver_administradores"))  # Me redirecciona a la función "ver_administradores()"


@app.route("/editar-admin/<id>")  # Esta ruta selecciona al/la administrador/a a editar (en base al id) y redirecciona a
def editar_admin(id):             # la pàgina donde está el formulario para editarlo
    admin = db.session.query(Administradores).filter_by(id_admin=int(id)).first()  # Busco al administrador en base al
    return render_template("editar_admin.html", admin=admin)  # id y lo "envió" a "editar_admin.html"


@app.route("/modificar-admin/<id>", methods=["POST", "GET"])  # Esta ruta recive el id del/a administrador/a y
def modificar_admin(id):                                           # realiza los canvios pertinentes
    admin = db.session.query(Administradores).filter_by(id_admin=id).first()  # Busco al/la administrador/a en base al
    admin.nombre_admin = request.form["editar-nombre-admin"]                  # id y realizo la actualización
    admin.contrasena_admin = request.form["editar-contrasena-admin"]
    db.session.commit()  # Se realizan los canvios en la base de datos
    db.session.close()   # Se cierra la base de datos
    return redirect(url_for("ver_administradores"))  # Volvemos a "ver_administradores" dónde ya podemos visualizar los
                                                     # cambios realizados


# -------------------- Películas --------------------
@app.route("/ver-peliculas")  # Esta  ruta me muestra todas las películas de la base de datos
def ver_peliculas():
    todas_pelis = db.session.query(Peliculas).all()  # Consulto y almaceno todas las películas
    print(todas_pelis)
    if todas_pelis is not None:  # Si hay películas en la db redirecciono y los cargo en la pàgina "zona_admin.html"
        return render_template("zona_admin.html", lista_pelis=todas_pelis)
    else:  # Si no hay películas en la db lanzo el mensaje flash y lo redirecciono a la misma pàgina
        flash("Actualmente no hay películas registradas")
        return render_template("zona_admin.html")


@app.route("/catalogo-peliculas")  # Esta ruta me muestra todas las películas de la base de datos
def catalogo_peliculas():
    todas_pelis = db.session.query(Peliculas).all()  # Consulto y almaceno todas las películas
    print(todas_pelis)
    usuario = db.session.query(Usuarios).filter_by(id_usuario=session["id"]).first()
    if todas_pelis is not None:  # Si hay películas en la db redirecciono y los cargo en la pàgina "zona_usuario.html"
        return render_template("zona_usuario.html", lista_pelis=todas_pelis, usuario=usuario)
    else:  # Si no hay películas en la db lanzo el mensaje flash y lo redirecciono a la misma pàgina
        flash("Actualmente no hay películas registradas")
        return render_template("zona_usuario.html")


@app.route("/crear-peli")  # Esta  ruta me redirecciona a la pagina para crear una película nueva
def redireccionar_crear_peli():
    return render_template("crear_peli.html")


@app.route("/crear-peli", methods=["POST"])  # En esta ruta registro la película nueva
def crear_peli():  # Todos los atributos del objeto se reciven por formulario
    peli = Peliculas(titulo_peli=request.form["titulo-peli"],
                     genero_peli=request.form["genero-peli"],
                     duracion_peli=request.form["duracion-peli"],
                     director_peli=request.form["director-peli"],
                     elenco_peli=request.form["elenco-peli"],
                     productora_peli=request.form["productora-peli"],
                     sinopsis_peli=request.form["sinopsis-peli"],
                     imagen=request.form["imagen-peli"])

    db.session.add(peli)  # Añado el objeto peli a la base de datos
    db.session.commit()  # Realizo los cambios
    db.session.close()  # Cierro la base de datos
    flash("Película creada correctamente")
    return render_template("zona_admin.html")  # Una vez creada la película vuelvo a la página principal


@app.route("/eliminar-peli/<id>")  # Esta ruta me permite eliminar la película de la base de datos
def eliminar_peli(id):  # Hago una consulta en la db en base al id, cuando lo encuentra lo elimina
        peli = db.session.query(Peliculas).filter_by(id_peli=int(id)).delete()
        peli_vista = db.session.query(Peliculas_vistas).filter_by(id_peli=int(id)).delete()
        peli_favorita = db.session.query(Peliculas_favoritas).filter_by(id_peli=int(id)).delete()
        db.session.commit()  # Ejecuto la operación
        db.session.close()
        return redirect(url_for("ver_peliculas"))  # Me redirecciona a la función "ver_peliculas()"


@app.route("/editar-peli/<id>")  # Esta ruta selecciona la película a editar (en base al id) y redirecciona a la
def editar_peli(id):             # pàgina donde está el formulario para editarla
    peli = db.session.query(Peliculas).filter_by(id_peli=int(id)).first()  # Busco la película en base al id y la
    return render_template("editar_peli.html", peli=peli)  # "envio" a "editar_peli.html"


@app.route("/modificar-peli/<id>", methods=["POST", "GET"])  # Esta ruta recive el id de la película y realiza los
def modificar_peli(id):                                           # canvios pertinentes
    peli = db.session.query(Peliculas).filter_by(id_peli=id).first()  # Busco la película en base al id y realizo la
    peli.titulo_peli = request.form["editar-titulo-peli"]             # actualización
    peli.genero_peli = request.form["editar-genero-peli"]
    peli.duracion_peli = request.form["editar-duracion-peli"]
    peli.director_peli = request.form["editar-director-peli"]
    peli.elenco_peli = request.form["editar-elenco-peli"]
    peli.productora_peli = request.form["editar-productora-peli"]
    peli.sinopsis_peli = request.form["editar-sinopsis-peli"]
    peli.imagen = request.form["editar-imagen"]
    db.session.commit()  # Se realizan los canvios en la base de datos
    db.session.close()   # Se cierra la base de datos
    return redirect(url_for("ver_peliculas"))  # Volvemos a "ver_peliculas" dónde ya podemos visualizar los cambios


@app.route("/peli-vista/<id>", methods=["POST", "GET"])  # Esta ruta permite marcar un película como vista
def peli_vista(id):  # Hago una consulta en la db en base al id para saber que película se esta marcando com vista
    peli = db.session.query(Peliculas).filter_by(id_peli=int(id)).first()
    acciones_hechas = db.session.query(Peliculas_vistas).all()  # Guardo todos los registros de la tabla
    # peliculas_vistas en esta variable
    if len(acciones_hechas) == 0:  # Si no hay registros en la tabla (lo se por la longitud de la lista)
        id_accion = 1  # El valor de id_accion es 1 (porque será el primer registro)
    else:  # Por el contrario, si la tabla tiene algun registro
        ultimo_registro = acciones_hechas[-1]  # Guardo el ultimo elemento de la lista en ultimo registro y el valor de
        id_accion = ultimo_registro.id_accion + 1  # id_accion es el ultimo id_accion de la tabla mas 1 (así me aseguro
                                                   # que este nunca se repita
    peli_vista = Peliculas_vistas(id_accion=id_accion,  # Uso la variable id_accion para indicar el id_accion de la tabla
                                  id_usuario=session["id"],  # Creo el registro con el id del usuario que esta en sesion
                                  id_peli=peli.id_peli)  # y con el id de la película
    db.session.add(peli_vista)  # Incorporo el registro a la tabla
    db.session.commit()         # Realizo los canvios
    db.session.close()          # Cierro la base de datos

    usuario = db.session.query(Usuarios).filter_by(id_usuario=session["id"]).first()  # Obtengo el usuario en sesion
    pelis_vistas = db.session.query(Peliculas_vistas).filter_by(id_usuario=usuario.id_usuario).all()  # Obtengo todas
    # las películas que ha visto el usuario que está en sesion y lo guardo en una lista
    numero_pelis_vistas = len(pelis_vistas)  # Guardo la longitud de la lista, o en otras palabras,
    # cuantas películas ha visto el usuario en numero_pelis_vistas
    usuario.pelis_vistas = numero_pelis_vistas   # Defino que el número de la variable numero_pelis_vistas será el
    # valor del atributo pelis_vistas del usuario en sesion
    db.session.commit()  # Realizo los canvios
    db.session.close()   # Cierro la base de datos
    return redirect(url_for("catalogo_peliculas"))  # Me redirecciona a la función "catalogo_peliculas()"


@app.route("/peliculas-visualizadas")  # Esta ruta me muestra todas las películas que el usuario ha visualizado
def peliculas_visualizadas():  # Consulto y almaceno todas las películas que ha visto un usuario (busco en base a su id)
    id_pelis_visualizadas = db.session.query(Peliculas_vistas).filter_by(id_usuario=session["id"]).all()
    pelis_visualizadas = []  # Creo una lista, de momento vacía
    usuario = db.session.query(Usuarios).filter_by(id_usuario=session["id"]).first()
    for peli in id_pelis_visualizadas:  # Con este bucle por cada película que ha visto el usuario, puedo obtener el
        pelicula_vista = db.session.query(Peliculas).get(peli.id_peli)  # objeto de esa película (de la tabla Peliculas)
        pelis_visualizadas.append(pelicula_vista)  # Y la almazeno en esta lista

    if pelis_visualizadas is not None:  # Si hay películas en la db redirecciono y los cargo en "zona_usuario.html"
        return render_template("zona_usuario.html", lista_pelis=pelis_visualizadas, usuario=usuario)
    else:  # Si no hay películas en la db lanzo el mensaje flash y lo redirecciono a la misma pàgina
        flash("De momento no se ha visualizado ninguna películas")
        return render_template("zona_usuario.html")


@app.route("/peli-favorita/<id>", methods=["POST", "GET"])  # Esta ruta permite marcar un película como favorita
def peli_favorita(id):  # Hago una consulta en la db en base al id para saber que película se esta marcando com favorita
    peli = db.session.query(Peliculas).filter_by(id_peli=int(id)).first()
    acciones_hechas = db.session.query(Peliculas_favoritas).all()  # Guardo todos los registros de la tabla en esta
    # variable
    if len(acciones_hechas) == 0:  # Si no hay registros en la tabla (lo se por la longitud de la lista)
        id_accion = 1  # El valor de id_accion es 1 (porque será el primer registro)
    else:  # Por el contrario, si la tabla tiene algun registro
        ultimo_registro = acciones_hechas[-1]  # Guardo el ultimo elemento de la lista en ultimo registro y el valor de
        id_accion = ultimo_registro.id_accion + 1  # id_accion es el ultimo id_accion de la tabla mas 1 (así me aseguro
        # que este nunca se repita
    peli_favorita = Peliculas_favoritas(id_accion=id_accion,
                                        id_usuario=session["id"],  # Creo el registro con el id del usuario que esta en
                                        id_peli=peli.id_peli)  # sesion y con el id de la película
    db.session.add(peli_favorita)  # Incorporo el registro a la tabla
    db.session.commit()            # Realizo los canvios
    db.session.close()             # Cierro la base de datos
    return redirect(url_for("catalogo_peliculas"))  # Me redirecciona a la función "catalogo_peliculas()"


@app.route("/peliculas-favoritas")  # Esta ruta me muestra todas las películas que el usuario ha marcado como favoritas
def peliculas_favoritas():  # Consulto y almaceno todas las películas que ha visto un usuario (busco en base a su id)
    id_pelis_favoritas = db.session.query(Peliculas_favoritas).filter_by(id_usuario=session["id"]).all()
    pelis_favoritas = []  # Creo una lista, de momento vacía
    usuario = db.session.query(Usuarios).filter_by(id_usuario=session["id"]).first()
    for peli in id_pelis_favoritas:  # Con este bucle por cada película que el usuario ha marcado como favorita, puedo
        pelicula_favorita = db.session.query(Peliculas).get(peli.id_peli)  # obtener el objeto de esa película
        pelis_favoritas.append(pelicula_favorita)  # Y la almazeno en esta lista

    if pelis_favoritas is not None:  # Si hay películas en la db redirecciono y los cargo en "zona_usuario.html"
        return render_template("zona_usuario.html", lista_pelis=pelis_favoritas, usuario=usuario)
    else:  # Si no hay películas en la db lanzo el mensaje flash y lo redirecciono a la misma pàgina
        flash("De momento no se ha visualizado ninguna películas")
        return render_template("zona_usuario.html")


# -------------------- Series --------------------
@app.route("/ver-series")  # Esta  ruta me muestra todas las series de la base de datos
def ver_series():
    todas_series = db.session.query(Series).all()  # Consulto y almaceno todas las series
    print(todas_series)
    if todas_series is not None:  # Si hay series en la db redirecciono y los cargo en la pàgina "zona_admin.html"
        return render_template("zona_admin.html", lista_series=todas_series)
    else:  # Si no hay series en la db lanzo el mensaje flash y lo redirecciono a la misma pàgina
        flash("Actualmente no hay series registradas")
        return render_template("zona_admin.html")


@app.route("/catalogo-series")  # Esta  ruta me muestra todas las series de la base de datos
def catalogo_series():
    todas_series = db.session.query(Series).all()  # Consulto y almaceno todas las series
    print(todas_series)
    usuario = db.session.query(Usuarios).filter_by(id_usuario=session["id"]).first()
    if todas_series is not None:  # Si hay series en la db redirecciono y los cargo en la pàgina "zona_admin.html"
        return render_template("zona_usuario.html", lista_series=todas_series, usuario=usuario)
    else:  # Si no hay series en la db lanzo el mensaje flash y lo redirecciono a la misma pàgina
        flash("Actualmente no hay series registradas")
        return render_template("zona_usuario.html")


@app.route("/crear-serie")  # Esta  ruta me redirecciona a la pagina para crear una serie nueva
def redireccionar_crear_serie():
    return render_template("crear_serie.html")


@app.route("/crear-serie", methods=["POST"])  # En esta ruta registro la nueva serie
def crear_serie():
    serie = Series(titulo_serie=request.form["titulo-serie"],
                     genero_serie=request.form["genero-serie"],
                     temporadas=request.form["temporadas"],
                     capitulos=request.form["capitulos"],
                     duracion_cap=request.form["duracion-cap"],
                     director_serie=request.form["director-serie"],
                     elenco_serie=request.form["elenco-serie"],
                     productora_serie=request.form["productora-serie"],
                     sinopsis_serie=request.form["sinopsis-serie"],
                     imagen=request.form["imagen-serie"])

    db.session.add(serie)  # Añado el objeto serie a la base de datos
    db.session.commit()  # Realizo los cambios
    db.session.close()  # Cierro la base de datos
    flash("Serie creada correctamente")  # Lanzo el mensaje flash
    return render_template("zona_admin.html")  # Una vez creada la serie vuelvo a la página principal


@app.route("/eliminar-serie/<id>")  # Esta ruta me permite eliminar la serie de la base de datos
def eliminar_serie(id):  # Hago una consulta en la db en base al id, cuando la encuentra la elimina
        serie = db.session.query(Series).filter_by(id_serie=int(id)).delete()
        serie_vista = db.session.query(Series_vistas).filter_by(id_serie=int(id)).delete()
        serie_favorita = db.session.query(Series_vistas).filter_by(id_serie=int(id)).delete()
        db.session.commit()  # Ejecuto la operación
        return redirect(url_for("ver_series"))  # Me redirecciona a la función "ver_series()"


@app.route("/editar-serie/<id>")  # Esta ruta selecciona la serie a editar (en base al id) y redirecciona a la
def editar_serie(id):              # pàgina donde está el formulario para editarla
    serie = db.session.query(Series).filter_by(id_serie=int(id)).first()  # Busco la serie en base al id y lo
    return render_template("editar_serie.html", serie=serie)  # "envio" a "editar_serie.html"


@app.route("/modificar-serie/<id>", methods=["POST", "GET"])  # Esta ruta recive el id de la serie y realiza los
def modificar_serie(id):                                           # canvios pertinentes
    serie = db.session.query(Series).filter_by(id_serie=id).first()  # Busco la serie en base al id y realizo la
    serie.titulo_serie = request.form["editar-titulo-serie"]         # actualización
    serie.genero_serie = request.form["editar-genero-serie"]
    serie.temporadas = request.form["editar-temporadas"]
    serie.capitulos = request.form["editar-capitulos"]
    serie.duracion_cap = request.form["editar-duracion-cap"]
    serie.director_serie = request.form["editar-director-serie"]
    serie.elenco_serie = request.form["editar-elenco-serie"]
    serie.productora_serie = request.form["editar-productora-serie"]
    serie.sinopsis_serie = request.form["editar-sinopsis-serie"]
    serie.imagen = request.form["editar-imagen-serie"]
    db.session.commit()  # Se realizan los canvios en la base de datos
    db.session.close()   # Se cierra la base de datos
    return redirect(url_for("ver_series"))  # Volvemos a "ver_series" dónde ya podemos visualizar los cambios


@app.route("/serie-vista/<id>", methods=["POST", "GET"])  # Esta ruta permite marcar una serie como vista
def serie_vista(id):  # Hago una consulta en la db en base al id para saber que serie se esta marcando com vista
    serie = db.session.query(Series).filter_by(id_serie=int(id)).first()
    acciones_hechas = db.session.query(Series_vistas).all()  # Guardo todos los registros de la tabla en esta variable
    if len(acciones_hechas) == 0:  # Si no hay registros en la tabla (lo se por la longitud de la lista)
        id_accion = 1  # El valor de id_accion es 1 (porque será el primer registro)
    else:  # Por el contrario, si la tabla tiene algun registro
        ultimo_registro = acciones_hechas[-1]  # Guardo el ultimo elemento de la lista en ultimo registro y el valor de
        id_accion = ultimo_registro.id_accion + 1  # id_accion es el ultimo id_accion de la tabla mas 1 (así me aseguro
        # que este nunca se repita
    serie_vis = Series_vistas(id_accion=id_accion,
                              id_usuario=session["id"],  # Creo el registro con el id del usuario que esta en sesion
                              id_serie=serie.id_serie)  # y con el id de la serie
    db.session.add(serie_vis)  # Incorporo el registro a la tabla
    db.session.commit()          # Realizo los canvios
    db.session.close()           # Cierro la base de datos

    usuario = db.session.query(Usuarios).filter_by(id_usuario=session["id"]).first()  # Obtengo el usuario en sesion
    series_vistas = db.session.query(Series_vistas).filter_by(id_usuario=usuario.id_usuario).all()  # Obtengo todas las
    # series que ha visto el usuario que está en sesion y lo guardo en una lista
    numero_series_vistas = len(series_vistas)  # Guardo la longitud de la lista, o en otras palabras, cuantas series ha
    # ha visto el usuario en numero_series_vistas
    usuario.series_vistas = numero_series_vistas  # Defino que el número de la variable numero_series_vistas será el
    # valor del atributo series_vistas del usuario en sesion
    db.session.commit()  # Realizo los canvios
    db.session.close()  # Cierro la base de datos
    return redirect(url_for("catalogo_series"))  # Me redirecciona a la función "catalogo_series()"


@app.route("/series-visualizadas")  # Esta ruta me muestra todas las series que el usuario ha visualizado
def series_visualizadas():  # Consulto y almaceno todas las series que ha visto un usuario (busco en base a su id)
    id_series_visualizadas = db.session.query(Series_vistas).filter_by(id_usuario=session["id"]).all()
    series_visual = []  # Creo una lista, de momento vacía
    usuario = db.session.query(Usuarios).filter_by(id_usuario=session["id"]).first()
    for serie in id_series_visualizadas:  # Con este bucle por cada película que ha visto el usuario, puedo obtener el
        serie_vi = db.session.query(Series).get(serie.id_serie)  # objeto de esa película (de la tabla Peliculas)
        series_visual.append(serie_vi)  # Y la almazeno en esta lista

    if series_visual is not None:  # Si hay series en la db redirecciono y los cargo en "zona_usuario.html"
        return render_template("zona_usuario.html", lista_series=series_visual, usuario=usuario)
    else:  # Si no hay películas en la db lanzo el mensaje flash y lo redirecciono a la misma pàgina
        flash("De momento no se ha visualizado ninguna serie")
        return render_template("zona_usuario.html")


@app.route("/serie-favorita/<id>", methods=["POST", "GET"])  # Esta ruta permite marcar un serie como favorita
def serie_favorita(id):  # Hago una consulta en la db en base al id para saber que serie se esta marcando com favorita
    serie = db.session.query(Series).filter_by(id_serie=int(id)).first()
    acciones_hechas = db.session.query(Series_favoritas).all()  # Guardo todos los registros de la tabla en esta
    # variable
    if len(acciones_hechas) == 0:  # Si no hay registros en la tabla (lo se por la longitud de la lista)
        id_accion = 1  # El valor de id_accion es 1 (porque será el primer registro)
    else:  # Por el contrario, si la tabla tiene algun registro
        ultimo_registro = acciones_hechas[-1]  # Guardo el ultimo elemento de la lista en ultimo registro y el valor de
        id_accion = ultimo_registro.id_accion + 1  # id_accion es el ultimo id_accion de la tabla mas 1 (así me aseguro
        # que este nunca se repita
    serie_favor = Series_favoritas(id_accion=id_accion,
                                   id_usuario=session["id"],  # Creo el registro con el id del usuario en sesion
                                   id_serie=serie.id_serie)  # y con el id de la serie
    db.session.add(serie_favor)  # Incorporo el registro a la tabla
    db.session.commit()  # Realizo los canvios
    db.session.close()  # Cierro la base de datos
    return redirect(url_for("catalogo_series"))  # Me redirecciona a la función "catalogo_series()"


@app.route("/series-favoritas")  # Esta ruta me muestra todas las series que el usuario ha marcado como favoritas
def series_favoritas():  # Consulto y almaceno todas las series que un usuario ha marcado como favoritas
    id_series_favoritas = db.session.query(Series_favoritas).filter_by(id_usuario=session["id"]).all()
    series_favs = []  # Creo una lista, de momento vacía
    usuario = db.session.query(Usuarios).filter_by(id_usuario=session["id"]).first()
    for serie in id_series_favoritas:  # Con este bucle por cada serie que el usuario ha marcado como favorita, puedo
        serie_fav = db.session.query(Series).get(serie.id_serie)  # obtener el objeto de esa serie (usando el id)
        series_favs.append(serie_fav)  # Y la almazeno en esta lista

    if series_favs is not None:  # Si hay series en la db redirecciono y los cargo en "zona_usuario.html"
        return render_template("zona_usuario.html", lista_series=series_favs, usuario=usuario)
    else:  # Si no hay películas en la db lanzo el mensaje flash y lo redirecciono a la misma pàgina
        flash("De momento no se ha marcado como favorita ninguna serie")
        return render_template("zona_usuario.html")


# -------------------- Buscadores --------------------
@app.route("/buscador", methods=["POST"])  # En esta ruta creo el buscador
def buscador():
    usuario = db.session.query(Usuarios).filter_by(id_usuario=session["id"]).first()
    consulta = request.form["buscar"]  # Guardo en la variable genero el valor introducido en el buscador
    pelis_genero = db.session.query(Peliculas).filter_by(genero_peli=consulta).all()  # Hago una busqueda por género
    # en la tabla Peliculas
    pelis_titulo = db.session.query(Peliculas).filter_by(titulo_peli=consulta).all()  # Hago una busqueda por título en
    # la tabla Peliculas
    series_genero = db.session.query(Series).filter_by(genero_serie=consulta).all()  # Hago una busqueda por género
    # en la tabla Series
    series_titulo = db.session.query(Series).filter_by(titulo_serie=consulta).all()  # Hago una busqueda por título en
    # la tabla Series
    resultado_pelis = pelis_genero + pelis_titulo
    resultado_series = series_genero + series_titulo
    print(resultado_pelis, resultado_series)
    return render_template("zona_usuario.html", lista_pelis=resultado_pelis,  # Envio el resultado de
                           lista_series=resultado_series, usuario=usuario)  # las busquedas a "zona_usuario.html"


# -------------------- Logout --------------------
@app.route("/logout")
def logout():
    return render_template("index.html")


if __name__ == "__main__":
    db.Base.metadata.create_all(db.engine)  # Creamos la base de datos
    app.run(debug=True)  # Con el debug el servidor se reinicia despues de cada canvio
