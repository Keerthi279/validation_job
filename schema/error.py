from marshmallow import Schema, fields


class ErrorsSchema(Schema):
    # "json" contains the field-specific errors
    json = fields.Dict(
        keys=fields.String(),
        values=fields.List(fields.String()),
        required=True
    )


class ErrorResponse422Schema(Schema):
    errors = fields.Nested(ErrorsSchema, required=True)
    status = fields.Str(required=True)


class ErrorResponseSchema(Schema):
    errors = fields.Str(required=True)
