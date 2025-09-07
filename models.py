import db # Puedo acceder a la db
from sqlalchemy import Column, Integer, String, Text, ForeignKey


class Administradores(db.Base):
    """Clase Administradores
     Incluye la información necesaria para acceder al perfíl de administrador que se desee.

     args
     - id_admin: Es un integer que indica el número de indentificación que el administrador tendrá en la base de datos.
     Es la primary key.
     - nombre_admin: Es una cadena que indica el nombre del administrador. Es necesario para acceder al perfíl
     del administrador.
     - contrasena_admin: Es una cadena que indica la contraseña del administrador. Es necesario para acceder al perfíl
     del administrador."""

    __tablename__ = "administradores"
    id_admin = Column(Integer, primary_key=True)  # Identificador único de cada usuario, al ser la PK no hace
                                                  # falta especificar el autoincrementador, lo hace por defecto
    nombre_admin = Column(String(50), nullable=False, unique=True)  # Campo obligatorio e irrepetible,
                                                                    # acepta 50 carácteres como mucho
    contrasena_admin = Column(String(50), nullable=False, unique=True)  # Campo obligatorio e irrepetible,
                                                                        # acepta 50 carácteres como mucho

    def __init__(self, nombre_admin, contrasena_admin):  # El id lo añade la base de datos automaticamente
        """Constructor de la clase Administrador"""
        self.nombre_admin = nombre_admin
        self.contrasena_admin = contrasena_admin
        print("El administrador se ha creado correctamente")

    def __repr__(self):
        """Método __repr__ de la clase Administrador. Devuelve la información necesaria para replicar el objeto"""
        return """Administrador {}: 
                    - Nombre: {} 
                    - Contraseña: {}\n""".format(self.id_admin, self.nombre_admin, self.contrasena_admin)

    def __str__(self):
        """Método __str__ de la clase Administrador. Indica al sistema la información del objeto"""
        return """Administrador {}: 
                    - Nombre: {} 
                    - Contraseña: {}\n""".format(self.id_admin, self.nombre_admin, self.contrasena_admin)


class Usuarios(db.Base):
    """Clase Usuarios
         Incluye la información relevante del usuario.

         args
         - id_usuario: Es un integer que indica el número de indentificación que el usuario tendrá en la base de datos.
         Es la primary key.
         - nombre_usuario: Es una cadena que indica el nombre del usuario. Es necesario para acceder al perfíl del
         usuario.
         - contrasena_usuario: Es una cadena que indica la contraseña del usuario. Es necesario para acceder al perfíl
         del usuario.
         - pelis_vistas: Es un integer que indica cuantas películas ha visto el usuario.
         - series_vistas: Es un integer que indica lcuantas series ha visto el usuario."""

    __tablename__ = "usuarios"
    id_usuario = Column(Integer, primary_key=True)  # Es la primary key
    nombre_usuario = Column(String(50), nullable=False, unique=True)  # Campo obligatorio e irrepetible,
                                                                      # acepta 50 carácteres como mucho
    contrasena_usuario = Column(String(50), nullable=False, unique=True)  # Campo obligatorio e irrepetible,
                                                                          # acepta 50 carácteres como mucho
    pelis_vistas = Column(Integer, nullable=True)
    series_vistas = Column(Integer, nullable=True)

    def __init__(self,
                 nombre_usuario,
                 contrasena_usuario,
                 pelis_vistas,
                 series_vistas):
        """Constructor de la clase Usuario"""
        self.nombre_usuario = nombre_usuario
        self.contrasena_usuario = contrasena_usuario
        self.pelis_vistas = pelis_vistas
        self.series_vistas = series_vistas
        print("Datos recogidos correctamente")

    def __repr__(self):
        """Método __repr__ de la clase Usuario. Devuelve la información necesaria para replicar el objeto"""
        return """Usuario {}:
                    - Nombre: {}
                    - Contraseña: {}
                    - Est@ usuari@ ha visualizado {} películas
                    - Est@ usuari@ ha visualizado {} películas\n""".format(self.id_usuario,
                                                                            self.nombre_usuario,
                                                                            self.contrasena_usuario,
                                                                            self.pelis_vistas,
                                                                            self.series_vistas)
    def __str__(self):
        """Método __str__ de la clase Usuario. Indica al sistema la información del objeto"""
        return """Usuario {}:
                            - Nombre: {}
                            - Contraseña: {}
                            - Est@ usuari@ ha visualizado {} películas
                            - Est@ usuari@ ha visualizado {} películas\n""".format(self.id_usuario,
                                                                                   self.nombre_usuario,
                                                                                   self.contrasena_usuario,
                                                                                   self.pelis_vistas,
                                                                                   self.series_vistas)


