#!/usr/bin/env python
# -*- coding: utf-8 -*-

from pprint import pprint


class DatabasePut:
    # --------------------------------
    # one
    # --------------------------------
    # Atualiza um documento na base de dados
    @staticmethod
    def one(dbPrepare):
        # Recupera a coleção principal
        collection = dbPrepare.collection()

        # Recupera dados e configurações
        db_data = dbPrepare.body()
        db_fields = dbPrepare.fieldsUpdate()
        db_filter = dbPrepare.filter()

        # Realiza busca na colecção para recuperar documentos que serão atualizados
        find_result = collection.find(db_filter, db_fields)
        find_result_count = find_result.count()

        # Verifica se existe documentos para serem atualizados
        update_count = 0
        if find_result_count > 0:
            # Recupera a coleção changes
            collection_changes = dbPrepare.collection_changes()

            # Grava os documentos localizados na coleção trash
            update_filter, update_data = DatabasePut.changes(dbPrepare, find_result)

            print "UPDATE_FILTER", update_filter, "UPDATE_DATA->"
            pprint(update_data)

            inserted_id = collection_changes.update(update_filter, update_data, upsert=True)
            print "inserted_id", inserted_id

            # Verifica se foi inserido documento na coleção _changes
            if inserted_id:
                # Atualiza os documentos da coleção principal
                update_result = collection.update_many(db_filter, db_data, upsert=True)
                update_count = update_result.modified_count

        #TODO:: Corrigir retorna de data, está voltando NULL

        return {
            "id": dbPrepare.id(),
            "response": {
                "operation": "putOne",
                "success": True,
                "data": find_result,
                "totals": update_count
            }
        }

    # --------------------------------
    # many
    # --------------------------------
    # Atualiza um documento na base de dados
    @staticmethod
    def many(dbPrepare):
        # Recupera a coleção principal
        collection = dbPrepare.collection()

        # Recupera dados e configurações
        db_data = dbPrepare.body()
        db_fields = dbPrepare.fieldsUpdate()
        db_filter = dbPrepare.filter()

        # Realiza busca na colecção para recuperar documentos que serão atualizados
        find_result = collection.find(db_filter, db_fields)
        find_result_count = find_result.count()

        # Verifica se existe documentos para serem atualizados
        update_count = 0
        if find_result_count > 0:
            # Recupera a coleção changes
            collection_changes = dbPrepare.collection_changes()

            # Grava os documentos localizados na coleção trash
            update_filter, update_data = DatabasePut.changes(dbPrepare, find_result)

            print "UPDATE_FILTER", update_filter, "UPDATE_DATA->"
            pprint(update_data)

            inserted_id = collection_changes.update(update_filter, update_data, upsert=True)
            print "inserted_id", inserted_id

            # Verifica se foi inserido documento na coleção _changes
            if inserted_id:
                # Atualiza os documentos da coleção principal
                update_result = collection.update_many(db_filter, db_data, upsert=True)
                update_count = update_result.modified_count

        return {
            "id": dbPrepare.id(),
            "response": {
                "operation": "putMany",
                "success": True,
                "data": find_result,
                "totals": update_count
            }
        }

    # --------------------------------
    # changes
    # --------------------------------
    @staticmethod
    def changes(dbPrepare, data):
        data = (list(data)[0])
        id = dbPrepare.info_update(data)
        return {"_id": id}, {
            "$set": {"_id": id, "data": data},
            "$inc": {"total_occurrences": 1}
        }
