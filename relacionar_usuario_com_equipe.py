# será acionada quando o usuário for adicionado/removido da equipe
# pois não tem um endpoint que o usuário possa saber quais suas poermissões dentro daquela equipe
# https://github.com/appwrite/appwrite/issues/3046


import json
from appwrite.client import Client
from appwrite.services.databases import Databases


# appwrite functions createDeployment --functionId=relacionar_usuario_com_equipe --activate=true --entrypoint="relacionar_usuario_com_equipe.py" --code="."



# essa função já está protegida pelos papeis team:admin/owner
def main(request, response):
    if request.variables.get('host', '') == '':
        return response.send('coloque o host nas variáveis', 500)
    if request.variables.get('projeto', '') == '':
        return response.send('coloque o projeto nas variáveis', 500)
    if request.variables.get('key', '') == '':
        return response.send('coloque o key nas variáveis', 500)
    if request.variables.get('db', '') == '':
        return response.send('coloque o db nas variáveis', 500)
    database_id = request.variables.get('db', '')

    client = Client()
    client.set_endpoint(request.variables.get('host', ''))
    client.set_project(request.variables.get('projeto', ''))
    client.set_key(request.variables.get('key', ''))
    database = Databases(client)

    # data = json.loads(request.payload or "{}")
    # if len(data) == 0:
    data = json.loads(request.variables['APPWRITE_FUNCTION_EVENT_DATA'] or "{}")

    evento = request.variables['APPWRITE_FUNCTION_EVENT']


    def created():
        database.create_document(database_id, collection_id='usuario_equipes', document_id=data['$id'],
                                 data={
                                     'user_id': data['userId'],
                                     'equipe_id': data['teamId'],
                                     'papeis': data['roles']
                                 }
                                 )
        return response.json(data)

    def updated():
        database.update_document(database_id, collection_id='usuario_equipes', document_id=data['$id'],
                                 data={
                                     'papeis': data['roles']
                                 }
                                 )
        return response.json(data)



    if '.create' in evento:
        try:
            created()
        except:
            updated()

    if '.update' in evento:
        try:
            updated()
        except:
            created()


    if '.delete' in evento:
        database.delete_document(database_id, collection_id='usuario_equipes', document_id=data['$id'])
        return response.json({})