class Peliculas(db.Base):
    """Clase Peliculas
    Incluye la información relevante de la película.

    args:
    - id_peli: Es un integer que indica el número de indentificación que la película tendrá en la base de datos.
    Es la primary key.
    - genero_peli: Es una cadena que indica el género de la película.
    - titulo_peli: Es una cadena que indica el título de la película.
    - duracion_peli: Es un integer que indica la duración de la película en minutos.
    - director_peli: Es una cadena que indica el nombre del director/a de la película.
    - elenco_peli: Es una cadena que indica los actores y actrizes principales de la película.
    - productora_peli: Es una cadena que indica la productura de la película.
    - sinopsis_peli: Es una cadena que da una breve explicación de la película.
    - imagen: Es una cadena con el nombre de la imagen."""

    __tablename__ = "peliculas"
    id_peli = Column(Integer, primary_key=True)  # Es la primary key
    genero_peli = Column(String(50), nullable=False) # Campo obligatorio, acepta 50 carácteres como mucho
    titulo_peli = Column(String(100), nullable=False)  # Campo obligatorio, acepta 100 carácteres como mucho
    duracion_peli = Column(Integer, nullable=False)  # Campo obligatorio
    director_peli = Column(String(75), nullable=False)  # Campo obligatorio, acepta 75 carácteres como mucho
    elenco_peli = Column(Text, nullable=False) # Campo obligatorio
    productora_peli = Column(String(75), nullable=False) # Campo obligatorio, acepta 75 carácteres como mucho
    sinopsis_peli = Column(Text, nullable=False) # Campo obligatorio, no tiene un límite de carácteres
    imagen = Column(Text, nullable=False)  # Campo obligatorio, no tiene un límite de carácteres

    def __init__(self,
                 genero_peli,
                 titulo_peli,
                 duracion_peli,
                 director_peli,
                 elenco_peli,
                 productora_peli,
                 sinopsis_peli,
                 imagen):
        """Constructor de la clase Pelicula"""
        self.genero_peli = genero_peli
        self.titulo_peli = titulo_peli
        self.duracion_peli = duracion_peli
        self.director_peli = director_peli
        self.elenco_peli = elenco_peli
        self.productora_peli = productora_peli
        self.sinopsis_peli = sinopsis_peli
        self.imagen = imagen
        print("La película se ha creado correctamente")

    def __repr__(self):
        """Método __repr__ de la clase Pelicula. Devuelve la información necesaria para replicar el objeto"""
        return """Película {}:
                    - Título: {}
                    - Género: {}
                    - Duración: {} minutos
                    - Director/a: {}
                    - Elenco: {}
                    - Productora: {}
                    - Sinopsis: {}
                    - Imagen: {}\n""". format(self.id_peli,
                                              self.titulo_peli,
                                              self.genero_peli,
                                              self.duracion_peli,
                                              self.director_peli,
                                              self.elenco_peli,
                                              self.productora_peli,
                                              self.sinopsis_peli,
                                              self.imagen)

    def __str__(self):
        """Método __str__ de la clase Pelicula. Indica al sistema la información del objeto"""
        return """Película {}:
                    - Título: {}
                    - Género: {}
                    - Duración: {} minutos
                    - Director/a: {}
                    - Elenco: {}
                    - Productora: {}
                    - Sinopsis: {}
                    - Imagen: {}\n""". format(self.id_peli,
                                              self.titulo_peli,
                                              self.genero_peli,
                                              self.duracion_peli,
                                              self.director_peli,
                                              self.elenco_peli,
                                              self.productora_peli,
                                              self.sinopsis_peli,
                                              self.imagen)

