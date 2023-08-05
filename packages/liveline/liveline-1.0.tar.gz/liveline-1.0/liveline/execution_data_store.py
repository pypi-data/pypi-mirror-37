import pymongo


class ExecutionDataStore:
    def __init__(self):
        pass

    def insert(self, day: str, strategy: str, execution: str):
        pass

    def get(self, day: str, strategy: str):
        pass


class MongoExecutionDataStore(ExecutionDataStore):
    """
    Save the executions of a strategy during a day

    Mongodb collection looks like:
    {
        'day': '2018-09-01',
        'strategy': 'buy FB',
        'executions': [
            {
                timestamp: 12345678,
                order_placed: [
                    {...}
                ]
            },
            {
                timestamp: 12345679,
                order_placed: []
            }
        ]
    }
    """

    def __init__(self, db: pymongo.database.Database):
        self.db: pymongo.database.Database = db

    def insert(self, day: str, strategy: str, execution: str):
        strategy_executions = self.db.executions.find_one({
            'day': day,
            'strategy': strategy
        })

        if strategy_executions is None:
            strategy_executions = {
                'day': day,
                'strategy': strategy,
                'executions': []
            }

        strategy_executions['executions'].append(execution)

        self.db.executions.update(
            {
                'day': day,
                'strategy': strategy
            }, 
            {
                '$set': {'executions': strategy_executions['executions']}
            }, 
            upsert=True)

    def get(self, day: str = None, strategy: str = None):
        filter = {}
        if day is not None: 
            filter['day'] = day
        if strategy is not None:
            filter['strategy'] = strategy

        return list(self.db.executions.find(filter, {'_id': False}))

    def clear(self, day: str = None, strategy: str = None):
        filter = {}
        if day is not None: 
            filter['day'] = day
        if strategy is not None:
            filter['strategy'] = strategy

        return self.db.executions.delete_many(filter)