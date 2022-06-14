#-----------------IMPORTACION DE TODAS LAS LIBRERIAS QUE SE UTILIZAN EN LA APLIACION-----------------

from tkinter import *                                       #importar todo de la libreria tkinter   
import tkinter as tk                                        #importar tkinter como tk
from tkinter import ttk, messagebox                         #de la libreria tkinter importar tk y messagebox
import Estilos                                              #importar el archivo estilos
from tkcalendar import DateEntry                            #de la libreria tkcalendar importar DateEntry
import os, io                                               #import os e io 
from time import sleep, time                                #de la libreia time importar sleep y time
from tkinter.messagebox import showerror                    #de la libreria tkinter import messagebox
import cv2 as cv                                            #importar la libreria cv2
import threading                                            #importar la libreria threading
from pygame import mixer                                    #de pygame importar mixer para reproducir sonido
import datetime                                             #importar la libreria datetime
from datetime import datetime                               #de la libreria datetime importar datetime
import schedule                                             #importar la libreria schedule
import time                                                 #importar la libreria time

#---------------------------------------------------VARIABLES---------------------------------------------------

global cursos_estudiante                                    #se hace global la variable cursos_estudiante
global carrera_estudiante                                   #se hace global la variable carrera_estudiante
global actividades                                          #se hace global la variable actividades

cursos = []                                                 #se crea una lista vacia para guardar los cursos
carreras = []                                               #se crea una lista vacia para guardar las carreras
cursos_estudiante = []                                      #se crea una lista vacia para guardar los cursos del estudiante
lista_actividades = []                                      #se crea una lista vacia para guardar las actividades
lista_usuarios_estudiantes = []                             #se crea una lista que guarda los usuarios tipo estudiante
lista_usuarios_admin = []                                   #se crea una lista vacia para guardar los usuarios tipo administrador
lista = []                                                  #se crea una lista vacia para averiguar el numero mayor de los que se vayan a almacenar dentro de ella
lst_emociones = []                                          #se crea una lista que almacena todas las emociones predominantes
lst_dia = []                                                #se crea una lista que almacena las emociones que hubieron durante la mañana
lst_tarde = []                                              #se crea una lista que almacena las emociones que hubieron durante la tarde
lst_noche = []                                              #se crea una lista que almacena las emociones que hubieron durante la noche
dia = ''                                                    #se crea una variable que almacena la emocion predominante la mañana
tarde = ''                                                  #se crea una variable que almacena la emocion predominante la tarde
noche = ''                                                  #se crea una variable que almacena la emocion predominante la noche
estado3 = [True]                                            #se crea una variable que mantiene el proceso de la toma de fotos activo
estado_prueba = True                                        #se crea una variable que mantiene la varianle estado3 activa
sonido = True                                               #se crea una variable que hace que el sonido de la alarma esté activo
carrera_estudiante = None                                   #se crea una variable que almacena la carrera que el estudiante matricula
cont2 = 0                                                   #se crea una variable que se usa como condicion de parada del proceso que identifica la cantidad de expresiones por tipo de cada actividad
cont3 = 0                                                   #se crea una varible que se usa para notificar que no se detecta ninguna cara
suma = 0                                                    #se crea una variable que sumara todas la cantidad de expresiones por tipo de cada actividad 
cont4 = 0                                                   #se crea una variable para saber las emociones de los primeros 5 minutos
emocion_final = ''                                          #se crea una variable que almacena la emocion predominante de la persona por actividad
emocion = ''                                                #se crea una variable para saber cual emocion se tiene seleccionada
nombre_act = ''                                             #se crea una variable para identificar la actividad de cual se esta tomadando la foto
coma = ', '                                                 #se crea una variable que nos añade una coma a lo que deseemos
fecha = datetime.now()                                      #se crea una variable que obtiene la fecha de hoy
dia = fecha.day                                             #se crea una variable que obtiene el dia de la fecha de hoy
mes = fecha.month                                           #se crea una variable que obtiene el mes de la fecha de hoy
ano = fecha.year                                            #se crea una variable que obtiene el año de la fecha de hoy
fecha1 = str(dia) + '/' + str(mes) + '/' + str(ano)         #se crea una variable que acomoda la fecha de hoy según los datos obtenidos anteriormente
hora1 = time.strftime('%H:%M', time.localtime())            #se crea una variable que obtiene la hora de hoy

dias = ['Lunes','Martes','Miércoles','Jueves','Viernes','Sábado','Domingo']             #se crea una lista que contiene los dias de la semana 

horas_dias = {                                                                          #se crea un diccionario que contiene las horas de cada dia de las actividades
        'Lunes' : [], 
        'Martes' : [], 
        'Miércoles' : [], 
        'Jueves' : [], 
        'Viernes' : [], 
        'Sábado' : [], 
        'Domingo' : []
            }

registro_expresiones = {                                                                #se crea un diccionario que contiene las expresiones de cada dia de las actividades
            'joy_likelihood' : [], 
            'sorrow_likelihood' : [], 
            'anger_likelihood' : [], 
            'surprise_likelihood' : [], 
            'under_exposed_likelihood' : [], 
            'blurred_likelihood' : [], 
            'headwear_likelihood' : []
                        }

registro_expresiones2 = {                                                               #se crea un diccionario que contiene las expresiones de cada dia de las actividades que guarda las de los primeros 5 minutos
            'joy_likelihood' : [], 
            'sorrow_likelihood' : [], 
            'anger_likelihood' : [], 
            'surprise_likelihood' : [], 
            'under_exposed_likelihood' : [], 
            'blurred_likelihood' : [], 
            'headwear_likelihood' : []
                        }

emociones = [                                                                           #se crea una lista que contiene las emociones
            'joy_likelihood', 
            'sorrow_likelihood', 
            'anger_likelihood', 
            'surprise_likelihood', 
            'under_exposed_likelihood', 
            'blurred_likelihood', 
            'headwear_likelihood'
            ]

#---------------------------------------------------CLASES---------------------------------------------------

class rostro ():                                                                        #se crea la clase rostro la cual hara las capturas de la imagen de la cara
    def __init__(self) -> None:
        pass

    def capturar_imagen(self,vista):                                                    #se crea un metodo que captura la imagen de la cara
        camara = cv.VideoCapture(0)
        leido, imagen = camara.read()
        camara.release()

        if leido == True:                                                                   
            cv.imwrite("foto.png", imagen)
            if vista:
                cv.imshow('Toma de fotografia',imagen)
                cv.waitKey(0)
        else:
            showerror(
                title='Error en la toma de imagen', 
                message='¡No fue posible capturar la imagen con esta dispositivo!')
        return imagen

class curso_class:                                                                      #se crea la clase curso_class la cual guarda los cursos que se matriculan
    def __init__(self, nombre, creditos, horas, fecha1, fecha2, dia, hora1, hora2):
        self.nombre = nombre
        self.creditos = creditos
        self.horas = horas
        self.fecha1 = fecha1
        self.fecha2 = fecha2
        self.dia = dia
        self.hora1 = hora1
        self.hora2 = hora2

    def __str__(self):
        return self.nombre
    
class carrera_class:                                                                    #se crea la clase carrera_class la cual guarda las carreras que se matriculan
    def __init__(self, nombre):
        self.nombre = nombre
        self.cursos_carrera = []

    def agregar_curso(self, curso):                                                     #se crea un metodo que agrega los cursos a la carrera
        if curso in self.cursos_carrera:
            messagebox.showinfo(message= '¡Este curso ya se encuentra vinculado a la carrera!', title = 'Alerta')
        else:
            self.cursos_carrera.append(curso)

    def quitar_curso(self, curso):                                                      #se crea un metodo que quita los cursos de la carrera
        if curso not in self.cursos_carrera:
            messagebox.showinfo(message= '¡Este curso no está vinculado a esta carrera!', title = 'Alerta')
        elif len(self.cursos_carrera) == 1:
            messagebox.showinfo(message= '¡Debe tener mínimo un curso agregado!', title = 'Alerta')
        else:
            self.cursos_carrera.remove(curso)

    def __str__(self):
        return self.nombre

class UsuariosAdmin:                                                                    #se crea la clase UsuariosAdmin la cual guarda los usuarios administradores
    def __init__(self, nombre, apellido1, apellido2, numero, usuario, contraseña):
        self.nombre = nombre
        self.apellido1 = apellido1
        self.apellido2 = apellido2
        self.numero = numero
        self.usuario = usuario
        self.contraseña = contraseña

class UsuariosEstudiante:                                                               #se crea la clase UsuariosEstudiante la cual guarda los usuarios estudiantes
    def __init__(self, nombre, apellido1, apellido2, numero, usuario, contraseña):
        self.nombre = nombre
        self.apellido1 = apellido1
        self.apellido2 = apellido2
        self.numero = numero
        self.usuario = usuario
        self.contraseña = contraseña

class estudiante_class:                                                                 #se crea la clase estudiante_class la cual guarda los datos de los estudiantes
    carrera_estudiante = None
    cursos_estudiante = None
    actividades = None

    def __init__(self, usuario, carrera_estudiante, cursos_estudiante, actividades):
        self.usuario = usuario
        self.carrera_estudiante = carrera_estudiante
        self.cursos_estudiante = cursos_estudiante
        self.actividades = actividades

class actividades_class:                                                                #se crea la clase actividades_class la cual guarda las actividades de los estudiantes
    nombre = None
    descripcion = None
    curso_asociado = None
    fecha1 = None
    fecha2 = None
    dia = None
    horas_actividad = None
    hora_inicio = None
    hora_final = None
    estado = 'Pendiente'
    emocion_general = 'Actividad sin realizar'
    emocion_5_min = 'Actividad sin realizar'

    def __init__(self, nombre, descripcion, curso_asociado, fecha1, fecha2, dia, horas_actividad, hora_inicio, hora_final, estado):
        self.nombre = nombre
        self.descripcion = descripcion
        self.curso_asociado = curso_asociado
        self.fecha1 = fecha1
        self.fecha2 = fecha2
        self.dia = dia
        self.horas_actividad = horas_actividad
        self.hora_inicio = hora_inicio
        self.hora_final = hora_final
        self.estado = estado

#---------------------------------------------------DEFINICIONES PARA EL RECONOCIMIENTO DE EMOCIONES Y CONTROL DE DISTRACCION---------------------------------------------------

