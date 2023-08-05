#!/usr/bin/env python
# -*- coding: utf-8 -*-

from pprint import pprint
from convert import Convert


class DatabaseDelete:
    # --------------------------------
    # one
    # --------------------------------
    # Insere um ou muitos documentos na base de dados
    @staticmethod
    def one(dbPrepare):
        # Recupera a coleção principal
        collection = dbPrepare.collection()

        # Recupera dados e configurações
        db_filter = dbPrepare.filter()

        # Realiza busca na colecção para recuperar documentos que serão atualizados
        find_result = collection.find(db_filter)
        find_count = find_result.count()

        print "REMOVE ONE:::--->>>"

        # Verifica se existe documentos para serem removidos
        deleted_count = 0
        deleted_ids = []

        if find_count > 0:
            # Recupera a coleção trash
            collection_trash = dbPrepare.collection_trash()

            # Grava os documentos localizados na coleção trash
            insert_data_trash, deleted_ids = DatabaseDelete.trash(find_result)
            insert_many_result = collection_trash.insert_many(insert_data_trash).inserted_ids

            # Verifica se foi inserido documento na coleção trash
            if len(insert_many_result) > 0:
                # Atualiza os documentos da coleção principal
                delete_result = collection.delete_many(db_filter)
                deleted_count = delete_result.deleted_count

                # Verifica se os documentos não foram atualizados
                if deleted_count == 0:
                    # Remove itens inseridos na tabela trash
                    collection_trash.delete_many({"_id": {"$in": insert_many_result}})

        # Prepara configurações que serão retornadas para o cliente
        return {
            "id": dbPrepare.id(),
            "response": {
                "operation": "deleteOne",
                "success": True,
                "deleted_ids": deleted_ids,
                "totals": deleted_count,
                "query": {
                    "filter": db_filter
                }
            }
        }

    # --------------------------------
    # many
    # --------------------------------
    # Remove um ou muitos documentos na base de dados
    @staticmethod
    def many(dbPrepare):
        # Recupera a coleção principal
        collection = dbPrepare.collection()

        # Recupera dados e configurações
        db_filter = dbPrepare.filter()

        # Realiza busca na colecção para recuperar documentos que serão atualizados
        find_result = collection.find(db_filter)
        find_count = find_result.count()

        print "REMOVE MANY:::--->>>"

        # Verifica se existe documentos para serem removidos
        deleted_count = 0
        deleted_ids = []

        if find_count > 0:
            # Recupera a coleção trash
            collection_trash = dbPrepare.collection_trash()

            # Grava os documentos localizados na coleção trash
            insert_data_trash, deleted_ids = DatabaseDelete.trash(find_result)
            insert_many_result = collection_trash.insert_many(insert_data_trash).inserted_ids

            # Verifica se foi inserido documento na coleção trash
            if len(insert_many_result) > 0:
                # Atualiza os documentos da coleção principal
                delete_result = collection.delete_many(db_filter)
                deleted_count = delete_result.deleted_count

                # Verifica se os documentos não foram atualizados
                if deleted_count == 0:
                    # Remove itens inseridos na tabela trash
                    collection_trash.delete_many({"_id": {"$in": insert_many_result}})

        # Prepara configurações que serão retornadas para o cliente
        return {
            "id": dbPrepare.id(),
            "response": {
                "operation": "deleteMany",
                "success": True,
                "deleted_ids": deleted_ids,
                "totals": deleted_count,
                "query": {
                    "filter": db_filter
                }
            }
        }

    # --------------------------------
    # trash
    # --------------------------------
    @staticmethod
    def trash(data):
        # Retirar list de ids que foram removidos da base de dados
        deleted_ids = []
        insert_data_trash = []

        for item in data:
            deleted_ids.append(Convert.to_str(item["_id"]))
            insert_data_trash.append({
                "data": item
                # "_info": self.dbPrepare.info(item)
            })
        return insert_data_trash, deleted_ids
