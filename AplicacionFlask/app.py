from datetime import datetime
from flask import Flask, request, render_template
from flask_sqlalchemy import SQLAlchemy

app=Flask(__name__)
app.config.from_pyfile('config.py')

from models import db
from models import Trabajador, Registro

@app.route('/')
def inicio():
    return render_template('inicio.html')

#FUNCIONALIDAD 1
@app.route('/RegistroEntrada', methods= ['POST','GET'])
def registrar_entrada():
    if request.method == 'POST':

        if not request.form['legajo'] or not request.form['dni'] or not request.form['dep']:
            return render_template('error.html', error="Complete el formulario")
        
        trabajador_actual=Trabajador.query.filter(Trabajador.legajo==request.form['legajo'],Trabajador.dni.endswith(request.form['dni'])).first()

        if trabajador_actual:
            registro_existente=Registro.query.filter_by(idtrabajador=trabajador_actual.id,horasalida=None).first()

            if registro_existente:
                return render_template('error.html', error="El trabajador no registro su salida aun")
            
            else:
                registro_entrada= Registro(fecha=datetime.now().date(),horaentrada= datetime.now().time(),horasalida= None, dependencia= request.form['dep'], idtrabajador= trabajador_actual.id)
                db.session.add(registro_entrada)
                db.session.commit()
                return render_template('aviso.html', mensaje="Exito al registrar la entrada del trabajador")
        else:
            return render_template('error.html', error="El trabajador con los datos ingresados no se encuentra en el sistema")
    else:
        return render_template('formulario_entrada.html')

#FUNCIONALIDAD 2
@app.route('/RegistroSalida', methods= ['POST','GET'])
def registrar_salida():
    dep=""
    if request.method=='POST':

        if not request.form['legajo'] or not request.form['dni']:
            return render_template('error.html', error="Complete el formulario")
        
        trabajador_actual= Trabajador.query.filter(Trabajador.legajo==request.form['legajo'],Trabajador.dni.endswith(request.form['dni'])).first()

        if trabajador_actual:
            registro_existente=Registro.query.filter(Registro.idtrabajador==trabajador_actual.id,Registro.horasalida==None).first()
            
            if registro_existente:
                return render_template('confirmar_salida.html',registro= registro_existente,dep=registro_existente.dependencia)
            else:
                return render_template('error.html', error="El trabajador con esos datos no tiene una entrada en la fecha actual")
        else:
            return render_template('error.html', error="El trabajador con esos datos no esta registrado en el sistema") 
    else:
        return render_template('formulario_salida.html')
    
@app.route('/ConfirmarSalida/<int:id_registro>', methods=['POST'])
def confirmar_salida(id_registro):
    registro_actual= Registro.query.get(id_registro)
    if registro_actual:
        registro_actual.horasalida=datetime.now().time()
        db.session.commit()
        return render_template('aviso.html', mensaje="Salida registrada exitosamente")

#FUNCIONALIDAD 3
@app.route('/ConsultarHorarioPropio', methods= ['POST','GET'])
def consultar_horario_propio():
    if request.method=='POST':
        
        if not request.form['legajo'] or not request.form['dni'] or not request.form['fecha_in'] or not request.form['fecha_fn']:
            return render_template('error.html', error="Complete el formulario")
        
        trabajador_actual=Trabajador.query.filter(Trabajador.dni.endswith(request.form['dni']),Trabajador.legajo==request.form['legajo']).first()
        
        if trabajador_actual:

            registro=Registro.query.filter_by(idtrabajador=trabajador_actual.id).filter(Registro.fecha.between(request.form['fecha_in'],request.form['fecha_fn'])).order_by(Registro.fecha).all()   #Busca los registros del trabajador en cuestion, entre las fechas dadas, y los ordena segun estas.
            return render_template('listar_registros.html', registros= registro, id=trabajador_actual.id)
        else:
            return render_template('error.html', error="El trabajador con los datos ingresados no se encontro")
    else:
        return render_template('con_horario_propio.html')

if __name__=='__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)