def reconocimiento_facial():                                                            #se crea la funcion reconocimiento_facial la cual realiza el reconocimiento facial
    global emocion, suma, cont2, lista, maximo, cont3, cont4, nombre_act, registro_expresiones, registro_expresiones2, lst_emociones, emocion_final, coma
    fecha = datetime.now()
    dia = fecha.day
    mes = fecha.month
    ano = fecha.year
    fecha1 = str(dia) + '/' + str(mes) + '/' + str(ano)
    hora1 = time.strftime('%H:%M', time.localtime())

    for actividad in lista_actividades:
        if actividad.fecha1 == fecha1:
            if actividad.hora_inicio <= hora1:
                if actividad.hora_final > hora1:
                    nombre_act = actividad.nombre
                    mi_rostro = rostro()
                    imagen = mi_rostro.capturar_imagen(vista=False)

                    from google.cloud import vision
                    os.environ['GOOGLE_APPLICATION_CREDENTIALS']= r'key.json'
                    client = vision.ImageAnnotatorClient()
    
                    with io.open('foto.png','rb') as image_file:
                        content = image_file.read()
    
                    image = vision.Image(content=content)
    
                    response = client.face_detection(image=image)
    
                    faces = response.face_annotations
    
                    likelihood_name = ('UNKNOWN', 'VERY_UNLIKELY', 'UNLIKELY', 'POSSIBLE', 'LIKELY', 'VERY_LIKELY')
    
                    faces_list=[]
    
                    for face in faces:
                        face_angles=dict(roll_angle=face.roll_angle,pan_angle=face.pan_angle,tilt_angle=face.tilt_angle)
                        detection_confidence=face.detection_confidence
                        face_expressions=dict(  joy_likelihood=likelihood_name[face.joy_likelihood],
                                                        sorrow_likelihood=likelihood_name[face.sorrow_likelihood],
                                                        anger_likelihood=likelihood_name[face.anger_likelihood],
                                                        surprise_likelihood=likelihood_name[face.surprise_likelihood],
                                                        under_exposed_likelihood=likelihood_name[face.under_exposed_likelihood],
                                                        blurred_likelihood=likelihood_name[face.blurred_likelihood],
                                                        headwear_likelihood=likelihood_name[face.headwear_likelihood])
    
                        vertices=[]
                        for vertex in face.bounding_poly.vertices:
                            vertices.append (dict (x=vertex.x, y=vertex.y))
    
                        face_dict=dict( face_angles=face_angles,
                                        detection_confidence=detection_confidence,
                                        face_expressions=face_expressions,
                                        vertices=vertices
                                        )
                        faces_list.append(face_dict)
                    try:
                        x1=faces_list[0]['vertices'][0]['x']
                        y1=faces_list[0]['vertices'][0]['y']
                        x2=faces_list[0]['vertices'][2]['x']
                        y2=faces_list[0]['vertices'][2]['y']
                    except:
                        print('El indice se encuentra fuera de rango')
    
                    cv.rectangle(imagen,(x1,y1),(x2,y2),(0,255,0),3)
    
                    cv.waitKey(0)
    
                    cont3 = 0    

                    if face_expressions['joy_likelihood']=='VERY_LIKELY' or face_expressions['joy_likelihood']=='LIKELY' or face_expressions['joy_likelihood']=='POSSIBLE':         #aqui se comparan el reconocimiento facial para saber cuales son las emociones que se detectan
                        registro_expresiones['joy_likelihood'].append(1)
                        cont3 = cont3 + 1
                        print('Felicidades, se identificó una cara feliz')
                        if cont4 < 5:
                            registro_expresiones2['joy_likelihood'].append(1)
                            cont4 = cont4 + 1
                    if face_expressions['sorrow_likelihood']=='VERY_LIKELY' or face_expressions['sorrow_likelihood']=='LIKELY' or face_expressions['sorrow_likelihood']=='POSSIBLE':
                        registro_expresiones['sorrow_likelihood'].append(1)
                        cont3 = cont3 + 1
                        print('Felicidades, se identificó una cara triste')
                        if cont4 < 5:
                            registro_expresiones2['sorrow_likelihood'].append(1)
                            cont4 = cont4 + 1
                    if face_expressions['anger_likelihood']=='VERY_LIKELY' or face_expressions['anger_likelihood']=='LIKELY' or face_expressions['anger_likelihood']=='POSSIBLE':
                        registro_expresiones['anger_likelihood'].append(1)
                        cont3 = cont3 + 1
                        print('Felicidades, se identificó una cara enfadada')
                        if cont4 < 5:
                            registro_expresiones2['anger_likelihood'].append(1)
                            cont4 = cont4 + 1
                    if face_expressions['surprise_likelihood']=='VERY_LIKELY' or face_expressions['surprise_likelihood']=='LIKELY' or face_expressions['surprise_likelihood']=='POSSIBLE':
                        registro_expresiones['surprise_likelihood'].append(1)
                        cont3 = cont3 + 1
                        print('Felicidades, se identificó una cara sorpresa')
                        if cont4 < 5:
                            registro_expresiones2['surprise_likelihood'].append(1)
                            cont4 = cont4 + 1
                    if face_expressions['under_exposed_likelihood']=='VERY_LIKELY' or face_expressions['under_exposed_likelihood']=='LIKELY' or face_expressions['under_exposed_likelihood']=='POSSIBLE':
                        registro_expresiones['under_exposed_likelihood'].append(1)
                        cont3 = cont3 + 1
                        print('Felicidades, se identificó una cara sin sombrero')
                        if cont4 < 5:
                            registro_expresiones2['under_exposed_likelihood'].append(1)
                            cont4 = cont4 + 1
                    if face_expressions['blurred_likelihood']=='VERY_LIKELY' or face_expressions['blurred_likelihood']=='LIKELY' or face_expressions['blurred_likelihood']=='POSSIBLE':
                        registro_expresiones['blurred_likelihood'].append(1)
                        cont3 = cont3 + 1
                        print('Felicidades, se identificó una cara desenfocada')
                        if cont4 < 5:
                            registro_expresiones2['blurred_likelihood'].append(1)
                            cont4 = cont4 + 1
                    if face_expressions['headwear_likelihood']=='VERY_LIKELY' or face_expressions['headwear_likelihood']=='LIKELY' or face_expressions['headwear_likelihood']=='POSSIBLE':
                        registro_expresiones['headwear_likelihood'].append(1)
                        cont3 = cont3 + 1
                        print('Felicidades, se identificó una cara un sombrero')
                        if cont4 < 5:
                            registro_expresiones2['headwear_likelihood'].append(1)
                            cont4 = cont4 + 1
                    if cont3 == 0:
                        if cont4 < 5:
                            cont4 = cont4 + 1
                        messagebox.showwarning(title= 'Alerta de no detección de una cara',message='Lo sentimos, no se pudo identificar la cara')

                elif nombre_act == actividad.nombre:                                        #aqui comparan las emociones detectadas anteriormente para identificar la más predominante
                    while cont2 < len(registro_expresiones):
                        emocion = emociones[cont2]
                        cont2 = cont2 + 1
                        for x in registro_expresiones.get(emocion):
                            suma = suma + 1
                        registro_expresiones[emocion].clear()
                        registro_expresiones[emocion].append(suma)
                        lista.append(suma)
                        suma = 0
                    maximo = (max(lista))
                    cont2 = 0
                    while cont2 < len(registro_expresiones):                                #aqui se identifica la emoción más predominante y se asigna a la actividad
                        emocion = emociones[cont2]
                        cont2 = cont2 + 1
                        for x in registro_expresiones.get(emocion):
                            if x == maximo:
                                if emocion == 'joy_likelihood':
                                    lst_emociones.append('Felicidad')
                                    print('El estado más constante durante el dia es feliz')
                                elif emocion == 'sorrow_likelihood':
                                    lst_emociones.append('Tristeza')
                                    print('El estado más constante durante el dia es triste')
                                elif emocion == 'anger_likelihood':
                                    lst_emociones.append('Enfado')
                                    print('El estado más constante durante el dia es enfadado')
                                elif emocion == 'surprise_likelihood':
                                    lst_emociones.append('Sorpinpresa')
                                    print('El estado más constante durante el dia es sorpresa')
                                elif emocion == 'under_exposed_likelihood':
                                    lst_emociones.append('Sin uso de sombrero')
                                    print('El estado más constante durante el dia es desnudo')
                                elif emocion == 'blurred_likelihood':
                                    lst_emociones.append('Desenfocado')
                                    print('El estado más constante durante el dia es desenfocado')
                                elif emocion == 'headwear_likelihood':
                                    lst_emociones.append('Con uso de sombrero')
                                    print('El estado más constante durante el dia es el uso de ropa para cabeza')

                    emocion_final = coma.join(lst_emociones)
                    actividad.emocion_general = emocion_final

                    suma = 0                
                    cont = 0
                    cont2 = 0
                    lista = []
                    cont3 = 0
                    nombre_act = ''
                    cont4 = 0
                    lst_emociones = []
                    emocion_final = ''
                    registro_expresiones = {
                                'joy_likelihood' : [], 
                                'sorrow_likelihood' : [], 
                                'anger_likelihood' : [], 
                                'surprise_likelihood' : [], 
                                'under_exposed_likelihood' : [], 
                                'blurred_likelihood' : [], 
                                'headwear_likelihood' : []
                                            }

                    while cont2 < len(registro_expresiones2):                               #aqui comparan las emociones detectadas anteriormente para identificar la más predominante durante los primeros 5 minutos
                        emocion = emociones[cont2]
                        cont2 = cont2 + 1
                        for x in registro_expresiones2.get(emocion):
                            suma = suma + 1
                        registro_expresiones2[emocion].clear()
                        registro_expresiones2[emocion].append(suma)
                        lista.append(suma)
                        suma = 0
                    maximo = (max(lista))
                    cont2 = 0
                    while cont2 < len(registro_expresiones2):                               #aqui se identifica la emoción más predominante durante los primeros 5 minutos y se asigna a la actividad
                        emocion = emociones[cont2]
                        cont2 = cont2 + 1
                        for x in registro_expresiones2.get(emocion):
                            if x != 0:
                                if x == maximo:
                                    if emocion == 'joy_likelihood':
                                        lst_emociones.append('Felicidad')
                                        print('El estado más constante durante los primeros 5 minutos es feliz')
                                    elif emocion == 'sorrow_likelihood':
                                        lst_emociones.append('Tristeza')
                                        print('El estado más constante durante los primeros 5 minutos es triste')
                                    elif emocion == 'anger_likelihood':
                                        lst_emociones.append('Enfado')
                                        print('El estado más constante durante los primeros 5 minutos es enfadado')
                                    elif emocion == 'surprise_likelihood':
                                        lst_emociones.append('Sorpinpresa')
                                        print('El estado más constante durante los primeros 5 minutos es sorpresa')
                                    elif emocion == 'under_exposed_likelihood':
                                        lst_emociones.append('Sin uso de sombrero')
                                        print('El estado más constante durante los primeros 5 minutos es desnudo')
                                    elif emocion == 'blurred_likelihood':
                                        lst_emociones.append('Desenfocado')
                                        print('El estado más constante durante los primeros 5 minutos es desenfocado')
                                    elif emocion == 'headwear_likelihood':
                                        lst_emociones.append('Con uso de sombrero')
                                        print('El estado más constante durante los primeros 5 minutos es el uso de ropa para cabeza')
                    
                    emocion_final = coma.join(lst_emociones)
                    actividad.emocion_5_min = emocion_final

                    suma = 0                
                    cont = 0
                    cont2 = 0
                    lista = []
                    cont3 = 0
                    cont4 = 0
                    nombre_act = ''
                    lst_emociones = []
                    emocion_final = ''
                    registro_expresiones2 = {
                                'joy_likelihood' : [], 
                                'sorrow_likelihood' : [], 
                                'anger_likelihood' : [], 
                                'surprise_likelihood' : [], 
                                'under_exposed_likelihood' : [], 
                                'blurred_likelihood' : [], 
                                'headwear_likelihood' : []
                                            }

def control_concentracion():                                                            #se crea la funcion control_concentracion la cual realiza el control de la concentracion de la persona
    fecha = datetime.now()
    dia = fecha.day
    mes = fecha.month
    ano = fecha.year
    fecha1 = str(dia) + '/' + str(mes) + '/' + str(ano)
    hora1 = time.strftime('%H:%M', time.localtime())

    for actividad in lista_actividades:
        if actividad.fecha1 == fecha1:
            if actividad.hora_inicio <= hora1:
                if actividad.hora_final > hora1:
                    mi_rostro2=rostro()
                    cv.waitKey(0)
                    imagen=mi_rostro2.capturar_imagen(vista=False)

                    from google.cloud import vision
                    os.environ['GOOGLE_APPLICATION_CREDENTIALS']= r'key.json'
                    client=vision.ImageAnnotatorClient()

                    with io.open('foto.png','rb') as image_file: 
                        content = image_file.read()

                    image = vision.Image(content=content)

                    response = client.face_detection(image=image)

                    faces = response.face_annotations

                    faces_list=[]

                    for face in faces:
                        face_angles=dict(roll_angle=face.roll_angle,pan_angle=face.pan_angle,tilt_angle=face.tilt_angle)
                        detection_confidence=face.detection_confidence

                        vertices=[]
                        for vertex in face.bounding_poly.vertices:
                            vertices.append (dict (x=vertex.x, y=vertex.y))
                            
                        face_dict=dict( face_angles=face_angles,
                                        detection_confidence=detection_confidence,
                                        vertices=vertices
                                        )
                        faces_list.append(face_dict)
                    try:    
                        x1=faces_list[0]['vertices'][0]['x']
                        y1=faces_list[0]['vertices'][0]['y']
                        x2=faces_list[0]['vertices'][2]['x']
                        y2=faces_list[0]['vertices'][2]['y']
                    except:
                        print('El indice se encuentra fuera de rango')

                    cv.rectangle(imagen,(x1,y1),(x2,y2),(0,255,0),3)

                    if face_angles['pan_angle']<-35:                                                     #aqui se comparan los angulos de la foto para identificar si existe algun tipo de distracción
                        print('La cara esta mirando a la derecha')
                        emitir_sonido()
                        messagebox.showwarning(title= 'Alerta',message='Pérdida de concentración')
                    elif face_angles['pan_angle']>35:
                        print('La cara esta mirando a la izquierda')
                        emitir_sonido()
                        messagebox.showwarning(title= 'Alerta',message='Pérdida de concentración')
                    elif face_angles['tilt_angle']<-16: 
                        print('La cara esta mirando hacia abajo')
                        emitir_sonido()
                        messagebox.showwarning(title= 'Alerta',message='Pérdida de concentración')
                    elif face_angles['tilt_angle']>16:
                        print('La cara esta mirando hacia arriba')
                        emitir_sonido()
                        messagebox.showwarning(title= 'Alerta',message='Pérdida de concentración')
                    else:
                        print('La cara está mirando hacia la cámara')

def emitir_sonido():                                                                    #se crea la funcion emitir_sonido la cual reproduce un sonido para alertar al usuario en caso de desconcentración
    if sonido == True:
        mixer.init()
        mixer.music.load('bruh.mp3')
        mixer.music.play()
        sleep(1)
        mixer.music.stop()

def proceso_fotos(estado2):                                                             #se crea la funcion proceso_fotos la cual mantiene activo el proceso para la toma de fotos cada minutos y cada 30 segundos
    while estado_prueba == True:    
        if estado3[0] == True:
            schedule.run_pending()
            sleep(1) 
        else:
            pass

estado2 = [True]
parametros2 = [estado2]
proceso_fotos_ = threading.Thread(target=proceso_fotos, args=parametros2)
proceso_fotos_.start()                                                                  #se crea el hilo para el proceso de fotos

def test():                                                                             #se crea la funcion test la cual se utiliza para saber si la persona desea realizar capturas de fotos
    global estado_prueba
    if (variable_foto.get() == 1):                      
        schedule.every(1).minutes.do(reconocimiento_facial)
        schedule.every(30).seconds.do(control_concentracion)
        estado3[0] = True
    else:
        try:
            estado3[0] = False
        except:
            pass

#---------------------------------------------------DEFINICIONES PARA LA INTERFAZ GRAFICA Y SUS FUNCIONES---------------------------------------------------

def usuarios_admin():                                                                   #se crea la funcion usuarios_admin la cual se utiliza para iniciar sesion como administrador
    global  sv_usuario_admin, sv_contraseña_admin
    if sv_usuarios.get() == 'Administrador':
        ventana_usuarios_admin = Toplevel(ventana_inicial)
        ventana_usuarios_admin.minsize(500,250)
        ventana_usuarios_admin.title('Sistema de Administración del Tiempo')
        ventana_usuarios_admin.resizable(False,False)
        ventana_usuarios_admin.configure(background=Estilos.BACKGROUND1)

        lb_principal = tk.Label(ventana_usuarios_admin, text = '''-----------------------------------------------------------------
        Inicio de Sesión Administrativo
        -----------------------------------------------------------------''', **Estilos.STYLE).pack(side=TOP)

        lb_usuario = tk.Label(ventana_usuarios_admin, text = "Nombre de usuario:", **Estilos.LABELS).place(x = 20,y = 100)  
            
        lb_contraseña = tk.Label(ventana_usuarios_admin, text = "Contraseña:", **Estilos.LABELS).place(x = 20, y = 135)  
        sv_usuario_admin = tk.StringVar()        
        ent_usuario = tk.Entry(ventana_usuarios_admin, width = 30, textvariable=sv_usuario_admin).place(x = 200,y = 105)  
        sv_contraseña_admin = tk.StringVar()        
        ent_contraseña = tk.Entry(ventana_usuarios_admin, show='*', width = 30, textvariable=sv_contraseña_admin).place(x = 200, y = 140)  
            
        boton_ingresar = tk.Button(ventana_usuarios_admin, 
                                    text = "Ingresar",
                                    command=lambda:[administrador(),esconder(ventana_usuarios_admin)], 
                                    **Estilos.BOTONES
                                    ).place(x = 425, y = 210)
    elif sv_usuarios.get() == 'Estudiante':
        usuarios_estudiantes()
    elif sv_usuarios.get() == '':
        mostrar(ventana_inicial)
        messagebox.showinfo(message='¡Debe seleccionar su tipo de usuario!', title='Alerta')    