class Peliculas_vistas(db.Base):
    """Peliculas_vistas
    Mostrara que película ha visto cada usuario y la duración de la películas.

    args:
    - id_accion: Es un integer que identifica cada acción que se registra en la tabla. Es la primary key.
    - id_usuario: Es un integer que identifica a un usuario en base a su id (definido en la clase Usuarios).
    - id_peli:Es un integer que identifica una película en base a su id (definido en la clase Peliculas)."""

    __tablename__ = "peliculas_vistas"
    id_accion = Column(Integer, primary_key=True, autoincrement=True)  # Es la primary key
    id_usuario = Column(Integer, ForeignKey(Usuarios.id_usuario), nullable=False)  # Campo obligatorio
    id_peli = Column(Integer, ForeignKey(Peliculas.id_peli), nullable=False)  # Campo obligatorio

    def __init__(self,
                 id_accion,
                 id_usuario,
                 id_peli):
        """Constructor de la clase Peliculas_vistas"""
        self.id_accion = id_accion
        self.id_usuario = id_usuario
        self.id_peli = id_peli
        print("La relación se ha creado correctamente")

    def __repr__(self):
        """Método __repr__ de la clase Peliculas_vistas. Devuelve la información necesaria para replicar el objeto"""
        return """{}: Usuario {} ha visto la película {}\n""".format(self.id_accion,
                                                                           self.id_usuario,
                                                                           self.id_peli)


    def __str__(self):
        """Método __str__ de la clase Peliculas_vistas. Indica al sistema la información del objeto"""
        return """{}: Usuario {} ha visto la película {}\n""".format(self.id_accion,
                                                                           self.id_usuario,
                                                                           self.id_peli)

class Peliculas_favoritas(db.Base):
    """Peliculas_favoritas
    Mostrara que películas ha marcado cada usuario como favoritas.

    args:
    - id_accion: Es un integer que identifica cada accion que se registra en la tabla. Es la primary key.
    - id_usuario: Es un integer que identifica a un usuario en base a su id (definido en la clase Usuarios).
    - id_peli:Es un integer que identifica una película en base a su id (definido en la clase Peliculas)."""

    __tablename__ = "peliculas_favoritas"
    id_accion = Column(Integer, primary_key=True, autoincrement=True)  # Es la primary key
    id_usuario = Column(Integer, ForeignKey(Usuarios.id_usuario), nullable=False)  # Campo obligatorio
    id_peli = Column(Integer, ForeignKey(Peliculas.id_peli), nullable=False)  # Campo obligatorio

    def __init__(self,
                 id_accion,
                 id_usuario,
                 id_peli):
        """Constructor de la clase Peliculas_favoritas"""
        self.id_accion = id_accion
        self.id_usuario = id_usuario
        self.id_peli = id_peli
        print("La relación se ha creado correctamente")

    def __repr__(self):
        """Método __repr__ de la clase Peliculas_favoritas. Devuelve la información necesaria para replicar el objeto"""
        return """{}: Usuario {} ha marcado como favorita la película {}\n""".format(self.id_accion,
                                                                                      self.id_usuario,
                                                                                      self.id_peli)


    def __str__(self):
        """Método __str__ de la clase Peliculas_favoritas. Indica al sistema la información del objeto"""
        return """{}: Usuario {} ha marcado como favorita la película {}\n""".format(self.id_accion,
                                                                                     self.id_usuario,
                                                                                     self.id_peli)

