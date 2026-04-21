from neo4j import GraphDatabase
from flask import current_app
import logging

class Neo4jDriver:
    """Neo4j驱动封装类"""

    _instance = None

    def __new__(cls, *args, **kwargs):
        """单例模式"""
        if cls._instance is None:
            cls._instance = super(Neo4jDriver, cls).__new__(cls)
            cls._instance._initialized = False
        return cls._instance

    def __init__(self, uri=None, user=None, password=None):
        """初始化连接"""
        if self._initialized:
            return
        self.uri = uri
        self.user = user
        self.password = password
        self.driver = None
        self._initialized = False

    def connect(self):
        if self.driver:
            return
        from flask import current_app
        self.uri = self.uri or current_app.config.get('NEO4J_URI')
        self.user = self.user or current_app.config.get('NEO4J_USER')
        self.password = self.password or current_app.config.get('NEO4J_PASSWORD')
        try:
            self.driver = GraphDatabase.driver(self.uri, auth=(self.user, self.password))
            logging.info(f"Connected to Neo4j at {self.uri}")
            self._initialized = True
        except Exception as e:
            logging.error(f"Failed to connect to Neo4j: {str(e)}")
            self.driver = None
            raise e

    def close(self):
        """关闭连接"""
        if self.driver:
            self.driver.close()
            self.driver = None
            self._initialized = False
            logging.info("Neo4j connection closed")

    def run_query(self, query, parameters=None):
        """执行Cypher查询"""
        if not self.driver:
            self.connect()
        if not self.driver:
            logging.error("Neo4j driver not initialized")
            return None
        try:
            with self.driver.session() as session:
                result = session.run(query, parameters or {})
                return [record for record in result]
        except Exception as e:
            logging.error(f"Neo4j query error: {str(e)}")
            return None

    def run_transaction(self, func, *args, **kwargs):
        """执行事务"""
        if not self.driver:
            self.connect()
        if not self.driver:
            logging.error("Neo4j driver not initialized")
            return None
        with self.driver.session() as session:
            return session.execute_write(func, *args, **kwargs)

    def test_connection(self):
        """测试连接"""
        if not self.driver:
            self.connect()
        if not self.driver:
            return False
        try:
            with self.driver.session() as session:
                result = session.run("RETURN 1 as test")
                return result.single()["test"] == 1
        except Exception as e:
            logging.error(f"Neo4j connection test failed: {str(e)}")
            return False 