def administrador():                                                                    #se crea la funcion administrador la cual accede a todas las funciones del usuario administrador
    try:
        global sv_opciones
        for x in lista_usuarios_admin:
            if x.usuario == sv_usuario_admin.get():
                if x.contraseña == sv_contraseña_admin.get():
                    ventana_admin = Toplevel(ventana_inicial)
                    ventana_admin.title('Sistema de Administración del Tiempo')
                    ventana_admin.minsize(740,300)
                    ventana_admin.resizable(False, False)
                    ventana_admin.configure(background=Estilos.BACKGROUND1)

                    titulo = tk.Label(ventana_admin, text = '''-----------------------------------------------------------------
                    Sistema Administrativo
                    -----------------------------------------------------------------''', **Estilos.STYLE
                    ).pack(side=TOP)

                    instruccion1 = tk.Label(ventana_admin, text = "Seleccione la opción que desea realizar:" , **Estilos.LABELS).place(x = 20, y = 135)  

                    sv_opciones = tk.StringVar()
                    combo_opciones = ttk.Combobox(ventana_admin, textvariable=sv_opciones)
                    combo_opciones['values'] = ["Agregar/Modificar un curso","Agregar/Modificar una carrera", "Agregar un nuevo usuario"]
                    combo_opciones['state'] = 'readonly'
                    combo_opciones.place(x = 370, y = 140, width= 260, height=23)

                    boton_regresar = tk.Button(ventana_admin, text = "Regresar a la pantalla inicial", command=lambda:[mostrar(ventana_inicial), esconder(ventana_admin)], **Estilos.BOTONES).place(x =20, y = 260)
                    boton_ingresar = tk.Button(ventana_admin, text = "Seleccionar", command=lambda:[admin_cursos(), esconder(ventana_admin)],**Estilos.BOTONES).place(x =640, y = 138)
                    break
                else:
                    messagebox.showinfo(message='¡¡¡SU USUARIO O CONTRASEÑA SON INCORRECTOS!!!', title='Alerta')
                    mostrar(ventana_admin)
            elif sv_usuario_admin.get() == '':
                messagebox.showinfo(message='¡¡¡SU USUARIO O CONTRASEÑA SON INCORRECTOS!!!', title='Alerta')
                mostrar(ventana_admin)
        if sv_usuario_admin.get() != x.usuario:
            messagebox.showinfo(message='¡¡¡SU USUARIO O CONTRASEÑA SON INCORRECTOS!!!', title='Alerta')
            mostrar(ventana_admin)
    except:
        pass

def admin_cursos():                                                                     #se crea la funcion admin_cursos la cual permite añadir nuevos cursos
    def boton_limpiar_cursos():                                                         #se crea la funcion boton_limpiar_cursos la cual permite limpiar los campos de texto
        sv_nombre.set('')
        sv_creditos.set('')
        sv_horas.set('')
        sv_fecha1.set('')
        sv_fecha2.set('')
        tkvarqdias.set('')
        sv_hora1.set('')
        sv_hora2.set('')
        tkvarq.set('')

    def boton_agregar_curso():                                                          #se crea la funcion boton_agregar_curso la cual permite agregar un nuevo curso
        nombre = sv_nombre.get()
        creditos = sv_creditos.get()
        horas = sv_horas.get()
        fecha1 = sv_fecha1.get()
        fecha2 = sv_fecha2.get()
        dia = tkvarqdias.get()
        hora1 = sv_hora1.get()
        hora2 = sv_hora2.get()

        if nombre == '':                                                                #se crea la condicion para que no se pueda agregar un curso sin espacios en blanco
            messagebox.showinfo(message='¡No puede dejar espacios en blanco!', title='Alerta')
        elif creditos == '':
            messagebox.showinfo(message='¡No puede dejar espacios en blanco!', title='Alerta')
        elif horas  == '':
            messagebox.showinfo(message='¡No puede dejar espacios en blanco!', title='Alerta')
        elif fecha1 == '':
            messagebox.showinfo(message='¡No puede dejar espacios en blanco!', title='Alerta')
        elif fecha2  == '':
            messagebox.showinfo(message='¡No puede dejar espacios en blanco!', title='Alerta')
        elif dia  == '':
            messagebox.showinfo(message='¡No puede dejar espacios en blanco!', title='Alerta')
        elif hora1  == '':
            messagebox.showinfo(message='¡No puede dejar espacios en blanco!', title='Alerta')
        elif hora2  == '':
            messagebox.showinfo(message='¡No puede dejar espacios en blanco!', title='Alerta')
        else:
            cond = False
            for x in cursos:
                if x.nombre == nombre:
                    messagebox.showinfo(message='¡Este curso ya fue agregado!', title='Alerta')
                    cond = True
                    break
            if cond != True:                                                          #se crea la condicion la cual permite limpiar los campos de texto y añadir el nuevo curso
                curso = curso_class(nombre,creditos,horas,fecha1,fecha2,dia,hora1,hora2)
                cursos.append(curso)
                nombre = sv_nombre.set('')
                creditos = sv_creditos.set('')
                horas = sv_horas.set('')
                fecha1 = sv_fecha1.set('')
                fecha2 = sv_fecha2.set('')
                dia = tkvarqdias.set('')
                hora1 = sv_hora1.set('')
                hora2 = sv_hora2.set('')
                opciones = OptionMenu(ventana_admin_cursos, tkvarq,*cursos,command = cambiar_valores_boton_modificar)
                opciones.pack(pady=20)
                opciones.place(x = 300, y = 125, width= 200, height=23)
                messagebox.showinfo(message='¡El curso fue agregado con éxito!', title='Alerta')

    def cambiar_valores_boton_modificar(self):                                        #se crea la funcion cambiar_valores_boton_modificar la cual permite cambiar los valores de los campos de texto
        curso = tkvarq.get()
        for x in cursos:
            if x.nombre == curso:
                x == curso
                sv_nombre.set(x.nombre)
                sv_creditos.set(x.creditos)
                sv_horas.set(x.horas)
                sv_fecha1.set(x.fecha1)
                sv_fecha2.set(x.fecha2)
                tkvarqdias.set(x.dia)
                sv_hora1.set(x.hora1)
                sv_hora2.set(x.hora2)
                opciones = OptionMenu(ventana_admin_cursos, tkvarq,*cursos,command = cambiar_valores_boton_modificar)
                opciones.pack(pady=20)
                opciones.place(x = 300, y = 125, width= 200, height=23)

    def boton_modificar_curso():                                                        #se crea la funcion boton_modificar_curso la cual permite modificar un curso
        curso = tkvarq.get()
        if curso == '':
            messagebox.showinfo(message='¡Debe seleccionar un curso!', title='Alerta')
        for x in cursos:
            if x.nombre == curso:
                if sv_nombre.get() == '':
                    messagebox.showinfo(message='¡No puede dejar espacios en blanco!', title='Alerta')
                elif sv_creditos.get() == '':
                    messagebox.showinfo(message='¡No puede dejar espacios en blanco!', title='Alerta')
                elif sv_horas.get()  == '':
                    messagebox.showinfo(message='¡No puede dejar espacios en blanco!', title='Alerta')
                elif sv_fecha1.get() == '':
                    messagebox.showinfo(message='¡No puede dejar espacios en blanco!', title='Alerta')
                elif sv_fecha2.get()  == '':
                    messagebox.showinfo(message='¡No puede dejar espacios en blanco!', title='Alerta')
                elif tkvarqdias.get()  == '':
                    messagebox.showinfo(message='¡No puede dejar espacios en blanco!', title='Alerta')
                elif sv_hora1.get()  == '':
                    messagebox.showinfo(message='¡No puede dejar espacios en blanco!', title='Alerta')
                elif sv_hora2.get()  == '':
                    messagebox.showinfo(message='¡No puede dejar espacios en blanco!', title='Alerta')
                else:
                    x == curso
                    x.nombre = sv_nombre.get()
                    x.creditos = sv_creditos.get()
                    x.horas = sv_horas.get()
                    x.fecha1 = sv_fecha1.get()
                    x.fecha2 = sv_fecha2.get()
                    x.dia = tkvarqdias.get()
                    x.hora1 = sv_hora1.get()
                    x.hora2 = sv_hora2.get()
                    messagebox.showinfo(message='¡Las modificaciones fueron exitosas!', title='Alerta')

                tkvarq.set(x.nombre)
                opciones = OptionMenu(ventana_admin_cursos, tkvarq,*cursos,command = cambiar_valores_boton_modificar)
                opciones.pack(pady=20)
                opciones.place(x = 300, y = 125, width= 200, height=23)

    def boton_eliminar_curso():                                                             #se crea la funcion boton_eliminar_curso la cual permite eliminar un curso
        curso = tkvarq.get()
        if curso == '':                                                                     
            messagebox.showinfo(message='¡Debe seleccionar una carrera!', title='Alerta')
        if len(cursos) == 1:
            messagebox.showinfo(message='¡Debe tener minimo 1 curso agregado!', title='Alerta')
        else:
            curso = tkvarq.get()
            for x in cursos:
                if x.nombre == curso:
                    cursos.remove(x)
                    nombre = sv_nombre.set('')
                    creditos = sv_creditos.set('')
                    horas = sv_horas.set('')
                    fecha1 = sv_fecha1.set('')
                    fecha2 = sv_fecha2.set('')
                    dia = tkvarqdias.set('')
                    hora1 = sv_hora1.set('')
                    hora2 = sv_hora2.set('')
                    messagebox.showinfo(message='¡Curso eliminado con éxito!', title='Alerta')
                tkvarq.set('')
                opciones = OptionMenu(ventana_admin_cursos, tkvarq,*cursos,command = cambiar_valores_boton_modificar)
                opciones.pack(pady=20)
                opciones.place(x = 300, y = 125, width= 200, height=23)
                
    if sv_opciones.get() == "Agregar/Modificar un curso":
        ventana_admin_cursos= Toplevel(ventana_inicial)
        ventana_admin_cursos.title('Sistema de Administración del Tiempo')
        ventana_admin_cursos.minsize(700,575)
        ventana_admin_cursos.resizable(False, False)
        ventana_admin_cursos.configure(background=Estilos.BACKGROUND1)

        titulo = tk.Label(ventana_admin_cursos, text = '''-----------------------------------------------------------------
        Adición o Modificación de Cursos
        -----------------------------------------------------------------''', **Estilos.STYLE
        ).pack(side=TOP)
        opcion_curso = tk.Label(ventana_admin_cursos, text= 'Seleccione el curso a modificar:', **Estilos.LABELS).place(x = 20, y = 120) 

        tkvarq = StringVar(ventana_admin_cursos)
        opciones = OptionMenu(ventana_admin_cursos, tkvarq,*cursos,command = cambiar_valores_boton_modificar)
        opciones.pack(pady=20)
        opciones.place(x = 300, y = 125, width= 200, height=23)
        nombrelabel = tk.Label(ventana_admin_cursos, text= 'Nombre del curso:', **Estilos.LABELS).place(x = 20, y = 160)   
        creditoslabel = tk.Label(ventana_admin_cursos, text= 'Número de créditos:', **Estilos.LABELS).place(x = 20, y = 200)   
        horaslabel = tk.Label(ventana_admin_cursos, text= 'Número de horas lectivas diarias:', **Estilos.LABELS).place(x = 20, y = 240)   
        fecha_iniciolabel = tk.Label(ventana_admin_cursos, text= 'Fecha de inicio del curso:', **Estilos.LABELS).place(x = 20, y = 280)   
        fecha_finallabel = tk.Label(ventana_admin_cursos, text= 'Fecha de finalización del curso:', **Estilos.LABELS).place(x = 20, y = 320)   
        dialabel = tk.Label(ventana_admin_cursos, text= 'Día de la clase:', **Estilos.LABELS).place(x = 20, y = 360)   
        hora_iniciolabel = tk.Label(ventana_admin_cursos, text= 'Hora de inicio de la clase:', **Estilos.LABELS).place(x = 20, y = 400)
        hora_finallabel = tk.Label(ventana_admin_cursos, text= 'Hora de finalización de la clase:', **Estilos.LABELS).place(x = 20, y = 440)
        sv_nombre = tk.StringVar()
        sv_creditos = tk.StringVar()
        sv_horas = tk.StringVar()
        sv_fecha1 = tk.StringVar()
        sv_fecha2 = tk.StringVar()
        sv_hora1 = tk.StringVar()
        sv_hora2 = tk.StringVar()
        nombre_input = tk.Entry(ventana_admin_cursos, width = 30, textvariable = sv_nombre).place(x = 185, y = 165,)
        creditos_input = tk.Entry(ventana_admin_cursos, width = 30, textvariable = sv_creditos).place(x = 200, y = 205)
        horas_input = tk.Entry(ventana_admin_cursos, width = 30, textvariable = sv_horas).place(x = 305, y = 245)
        fecha1_input = DateEntry(ventana_admin_cursos, selectmode='day', textvariable = sv_fecha1).place(x = 245, y = 285)
        fecha2_input = DateEntry(ventana_admin_cursos, selectmode='day', textvariable = sv_fecha2).place(x = 295, y = 325)
        hora1_input = tk.Entry(ventana_admin_cursos, width = 30, textvariable = sv_hora1).place(x = 245, y = 405)
        hora2_input = tk.Entry(ventana_admin_cursos, width = 30, textvariable = sv_hora2).place(x = 295, y = 445)

        tkvarqdias = tk.StringVar(ventana_admin_cursos)
        dia1_1 = OptionMenu(ventana_admin_cursos, tkvarqdias,*dias)
        dia1_1.pack(pady=20)
        dia1_1.place(x = 160, y = 365, width= 200, height=23)
        boton_regresar = tk.Button(ventana_admin_cursos, text = "Regresar a la pantalla inicial", command=lambda:[administrador(), esconder(ventana_admin_cursos)],**Estilos.BOTONES).place(x =20, y = 530)
        boton_añadir = tk.Button(ventana_admin_cursos, text='Añadir curso',command = boton_agregar_curso, **Estilos.BOTONES).place(x = 605, y = 530)
        boton_modificar = tk.Button(ventana_admin_cursos, text='Modificar', **Estilos.BOTONES,command = boton_modificar_curso).place(x = 530, y = 530)
        boton_limpiar = tk.Button(ventana_admin_cursos, text='Limpiar Valores', **Estilos.BOTONES,command= boton_limpiar_cursos).place(x = 415, y = 530)
        boton_eliminar = tk.Button(ventana_admin_cursos, text='Eliminar curso',command = boton_eliminar_curso, **Estilos.BOTONES_ALARMA).place(x = 505, y = 122)
        
    elif sv_opciones.get() == "Agregar/Modificar una carrera":
        admin_carreras()
    elif sv_opciones.get() == "Agregar un nuevo usuario":
        admin_usuarios()
    elif sv_opciones.get() == '':
        messagebox.showinfo(message='¡Debe seleccionar una opción!', title='Alerta')
        mostrar(ventana_admin_cursos)