class Series(db.Base):
    """Clase Series
    Incluye la información relevante de la serie.

    args:
    - id_serie: Es un integer que indica el número de indentificación que la serie tendrá en la base de datos.
    Es la primary key.
    - genero_serie: Es una cadena que indica el género de la serie.
    - titulo_serie: Es una cadena que indica el título de la serie.
    - temporadas: Es un intgere que indica el número de temporadas que tiene la serie.
    - capitulos: Es un integer que indica el total de capítulos que forman la serie.
    - duracion_cap: Es un integer que indica la duración media de los capítulos de la serie en minutos.
    - director_serie: Es una cadena que indica el nombre del director/a principal de la serie.
    - elenco_serie: Es una cadena que indica los actores y actrizes principales de la serie.
    - productora_serie: Es una cadena que indica la productura de la serie.
    - sinopsis_serie: Es una cadena que da una breve explicación de la serie.
    - imagen: Es una cadena con el nombre de la imagen."""

    __tablename__ = "series"
    id_serie = Column(Integer, primary_key=True)  # Es la primary key
    genero_serie = Column(String(50), nullable=False)  # Campo obligatorio, acepta 50 carácteres como mucho
    titulo_serie = Column(String(100), nullable=False)  # Campo obligatorio, acepta 100 carácteres como mucho
    temporadas = Column(Integer, nullable=False)  # Campo obligatorio
    capitulos = Column(Integer, nullable=False)  # Campo obligatorio
    duracion_cap = Column(Integer, nullable=False)  # Campo obligatorio
    director_serie = Column(String(75), nullable=False)  # Campo obligatorio, acepta 75 carácteres como mucho
    elenco_serie = Column(Text, nullable=False)  # Campo obligatorio
    productora_serie = Column(String(75), nullable=False)  # Campo obligatorio, acepta 75 carácteres como mucho
    sinopsis_serie = Column(Text, nullable=False)  # Campo obligatorio, no tiene un límite de carácteres
    imagen = Column(Text, nullable=False)  # Campo obligatorio, no tiene un límite de carácteres

    def __init__(self,
                 genero_serie,
                 titulo_serie,
                 temporadas,
                 capitulos,
                 duracion_cap,
                 director_serie,
                 elenco_serie,
                 productora_serie,
                 sinopsis_serie,
                 imagen):
        """Constructor de la clase Pelicula"""
        self.genero_serie = genero_serie
        self.titulo_serie = titulo_serie
        self.temporadas = temporadas
        self.capitulos = capitulos
        self.duracion_cap = duracion_cap
        self.director_serie = director_serie
        self.elenco_serie = elenco_serie
        self.productora_serie = productora_serie
        self.sinopsis_serie = sinopsis_serie
        self.imagen = imagen
        print("La serie se ha creado correctamente")

    def __repr__(self):
        """Método __repr__ de la clase Serie. Devuelve la información necesaria para replicar el objeto"""
        return """Serie {}:
                    - Título: {}
                    - Género: {}
                    - Temporadas: {}
                    - Capítulos: {}
                    - Duración capítulo: {} minutos aproximadamente 
                    - Director/a: {}
                    - Elenco: {}
                    - Productora: {}
                    - Sinopsis: {}
                    - Imagen: {}\n""".format(self.id_serie,
                                             self.titulo_serie,
                                             self.genero_serie,
                                             self.temporadas,
                                             self.capitulos,
                                             self.duracion_cap,
                                             self.director_serie,
                                             self.elenco_serie,
                                             self.productora_serie,
                                             self.sinopsis_serie,
                                             self.imagen)

    def __str__(self):
        """Método __str__ de la clase Serie. Indica al sistema la información del objeto"""
        return """Serie {}:
                            - Título: {}
                            - Género: {}
                            - Temporadas: {}
                            - Capítulos: {}
                            - Duración capítulo: {} minutos aproximadamente 
                            - Director/a: {}
                            - Elenco: {}
                            - Productora: {}
                            - Sinopsis: {}
                            - Imagen: {}\n""".format(self.id_serie,
                                                     self.titulo_serie,
                                                     self.genero_serie,
                                                     self.temporadas,
                                                     self.capitulos,
                                                     self.duracion_cap,
                                                     self.director_serie,
                                                     self.elenco_serie,
                                                     self.productora_serie,
                                                     self.sinopsis_serie,
                                                     self.imagen)

