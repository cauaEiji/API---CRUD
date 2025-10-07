from marshmallow import Schema, fields, validate, EXCLUDE

class BaseSchema(Schema):
    class Meta:
        unknown = EXCLUDE 

class AuthSchema(BaseSchema):
    username = fields.Str(
        required=True, 
        validate=validate.Length(min=3, max=80),
        error_messages={"required": "O campo 'username' é obrigatório."}
    )
    password = fields.Str(
        required=True, 
        validate=validate.Length(min=6),
        error_messages={"required": "O campo 'password' é obrigatório."}
    )

class CategoriaSchema(BaseSchema):
    nome = fields.Str(
        required=True, 
        validate=validate.Length(min=1, max=120), 
        error_messages={"required": "O nome da categoria é obrigatório."}
    )
    descricao = fields.Str(required=False, allow_none=True) 

class DispositivoSchema(BaseSchema):
    nome = fields.Str(
        required=True, 
        validate=validate.Length(min=1, max=140),
        error_messages={"required": "O nome do dispositivo é obrigatório."}
    )
    serial = fields.Str(
        required=True, 
        validate=validate.Length(min=1, max=140),
        error_messages={"required": "O serial do dispositivo é obrigatório."}
    )
    status = fields.Str(
        required=False,
        validate=validate.OneOf(
            choices=["ativo", "inativo"],
            error="Status deve ser 'ativo' ou 'inativo'."
        )
    )
    categoria_id = fields.Int(
        required=False, 
        allow_none=True 
    )