def admin_carreras():                                                                   #se crea la funcion admin_carreras para que se pueda agregar una carrera
    def cambiar_valores_opcionbox_carreras(self):                                       #se crea la funcion cambiar_valores_opcionbox_carreras para que se pueda cambiar el valor de la opcion seleccionada en el opcionbox
        carrera = tkvarq_carreras.get()
        for x in carreras:
            if x.nombre == carrera:
                x == carrera
                sv_nombre_carrera.set(x.nombre)
                opcionescarreras = OptionMenu(ventana_admin_carreras, tkvarq_carreras,*carreras,command=cambiar_valores_opcionbox_carreras)
                opcionescarreras.pack(pady=20)
                opcionescarreras.place(x = 310, y = 125, width= 200, height=23)

    def cambiar_nombre_carrera():                                                       #se crea la funcion cambiar_nombre_carrera para que se pueda cambiar el nombre de la carrera
        carrera = tkvarq_carreras.get()
        for x in carreras:
            if x.nombre == carrera:
                if sv_nombre_carrera.get() != '':
                    x == carrera
                    x.nombre = sv_nombre_carrera.get()
                    tkvarq_carreras.set(x.nombre)
                    opcionescarreras = OptionMenu(ventana_admin_carreras, tkvarq_carreras,*carreras,command=cambiar_valores_opcionbox_carreras)
                    opcionescarreras.pack(pady=20)
                    opcionescarreras.place(x = 310, y = 125, width= 200, height=23)
                    messagebox.showinfo(message='¡El nombre fue modificado con éxito!', title='Alerta')
        if sv_nombre_carrera.get() == '':
            messagebox.showinfo(message='¡Seleccione una carrea!', title='Alerta')

    def vincular_curso_a_carrera():                                                     #se crea la funcion vincular_curso_a_carrera para que se pueda vincular un curso a una carrera
        curso = tkvarq_vincular_cursos_a_carreras.get()
        carrera = tkvarq_carreras.get()

        if carrera == '' :
            messagebox.showinfo(message='¡Debe seleccionar una carrera! ', title='Alerta')
        elif curso == '':
            messagebox.showinfo(message='¡Debe seleccionar un curso!', title='Alerta')
        else:
            for x in carreras:
                if carrera == x.nombre:
                    carrera = x
                    break
            for y in cursos:
                if y.nombre == curso:
                    curso = y
                    break
            carrera.agregar_curso(curso)

    def agregar_carrera():                                                              #se crea la funcion agregar_carrera para que se pueda agregar una nueva carrera
        carrera = sv_nombre_carrera.get()
        condicion = True
        for x in carreras:
            if x.nombre == carrera:
                messagebox.showinfo(message='¡Esta carrera ya fue agregada!', title='Alerta')
                condicion = False
                break
            else:
                pass
        if carrera == '':
            messagebox.showinfo(message='¡Añada un nombre!', title='Alerta')
            condicion = False    
        if condicion == True:
            carreraa = carrera_class(carrera)
            carreras.append(carreraa)
            opcionescarreras = OptionMenu(ventana_admin_carreras, tkvarq_carreras,*carreras,command=cambiar_valores_opcionbox_carreras)
            opcionescarreras.pack(pady=20)
            opcionescarreras.place(x = 310, y = 125, width= 200, height=23)
            sv_nombre_carrera.set('')
            tkvarq_carreras.set('')
            messagebox.showinfo(message='¡Carrera agregada con éxito!', title='Alerta')

    def limpiar_carreras():                                                             #se crea la funcion limpiar_carreras para que se pueda limpiar los valores de los campos de texto
        sv_nombre_carrera.set('')
        tkvarq_carreras.set('')
        tkvarq_vincular_cursos_a_carreras.set('')

    def desvincular_curso_a_carrera():                                                  #se crea la funcion desvincular_curso_a_carrera para que se pueda desvincular un curso de una carrera
        curso = tkvarq_vincular_cursos_a_carreras.get()
        carrera = tkvarq_carreras.get()
        for x in carreras:
            if carrera == x.nombre:
                carrera = x
                break
        for y in cursos:
            if y.nombre == curso:
                curso = y
                break
        carrera.quitar_curso(curso)

    def eliminar_carrera():                                                             #se crea la funcion eliminar_carrera para que se pueda eliminar una carrera
        carrera = tkvarq_carreras.get()
        if carrera == '':
            messagebox.showinfo(message='¡Debe seleccionar una carrera!', title='Alerta')
        if len(carreras) == 1:
            messagebox.showinfo(message='¡Debe tener mínimo una carrera agregada!', title='Alerta')
        else:
            carrera = tkvarq_carreras.get()
            for x in carreras:
                if x.nombre == carrera:
                    carreras.remove(x)
                    sv_nombre_carrera.set('')
                    tkvarq_carreras.set('')
                    tkvarq_vincular_cursos_a_carreras.set('')
                    messagebox.showinfo(message='¡La carrera fue eliminada con éxito!', title='Alerta')

                opcionescarreras = OptionMenu(ventana_admin_carreras, tkvarq_carreras,*carreras,command=cambiar_valores_opcionbox_carreras)
                opcionescarreras.pack(pady=20)
                opcionescarreras.place(x = 310, y = 125, width= 200, height=23)
            
    ventana_admin_carreras = Toplevel(ventana_inicial)
    ventana_admin_carreras.title('Sistema de Administración del Tiempo')
    ventana_admin_carreras.minsize(650,340)
    ventana_admin_carreras.resizable(False, False)
    ventana_admin_carreras.configure(background=Estilos.BACKGROUND1)
    titulo = tk.Label(ventana_admin_carreras, text = '''-----------------------------------------------------------------
    Adición o Modificación de Carreras
    -----------------------------------------------------------------''', **Estilos.STYLE
    ).pack(side=TOP)

    opcion_carrera = tk.Label(ventana_admin_carreras, text= 'Seleccione la carrera a modificar:', **Estilos.LABELS).place(x = 20, y = 120)

    tkvarq_carreras = StringVar(ventana_admin_carreras)
    opcionescarreras = OptionMenu(ventana_admin_carreras, tkvarq_carreras,*carreras,command=cambiar_valores_opcionbox_carreras)
    opcionescarreras.pack(pady=20)
    opcionescarreras.place(x = 310, y = 125, width= 200, height=23)

    nombre = tk.Label(ventana_admin_carreras, text= 'Nombre de la carrera:', **Estilos.LABELS).place(x = 20, y = 170)   
    vincular = tk.Label(ventana_admin_carreras, text= 'Seleccionar curso:', **Estilos.LABELS).place(x = 20, y = 220)   

    sv_nombre_carrera = tk.StringVar(ventana_admin_carreras)
    nombrecarrerainput = tk.Entry(ventana_admin_carreras,textvariable= sv_nombre_carrera,width = 30).place(x = 210, y = 176)

    tkvarq_vincular_cursos_a_carreras = StringVar(ventana_admin_carreras)
    vincular_cursos_a_carreras = OptionMenu(ventana_admin_carreras, tkvarq_vincular_cursos_a_carreras,*cursos)
    vincular_cursos_a_carreras.place(x = 185, y = 224,width=200,height=23)

    boton_eliminar = tk.Button(ventana_admin_carreras, text='Eliminar carrera', **Estilos.BOTONES_ALARMA,command = eliminar_carrera).place(x = 525, y = 122)
    boton_regresar = tk.Button(ventana_admin_carreras, text = "Regresar a la pantalla inicial", command=lambda:[administrador(), esconder(ventana_admin_carreras)], **Estilos.BOTONES).place(x =20, y = 300)
    boton_añadir_carrera = tk.Button(ventana_admin_carreras, text='Añadir carrera', **Estilos.BOTONES,command=agregar_carrera).place(x = 402, y = 170)
    boton_modificar_nombre_carrera = tk.Button(ventana_admin_carreras, text='Modificar nombre', **Estilos.BOTONES, command = cambiar_nombre_carrera).place(x = 502, y = 170)
    boton_vincular_curso_a_carrera = tk.Button(ventana_admin_carreras, text='Vincular curso', **Estilos.BOTONES,command = vincular_curso_a_carrera).place(x = 395, y = 221)
    boton_desvincular_curso_a_carrera = tk.Button(ventana_admin_carreras, text='Desvincular curso', **Estilos.BOTONES,command = desvincular_curso_a_carrera).place(x = 500, y = 221)
    boton_limpiar = tk.Button(ventana_admin_carreras, text='Limpiar valores', **Estilos.BOTONES,command = limpiar_carreras).place(x = 532, y = 300)
    '''messagebox.showinfo(message='¡Carrera agregada con éxito!', title='Alerta')
    messagebox.showinfo(message='¡Los datos fueron modificados con éxito!', title='Alerta')
    messagebox.askyesno(message="¿Está seguro que desea regresar a la pantalla anterior? \n\nTodo los datos digitados se perderán.", title="Título")
    messagebox.showinfo(message='Ya existe una carrera con este nombre. Ingrese un nuevo nombre.', title='Alerta')
    messagebox.showinfo(message='Por favor, seleccione primero una carrera para modificar.', title='Alerta')
    messagebox.showinfo(message='¡¡¡Ingrese un nombre válido!!!', title='Alerta')'''

def admin_usuarios():                                                                   #se crea la funcion admin_usuarios que se encarga de crear la ventana para añadir nuevos usuarios
    def boton_agregar_usuarios():                                                       #se crea la funcion boton_agregar_usuarios que se encarga de agregar un nuevo usuario
        nombre = sv_nombre_usuario.get()
        apellido1 = sv_apellido1.get()
        apellido2 = sv_apellido2.get()
        numero = sv_numero.get()
        usuario = sv_usuario.get()
        contraseña = sv_contra.get()
        tipo_usuario = sv_opciones_usuario.get()
        if tipo_usuario == "Administrativo":                                            #se crea la condicion para que el usuario sea administrador
            if nombre == '':                                                            #se crea la condicion para que los espacios no esten vacios
                messagebox.showinfo(message='¡No puede dejar espacios en blanco!', title='Alerta')
            elif apellido1 == '':
                messagebox.showinfo(message='¡No puede dejar espacios en blanco!', title='Alerta')
            elif apellido2  == '':
                messagebox.showinfo(message='¡No puede dejar espacios en blanco!', title='Alerta')          
            elif numero == '':
                messagebox.showinfo(message='¡No puede dejar espacios en blanco!', title='Alerta')
            elif usuario  == '':
                messagebox.showinfo(message='¡No puede dejar espacios en blanco! ', title='Alerta')
            elif contraseña  == '':
                messagebox.showinfo(message='¡No puede dejar espacios en blanco!', title='Alerta')
            else:
                usuario_final = UsuariosAdmin(nombre, apellido1, apellido2, numero, usuario, contraseña)
                if len(lista_usuarios_admin) == 0:                                        
                    lista_usuarios_admin.append(usuario_final)      
                    sv_nombre_usuario.set('')
                    sv_apellido1.set('')
                    sv_apellido2.set('')                                                                       
                    sv_numero.set('')
                    sv_usuario.set('')
                    sv_contra.set('')
                    messagebox.showinfo(message='¡Usuario agregado con éxito!', title='Alerta')
                else:
                    for x in lista_usuarios_admin:
                        if x.usuario == usuario:
                            messagebox.showinfo(message='¡ESTE NOMBRE DE USUARIO YA EXISTE!', title='Alerta')  
                            cond = True
                            break
                        else:
                            cond = False
                    if cond != True:
                        lista_usuarios_admin.append(usuario_final)
                        sv_nombre_usuario.set('')
                        sv_apellido1.set('')
                        sv_apellido2.set('')                                             
                        sv_numero.set('')
                        sv_usuario.set('')
                        sv_contra.set('')
                        messagebox.showinfo(message='¡Usuario agregado con éxito!', title='Alerta')

        elif tipo_usuario == 'Estudiante':                                                  #se crea la condicion para que el usuario sea estudiante
            if nombre == '':
                messagebox.showinfo(message='¡No puede dejar espacios en blanco!', title='Alerta')
            elif apellido1 == '':
                messagebox.showinfo(message='¡No puede dejar espacios en blanco!', title='Alerta')
            elif apellido2  == '':
                messagebox.showinfo(message='¡No puede dejar espacios en blanco!', title='Alerta')
            elif numero == '':
                messagebox.showinfo(message='¡No puede dejar espacios en blanco!', title='Alerta')   #No deja agregar un usuario si tiene espacios en blanco
            elif usuario  == '':
                messagebox.showinfo(message='¡No puede dejar espacios en blanco! ', title='Alerta')
            elif contraseña  == '':
                messagebox.showinfo(message='¡No puede dejar espacios en blanco!', title='Alerta')
            else:
                usuario_final = UsuariosEstudiante(nombre, apellido1, apellido2, numero, usuario, contraseña)
                if len(lista_usuarios_estudiantes) == 0:
                    lista_usuarios_estudiantes.append(usuario_final)
                    sv_nombre_usuario.set('')
                    sv_apellido1.set('')
                    sv_apellido2.set('')                                                
                    sv_numero.set('')
                    sv_usuario.set('')
                    sv_contra.set('')
                    messagebox.showinfo(message='¡Usuario agregado con éxito!', title='Alerta')
                else:
                    for x in lista_usuarios_estudiantes:
                        if x.usuario == usuario:
                            messagebox.showinfo(message='¡ESTE NOMBRE DE USUARIO YA EXISTE!', title='Alerta') 
                            cond = True
                            break
                        else:
                            cond = False
                    if cond != True:
                        lista_usuarios_estudiantes.append(usuario_final)
                        sv_nombre_usuario.set('')
                        sv_apellido1.set('')
                        sv_apellido2.set('')                                                
                        sv_numero.set('')
                        sv_usuario.set('')
                        sv_contra.set('')
                        messagebox.showinfo(message='¡Usuario agregado con éxito!', title='Alerta')
        elif tipo_usuario == '':
            messagebox.showinfo(message='¡Debe seleccionar un tipo de usuario!', title='Alerta')

        
    ventana_admin_usuarios = Toplevel(ventana_inicial)
    ventana_admin_usuarios.title('Sistema de Administración del Tiempo')
    ventana_admin_usuarios.minsize(650,500)                 
    ventana_admin_usuarios.resizable(False, False)                                                      
    ventana_admin_usuarios.configure(background=Estilos.BACKGROUND1)

    titulo = tk.Label(ventana_admin_usuarios, text = '''-----------------------------------------------------------------
    Adición de Usuarios
    -----------------------------------------------------------------''', **Estilos.STYLE
    ).pack(side=TOP)

    lbl_opcion_usuarios = tk.Label(ventana_admin_usuarios, text= 'Seleccione el tipo de usuario:', **Estilos.LABELS).place(x = 20, y = 120)  
    sv_opciones_usuario = tk.StringVar()
    combo_opciones = ttk.Combobox(ventana_admin_usuarios, textvariable=sv_opciones_usuario)
    combo_opciones['values'] = ["Administrativo", 'Estudiante']
    combo_opciones['state'] = 'readonly'
    combo_opciones.place(x = 280, y = 125, width= 210, height=23)
    lbl_nombre = tk.Label(ventana_admin_usuarios, text = 'Nombre:', **Estilos.LABELS).place(x = 20, y = 160)
    lbl_apellido1 = tk.Label(ventana_admin_usuarios, text = 'Primer apellido:', **Estilos.LABELS).place(x = 20, y = 200) 
    lbl_apellido2 = tk.Label(ventana_admin_usuarios, text = 'Segundo apellido:', **Estilos.LABELS).place(x = 20, y = 240)
    lbl_numero = tk.Label(ventana_admin_usuarios, text = 'Número telefónico:', **Estilos.LABELS).place(x = 20, y = 280)          #Labels
    lbl_usuario = tk.Label(ventana_admin_usuarios, text = 'Nombre de usuario:', **Estilos.LABELS).place(x = 20, y = 320)
    lbl_contra = tk.Label(ventana_admin_usuarios, text = 'Contraseña:', **Estilos.LABELS).place(x = 20, y = 360)

    sv_nombre_usuario = tk.StringVar()
    ent_nombre = tk.Entry(ventana_admin_usuarios, width = 30, textvariable=sv_nombre_usuario).place(x = 100, y = 165)
    sv_apellido1 = tk.StringVar()
    ent_apellido1 = tk.Entry(ventana_admin_usuarios, width = 30, textvariable=sv_apellido1).place(x = 160, y = 205)
    sv_apellido2 = tk.StringVar()
    ent_apellido2= tk.Entry(ventana_admin_usuarios, width = 30, textvariable=sv_apellido2).place(x = 180, y = 245)          #Cajas de texto
    sv_numero = tk.StringVar()
    ent_numero = tk.Entry(ventana_admin_usuarios, width = 30, textvariable=sv_numero).place(x = 190, y = 285)
    sv_usuario = tk.StringVar()
    ent_usuario = tk.Entry(ventana_admin_usuarios, width = 30, textvariable=sv_usuario).place(x = 195, y = 325)
    sv_contra = tk.StringVar()
    ent_contra = tk.Entry(ventana_admin_usuarios, show='*', width = 30, textvariable=sv_contra).place(x = 130, y = 365)

    boton_regresar = tk.Button(ventana_admin_usuarios, text = "Regresar a la pantalla inicial", command=lambda:[administrador(), esconder(ventana_admin_usuarios)],**Estilos.BOTONES).place(x =20, y = 455)
    boton_añadir = tk.Button(ventana_admin_usuarios, text='Añadir usuario', command= boton_agregar_usuarios,**Estilos.BOTONES).place(x = 535, y = 455)       #Botones

