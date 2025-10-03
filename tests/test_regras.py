import pytest
import json
from app import create_app
from extensions import db
from models import User, Categoria, Dispositivo

@pytest.fixture
def client():
    app = create_app()
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:' 
    app.config['JWT_SECRET_KEY'] = 'teste-secret' 
    
    with app.test_client() as client:
      
        with app.app_context():
            db.create_all()

        yield client
        with app.app_context():
            db.drop_all()

@pytest.fixture
def auth_header(client):

    client.post('/auth/register', json={'username': 'testuser', 'password': 'password'})
    
    response = client.post('/auth/login', json={'username': 'testuser', 'password': 'password'})
    token = response.get_json()['access_token']

    return {'Authorization': f'Bearer {token}'}



def test_delete_categoria_com_dispositivo_vinculado(client, auth_header):

    response_cat = client.post('/categorias', json={'nome': 'Servidores', 'descricao': 'Servidores de aplicação'}, headers=auth_header)
    assert response_cat.status_code == 201
    categoria_id = response_cat.get_json()['id']
 
    response_dev = client.post('/dispositivos', json={'nome': 'Server 01', 'serial': 'SRV-001', 'categoria_id': categoria_id}, headers=auth_header)
    assert response_dev.status_code == 201

    response_delete = client.delete(f'/categorias/{categoria_id}', headers=auth_header)

    assert response_delete.status_code == 400
    assert "Não é possível excluir" in response_delete.get_json()['msg']

def test_create_dispositivo_serial_duplicado(client, auth_header):

    client.post('/dispositivos', json={'nome': 'Switch 1', 'serial': 'SW-001'}, headers=auth_header)

    response_fail = client.post('/dispositivos', json={'nome': 'Switch 2', 'serial': 'SW-001'}, headers=auth_header)

    assert response_fail.status_code == 409
    assert "Dispositivo com este serial já existe" in response_fail.get_json()['msg']