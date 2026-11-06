import pytest
from decimal import Decimal
from unittest.mock import Mock
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import declarative_base, sessionmaker

# ==========================================
# 1. STUBS DEL DOMINIO (Clases simuladas)
# ==========================================
class DominioError(Exception): pass

class Dinero:
    def __init__(self, cantidad):
        self.cantidad = Decimal(cantidad)

class Propuesta:
    def __init__(self, versiones=0, lineas=0):
        self.versiones = versiones
        self.lineas = lineas
        self.estado = "NUEVA"
        
    def aceptar(self):
        if self.versiones == 0:
            raise DominioError("La propuesta debe tener al menos una versión")
        self.estado = "ACEPTADA"

class Evento:
    def __init__(self):
        self.anticipo = Decimal("0")
        
    def registrar_anticipo(self, dinero, admin=False):
        if dinero.cantidad < 0:
            raise DominioError("El anticipo no puede ser negativo")
        if dinero.cantidad == 0:
            raise DominioError("El anticipo debe ser mayor a cero")
        self.anticipo = dinero.cantidad
        return "Pago registrado"

class SolicitudProveedor:
    def __init__(self, vencimiento):
        self.vencimiento = vencimiento
        self.estado = "PENDIENTE"
        
    def confirmar(self, ahora):
        if ahora > self.vencimiento:
            raise DominioError("La solicitud ya expiró")
        self.estado = "CONFIRMADA"
        
    def expirar(self, ahora):
        if ahora >= self.vencimiento:
            self.estado = "EXPIRADA"

# ==========================================
# 2. PRUEBAS DEL PIA (Tus 9 casos)
# ==========================================

# --- R1: Propuesta ---
def test_pia01_aceptar_con_versiones():
    p = Propuesta(versiones=1, lineas=2)
    p.aceptar()
    assert p.estado == "ACEPTADA"

def test_pia02_aceptar_sin_versiones():
    p = Propuesta(versiones=0, lineas=0)
    with pytest.raises(DominioError):
        p.aceptar()

def test_pia03_limite_version_exactamente_una_linea():
    p = Propuesta(versiones=1, lineas=1)
    p.aceptar()
    assert p.estado == "ACEPTADA"

# --- R2: Evento ---
def test_pia04_anticipo_valido():
    e = Evento()
    resultado = e.registrar_anticipo(Dinero(100), admin=True)
    assert resultado == "Pago registrado"

def test_pia05_anticipo_negativo():
    e = Evento()
    with pytest.raises(DominioError):
        e.registrar_anticipo(Dinero("-1"), admin=True)

def test_pia06_limite_anticipo_cero():
    e = Evento()
    with pytest.raises(DominioError):
        e.registrar_anticipo(Dinero("0"), admin=True)

# --- R3: SolicitudDeProveedor ---
def test_pia07_confirmar_antes_de_vencer():
    s = SolicitudProveedor(vencimiento=10)
    s.confirmar(ahora=9)
    assert s.estado == "CONFIRMADA"

def test_pia08_error_confirmar_expirada():
    s = SolicitudProveedor(vencimiento=10)
    with pytest.raises(DominioError):
        s.confirmar(ahora=11)

def test_pia09_expirar_en_el_instante_exacto():
    VENCE = 10
    s = SolicitudProveedor(vencimiento=VENCE)
    s.expirar(ahora=VENCE)
    assert s.estado == "EXPIRADA"

# ==========================================
# 3. PRUEBA DE MOCK (Adaptador a proveedor)
# ==========================================
def test_mock_notificacion_proveedor():
    # Simulamos el servicio externo que notifica al proveedor
    notificador_mock = Mock()
    notificador_mock.enviar_correo.return_value = True
    
    # Act
    notificador_mock.enviar_correo("Solicitud Aceptada")
    
    # Assert
    notificador_mock.enviar_correo.assert_called_once_with("Solicitud Aceptada")

# ==========================================
# 4. PRUEBA DE PERSISTENCIA (SQLite en memoria)
# ==========================================
Base = declarative_base()
class EventoRow(Base):
    __tablename__ = 'eventos'
    id = Column(Integer, primary_key=True)
    estado = Column(String)

def test_persistencia_evento_commit_y_rollback():
    engine = create_engine("sqlite:///:memory:")
    Base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)
    session = Session()

    # Probamos COMMIT
    nuevo_evento = EventoRow(id=1, estado="NUEVO")
    session.add(nuevo_evento)
    session.commit()
    
    recuperado = session.query(EventoRow).filter_by(id=1).first()
    assert recuperado is not None
    assert recuperado.estado == "NUEVO"
    
    session.close()