def usuarios_estudiantes():                                                             #se crea la funcion usuarios_estudiantes para iniciar sesion como estudiante
    global sv_contraseña_estudiante, sv_usuario_estudiante
    if sv_usuarios.get() == 'Estudiante':
        ventana_usuarios_admin = Toplevel(ventana_inicial)
        ventana_usuarios_admin.minsize(500,250)
        ventana_usuarios_admin.title('Sistema de Administración del Tiempo')                                               
        ventana_usuarios_admin.resizable(False,False)
        ventana_usuarios_admin.configure(background=Estilos.BACKGROUND1)

        lb_principal = tk.Label(ventana_usuarios_admin, text = '''-----------------------------------------------------------------
        Inicio de Sesión Estudiante
        -----------------------------------------------------------------''', **Estilos.STYLE).pack(side=TOP)

        lb_usuario = tk.Label(ventana_usuarios_admin, text = "Nombre de usuario:", **Estilos.LABELS).place(x = 20,y = 100)  
            
        lb_contraseña = tk.Label(ventana_usuarios_admin, text = "Contraseña:", **Estilos.LABELS).place(x = 20, y = 135)  
        sv_usuario_estudiante = tk.StringVar()        
        ent_usuario = tk.Entry(ventana_usuarios_admin, width = 30, textvariable=sv_usuario_estudiante).place(x = 200,y = 105)             
        sv_contraseña_estudiante = tk.StringVar()        
        ent_contraseña = tk.Entry(ventana_usuarios_admin, show='*', width = 30, textvariable=sv_contraseña_estudiante).place(x = 200, y = 140)  
            
        boton_ingresar = tk.Button(ventana_usuarios_admin, 
                                    text = "Ingresar",
                                    command=lambda:[estudiante(),esconder(ventana_usuarios_admin)], 
                                    **Estilos.BOTONES
                                    ).place(x = 425, y = 210)

    else:
        usuarios_admin()

def estudiante():                                                                       #se crea la funcion estudiante para acceder a las funciones del usuario estudiante
    global estudiantec, sv_opciones_estudiantes, ventana_usuario, variable_foto, sonido

    def desactivar_alarma():                                                            #se crea la funcion desactivar_alarma para desactivar la el sonido de alarma de la concentracción
        global sonido
        if sonido == True:
            sonido = False
            messagebox.showinfo(title='Desactivacion de alarma', message='Se ha desactivado el sonido la alarma')
        elif sonido == False:
            sonido = True
            messagebox.showinfo(title='Activacion de alarma', message='Se ha activado el sonido la alarma')

    for x in lista_usuarios_estudiantes:
        if x.usuario == sv_usuario_estudiante.get():
            if x.contraseña == sv_contraseña_estudiante.get():                                                 
                estudiantec = x

                ventana_usuario = Toplevel(ventana_inicial)
                ventana_usuario.title('Sistema de Administración del Tiempo')
                ventana_usuario.minsize(700,300)
                ventana_usuario.resizable(False, False)
                ventana_usuario.configure(background=Estilos.BACKGROUND1)

                titulo = tk.Label(ventana_usuario, text = '''----------------------------------------------------------
                    Sistema Estudiante
                -----------------------------------------------------------''', **Estilos.STYLE
                ).pack(side=TOP)

                instruccion1 = tk.Label(ventana_usuario, text = "Seleccione la opción que desea realizar:" , **Estilos.LABELS).place(x = 20, y = 115)  

                sv_opciones_estudiantes = tk.StringVar()
                opciones1 = ttk.Combobox(ventana_usuario, textvariable=sv_opciones_estudiantes)
                opciones1['values'] = ["Matricular una carrera", 
                                        "Matricular cursos", 
                                        'Agregar actividades',
                                        'Ver actividades',
                                        'Generar reporte']
                opciones1['state'] = 'readonly'
                opciones1.place(x = 370, y = 120, width= 200, height=23)

                variable_foto = tk.IntVar()
                check_toma_fotos = tk.Checkbutton(ventana_usuario,text= 'Registro de fotografias',onvalue=1,offvalue=0,variable=variable_foto,command=test).place(x =300, y=260)
                boton_desactivar_sonido = tk.Button(ventana_usuario, text = 'Desactivar sonido de alarma', command=lambda:[desactivar_alarma()],**Estilos.BOTONES).place(x =510, y = 260)
                boton_regresar = tk.Button(ventana_usuario, text = "Regresar a la pantalla inicial", command=lambda:[mostrar(ventana_inicial),esconder(ventana_usuario)],**Estilos.BOTONES).place(x =20, y = 260) #Botones
                boton_ingresar = tk.Button(ventana_usuario, text = "Seleccionar", command=lambda:[estudiante_carreras(), esconder(ventana_usuario)],**Estilos.BOTONES).place(x =575, y = 118)
            else:
                messagebox.showinfo(message='¡¡¡SU USUARIO O CONTRASEÑA SON INCORRECTOS!!!', title='Alerta')
                mostrar(ventana_usuario)
        elif sv_usuario_estudiante.get() == '':
            messagebox.showinfo(message='¡¡¡SU USUARIO O CONTRASEÑA SON INCORRECTOS!!!', title='Alerta')
            mostrar(ventana_usuario)
    if sv_usuario_estudiante.get() != x.usuario:
        messagebox.showinfo(message='¡¡¡SU USUARIO O CONTRASEÑA SON INCORRECTOS!!!', title='Alerta')
        mostrar(ventana_usuario)

def estudiante_carreras():                                                              #se crea la funcion estudiante_carreras para matricular una carrera a un estudiante
    global carrera_estudiante,  carrera_activa
    carrera_activa = False
    def elegir_carrera_estudiante():                                                    #se crea la funcion elegir_carrera_estudiante para elegir la carrera que se quiere matricular
        carrera = tkvarq_carrera_estudiante.get()
        if carrera == '':
            messagebox.showinfo(message='¡Seleccione la carrera que desea matricular!', title='Alerta')
        else:
            for x in carreras:
                if x.nombre == carrera:
                    global carrera_estudiante
                    carrera_estudiante = x

                    break
            try:
                if carrera_activa == False:
                    messagebox.showinfo(message='¡Seleccione la carrera que desea matricular!', title='Alerta')
            except:
                carrera_matriculada = tk.Label(ventana_usuario_carrera, text = '''''''''''''''''''''''', **Estilos.LABEL_1).place(x = 20, y = 205,width=500, height=50)
                carrera_matriculada_texto = tk.Label(ventana_usuario_carrera, text = 'Carrera matriculada: ' , **Estilos.LABELS).place(x = 20, y = 205)                #Label
                carrera_matriculada = tk.Label(ventana_usuario_carrera, text = carrera_estudiante , **Estilos.LABEL_1).place(x = 200, y = 208)
                cursos_estudiante = []
                carrera_activa = True

    def darse_de_baja():                                                                #se crea la funcion darse_de_baja para dar de baja al estudiante de la carrera
        global carrera_estudiante
        try:
            if carrera_estudiante == None:
                messagebox.showinfo(message='¡No ha matriculado niguna carrera!', title='Alerta')
            else:
                carrera_estudiante = None
                tkvarq_carrera_estudiante.set('')
                carrera_matriculada = tk.Label(ventana_usuario_carrera, text = '''''''''''''''''''''''', **Estilos.LABELS).place(x = 20, y = 205,width=500, height=50)
                carrera_matriculada_texto = tk.Label(ventana_usuario_carrera, text = 'Carrera matriculada: ' , **Estilos.LABELS).place(x = 20, y = 205)
                carrera_activa = False
                cursos_estudiante = []
        except:
            messagebox.showinfo(message='¡No ha matriculado niguna carrera!', title='Alerta')

    if sv_opciones_estudiantes.get() == "Matricular una carrera":
        ventana_usuario_carrera = Toplevel(ventana_inicial)
        ventana_usuario_carrera.title('Sistema de Administración del Tiempo')
        ventana_usuario_carrera.minsize(700,300)
        ventana_usuario_carrera.resizable(False, False)
        ventana_usuario_carrera.configure(background=Estilos.BACKGROUND1)

        titulo = tk.Label(ventana_usuario_carrera, text = '''-----------------------------------------------------------------
        Matrícula de Carreras
        -----------------------------------------------------------------''', **Estilos.STYLE
        ).pack(side=TOP)

        instruccion1 = tk.Label(ventana_usuario_carrera, text = "Seleccione la carrera que desea matricular:" , **Estilos.LABELS).place(x = 20, y = 135)  


        tkvarq_carrera_estudiante = StringVar(ventana_usuario_carrera)
        opciones_carrera_estudiante = OptionMenu(ventana_usuario_carrera, tkvarq_carrera_estudiante,*carreras)
        opciones_carrera_estudiante.pack(pady=20)
        opciones_carrera_estudiante.place(x = 390, y = 140, width= 200, height=23)


        boton_regresar = tk.Button(ventana_usuario_carrera, text = "Regresar a la pantalla inicial", command=lambda:[estudiante(), esconder(ventana_usuario_carrera)],**Estilos.BOTONES).place(x =20, y = 260)
        boton_matricular = tk.Button(ventana_usuario_carrera, text = "Matricular", **Estilos.BOTONES,command=elegir_carrera_estudiante).place(x =595, y = 138)
        boton_desmatricular = tk.Button(ventana_usuario_carrera, text = "Darse de baja", **Estilos.BOTONES_ALARMA,command=darse_de_baja).place(x =590, y = 260)        #Botones
        try:
            carrera_matriculada_texto = tk.Label(ventana_usuario_carrera, text = 'Carrera matriculada: ' , **Estilos.LABELS).place(x = 20, y = 205)
            carrera_matriculada = tk.Label(ventana_usuario_carrera, text = carrera_estudiante , **Estilos.LABELS).place(x = 210, y = 205)
            tkvarq_carrera_estudiante.set(carrera_estudiante)
        except:
            pass
    elif sv_opciones_estudiantes.get() == "Matricular cursos": 
        estudiante_cursos()
    elif sv_opciones_estudiantes.get() == 'Agregar actividades':
        agregar_actividades()
    elif sv_opciones_estudiantes.get() == 'Ver actividades':
        ver_actividades()
    elif sv_opciones_estudiantes.get() == 'Generar reporte':
        generar_reporte()