class Series_vistas(db.Base):
    """Series_vistas
    Mostrara que serie ha visto cada usuario.

    args:
    - id_accion: Es un integer que identifica cada accion que se registra en la tabla. Es la primary key.
    - id_usuario: Es un integer que identifica a un usuario en base a su id (definido en la clase Usuarios).
    - id_serie:Es un integer que identifica una serie en base a su id (definido en la clase Series)"""

    __tablename__ = "series_vistas"
    id_accion = Column(Integer, primary_key=True, autoincrement=True)  # Es la primary key
    id_usuario = Column(Integer, ForeignKey(Usuarios.id_usuario), nullable=False)  # Campo obligatorio
    id_serie = Column(Integer, ForeignKey(Series.id_serie), nullable=False)  # Campo obligatorio

    def __init__(self,
                 id_accion,
                 id_usuario,
                 id_serie):
        """Constructor de la clase Series_vistas"""
        self.id_accion = id_accion
        self.id_usuario = id_usuario
        self.id_serie = id_serie
        print("La relación se ha creado correctamente")

    def __repr__(self):
        """Método __repr__ de la clase Series_vistas. Devuelve la información necesaria para replicar el objeto"""
        return """{}: Usuario {} ha visto la serie {}\n""".format(self.id_accion,
                                                                        self.id_usuario,
                                                                        self.id_serie)


    def __str__(self):
        """Método __str__ de la clase Series_vistas. Indica al sistema la información del objeto"""
        return """{}: Usuario {} ha visto la serie {}\n""".format(self.id_accion,
                                                                  self.id_usuario,
                                                                  self.id_serie)

class Series_favoritas(db.Base):
    """Series_favoritas
    Mostrara que serie ha marcado como favoritas cada usuario.

    args:
    - id_accion: Es un integer que identifica cada accion que se registra en la tabla. Es la primary key.
    - id_usuario: Es un integer que identifica a un usuario en base a su id (definido en la clase Usuarios).
    - id_serie:Es un integer que identifica una serie en base a su id (definido en la clase Series)"""

    __tablename__ = "series_favoritas"
    id_accion = Column(Integer, primary_key=True, autoincrement=True)  # Es la primary key
    id_usuario = Column(Integer, ForeignKey(Usuarios.id_usuario), nullable=False)  # Campo obligatorio
    id_serie = Column(Integer, ForeignKey(Series.id_serie), nullable=False)  # Campo obligatorio

    def __init__(self,
                 id_accion,
                 id_usuario,
                 id_serie):
        """Constructor de la clase Series_vistas"""
        self.id_accion = id_accion
        self.id_usuario = id_usuario
        self.id_serie = id_serie
        print("La relación se ha creado correctamente")

    def __repr__(self):
        """Método __repr__ de la clase Series_vistas. Devuelve la información necesaria para replicar el objeto"""
        return """{}: Usuario {} ha marcado como favorita la serie {}\n""".format(self.id_accion,
                                                                                   self.id_usuario,
                                                                                   self.id_serie)


    def __str__(self):
        """Método __str__ de la clase Series_vistas. Indica al sistema la información del objeto"""
        return """{}: Usuario {} ha marcado como favorita la serie {}\n""".format(self.id_accion,
                                                                                  self.id_usuario,
                                                                                  self.id_serie)
