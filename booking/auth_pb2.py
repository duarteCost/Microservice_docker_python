# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: auth.proto

import sys
_b=sys.version_info[0]<3 and (lambda x:x) or (lambda x:x.encode('latin1'))
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
from google.protobuf import descriptor_pb2
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor.FileDescriptor(
  name='auth.proto',
  package='',
  syntax='proto3',
  serialized_pb=_b('\n\nauth.proto\"\x17\n\x06UserId\x12\r\n\x05value\x18\x01 \x01(\t\"\x1a\n\tAuthToken\x12\r\n\x05value\x18\x01 \x01(\t\"#\n\x12GeneratedAuthToken\x12\r\n\x05value\x18\x01 \x01(\t\"\x18\n\x07Payload\x12\r\n\x05value\x18\x01 \x01(\t2f\n\x04\x41uth\x12*\n\x11\x63reate_auth_token\x12\x07.UserId\x1a\n.AuthToken\"\x00\x12\x32\n\x0fread_auth_token\x12\x13.GeneratedAuthToken\x1a\x08.Payload\"\x00\x62\x06proto3')
)




_USERID = _descriptor.Descriptor(
  name='UserId',
  full_name='UserId',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='value', full_name='UserId.value', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=14,
  serialized_end=37,
)


_AUTHTOKEN = _descriptor.Descriptor(
  name='AuthToken',
  full_name='AuthToken',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='value', full_name='AuthToken.value', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=39,
  serialized_end=65,
)


_GENERATEDAUTHTOKEN = _descriptor.Descriptor(
  name='GeneratedAuthToken',
  full_name='GeneratedAuthToken',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='value', full_name='GeneratedAuthToken.value', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=67,
  serialized_end=102,
)


_PAYLOAD = _descriptor.Descriptor(
  name='Payload',
  full_name='Payload',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='value', full_name='Payload.value', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=104,
  serialized_end=128,
)

DESCRIPTOR.message_types_by_name['UserId'] = _USERID
DESCRIPTOR.message_types_by_name['AuthToken'] = _AUTHTOKEN
DESCRIPTOR.message_types_by_name['GeneratedAuthToken'] = _GENERATEDAUTHTOKEN
DESCRIPTOR.message_types_by_name['Payload'] = _PAYLOAD
_sym_db.RegisterFileDescriptor(DESCRIPTOR)

UserId = _reflection.GeneratedProtocolMessageType('UserId', (_message.Message,), dict(
  DESCRIPTOR = _USERID,
  __module__ = 'auth_pb2'
  # @@protoc_insertion_point(class_scope:UserId)
  ))
_sym_db.RegisterMessage(UserId)

AuthToken = _reflection.GeneratedProtocolMessageType('AuthToken', (_message.Message,), dict(
  DESCRIPTOR = _AUTHTOKEN,
  __module__ = 'auth_pb2'
  # @@protoc_insertion_point(class_scope:AuthToken)
  ))
_sym_db.RegisterMessage(AuthToken)

GeneratedAuthToken = _reflection.GeneratedProtocolMessageType('GeneratedAuthToken', (_message.Message,), dict(
  DESCRIPTOR = _GENERATEDAUTHTOKEN,
  __module__ = 'auth_pb2'
  # @@protoc_insertion_point(class_scope:GeneratedAuthToken)
  ))
_sym_db.RegisterMessage(GeneratedAuthToken)

Payload = _reflection.GeneratedProtocolMessageType('Payload', (_message.Message,), dict(
  DESCRIPTOR = _PAYLOAD,
  __module__ = 'auth_pb2'
  # @@protoc_insertion_point(class_scope:Payload)
  ))
_sym_db.RegisterMessage(Payload)



_AUTH = _descriptor.ServiceDescriptor(
  name='Auth',
  full_name='Auth',
  file=DESCRIPTOR,
  index=0,
  options=None,
  serialized_start=130,
  serialized_end=232,
  methods=[
  _descriptor.MethodDescriptor(
    name='create_auth_token',
    full_name='Auth.create_auth_token',
    index=0,
    containing_service=None,
    input_type=_USERID,
    output_type=_AUTHTOKEN,
    options=None,
  ),
  _descriptor.MethodDescriptor(
    name='read_auth_token',
    full_name='Auth.read_auth_token',
    index=1,
    containing_service=None,
    input_type=_GENERATEDAUTHTOKEN,
    output_type=_PAYLOAD,
    options=None,
  ),
])
_sym_db.RegisterServiceDescriptor(_AUTH)

DESCRIPTOR.services_by_name['Auth'] = _AUTH

# @@protoc_insertion_point(module_scope)