def estudiante_cursos():                                                                #se crea la funcion estudiante_cursos para mostrar los cursos que el estudiante puede matricular
    try:
        def matricular_curso():                                                         #se crea la funcion matricular_curso para matricular un curso
            curso_elegido = tkvarq_cursos_estudiante.get()
            for x in cursos:
                if curso_elegido == x.nombre:
                    curso_elegido = x
                    break
            if curso_elegido in cursos_estudiante:
                messagebox.showinfo(message='¡Este curso ya fue matriculado!', title='Alerta')
            else:
                cursos_estudiante.append(curso_elegido)
            lista_cursos = Listbox(ventana_usuario_cursos)
            for x in cursos_estudiante:
                lista_cursos.insert(END,x)                                                              
            lista_cursos.place(x = 205, y = 180, height=75)


        def desmatricular_curso():                                                      #se crea la funcion desmatricular_curso para desmatricular un curso
            curso_elegido = tkvarq_cursos_estudiante.get()
            for x in cursos:
                if curso_elegido == x.nombre:
                    curso_elegido = x
                    break
            if curso_elegido in cursos_estudiante:
                cursos_estudiante.remove(curso_elegido)
            else:
                messagebox.showinfo(message='¡Este curso no ha sido matriculado!', title='Alerta')                                 
            lista_cursos = Listbox(ventana_usuario_cursos)
            for x in cursos_estudiante:
                lista_cursos.insert(END,x)                                                              
            lista_cursos.place(x = 205, y = 180, height=75)

        ventana_usuario_cursos= Toplevel(ventana_inicial)
        ventana_usuario_cursos.title('Sistema de Administración del Tiempo')
        ventana_usuario_cursos.minsize(700,300)
        ventana_usuario_cursos.resizable(False, False)
        ventana_usuario_cursos.configure(background=Estilos.BACKGROUND1)

        titulo = tk.Label(ventana_usuario_cursos, text = '''-----------------------------------------------------------------
        Matrícula de Cursos
        -----------------------------------------------------------------''', **Estilos.STYLE
        ).pack(side=TOP)

        instruccion1 = tk.Label(ventana_usuario_cursos, text = "Seleccione los cursos que desea matricular:" , **Estilos.LABELS).place(x = 20, y = 135)  
        cursos_matriculados_label = tk.Label(ventana_usuario_cursos, text = "Cursos matriculados:" , **Estilos.LABELS).place(x = 20, y = 180)
        global lista_cursos
        lista_cursos = Listbox(ventana_usuario_cursos)
        for x in cursos_estudiante:
            lista_cursos.insert(END,x)           #Actualiza la listbox
        lista_cursos.place(x = 205, y = 180, height=30)

        tkvarq_cursos_estudiante = StringVar(ventana_usuario_cursos)
        opciones_cursos_estudiante = OptionMenu(ventana_usuario_cursos, tkvarq_cursos_estudiante, *carrera_estudiante.cursos_carrera)
        opciones_cursos_estudiante.pack(pady=20)
        opciones_cursos_estudiante.place(x = 405, y = 137, width= 200, height=23)

        boton_desmatricular = tk.Button(ventana_usuario_cursos, text = "Desmatricular", **Estilos.BOTONES,command=desmatricular_curso).place(x =597, y = 180)
        boton_regresar = tk.Button(ventana_usuario_cursos, text = "Regresar a la pantalla inicial", command=lambda:[estudiante(), esconder(ventana_usuario_cursos)], **Estilos.BOTONES).place(x =20, y = 260)
        boton_matricular = tk.Button(ventana_usuario_cursos, text = "Matricular", **Estilos.BOTONES,command=matricular_curso).place(x =620, y = 137)
    except:
        esconder(ventana_usuario_cursos)
        messagebox.showinfo(message='¡No ha matriculado niguna carrera!', title='Alerta')
        estudiante()
    
def agregar_actividades():                                                              #se crea la funcion agregar_actividades para agregar actividades
    def boton_agregar_actividades():                                                    #se crea la funcion boton_agregar_actividades para agregar una actividad la lista de actividades
        limite = 0
        limite2 = 0
        nombre = sv_nombre.get()
        descripcion = sv_descripcion.get()
        curso_asociado = sv_cursos.get()
        fecha1 = sv_fecha_inicio.get()                             
        fecha2 = sv_fecha_final.get()
        dia = sv_dias.get()
        horas_actividad = sv_horas.get()
        estado = 'Pendiente'
        hora_inicio = sv_hora_inicio.get()
        hora_final = sv_hora_final.get()

        if nombre == '':                                                                #se crea la condicion para que no se pueda agregar una actividad sin espacios
            messagebox.showinfo(message='¡No puede dejar espacios en blanco!', title='Alerta')
        elif descripcion == '':
            messagebox.showinfo(message='¡No puede dejar espacios en blanco!', title='Alerta')
        elif curso_asociado  == '':
            messagebox.showinfo(message='¡No puede dejar espacios en blanco!', title='Alerta')
        elif fecha1 == '':
            messagebox.showinfo(message='¡No puede dejar espacios en blanco!', title='Alerta')         
        elif fecha2  == '':
            messagebox.showinfo(message='¡No puede dejar espacios en blanco! ', title='Alerta')
        elif dia  == '':
            messagebox.showinfo(message='¡No puede dejar espacios en blanco!', title='Alerta')
        elif horas_actividad  == '':
            messagebox.showinfo(message='¡No puede dejar espacios en blanco!', title='Alerta')   
        elif estado  == '':
            messagebox.showinfo(message='¡No puede dejar espacios en blanco!', title='Alerta') 
        else:
            primer_slash = False
            cambio_fecha = None
            segundo_slash = False
            for x in fecha1:
                try:
                    if x == '/' and primer_slash == True:
                        cambio_fecha = cambio_fecha + x
                        segundo_slash = True
                        primer_slash = False
                    elif segundo_slash == True:
                        cambio_fecha = cambio_fecha + '20'
                        cambio_fecha = cambio_fecha + x                                  #Cambia el formato de la fecha de inicio de la actividad
                        segundo_slash = False
                    elif x == '/' and primer_slash == False:
                        primer_slash = True
                        cambio_fecha = cambio_fecha + x
                    else:
                        cambio_fecha = cambio_fecha + x
                except:
                    cambio_fecha = x
            fecha1 = cambio_fecha
            primer_slash = False
            cambio_fecha = None
            segundo_slash = False
            for x in fecha2:
                try:
                    if x == '/' and primer_slash == True:
                        cambio_fecha = cambio_fecha + x
                        segundo_slash = True
                        primer_slash = False
                    elif segundo_slash == True:
                        cambio_fecha = cambio_fecha + '20'
                        cambio_fecha = cambio_fecha + x                                    #Cambia el formato de la fecha de finalización de la actividad
                        segundo_slash = False
                    elif x == '/' and primer_slash == False:
                        primer_slash = True
                        cambio_fecha = cambio_fecha + x
                    else:
                        cambio_fecha = cambio_fecha + x
                except:
                    cambio_fecha = x
            fecha2 = cambio_fecha

            actividad = actividades_class(nombre, descripcion, curso_asociado, fecha1, fecha2, dia, horas_actividad, hora_inicio, hora_final, estado)
            if len(lista_actividades) == 0:
                lista_actividades.append(actividad)
                sv_nombre.set('')
                sv_descripcion.set('') 
                sv_cursos.set('')
                sv_fecha_inicio.set('')                                          
                sv_fecha_final.set('')
                sv_dias.set('')
                sv_horas.set('')
                sv_hora_inicio.set('')
                sv_hora_final.set('')
                messagebox.showinfo(message='¡Actividad agregada con éxito!', title='Alerta')
            else:
                for x in lista_actividades:
                    if x.nombre == nombre:
                        messagebox.showinfo(message='¡YA SE ENCUENTRA UNA ACTIVIDAD CON ESTE NOMBRE!', title='Alerta')
                        cond = True
                        break
                    else:
                        cond = False
                horas_actividad = int(horas_actividad)        
                horas_dias[dia].append(horas_actividad)
                                
                cont1 = 0
                cont = dias[cont1]
                while cont1 < len(horas_dias):
                    cont = dias[cont1]
                    cont1 = cont1 + 1                                              
                    for x in horas_dias.get(cont):
                        limite = limite + x

                for x in horas_dias.get(dia):
                    limite2 = limite2 + x
                
                if limite2 > 12:                                                                #se crea la condicion para verificar que las horas diarias de actividades no se excedan de 12 y las semanales de 74
                    horas_dias[dia].remove(horas_actividad)
                    messagebox.showinfo(message='¡La cantidad de horas de esta actividad provoca que se alcance el límite máximo de horas diarias!', title='Alerta')
                elif limite > 74:
                    horas_dias[dia].remove(horas_actividad)
                    messagebox.showinfo(message='¡La cantidad de horas de esta actividad provoca que se alcance el límite máximo de horas semanales!', title='Alerta')
                else:   
                    if cond != True:
                        lista_actividades.append(actividad)
                        sv_nombre.set('')
                        sv_descripcion.set('')
                        sv_cursos.set('')
                        sv_fecha_inicio.set('')
                        sv_fecha_final.set('')                               
                        sv_dias.set('')
                        sv_horas.set('')
                        sv_hora_inicio.set('')
                        sv_hora_final.set('')
                        messagebox.showinfo(message='¡Actividad agregada con éxito!', title='Alerta')
    
    if sv_opciones_estudiantes.get() == "Agregar actividades":
        ventana_actividades = Toplevel(ventana_inicial)
        ventana_actividades.title('Sistema de Administración del Tiempo')
        ventana_actividades.minsize(700,575)
        ventana_actividades.resizable(False, False)
        ventana_actividades.configure(background=Estilos.BACKGROUND1)

        titulo = tk.Label(ventana_actividades, text = '''-----------------------------------------------------------------
        Adición de Actividades
        -----------------------------------------------------------------''', **Estilos.STYLE
        ).pack(side=TOP)

        lbl_nombre = tk.Label(ventana_actividades, text = "Nombre:" , **Estilos.LABELS).place(x = 20, y = 135)  
        lbl_desripcion = tk.Label(ventana_actividades, text='Descripción:', **Estilos.LABELS).place(x = 20, y = 175) 
        lbl_cursos = tk.Label(ventana_actividades, text='Curso al que se asocia esta actividad:', **Estilos.LABELS).place(x = 20, y = 215) 
        lbl_fecha_inicio = tk.Label(ventana_actividades, text='Fecha de inicio:', **Estilos.LABELS).place(x = 20, y = 255) 
        lbl_fecha_final = tk.Label(ventana_actividades, text='Fecha de finalización:', **Estilos.LABELS).place(x = 20, y = 295)                #Labels
        lbl_dia = tk.Label(ventana_actividades, text='Día:', **Estilos.LABELS).place(x = 20, y = 335) 
        lbl_hora_inicio = tk.Label(ventana_actividades, text='Hora de inicio:', **Estilos.LABELS).place(x = 20, y = 375) 
        lbl_hora_final = tk.Label(ventana_actividades, text='Hora de finalización:', **Estilos.LABELS).place(x = 20, y = 415) 
        lbl_horas = tk.Label(ventana_actividades, text='Horas de dedicación:', **Estilos.LABELS).place(x = 20, y = 455) 

        sv_nombre = tk.StringVar()
        ent_nombre = tk.Entry(ventana_actividades, width = 30, textvariable=sv_nombre).place(x = 100, y = 140)
        sv_descripcion = tk.StringVar()
        ent_descripcion = tk.Entry(ventana_actividades, width = 30, textvariable=sv_descripcion).place(x = 133, y = 180)
        sv_fecha_inicio = tk.StringVar()
        ent_fecha_inicio = DateEntry(ventana_actividades, selectmode='day', textvariable = sv_fecha_inicio).place(x = 160, y = 260) #Entrys
        sv_fecha_final = tk.StringVar()
        ent_fecha_final = DateEntry(ventana_actividades, selectmode='day', textvariable = sv_fecha_final).place(x = 210, y = 300)
        sv_horas = tk.StringVar()
        ent_horas = tk.Entry(ventana_actividades, width = 30, textvariable=sv_horas).place(x = 210, y = 460)
        sv_dias = tk.StringVar()
        dias = ['Lunes', 'Martes', 'Miércoles','Jueves', 'Viernes', 'Sábado', 'Domingo']
        combo_dias = OptionMenu(ventana_actividades, sv_dias, *dias)
        combo_dias.place(x = 63, y = 338, width= 200, height=23)
        sv_cursos = tk.StringVar()
        cursos = ['Sin curso asociado', 'Taller de Programación', 'Introducción a la Programación']
        combo_cursos = OptionMenu(ventana_actividades, sv_cursos, *cursos)
        combo_cursos.place(x = 347, y = 217, width= 200, height=23)
        sv_hora_inicio = tk.StringVar()
        ent_hora_inicio = tk.Entry(ventana_actividades, width = 30, textvariable=sv_hora_inicio).place(x = 150, y = 379)
        sv_hora_final = tk.StringVar()
        ent_hora_final = tk.Entry(ventana_actividades, width = 30, textvariable=sv_hora_final).place(x = 197, y = 421)
        boton_regresar = tk.Button(ventana_actividades, text = "Regresar a la pantalla inicial", command=lambda:[estudiante(), esconder(ventana_actividades)], **Estilos.BOTONES).place(x =20, y = 535)
        boton_agregar = tk.Button(ventana_actividades, text = "Agregar", command=lambda:boton_agregar_actividades(),**Estilos.BOTONES).place(x =620, y = 535)

