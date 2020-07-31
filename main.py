#!/usr/bin/env python3
#coding: utf-8
import argparse
import random

from sqlitedborm import db

def main():
    # Get arguments. Handle if none was informed.
    parser = argparse.ArgumentParser()
    parser.add_argument("action", choices=["demo", "create", "drop", "truncate", "select", "update", "delete", "insert", "search"])
    args = parser.parse_args()

    data = db.Database('testdata')

    if args.action == 'demo':
        print('demo')

    elif args.action == 'create':
        columns = []
        columns.append({'name': 'id', 'type': 'INTEGER', 'extra': ['PRIMARY KEY', 'AUTOINCREMENT', 'NOT NULL']})
        columns.append({'name': 'name', 'type': 'VARCHAR', 'size': 80, 'extra': ['NOT NULL']})
        columns.append({'name': 'address', 'type': 'VARCHAR', 'size': 80})
        columns.append({'name': 'created_at', 'type': 'DATETIME', 'default': "CURRENT_TIMESTAMP"})
        columns.append({'name': 'updated_at', 'type': 'DATETIME', 'default': "CURRENT_TIMESTAMP"})
        data.create('tb_contacts', columns)
        print('Tabela criada com sucesso.')

    elif args.action == 'drop':
        data.drop('tb_contacts')
        print('Tabela eliminada com sucesso.')

    elif args.action == 'truncate':
        data.truncate('tb_contacts')
        print('Tabela limpa com sucesso.')

    elif args.action == 'select':
        tbContacts = db.Table(data, 'tb_contacts')
        res = tbContacts.getAll()
        for row in res:
            print(row)

    elif args.action == 'update':
        tbContacts = db.Table(data, 'tb_contacts')
        res = tbContacts.getAll()
        for i, row in enumerate(res):
            record = f"{(i + 1)}. [{row['id']}] - {row['name']}"
            print(record)

        c = False
        while (not c):
            c = True
            q = input('Indique qual deseja alterar: ')
            try:
                q = int(q)
                if q not in list(range(1, len(res) + 1)):
                    c = False
            
            except ValueError:
                c = False

        row = res[q - 1]
        for col in row.keys():
            if col not in ['id', 'created_at', 'updated_at']:
                q = input(f'{col} ({row[col]}): ') or row[col]
                row[col] = q

        tbContacts.update(row).where({'id': row['id']}).exec()
        print('Registo atualizado com sucesso.')

    elif args.action == 'delete':
        tbContacts = db.Table(data, 'tb_contacts')
        res = tbContacts.getAll()
        for i, row in enumerate(res):
            record = f"{(i + 1)}. [{row['id']}] - {row['name']}"
            print(record)

        c = False
        while (not c):
            c = True
            q = input('Indique qual deseja eliminar: ')
            try:
                q = int(q)
                if q not in list(range(1, len(res) + 1)):
                    c = False
            
            except ValueError:
                c = False

        row = res[q - 1]
        tbContacts.delete().where({'id': row['id']}).exec()
        print('Registo eliminado com sucesso.')
    
    elif args.action == 'insert':
        first_names = ['João', 'Raquel', 'Luciano', 'Ana', 'José', 'Fernanda', 'Carlos', 'Paula']
        middle_names = ['Gomes', 'Ferreira', 'Paula', 'Assis', 'Aguiar', 'Marcos']
        last_names = ['da Silva', 'Neves', 'Rodrigues', 'Tavares', 'Fonseca']
        name = first_names[random.randint(0, len(first_names) - 1)]
        name += f' {middle_names[random.randint(0, len(middle_names) - 1)]}'
        name += f' {last_names[random.randint(0, len(last_names) - 1)]}'

        lograd = ['Rua', 'Avenida', 'Praceta', 'Estrada']
        ruas = ['Liberdade', 'Eugênio dos Santos', 'Argonautas', 'Fernão Lopes', 'Marginal', 'Fontes Pereira de Melo']
        andar = ['R/C'] + list(range(2, 9))
        fracao = ['Dto', 'Fte', 'Esq']
        cpost = f'{random.randint(1200, 4500)}-{random.randint(100, 999)}'
        city = ['Lisboa', 'Oeiras', 'Cascais', 'Porto', 'Setúbal', 'Faro', 'Braga', 'Viseu']

        address = lograd[random.randint(0, len(lograd) - 1)]
        address += f' {ruas[random.randint(0, len(ruas) - 1)]}'
        address += f' {random.randint(1, 100)}'
        address += f', {andar[random.randint(0, len(andar) - 1)]}'
        address += f' {fracao[random.randint(0, len(fracao) - 1)]}'
        address += f', {cpost}'
        address += f' {city[random.randint(0, len(city) - 1)]}'

        contact = {'name': name, 'address': address}
        tbContacts = db.Table(data, 'tb_contacts')
        tbContacts.insert(contact).exec()
        print('Registo inserido com sucesso.')

    elif args.action == 'search':
        q = input('Indique o nome ou parte dele: ')

        tbContacts = db.Table(data, 'tb_contacts')
        res = tbContacts.select('id, name').whereLike({'name': q}).exec()
        for i, row in enumerate(res):
            record = f"{(i + 1)}. [{row['id']}] - {row['name']}"
            print(record)

    data.close()

if __name__ == '__main__':
    main()    
