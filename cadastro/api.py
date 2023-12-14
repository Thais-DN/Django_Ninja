from ninja import ModelSchema, NinjaAPI, Schema, UploadedFile
from .models import Livro
import json
from django.shortcuts import get_object_or_404
from django.forms.models import model_to_dict

import orjson
from ninja.parser import Parser
from django.http import HttpRequest

class ORJSONParser(Parser):
    def parse_body(self, request: HttpRequest):
        return orjson.loads(request.body)

api = NinjaAPI(parser=ORJSONParser())

@api.get('livro/')
def listar(request):
    livro = Livro.objects.all()
    response = [{'id': i.id, 'titulo': i.titulo, 'descricao': i.descricao, 'autor': i.autor} for i in livro]
    return response
  
@api.get('livro/{id}')
def listar_livro(request, id:int):
    livro = get_object_or_404(Livro, id=id)
    return model_to_dict(livro)

@api.get('livro_consulta/')
def listar_consultar(request, id: int = 1):
    livro = get_object_or_404(Livro, id=id)
    return model_to_dict(livro)

'''class LivroSchema(Schema):
    titulo: str
    descricao: str
    autor: str = None'''

class LivroSchema(ModelSchema):
    class Config:
        model = Livro
        model_fields = "__all__"
    
# from typing import List
# livro: List [LivroSchema]

@api.post('livro', response=LivroSchema)
def livro_criar(request, livro: LivroSchema):
    l1 = livro.dict()
    livro = Livro(**l1)
    livro.save()
    return livro

@api.post('/file')
def file_upload(request, file: UploadedFile):
    print(file.size)
    return 1