# -*- coding: utf-8 -*-
"""
runa.models
~~~~~~~~~~~

RUNA Models

"""
import logging
import json

logger = logging.getLogger('runa')


class PreparedContribuyente(object):
    def __init__(self):
        self.numeroRuc = None
        self.RUC = None
        self.razonSocial = None
        self.actividadEconomica = None
        self.codClaseContrib = None
        self.codEstado = None
        self.desClaseContrib = None
        self.desEstado = None
        self.direccionCorta = None
        self.email = None
        self.nombreComercial = None
        self.telefonoDomicilio = None
        self.telefonoTrabajo = None
        self.tipoContribuyente = None
        self.ubicacionGeografica = None
        self.obligadoContabilidad = False
        self.representanteLegal = {}
        self.ValidRUC = False

    def __getitem__(self, key):
        return self.__dict__[key]

    def __repr__(self):
        return '<Contribuyente [%s - %s]>' % (self.RUC, self.razonSocial)

    def json(self):
        return json.dumps(self.__dict__, indent=4)

    def is_valid(self):
        """ Validate RUC """
        try:
            import stdnum
        except ImportError:
            logger.warning("Warning: stdnum library not installed, can't validate.")  # noqa
            return False
        self.ValidRUC = stdnum.ec.ruc.is_valid(self.RUC)
        return self.RUC

    def clean_dict(self, cls):
        toclean = cls.__dict__
        toclean.pop('__metadata__')
        toclean.pop('__printer__')
        toclean.pop('__keylist__')
        return toclean

    def prepare(self, response):
        self.actividadEconomica = self.clean_dict(response.actividadEconomica)
        self.codClaseContrib = response.codClaseContrib
        self.codEstado = response.codEstado
        self.desClaseContrib = response.desClaseContrib
        self.desEstado = response.desEstado
        self.direccionCorta = response.direccionCorta
        self.email = response.email
        self.nombreComercial = response.nombreComercial
        self.numeroRuc = response.numeroRuc
        self.RUC = response.numeroRuc
        self.razonSocial = response.razonSocial
        self.telefonoDomicilio = response.telefonoDomicilio
        self.tipoContribuyente = self.clean_dict(response.tipoContribuyente)
        self.obligadoContabilidad = response.obligadoContabilidad
        self.representanteLegal = self.clean_dict(response.representanteLegal)
        self.ValidRUC = True


class PreparedRuna(object):

    def __init__(self):
        self.Calle = None
        # self.CodigoTipoCedulado = None
        self.CondicionCedulado = None
        self.Conyuge = None
        self.Domicilio = None
        self.EstadoCivil = None
        self.FechaCedulacion = None
        self.FechaMatrimonio = None
        self.FechaNacimiento = None
        self.IndividualDactilar = None
        self.Instruccion = None
        self.LugarMatrimonio = None
        self.LugarNacimiento = None
        self.NUI = None
        self.Nacionalidad = None
        self.Nombre = None
        self.NombreMadre = None
        self.NombrePadre = None
        self.NumeroCasa = None
        self.Profesion = None
        self.Sexo = None
        self.Genero = None
        self.FechaInscripcionGenero = None
        self.ValidNUI = True

    def __getitem__(self, key):
        return self.__dict__[key]

    def __repr__(self):
        return '<Runa [%s - %s]>' % (self.NUI, self.Nombre)

    def json(self):
        return json.dumps(self.__dict__, indent=4)

    def is_valid(self):
        """ Validate NUI """
        try:
            import stdnum
        except ImportError:
            logger.warning("Warning: stdnum library not installed, can't validate.")  # noqa
            return False
        self.ValidNUI = stdnum.ec.ci.is_valid(self.NUI)
        return self.ValidNUI

    def prepare(self, response):
        """ Prepare given response data in object"""
        self.Calle = response.Calle
        # self.CodigoTipoCedulado = response.CodigoTipoCedulado
        self.CondicionCedulado = response.CondicionCedulado
        self.Conyuge = response.Conyuge
        self.Domicilio = response.Domicilio
        self.EstadoCivil = response.EstadoCivil
        self.FechaCedulacion = response.FechaCedulacion
        self.FechaNacimiento = response.FechaNacimiento
        self.Instruccion = response.Instruccion
        self.LugarNacimiento = response.LugarNacimiento
        self.NUI = response.NUI
        self.Nacionalidad = response.Nacionalidad
        self.Nombre = response.Nombre
        self.NombreMadre = response.NombreMadre
        self.NombrePadre = response.NombrePadre
        self.NumeroCasa = response.NumeroCasa
        self.Profesion = response.Profesion
        self.Sexo = response.Sexo
        self.Genero = response.Genero
        self.FechaInscripcionGenero = response.FechaInscripcionGenero
        self.ValidNUI = True


class ActividadEconomica(object):
    def __init__(self):
        self.actividadGeneral = False
        self.codN1Familia = False
        self.codN2Grupo = False
        self.codN3SubGrupo = False
        self.codN4Clase = False
        self.codN5SubClase = False
        self.codN6Actividad = False
        self.n1Familia = False
        self.n2Grupo = False
        self.n3SubGrupo = False
        self.n4Clase = False
        self.n5SubClase = False
        self.n6Actividad = False
