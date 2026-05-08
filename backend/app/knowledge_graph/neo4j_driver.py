import logging


class Neo4jDriver:
    """Neo4j 驱动占位类（已禁用，改用 SQLite + 静态数据）"""

    _instance = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super(Neo4jDriver, cls).__new__(cls)
        return cls._instance

    def __init__(self, uri=None, user=None, password=None):
        pass

    def connect(self):
        pass

    def close(self):
        pass

    def run_query(self, query, parameters=None):
        logging.warning("Neo4j 已禁用，run_query 返回空列表")
        return []

    def run_transaction(self, func, *args, **kwargs):
        return None

    def test_connection(self):
        return False
