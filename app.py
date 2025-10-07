from flask import Flask, request, jsonify
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from sqlalchemy import desc, asc, or_
from flask_cors import CORS
from marshmallow import ValidationError # <--- NOVO: Importar para tratamento de erros
from config import Config
from extensions import db, migrate, jwt
from models import User, Categoria, Dispositivo
# ASSUMIDA A CRIAÇÃO DO arquivo schemas.py
from schemas import AuthSchema, CategoriaSchema, DispositivoSchema # <--- NOVO: Importar Schemas


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # Habilita CORS
    CORS(app)

    db.init_app(app)
    migrate.init_app(app, db)
    jwt.init_app(app)

    @app.route("/")
    def index():
        return {"message": "API de Gerenciamento de Dispositivos iniciada com sucesso!"}

    # Função auxiliar para padronizar o retorno de erro de validação
    def handle_validation_error(e):
        # O Marshmallow retorna um dicionário de erros
        return jsonify({"msg": "Erro de validação", "errors": e.messages}), 400

    # ---------- ROTAS DE AUTENTICAÇÃO ----------
    @app.route("/auth/register", methods=["POST"])
    def register():
        data = request.get_json() or {}
        
        try:
            # NOVO: Validação de entrada usando Marshmallow
            validated_data = AuthSchema().load(data)
        except ValidationError as err:
            return handle_validation_error(err)

        username = validated_data.get("username")
        password = validated_data.get("password")

        if User.query.filter_by(username=username).first():
            return jsonify({"msg": "Nome de usuário já existe"}), 409

        user = User(username=username)
        user.set_password(password)
        db.session.add(user)
        db.session.commit()

        return jsonify({"msg": "Usuário criado com sucesso"}), 201

    @app.route("/auth/login", methods=["POST"])
    def login():
        data = request.get_json() or {}
        
        try:
            # NOVO: Validação de entrada usando Marshmallow
            validated_data = AuthSchema().load(data)
        except ValidationError as err:
            return handle_validation_error(err)

        username = validated_data.get("username")
        password = validated_data.get("password")

        user = User.query.filter_by(username=username).first()

        if user and user.check_password(password):
            access_token = create_access_token(identity=str(user.id))
            return jsonify(access_token=access_token), 200

        return jsonify({"msg": "Credenciais inválidas"}), 401

    # ---------- CRUD DE CATEGORIAS ----------
    @app.route("/categorias", methods=["POST"])
    @jwt_required()
    def create_categoria():
        data = request.get_json() or {}
        
        try:
            # NOVO: Validação de entrada usando Marshmallow
            validated_data = CategoriaSchema().load(data)
        except ValidationError as err:
            return handle_validation_error(err)

        nome = validated_data.get("nome")
        descricao = validated_data.get("descricao", "")

        if Categoria.query.filter_by(nome=nome).first():
            return jsonify({"msg": "Categoria com este nome já existe"}), 409

        new_categoria = Categoria(nome=nome, descricao=descricao)
        db.session.add(new_categoria)
        db.session.commit()

        return jsonify(new_categoria.to_dict()), 201

    @app.route("/categorias", methods=["GET"])
    @jwt_required()
    def list_categorias():
        categorias = Categoria.query.all()
        return jsonify([cat.to_dict() for cat in categorias]), 200

    @app.route("/categorias/<int:id>", methods=["GET"])
    @jwt_required()
    def get_categoria(id):
        categoria = Categoria.query.get_or_404(id)
        return jsonify(categoria.to_dict()), 200

    @app.route("/categorias/<int:id>", methods=["PUT", "PATCH"])
    @jwt_required()
    def update_categoria(id):
        categoria = Categoria.query.get_or_404(id)
        data = request.get_json() or {}
        
        try:
            # NOVO: Validação de entrada. Usamos partial=True para permitir que campos obrigatórios (nome) sejam omitidos no PATCH.
            validated_data = CategoriaSchema().load(data, partial=True)
        except ValidationError as err:
            return handle_validation_error(err)

        nome = validated_data.get("nome")
        descricao = validated_data.get("descricao")

        if nome:
            if nome != categoria.nome and Categoria.query.filter_by(nome=nome).first():
                return jsonify({"msg": "Categoria com este nome já existe"}), 409
            categoria.nome = nome

        # Verificação se a descrição foi explicitamente enviada (pode ser None)
        if 'descricao' in validated_data:
            categoria.descricao = descricao

        db.session.commit()
        return jsonify(categoria.to_dict()), 200

    @app.route("/categorias/<int:id>", methods=["DELETE"])
    @jwt_required()
    def delete_categoria(id):
        categoria = Categoria.query.get_or_404(id)

        if categoria.dispositivos.count() > 0:
            return jsonify({"msg": "Não é possível excluir a categoria, pois existem dispositivos vinculados."}), 400

        db.session.delete(categoria)
        db.session.commit()
        return '', 204

    # ---------- CRUD DE DISPOSITIVOS ----------
    @app.route("/dispositivos", methods=["POST"])
    @jwt_required()
    def create_dispositivo():
        data = request.get_json() or {}
        
        try:
            # NOVO: Validação de entrada usando Marshmallow. 'nome' e 'serial' são obrigatórios.
            validated_data = DispositivoSchema().load(data)
        except ValidationError as err:
            return handle_validation_error(err)

        nome = validated_data.get("nome")
        serial = validated_data.get("serial")
        categoria_id = validated_data.get("categoria_id")
        status = validated_data.get("status", "ativo")

        if Dispositivo.query.filter_by(serial=serial).first():
            return jsonify({"msg": "Dispositivo com este serial já existe."}), 409

        if categoria_id is not None and not Categoria.query.get(categoria_id):
            return jsonify({"msg": "Categoria_id inválida."}), 400

        dispositivo = Dispositivo(
            nome=nome,
            serial=serial,
            categoria_id=categoria_id,
            status=status
        )
        db.session.add(dispositivo)
        db.session.commit()
        return jsonify(dispositivo.to_dict()), 201

    @app.route("/dispositivos", methods=["GET"])
    @jwt_required()
    def list_dispositivos():
        page = request.args.get('page', 1, type=int)
        limit = request.args.get('limit', 10, type=int)
        sort = request.args.get('sort', 'id', type=str)
        order = request.args.get('order', 'asc', type=str)
        filter_status = request.args.get('status', type=str)
        filter_categoria = request.args.get('categoria_id', type=int)
        search_term = request.args.get('busca', type=str)

        query = Dispositivo.query

        if filter_status in ['ativo', 'inativo']:
            query = query.filter(Dispositivo.status == filter_status)

        if filter_categoria:
            query = query.filter(Dispositivo.categoria_id == filter_categoria)

        if search_term:
            search_pattern = f"%{search_term}%"
            query = query.filter(or_(
                Dispositivo.nome.ilike(search_pattern),
                Dispositivo.serial.ilike(search_pattern)
            ))

        sort_column = getattr(Dispositivo, sort, Dispositivo.id)
        if order.lower() == 'desc':
            query = query.order_by(desc(sort_column))
        else:
            query = query.order_by(asc(sort_column))

        paginated_result = query.paginate(page=page, per_page=limit, error_out=False)

        return jsonify({
            "items": [dev.to_dict() for dev in paginated_result.items],
            "pagination": {
                "total_records": paginated_result.total,
                "total_pages": paginated_result.pages,
                "current_page": paginated_result.page,
                "limit": paginated_result.per_page,
            }
        }), 200

    @app.route("/dispositivos/<int:id>", methods=["GET"])
    @jwt_required()
    def get_dispositivo(id):
        dispositivo = Dispositivo.query.get_or_404(id)
        return jsonify(dispositivo.to_dict()), 200

    @app.route("/dispositivos/<int:id>", methods=["PUT", "PATCH"])
    @jwt_required()
    def update_dispositivo(id):
        dispositivo = Dispositivo.query.get_or_404(id)
        data = request.get_json() or {}

        try:
            # NOVO: Validação de entrada. Usamos partial=True para permitir campos opcionais (PATCH).
            validated_data = DispositivoSchema().load(data, partial=True)
        except ValidationError as err:
            return handle_validation_error(err)
            
        nome = validated_data.get("nome")
        serial = validated_data.get("serial")
        categoria_id = validated_data.get("categoria_id")
        status = validated_data.get("status")

        if nome:
            dispositivo.nome = nome

        if status: # status já é validado no Schema ('ativo' ou 'inativo')
            dispositivo.status = status

        if serial:
            if serial != dispositivo.serial and Dispositivo.query.filter_by(serial=serial).first():
                return jsonify({"msg": "Serial já em uso."}), 409
            dispositivo.serial = serial

        if 'categoria_id' in validated_data: # Checa se a chave foi enviada (mesmo que seja null/None)
            if categoria_id is not None and not Categoria.query.get(categoria_id):
                return jsonify({"msg": "Categoria_id inválida."}), 400
            dispositivo.categoria_id = categoria_id

        db.session.commit()
        return jsonify(dispositivo.to_dict()), 200

    @app.route("/dispositivos/<int:id>", methods=["DELETE"])
    @jwt_required()
    def delete_dispositivo(id):
        dispositivo = Dispositivo.query.get_or_404(id)
        db.session.delete(dispositivo)
        db.session.commit()
        return '', 204

    return app


if __name__ == "__main__":
    app = create_app()
    app.run(host="0.0.0.0", port=5000, debug=True)