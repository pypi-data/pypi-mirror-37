rule_dict = {'python_tx': """TreeModel:
    imports+=Import
    nodes+=Node
;

Import:
    'from' /[a-zA-Z0-9_.]*/ 'import *'
;

Node:
    handler=ID'='name=ID'()'
    properties*=Property
    (ID'.'func=Func'()')?
;

Property:
    Single | Nested
;

Single:
    ID'.'key=ID '=' value=Value
;

Nested:
    ID'.'ID'.'key=ID '=' value=Value
;

Value:
    name=STRING
;

Func:
    'show' | 'check'
;

Comment:
    /#.*$/
;
""", 'json_tx': """/*
    A grammar for JSON data-interchange format.
    See: http://www.json.org/
*/
File:
    Array | Object
;

Array:
    "[" values*=Value[','] "]"
;

Value:
    STRING | FLOAT | BOOL | Object | Array | "null"
;

Object:
    "{" nodes*=Member[','] "}"
;

Member:
    key=STRING ':' value=Value
;
""", 'pipeline_tx': """/*
    A grammar for JSON data-interchange format.
    See: http://www.json.org/
*/
File:
    Array | Object
;

Array:
    "[" values*=Value[','] "]"
;

Value:
    STRING | FLOAT | BOOL | Object | Array | "null"
;

Object:
    "{" nodes*=Member[','] "}"
;

Member:
    key=STRING ':' value=Value
;
"""
             }
