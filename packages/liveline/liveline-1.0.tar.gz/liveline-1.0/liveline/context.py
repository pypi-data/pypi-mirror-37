import json
import time
from typing import List

import pymongo


class Context:
    def __init__(self, json_source=None, dict_source=None):
        if json_source is not None:
            self.__dict__ = json.loads(json_source)
        if dict_source is not None:
            self.__dict__ = dict_source

    def to_json(self) -> str:
        return json.dumps(self.__dict__)

    def __repr__(self):
        return self.to_json()

    def __getattr__(self, name):
        return None


class ContextDataStore:
    def __init__(self):
        pass

    def save(self, strategy_name: str, context: Context):
        pass

    def get_strategy_context(self, strategy_name: str) -> List[Context]:
        pass

    def get_strategy_latest_context(self, strategy_name: str) -> Context:
        pass

    def clear_strategy_context(self, strategy_name: str):
        pass


class MongoContextDataStore(ContextDataStore):
    def __init__(self, db: pymongo.database.Database):
        self.db: pymongo.database.Database = db

    def save(self, strategy_name: str, context: Context):
        data = {
            'context': context.to_json(),
            'strategy_name': strategy_name,
            'timestamp': int(time.time())
        }
        self.db.context.insert_one(data)

    def get_strategy_context(self, strategy_name: str) -> List[Context]:
        data = self.db.context.find({'strategy_name': strategy_name}) 
        return [Context(json_source=d['context']) for d in data]

    def get_strategy_latest_context(self, strategy_name: str) -> Context:
        results = self.db.context.find({'strategy_name': strategy_name}).sort(
            'timestamp', pymongo.DESCENDING).limit(1)
        results = list(results)

        if len(results) == 1:
            return Context(json_source=results[0]['context'])
        else:
            return None

    def clear_strategy_context(self, strategy_name: str):
        self.db.context.delete_many({'strategy_name': strategy_name})