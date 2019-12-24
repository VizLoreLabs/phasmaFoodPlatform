from typing import List, Union

from pymongo import MongoClient
from bson.objectid import ObjectId
from django.conf import settings


class MongoDB:
    """
    Mongo DB object that is used to connect to DB

    Attributes:
        client (obj): Connected to DB
    """
    def __init__(self):
        self.client = MongoClient(settings.MONGO_HOST)

    @staticmethod
    def base_projection() -> dict:
        """Base values that are returned from Mongo DB query.

        Returns:
           base_values (dict): Base values that are returned from Mongo query
        """
        base_values = {
            "foodType": 1,
            "sample": 1,
            "rawDataRef": 1,
            "replicate": 1,
            "tempExposureHours": 1,
            "mainCat": 1,
            "customType2": 1,
            "cat": 1,
            "useCase": 1,
            "date": 1,
            "customType1": 1,
            "adul": 1,
            "time": 1,
            "laboratory": 1,
            "temperature": 1,
            "id": 1
        }
        return base_values

    @staticmethod
    def object_id_to_mongo(query: Union[List[str], dict]) -> dict:
        """Set object #ID to Mongo object #ID

        Parameter:
            query (dict): Query dictionary

        Returns:
            query (dict): Query dictionary with ObjectID updated
            to follow Mongo rules
        """
        if isinstance(query["id"], list):
            ids_list = []
            for q in query["id"]:
                ids_list.append(ObjectId(q))
            query["_id"] = {"$in": ids_list}
        else:
            query_id = query.get("id", None)
            if query_id:
                query["_id"] = ObjectId(query_id)
        del query["id"]

        return query

    def database_list(self) -> List[str]:
        """List of all DB in Mongo.

        Returns:
            dbs (list): databases in Mongo DB
        """
        dbs = self.client.list_database_names()
        return dbs

    def collection_list(self, db: str) -> List[str]:
        """List of all collections for particular DB.

        Parameters:
            db (str): Name of DB in Mongo

        Returns:
            collections (list): All collection for particular DB
        """
        collections = [coll for coll in self.client[db].collection_names(include_system_collections=False)]
        return collections

    def insert_one(self, measurement: dict = None, db: str = settings.MONGO_DEFAULT_DB,
                   collection: str = settings.MONGO_DEFAULT_COLLECTION) -> None:
        """Insert Mongo DB measurement.

        Parameters:
            measurement (dict): Measurement to push
            db (str): Mongo DB that is queried
            collection (str): Mongo DB collection that is queried

        Returns:
            None
        """
        self.client[db][collection].insert_one(measurement)

    def find_row(self, query: dict = None, project: bool = False,
                 db: str = settings.MONGO_DEFAULT_DB, collection: str = settings.MONGO_DEFAULT_COLLECTION) -> dict:
        """Query Mongo DB for single document with filters.

        Parameters:
            query (dict): Query for Mongo DB
            project (bool): Return all filed or exclude some of them
            db (str): Mongo DB that is queried
            collection (str): Mongo DB collection that is queried

        Returns:
            data (dict): Single document form Mongo DB
        """
        query = self.object_id_to_mongo(query)
        data = self.client[db][collection].find_one(query, self.base_projection() if project else None)
        data["id"] = str(data.pop("_id"))
        return data

    def find_rows(self, query: dict = None, project: bool = False, page_num: int = 1,
                  page_size: int = 10, db: str = settings.MONGO_DEFAULT_DB,
                  collection: str = settings.MONGO_DEFAULT_COLLECTION) -> List[int]:
        """Query Mongo DB for documents using filters and pagination.

        Parameters:
            query (dict): Query for Mongo DB
            project (bool): Return all filed or exclude some of them
            page_num (int): Page that is required
            page_size (int): Results per page
            db (str): Mongo DB that is queried
            collection (str): Mongo DB collection that is queried

        Returns:
            data_final (list): Documents form Mongo DB
            data_query_total (int): Number of result in query
            data_total (int): How much document are in Mongo DB
            page_num (int): Current page number
            page_size (int): Results per page
        """
        query = self.object_id_to_mongo(query) if query else {}
        projection = None

        if project:
            projection = self.base_projection()
            projection.update({
                "aflatoxin": 1,
                "microbiologicalMeasurement": 1
            })

        data = self.client[db][collection].find(query, projection)\
            .skip((page_num - 1) * page_size)\
            .limit(page_size)
        data_total = data.count()
        data_query_total = data.count(with_limit_and_skip=True)

        data_final = []
        for x in data:
            x['id'] = str(x.pop('_id'))
            data_final.append(x)

        return [data_final, data_query_total, data_total, page_num, page_size]

    def find_rows_machine_learning(self, query: dict = None, project: bool = False,
                                   db: str = settings.MONGO_DEFAULT_DB,
                                   collection: str = settings.MONGO_DEFAULT_COLLECTION) -> List[dict]:
        """Query Mongo DB for documents in Machine Learning DB.

        Parameters:
            query (dict): Query for Mongo DB
            project (bool): Return all filed or exclude some of them
            db (str): Mongo DB that is queried
            collection (str): Mongo DB collection that is queried

        Returns:
            data_final (list): Documents form Mongo DB
        """

        data = self.client[db][collection].find(query, self.base_projection() if project else None)

        data_final = []
        for x in data:
            data_final.append(x)

        return data_final

    def find_distinct_values(self, values: List[str] = None,
                             db: str = settings.MONGO_DEFAULT_DB,
                             collection: str = settings.MONGO_DEFAULT_COLLECTION) -> dict:
        """Unique values for use cases and food types that are used.

        Parameters:
            values (list/str): For what key/s to find distinct values
            db (str): Mongo DB that is queried
            collection (str): Mongo DB collection that is queried

        Returns:
            data (dict): Results for distinct values
        """
        data = {}
        if isinstance(values, list):
            for value in values:
                response = self.client[db][collection].distinct(value)
                data[value] = response
        else:
            response = self.client[db][collection].distinct(values)
            data[values] = response

        return data

    def find_distinct_values_for_use_case(self, use_cases: List[str] = None,
                                          db: str = settings.MONGO_DEFAULT_DB,
                                          collection: str = settings.MONGO_DEFAULT_COLLECTION) -> dict:
        """Unique values of food types for use cases.

        Parameters:
            use_cases (list/str): For what use case/s to find distinct values
            db (str): Mongo DB that is queried
            collection (str): Mongo DB collection that is queried

        Returns:
            data (dict): Results for distinct values
        """
        data = {}
        if isinstance(use_cases, list):
            for case in use_cases:
                response = self.client[db][collection].distinct("foodType", {"useCase": case})
                data[case] = response
        else:
            response = self.client[db][collection].distinct("foodType", {"useCase": use_cases})
            data[use_cases] = response

        return data

    def counter(self, item: dict = None,
                db: str = settings.MONGO_DEFAULT_DB, collection: str = settings.MONGO_DEFAULT_COLLECTION) -> dict:
        """Count number of particular value in Mongo DB

        Parameters:
            item (dict): Value to be counted
            db (str): Mongo DB that is queried
            collection (str): Mongo DB collection that is queried

        Returns:
            data (int): Number of item
        """
        data = {}
        if isinstance(item, dict):
            data = self.client[db][collection].count(item)

        return data