def ver_actividades():                                                                  #función para ver las actividades que han sido creadas
    def ver_actividad():                                                                #Función para ver una actividad en específico
        if sv_ver_act.get() == '':
            messagebox.showinfo(message='¡Debe seleccionar una actividad!', title='Alerta')
        else:
            for x in lista_actividades:                                                 
                if x.nombre == sv_ver_act.get():
                    sv_nombre_act.set(x.nombre)
                    sv_desc.set(x.descripcion)
                    sv_curso_asc.set(x.curso_asociado)                     
                    sv_fecha1.set(x.fecha1)
                    sv_fecha2.set(x.fecha2)
                    sv_dia.set(x.dia)
                    sv_horas.set(x.horas_actividad)
                    sv_estado.set(x.estado)
                    break

    def actualizar_estado():                                                           #Función para actualizar el estado de una actividad, ya sea de pendiente a ejecutada o viceversa
        if sv_ver_act.get() == '':
            messagebox.showinfo(message='¡Debe seleccionar una actividad!', title='Alerta')
        else: 
            for x in lista_actividades:
                if x.nombre == sv_ver_act.get():
                    if x.estado == 'Pendiente':
                        x.estado = 'Ejecutada'
                        sv_estado.set('Ejecutada')                                              
                        break   
                    elif x.estado == 'Ejecutada':
                        x.estado = 'Pendiente'
                        sv_estado.set('Pendiente')
                        break   

    global sv_reportes
    ventana_ver_actividades = Toplevel(ventana_inicial)
    ventana_ver_actividades.title('Sistema de Administración del Tiempo')
    ventana_ver_actividades.minsize(600,500)
    ventana_ver_actividades.resizable(False, False)
    ventana_ver_actividades.configure(background=Estilos.BACKGROUND1)
    titulo = tk.Label(ventana_ver_actividades, text = '''    --------------------------------------
    Visualización de Actividades
    --------------------------------------''', **Estilos.STYLE
    ).pack(side=TOP)

    opcion = tk.Label(ventana_ver_actividades, text = "Actividad:" , **Estilos.LABELS).place(x = 20, y = 100)  
    lbl_nombre = tk.Label(ventana_ver_actividades, text = "Nombre:" , **Estilos.LABELS).place(x = 20, y = 155)
    lbl_desc = tk.Label(ventana_ver_actividades, text = "Descripción:" , **Estilos.LABELS).place(x = 20, y = 190)
    lbl_curso_asc = tk.Label(ventana_ver_actividades, text = "Curso asociado:" , **Estilos.LABELS).place(x = 20, y = 225)              #Labels
    lbl_fecha1 = tk.Label(ventana_ver_actividades, text = "Fecha de inicio:" , **Estilos.LABELS).place(x = 20, y = 260)
    lbl_fecha2 = tk.Label(ventana_ver_actividades, text = "Fecha de finalización:" , **Estilos.LABELS).place(x = 20, y = 295)
    lbl_dia = tk.Label(ventana_ver_actividades, text = "Día:" , **Estilos.LABELS).place(x = 20, y = 330)
    lbl_horas = tk.Label(ventana_ver_actividades, text = "Horas invertidas:" , **Estilos.LABELS).place(x = 20, y = 365)
    lbl_estado = tk.Label(ventana_ver_actividades, text = "Estado de la actividad:" , **Estilos.LABELS).place(x = 20, y = 400)

    sv_nombre_act = tk.StringVar()
    txt_nombre = tk.Label(ventana_ver_actividades, textvariable=sv_nombre_act, text = '''''''''''''''''''''''''''''' , **Estilos.LABEL_1).place(x = 100, y = 158)
    sv_desc = tk.StringVar()
    txt_desc = tk.Label(ventana_ver_actividades, textvariable=sv_desc, text = '''''''''''''''''''''''''''''' , **Estilos.LABEL_1).place(x = 133, y = 193)
    sv_curso_asc= tk.StringVar()
    txt_curso_asc = tk.Label(ventana_ver_actividades, textvariable=sv_curso_asc, text = '''''''''''''''''''''''''''''' , **Estilos.LABEL_1).place(x = 165, y = 228)
    sv_fecha1 = tk.StringVar()
    txt_fecha1 = tk.Label(ventana_ver_actividades, textvariable=sv_fecha1, text = '''''''''''''''''''''''''''''' , **Estilos.LABEL_1).place(x = 158, y = 263)      #Labels
    sv_fecha2 = tk.StringVar()
    txt_fecha2 = tk.Label(ventana_ver_actividades, textvariable=sv_fecha2, text = '''''''''''''''''''''''''''''' , **Estilos.LABEL_1).place(x = 208, y = 298)
    sv_dia = tk.StringVar()
    txt_dia = tk.Label(ventana_ver_actividades, textvariable=sv_dia, text = '''''''''''''''''''''''''''''' , **Estilos.LABEL_1).place(x = 60, y = 333)
    sv_horas = tk.StringVar()
    txt_horas = tk.Label(ventana_ver_actividades, textvariable=sv_horas, text = '''''''''''''''''''''''''''''' , **Estilos.LABEL_1).place(x = 165, y = 368)
    sv_estado = tk.StringVar()
    txt_estado = tk.Label(ventana_ver_actividades, textvariable=sv_estado, text = '''''''''''''''''''''''''''''' , **Estilos.LABEL_1).place(x = 215, y = 403)

    lista_ver_acts = []
    for x in lista_actividades:
        lista_ver_acts.append(x.nombre)

    sv_ver_act = tk.StringVar()
    opt_ver_act = OptionMenu(ventana_ver_actividades, sv_ver_act, *lista_ver_acts)
    opt_ver_act.place(x = 108, y = 102, width= 150, height=23)

    boton_regresar = tk.Button(ventana_ver_actividades, text = "Regresar a la pantalla inicial", command=lambda:[estudiante(), esconder(ventana_ver_actividades)], **Estilos.BOTONES).place(x =20, y = 455)
    boton_ingresar = tk.Button(ventana_ver_actividades, text = "Seleccionar", command=lambda:ver_actividad(), **Estilos.BOTONES).place(x =265, y = 98)
    boton_actualizar = tk.Button(ventana_ver_actividades, text = "Cambiar estado de actividad", command=lambda:actualizar_estado(), **Estilos.BOTONES).place(x =350, y = 98) #Botones

def generar_reporte():                                                                  #funcion para ver las posibles opciones de reportes
    global sv_reportes
    ventana_reportes = Toplevel(ventana_inicial)
    ventana_reportes.title('Sistema de Administración del Tiempo')
    ventana_reportes.minsize(600,300)                                  
    ventana_reportes.resizable(False, False)
    ventana_reportes.configure(background=Estilos.BACKGROUND1)

    titulo = tk.Label(ventana_reportes, text = '''-----------------------------------------------------------------
    Generación de Reportes
    -----------------------------------------------------------------''', **Estilos.STYLE
    ).pack(side=TOP)

    opcion = tk.Label(ventana_reportes, text = "Tipo de reporte:" , **Estilos.LABELS).place(x = 20, y = 135)  

    sv_reportes = tk.StringVar()
    reportes1 = ttk.Combobox(ventana_reportes, textvariable=sv_reportes)
    reportes1['values'] = ['Reporte de actividades', 'Reporte de porcentaje de actividades ejecutadas', 'Reporte de tiempo disponible', 'Actividades concluidas', 'Reporte semanal']
    reportes1['state'] = 'readonly'
    reportes1.place(x = 163, y = 137, width= 265, height=23)

    boton_regresar = tk.Button(ventana_reportes, text = "Regresar a la pantalla inicial", command=lambda:[estudiante(), esconder(ventana_reportes)], **Estilos.BOTONES).place(x =20, y = 255)
    boton_ingresar = tk.Button(ventana_reportes, text = "Seleccionar", command=lambda:[reporte_actividades(), esconder(ventana_reportes)], **Estilos.BOTONES).place(x =500, y = 255)

def reporte_actividades():                                                              #funcion para generar un reporte de las actividades que hay por dia
    def vaciar_listbox():                                                               #Funcion para vaciar el listbox
        list_acts.delete(0,END)                                     

    def cambiar_dia():                                                                  #Funcion para cambiar el dia del reporte
        if dias.get() == '':
            messagebox.showinfo(message='¡Debe seleccionar un día!', title='Alerta')
        else:
            dia_seleccionado = dias.get()
            sv_dia.set(dia_seleccionado)
    
    def agregar_actividades():                                                          #Funcion para agregar actividades al listbox y mostarlas
        lista_activs = []
        for x in lista_actividades:
            if x.dia == dias.get():
                lista_activs.append(x.nombre)

        for x in lista_activs:
            list_acts.insert(END,x)
        list_acts.place(x = 285, y = 180, height=150)

    if sv_reportes.get() == 'Reporte de actividades':
        ventana_reportes_actividades = Toplevel(ventana_inicial)
        ventana_reportes_actividades.title('Sistema de Administración del Tiempo')
        ventana_reportes_actividades.minsize(600,415)                                                   
        ventana_reportes_actividades.resizable(False, False)
        ventana_reportes_actividades.configure(background=Estilos.BACKGROUND1)

        titulo = tk.Label(ventana_reportes_actividades, text = '''-----------------------------------------------------------------
        Reporte de Actividades
        -----------------------------------------------------------------''', **Estilos.STYLE
        ).pack(side=TOP)

        opcion = tk.Label(ventana_reportes_actividades, text = "Seleccione el día:" , **Estilos.LABELS).place(x = 20, y = 135)  
        lbl_acts =  tk.Label(ventana_reportes_actividades, text = "Actividades del día:" , **Estilos.LABELS).place(x = 20, y = 175)
        sv_dia = tk.StringVar()
        lbl_dia = tk.Label(ventana_reportes_actividades, text = '''''''''''''''''''', textvariable=sv_dia, **Estilos.LABELS).place(x = 195, y = 175)

        dias = tk.StringVar()
        dias1 = ttk.Combobox(ventana_reportes_actividades, textvariable=dias)
        dias1['values'] = ['Lunes', 'Martes', 'Miércoles', 'Jueves', 'Viernes', 'Sábado', 'Domingo']
        dias1['state'] = 'readonly'
        dias1.place(x = 180, y = 137, width= 150, height=23)

        list_acts = Listbox(ventana_reportes_actividades)

        lista_activs = []

        for x in lista_actividades:
            if x.dia == dias.get():
                lista_activs.append(x)


        for x in lista_activs:
            list_acts.insert(END,x)
        list_acts.place(x = 285, y = 180, height=150)

        boton_regresar = tk.Button(ventana_reportes_actividades, text = "Regresar a la pantalla inicial", command=lambda:[generar_reporte(), esconder(ventana_reportes_actividades)], **Estilos.BOTONES).place(x =20, y = 370)
        boton_seleccionar = tk.Button(ventana_reportes_actividades, text = "Seleccionar", command=lambda:[vaciar_listbox(), cambiar_dia(), agregar_actividades()],**Estilos.BOTONES).place(x =335, y = 135)

    elif sv_reportes.get() == 'Reporte de porcentaje de actividades ejecutadas':
        reporte_porcentaje()
    elif sv_reportes.get() == 'Reporte de tiempo disponible':
        reporte_tiempo()
    elif sv_reportes.get() == 'Actividades concluidas':
        reporte_concluidas()
    elif sv_reportes.get() == 'Reporte semanal':
        reporte_acts_semanal()

def reporte_porcentaje():                                                               #funcion para generar un reporte del porcentaje de actividade por dia que han sido ejecutadas
    def porcentaje():                                                                   #Funcion para calcular el porcentaje de actividades ejecutadas
        cont = 0
        cont2 = 0
        lista1 = []
        dia_porc = dias.get()
        for x in lista_actividades:
            if dia_porc  == x.dia:
                cont += 1 
                lista1.append(x.estado)
        if dia_porc == '':
            messagebox.showinfo(message='¡Debe seleccionar un día!', title='Alerta')
        else:
            for y in lista1:
                if y == 'Ejecutada':
                    cont2 +=1
            if cont == 0:
                sv_porcentaje.set('Usted no cuenta con actividades para este día')
            else:
                prcntj = (cont2/cont) * 100,'%'
                sv_porcentaje.set(prcntj)

    ventana_reportes_porcentaje = Toplevel(ventana_inicial)
    ventana_reportes_porcentaje.title('Sistema de Administración del Tiempo')
    ventana_reportes_porcentaje.minsize(600,400)
    ventana_reportes_porcentaje.resizable(False, False)
    ventana_reportes_porcentaje.configure(background=Estilos.BACKGROUND1)

    titulo = tk.Label(ventana_reportes_porcentaje, text = '''------------------------------------------------------------------------
    Reporte de Porcentaje de Actividades Ejecutadas
    ------------------------------------------------------------------------''', **Estilos.STYLE
    ).pack(side=TOP)

    opcion = tk.Label(ventana_reportes_porcentaje, text = "Seleccione el día:" , **Estilos.LABELS).place(x = 20, y = 135)  
    lbl_porct =  tk.Label(ventana_reportes_porcentaje, text = "El porcentaje es del:" , **Estilos.LABELS).place(x = 20, y = 175)
    sv_porcentaje = tk.StringVar()
    lbl_porcentaje = tk.Label(ventana_reportes_porcentaje, text = '''''''''''''''''', textvariable=sv_porcentaje, **Estilos.LABEL_1).place(x = 200, y = 178)

    dias = tk.StringVar()
    dias1 = ttk.Combobox(ventana_reportes_porcentaje, textvariable=dias)
    dias1['values'] = ['Lunes', 'Martes', 'Miércoles', 'Jueves', 'Viernes', 'Sábado', 'Domingo']
    dias1['state'] = 'readonly'
    dias1.place(x = 180, y = 137, width= 150, height=23)

    boton_regresar = tk.Button(ventana_reportes_porcentaje, text = "Regresar a la pantalla inicial", command=lambda:[generar_reporte(), esconder(ventana_reportes_porcentaje)], **Estilos.BOTONES).place(x =20, y = 355)
    boton_ingresar = tk.Button(ventana_reportes_porcentaje, text = "Seleccionar", command=lambda:porcentaje(),**Estilos.BOTONES).place(x =335, y = 135)

def reporte_tiempo():                                                                   #funcion para generar un reporte del tiempo que tiene disponible el usuario por dia para agregar actividades
    def tiempo():                                                                       #Funcion para calcular el tiempo disponible
        cont = 0
        dia_tiempo = dias.get()
        if dia_tiempo == '':
            messagebox.showinfo(message='¡Debe seleccionar un día!', title='Alerta')
        else:
            for x in horas_dias.get(dia_tiempo):
                cont = cont + x
            if cont == 0:
                sv_porcentaje.set('12 horas')
            else:
                horas_totales = 12 - cont, 'horas'
                sv_porcentaje.set(horas_totales)
        
    ventana_reportes_tiempo = Toplevel(ventana_inicial)
    ventana_reportes_tiempo.title('Sistema de Administración del Tiempo')
    ventana_reportes_tiempo.minsize(600,400)
    ventana_reportes_tiempo.resizable(False, False)
    ventana_reportes_tiempo.configure(background=Estilos.BACKGROUND1)

    titulo = tk.Label(ventana_reportes_tiempo, text = '''------------------------------------------------------------------------
    Reporte de Tiempo Disponible
    ------------------------------------------------------------------------''', **Estilos.STYLE
    ).pack(side=TOP)

    opcion = tk.Label(ventana_reportes_tiempo, text = "Seleccione el día:" , **Estilos.LABELS).place(x = 20, y = 135)  
    lbl_porct =  tk.Label(ventana_reportes_tiempo, text = "Tiempo disponible:" , **Estilos.LABELS).place(x = 20, y = 175)
    sv_porcentaje = tk.StringVar()
    lbl_porcentaje = tk.Label(ventana_reportes_tiempo, text = 'Porcentaje:', textvariable=sv_porcentaje, **Estilos.LABEL_1).place(x = 190, y = 178)


    dias = tk.StringVar()
    dias1 = ttk.Combobox(ventana_reportes_tiempo, textvariable=dias)
    dias1['values'] = ['Lunes', 'Martes', 'Miércoles', 'Jueves', 'Viernes', 'Sábado', 'Domingo']
    dias1['state'] = 'readonly'
    dias1.place(x = 180, y = 137, width= 150, height=23)

    boton_regresar = tk.Button(ventana_reportes_tiempo, text = "Regresar a la pantalla inicial", command=lambda:[generar_reporte(), esconder(ventana_reportes_tiempo)], **Estilos.BOTONES).place(x =20, y = 355)
    boton_seleccionar = tk.Button(ventana_reportes_tiempo, text = "Seleccionar", command=lambda:tiempo(), **Estilos.BOTONES).place(x =335, y = 135)

