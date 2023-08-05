#!/usr/bin/env python
# -*- coding: utf-8 -*-

from pprint import pprint


class DatabasePost:
    # --------------------------------
    # post_one
    # --------------------------------
    # Insere um ou muitos documentos na base de dados
    @staticmethod
    def post_one(dbPrepare):
        # Recupera a coleção principal
        collection = dbPrepare.collection()

        # Recupera dados e configurações
        db_data = dbPrepare.body()
        db_data = dbPrepare.info(db_data)
        db_fields = dbPrepare.fields()

        print "DB_DATA POST ONE:::--->>>"
        pprint(db_data)

        # Insere documentos na base de dados e recupera a lista dos identificadores dos documentos inseridos
        db_data['_id'] = collection.insert_one(db_data).inserted_id

        # Registra o total de elementos encontrados para retornar ao cliente
        totals = {
            "count": 1
        }

        links = {
            "self": "https://api.predicthq.com/v1/endpoint/?offset=0&limit=10"
        }

        # Prepara configurações que serão retornadas para o cliente
        return DatabasePost.response("postOne", True, dbPrepare, db_data, db_fields, totals, links)

    # --------------------------------
    # post_many
    # --------------------------------
    # Insere um ou muitos documentos na base de dados
    @staticmethod
    def post_many(dbPrepare):
        # Recupera a coleção principal
        collection = dbPrepare.collection()

        # Recupera dados e configurações
        db_data = dbPrepare.body()
        db_data = dbPrepare.info(db_data)
        db_fields = dbPrepare.fields()

        # Verifica o tipo de dados
        if type(db_data) == dict and len(db_data.keys()) > 0:
            db_data = [db_data]

        print "DB_DATA POST MANY:::--->>>"
        pprint(db_data)

        # Verifica se tem dados para inseretir na base de dados
        if len(db_data) > 0:
            # Insere documentos na base de dados e recupera a lista dos identificadores dos documentos inseridos
            insert_many_result = collection.insert_many(db_data).inserted_ids

            # Verifica se algum documento foi inserido
            if len(insert_many_result) > 0:
                # Prepara filtro para recuperar lista de documentos inseridos
                db_filter = {"_id": {"$in": insert_many_result}}

                # Realiza consulta na base de dados e recupera a lista de documentos inseridos
                find_result = collection.find(db_filter, projection=db_fields)

                # Registra o total de elementos encontrados para retornar ao cliente
                totals = {
                    "count": find_result.count()
                }

                links = {
                    "previous": None,
                    "next": "https://api.predicthq.com/v1/endpoint/?offset=10&limit=10",
                    "self": "https://api.predicthq.com/v1/endpoint/?offset=0&limit=10"
                }

                # Prepara configurações que serão retornadas para o cliente
                return DatabasePost.response("postMany", True, dbPrepare, find_result, db_fields, totals, links)
        else:
            # Em caso de erros por fata de documentos para inserir na base de dados ou qualquer outra falha no momento da inserção
            # registra mensagem de erro e configura a flha na operação
            # self.status.error("NO_DATA_TO_INSERT", None, ['AAAAA'])

            data = []
            totals = {
                "count": 0
            }
            links = {
                "previous": None,
                "next": "https://api.predicthq.com/v1/endpoint/?offset=10&limit=10",
                "self": "https://api.predicthq.com/v1/endpoint/?offset=0&limit=10"
            }

            # Prepara configurações que serão retornadas para o cliente
            return DatabasePost.response("postMany", False, dbPrepare, data, db_fields, totals, links)

    @staticmethod
    def response(operation, success, dbPrepare, data, fields, totals, links):
        result = {
            "id": dbPrepare.id(),
            "response": {
                "operation": operation,
                "success": success,
                "data": data,
                "totals": totals
            }
        }

        if dbPrepare.show_fields() or dbPrepare.show_links():
            result["response"]["query"] = {}

            if dbPrepare.show_fields() == True:
                result["response"]["query"]["fields"] = fields

            if dbPrepare.show_links() == True and len(links) > 0:
                result["response"]["query"]["links"] = links

        return result
