import enum
from typing import List
import mysql.connector
from mysql.connector import Error
from mysql.connector.connection import MySQLConnection


class Config( enum.Enum ):
    HOST = 'localhost'
    USER = 'root'
    PSWD = 'root'
    DB = 'Galeo-Cash-mov'
    PORT = 8888



def _open_connection() -> MySQLConnection:
    try:
        connection_config_dict = {
            'user' : Config.USER.value,
            'password' : Config.PSWD.value,
            'host': Config.HOST.value,
            'database': Config.DB.value,
            'port' : Config.PORT.value
        }

        connection = mysql.connector.connect(**connection_config_dict)

        if connection.is_connected():
            return connection
    
    except Error as error:
        return _database_error(Error)


def _close_connection(connection) -> None:
    if connection.is_connected():
        connection.close()


def _database_error(err:Error) -> str:
    return "Failed to get record from MySQL table: {}".format(err)



# insert update delete
def commit(query:str) -> dict[str:int]:
    try:
        connection = _open_connection()

        if connection.is_connected():
            cursor =  connection.cursor()
            cursor.execute(query)
            connection.commit()

            dict = {'rowcount' : cursor.rowcount}
            
            return dict
    
    except mysql.connector.Error as error:
            return _database_error(error)
            
    finally:
        if connection.is_connected():
            cursor.close()
            _close_connection(connection)



# les fonctions fetch ne font que récupéré des donnée elle ne peux jamais envoyer quoi que ce soit
def fetch_all(query:str) -> List:
    try:
        connection = _open_connection()

        if connection.is_connected():
            cursor =  connection.cursor()
            cursor.execute(query)
            record = cursor.fetchall()

            return record

    except mysql.connector.Error as error:
            return _database_error(error)
            
    finally:
        if connection.is_connected():
            cursor.close()
            _close_connection(connection)


def fetch_one(query:str) -> List:
    try:
        connection = _open_connection()

        if connection.is_connected():
            cursor =  connection.cursor()
            cursor.execute(query)
            record = cursor.fetchone()
            return record[0]

    except mysql.connector.Error as error:
            return _database_error(error)
            
    finally:
        if connection.is_connected():
            cursor.close()
            _close_connection(connection)
