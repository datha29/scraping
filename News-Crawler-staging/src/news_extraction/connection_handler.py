import pymongo

class MongoHandler:
    """Handling the MondoDB Connection 
    """
    def __init__(self, conn_str:str, db_name:str, col_name:str):
        """Initializing the MongoDB Credentials

        Args:
            conn_str (str): Mongo connection string
            db_name (str): MongoDB database name
            col_name (str): MongoDB collectione name
        """
        self.client = pymongo.MongoClient(conn_str)
        self.db_name = db_name
        self.col_name = col_name
    def get_col_obj(self):
        """ Connecting To MongoDB

        Args:
            conn_str (str): Connection String
            db_name (str): Database Name
            col_name (str): Collection Name
        """
        mydb = self.client[self.db_name]
        col_obj = mydb[self.col_name]
        return col_obj
    def close_conn(self):
        """_Close the MongoDB Connection"""
        self.client.close()