def reporte_concluidas():                                                               #funcion para generar un reporte de las actividades concluidas y sus emociones respectivas
    def concluidas():                                                                   #Funcion para mostrar la emocion predominante por actividad
        if sv_ver_act.get() == '':
            messagebox.showinfo(message='¡Debe seleccionar una actividad!', title='Alerta')
        else:
            for x in lista_actividades:
                if x.nombre == sv_ver_act.get():
                    sv_general.set(x.emocion_general)
                    sv_5_prim_min.set(x.emocion_5_min)
                    sv_5_ult_min.set('No se logró este proceso')
                    break

    ventana_reportes_concluidas = Toplevel(ventana_inicial)
    ventana_reportes_concluidas.title('Sistema de Administración del Tiempo')
    ventana_reportes_concluidas.minsize(600,415)
    ventana_reportes_concluidas.resizable(False, False)
    ventana_reportes_concluidas.configure(background=Estilos.BACKGROUND1)

    titulo = tk.Label(ventana_reportes_concluidas, text = '''-----------------------------------------------------------------
    Reporte de Actividades Concluidas
    -----------------------------------------------------------------''', **Estilos.STYLE).pack(side=TOP)

    lbl_seleccionar = tk.Label(ventana_reportes_concluidas, text = "Seleccione la actividad:" , **Estilos.LABELS).place(x = 20, y = 120)  
    lbl_general = tk.Label(ventana_reportes_concluidas, text = "Estado de ánimo general:" , **Estilos.LABELS).place(x = 20, y = 160)  
    lbl_primero5 = tk.Label(ventana_reportes_concluidas, text = "Primeros 5 minutos:" , **Estilos.LABELS).place(x = 20, y = 200)  
    lbl_ultimos5 = tk.Label(ventana_reportes_concluidas, text = "Últimos 5 minutos:" , **Estilos.LABELS).place(x = 20, y = 240)  

    sv_general = tk.StringVar()
    txt_general = tk.Label(ventana_reportes_concluidas, textvariable=sv_general, text = '''''''''''''''''''''''''''''''' , **Estilos.LABEL_1).place(x = 240, y = 163)
    sv_5_prim_min = tk.StringVar()
    txt_5_prim_min = tk.Label(ventana_reportes_concluidas, textvariable=sv_5_prim_min, text = '''''''''''''''''''''''''''''''' , **Estilos.LABEL_1).place(x = 200, y = 203)
    sv_5_ult_min = tk.StringVar()
    txt_5_ult_min = tk.Label(ventana_reportes_concluidas, textvariable=sv_5_ult_min, text = '''''''''''''''''''''''''''''''' , **Estilos.LABEL_1).place(x = 180, y = 243)
    
    btn_iniciar = tk.Button(ventana_reportes_concluidas, text = "Seleccionar", command=lambda:concluidas(), **Estilos.BOTONES).place(x = 430, y = 118, width=80)
    
    lista_ver_acts = []
    for x in lista_actividades:
        lista_ver_acts.append(x.nombre)

    sv_ver_act = tk.StringVar()
    opt_ver_act = OptionMenu(ventana_reportes_concluidas, sv_ver_act, *lista_ver_acts)
    opt_ver_act.place(x = 225, y = 122, width= 200, height=23)

    boton_regresar = tk.Button(ventana_reportes_concluidas, text = "Regresar a la pantalla inicial", command=lambda:[generar_reporte(), esconder(ventana_reportes_concluidas)], **Estilos.BOTONES).place(x =20, y = 370)

def reporte_acts_semanal():                                                             #funcion para generar un reporte de las emociones que se han obtenido durante una semana
    global dia, noche, tarde, lst_dia, lst_noche, lst_tarde
    def reporte_semanal():                                                              #Funcion para generar el reporte de las emociones que se han obtenido durante una semana, separandolas por actividades de la mañana, tarde y noche
        global dia, noche, tarde
        for x in lista_actividades:
            if '06:00' <= x.hora_inicio < '11:59':
                if x.emocion_general != 'Actividad sin realizar':
                    lst_dia.apend(x.emocion_general)
            elif '12:00' <= x.hora_inicio < '17:59':
                if x.emocion_general != 'Actividad sin realizar':
                    lst_noche.append(x.emocion_general)
            elif '18:00' <= x.hora_inicio < '23:59':
                if x.emocion_general != 'Actividad sin realizar':
                    lst_tarde.append(x.emocion_general)
            elif '00:00' <= x.hora_inicio < '05:59':
                if x.emocion_general != 'Actividad sin realizar':
                    lst_noche.append(x.emocion_general)

        if len(lst_dia) == 0:
            sv_temp1.set('No hubieron actividades en la mañana')
        else:
            dia = max(set(lst_dia), key=lst_dia.count)
            sv_temp1.set(dia)
        
        if len(lst_tarde) == 0:
            sv_temp2.set('No hubieron actividades en la tarde')              
        else:
            tarde = max(set(lst_tarde), key=lst_tarde.count)
            sv_temp2.set(tarde)

        if len(lst_noche) == 0:
            sv_temp3.set('No hubieron actividades en la noche')
        else:
            noche = max(set(lst_noche), key=lst_noche.count)
            sv_temp3.set(noche)

    ventana_reportes_semanal = Toplevel(ventana_inicial)
    ventana_reportes_semanal.title('Sistema de Administración del Tiempo')
    ventana_reportes_semanal.minsize(700,415)
    ventana_reportes_semanal.resizable(False, False)
    ventana_reportes_semanal.configure(background=Estilos.BACKGROUND1)

    titulo = tk.Label(ventana_reportes_semanal, text = '''-----------------------------------------------------------------
    Reporte de Actividades Semanal
    -----------------------------------------------------------------''', **Estilos.STYLE).pack(side=TOP)
    sv_temp1 = tk.StringVar()
    lbl_temp1 = tk.Label(ventana_reportes_semanal, textvariable= sv_temp1, text = '''''''''''''''''''''''' , **Estilos.LABEL_1).place(x = 330, y = 158)  
    sv_temp2 = tk.StringVar()
    lbl_temp2 = tk.Label(ventana_reportes_semanal, textvariable=sv_temp2, text = '''''''''''''''''''''''' , **Estilos.LABEL_1).place(x = 310, y = 208)  
    sv_temp3 = tk.StringVar()
    lbl_temp3 = tk.Label(ventana_reportes_semanal, textvariable= sv_temp3, text = '''''''''''''''''''''''' , **Estilos.LABEL_1).place(x = 320, y = 258)  

    lbl_general = tk.Label(ventana_reportes_semanal, text = "Estado predominante en la mañana:" , **Estilos.LABELS).place(x = 20, y = 155)  
    lbl_primero5 = tk.Label(ventana_reportes_semanal, text = "Estado predominante en la tarde:" , **Estilos.LABELS).place(x = 20, y = 205)  
    lbl_ultimos5 = tk.Label(ventana_reportes_semanal, text = "Estado predominante en la noche:" , **Estilos.LABELS).place(x = 20, y = 255)  

    btn_reporte = tk.Button(ventana_reportes_semanal, text = "Generar reporte semanal", command=lambda:reporte_semanal(),**Estilos.BOTONES).place(x = 230, y = 110, width=200)

    boton_regresar = tk.Button(ventana_reportes_semanal, text = "Regresar a la pantalla inicial", command=lambda:[generar_reporte(), esconder(ventana_reportes_semanal)], **Estilos.BOTONES).place(x =20, y = 370)

def esconder(v):                                                                        #funcion para esconder una ventana
    v.withdraw()

def mostrar(v):                                                                         #funcion para mostrar una ventana
    v.deiconify()

ventana_inicial = tk.Tk()                                                               #creacion de la ventana inicial
ventana_inicial.minsize(700,250)                                                        #tamaño minimo de la ventana
ventana_inicial.resizable(False, False)                                                 #no se puede cambiar el tamaño de la ventana
ventana_inicial.configure(background=Estilos.BACKGROUND1)                               #se personaliza la ventana
ventana_inicial.title('Sistema de Administración del Tiempo')                           #se le asigna un titulo a la ventana

lb_principal = tk.Label(ventana_inicial, text = '''-------------------------------------------------------------------------------------
Bienvenido al Sistema de Administración del Tiempo del TEC
-------------------------------------------------------------------------------------''', **Estilos.STYLE).pack(side=TOP)               #se crea un label para el titulo

lb_instruccion = tk.Label(ventana_inicial, text='Seleccione su tipo de usuario:', **Estilos.LABELS).place(x = 20, y = 125)              #se crea un label para la indicar instruccion

sv_usuarios = tk.StringVar()                                                                                                            #se crea una variable para el tipo de usuario
comobo_usuarios1 = ttk.Combobox(ventana_inicial, textvariable=sv_usuarios)                                                              #se crea un combobox para el tipo de usuario
comobo_usuarios1['values'] = ["Administrador","Estudiante"]                                                                             #se le asigna una lista de valores a la variable
comobo_usuarios1['state'] = 'readonly'                                                                                                  #se le asigna un estado de solo lectura
comobo_usuarios1.place(x = 285, y = 130, width= 200, height=23)                                                                         #se le asigna una posicion y tamaño a la variable

boton_principal = tk.Button(ventana_inicial,    
                            text='Seleccionar', 
                            command=lambda:[usuarios_admin(),esconder(ventana_inicial)], 
                            **Estilos.BOTONES
                            ).place(x = 495, y = 128)                                                                                   #se crea un boton para seleccionar el tipo de usuario

#---------------------------------------------------------DATOS QUEMADOS---------------------------------------------------------

usuario_final = UsuariosAdmin('Kevin', 'Varela', 'Rojas', '64363005', '123', '123')                             #se crea un objeto de tipo usuario administrador
lista_usuarios_admin.append(usuario_final)

usuario_final = UsuariosEstudiante('Anthony', 'Jiménez', 'Zamora', '62713210', '12', '12')                      #se crea un objeto de tipo usuario estudiante
lista_usuarios_estudiantes.append(usuario_final)

actividad = actividades_class('Tarea #1', 'Hacer tarea de introducción', 'Introducción a la Programación', '13/6/2022', '13/6/2022', 'Lunes', 2, '22:40', '22:42','Pendiente')      #se crea un objeto de tipo actividad
lista_actividades.append(actividad)                                                                                                                                                 #se agrega el objeto a la lista de actividades
horas_dias[actividad.dia].append(actividad.horas_actividad)
actividad = actividades_class('Tarea #2', 'Hacer tarea de progra', 'Taller de Programacion', '13/6/2022', '13/6/2022', 'Lunes', 2, '22:44', '22:46','Pendiente')                   
lista_actividades.append(actividad)                                                                                                                                                
horas_dias[actividad.dia].append(actividad.horas_actividad)
actividad = actividades_class('Tarea #3', 'Hacer tarea de mate', 'Matematica Elemental', '13/6/2022', '13/6/2022', 'Lunes', 2, '22:48', '22:50','Pendiente')                       
lista_actividades.append(actividad)                                                                                                                                                 
horas_dias[actividad.dia].append(actividad.horas_actividad) 
actividad = actividades_class('Tarea #4', 'Hacer tarea de comunicación', 'Comunicación Escrita', '13/6/2022', '13/6/2022', 'Lunes', 2, '22:52', '22:54','Pendiente')                
lista_actividades.append(actividad)
horas_dias[actividad.dia].append(actividad.horas_actividad)
actividad = actividades_class('Tarea #5', 'Hacer tarea de inglés', 'Inglés I', '13/6/2022', '13/6/2022', 'Lunes', 2, '22:56', '22:58','Pendiente')
lista_actividades.append(actividad)
horas_dias[actividad.dia].append(actividad.horas_actividad)
actividad = actividades_class('Tarea #6', 'Hacer tarea de apreciacion', 'Apreciacion de Cine', '13/6/2022', '13/6/2022', 'Lunes', 2, '21:00', '21:02','Pendiente')
lista_actividades.append(actividad)
horas_dias[actividad.dia].append(actividad.horas_actividad)

programacion = curso_class('Programacion','4','5','06/01/2022','06/02/2022','Lunes','17:00','19:00')                            #se crea un objeto de tipo curso
cursos.append(programacion)
comunicacion = curso_class('Comunicacion','2','3','10/06/2022','10/07/2022','Martes','18:00','20:00')
cursos.append(comunicacion)
fundamentos = curso_class('Fundamentos','6','5','06/01/2022','06/02/2022','Miercoles','10:00','12:00')
cursos.append(fundamentos)
soldadura = curso_class('Soldadura','7','8','06/01/2022','06/02/2022','Jueves','13:00','15:00')
cursos.append(soldadura)

computacion = carrera_class('Computacion')                                                                                       #se crea un objeto de tipo carrera
carreras.append(computacion)
Ingenieria_electrica = carrera_class('Ingenieria Eléctrica')
carreras.append(Ingenieria_electrica)
computacion.agregar_curso(programacion)
computacion.agregar_curso(comunicacion)
Ingenieria_electrica.agregar_curso(comunicacion)

ventana_inicial.mainloop()                                                                          #se crea un loop para que la ventana se mantenga abierta            