import json
import logging
from typing import Optional

import aiosqlite
import pandas as pd

from terminal_colors import TerminalColors as tc
from utilities import Utilities

DATA_BASE = "database/contoso-sales.db"

logging.basicConfig(level=logging.ERROR)
logger = logging.getLogger(__name__)


class SalesData:
    def __init__(self: "SalesData", utilities: Utilities) -> None:
        self.conn: Optional[aiosqlite.Connection] = None
        self.utilities = utilities

    async def connect(self: "SalesData") -> None:
        db_uri = f"file:{self.utilities.shared_files_path}/{DATA_BASE}?mode=ro"

        try:
            self.conn = await aiosqlite.connect(db_uri, uri=True)
            logger.debug("Database connection opened.")
        except aiosqlite.Error as e:
            logger.exception("An error occurred", exc_info=e)
            self.conn = None

    async def close(self: "SalesData") -> None:
        if self.conn:
            await self.conn.close()
            logger.debug("Database connection closed.")

    def _ensure_connection(self: "SalesData") -> None:
        """database (데이터베이스) 연결이 설정되었는지 확인합니다."""
        if self.conn is None:
            raise RuntimeError("Database connection is not established. Call connect() first.")

    async def _get_table_names(self: "SalesData") -> list:
        """테이블 이름 목록을 반환합니다."""
        self._ensure_connection()
        assert self.conn is not None
        table_names = []
        async with self.conn.execute("SELECT name FROM sqlite_master WHERE type='table';") as tables:
            return [table[0] async for table in tables if table[0] != "sqlite_sequence"]

    async def _get_column_info(self: "SalesData", table_name: str) -> list:
        """컬럼 이름과 타입을 포함하는 튜플 목록을 반환합니다."""
        self._ensure_connection()
        assert self.conn is not None
        column_info = []
        async with self.conn.execute(f"PRAGMA table_info('{table_name}');") as columns:
            # col[1]은 컬럼 이름, col[2]는 컬럼 타입
            return [f"{col[1]}: {col[2]}" async for col in columns]

    async def _get_regions(self: "SalesData") -> list:
        """database (데이터베이스)의 고유한 지역 목록을 반환합니다."""
        self._ensure_connection()
        assert self.conn is not None
        async with self.conn.execute("SELECT DISTINCT region FROM sales_data;") as regions:
            result = await regions.fetchall()
        return [region[0] for region in result]

    async def _get_product_types(self: "SalesData") -> list:
        """database (데이터베이스)의 고유한 제품 타입 목록을 반환합니다."""
        self._ensure_connection()
        assert self.conn is not None
        async with self.conn.execute("SELECT DISTINCT product_type FROM sales_data;") as product_types:
            result = await product_types.fetchall()
        return [product_type[0] for product_type in result]

    async def _get_product_categories(self: "SalesData") -> list:
        """database (데이터베이스)의 고유한 제품 카테고리 목록을 반환합니다."""
        self._ensure_connection()
        assert self.conn is not None
        async with self.conn.execute("SELECT DISTINCT main_category FROM sales_data;") as product_categories:
            result = await product_categories.fetchall()
        return [product_category[0] for product_category in result]

    async def _get_reporting_years(self: "SalesData") -> list:
        """database (데이터베이스)의 고유한 보고 연도 목록을 반환합니다."""
        self._ensure_connection()
        assert self.conn is not None
        async with self.conn.execute("SELECT DISTINCT year FROM sales_data ORDER BY year;") as reporting_years:
            result = await reporting_years.fetchall()
        return [str(reporting_year[0]) for reporting_year in result]

    async def get_database_info(self: "SalesData") -> str:
        """database (데이터베이스) schema (스키마) 정보와 일반적인 query (쿼리) 필드를 포함하는 문자열을 반환합니다."""
        self._ensure_connection()
        table_dicts = []
        for table_name in await self._get_table_names():
            columns_names = await self._get_column_info(table_name)
            table_dicts.append(
                {"table_name": table_name, "column_names": columns_names})

        database_info = "\n".join(
            [
                f"Table {table['table_name']} Schema: Columns: {', '.join(table['column_names'])}"
                for table in table_dicts
            ]
        )
        regions = await self._get_regions()
        product_types = await self._get_product_types()
        product_categories = await self._get_product_categories()
        reporting_years = await self._get_reporting_years()

        database_info += f"\nRegions: {', '.join(regions)}"
        database_info += f"\nProduct Types: {', '.join(product_types)}"
        database_info += f"\nProduct Categories: {', '.join(product_categories)}"
        database_info += f"\nReporting Years: {', '.join(reporting_years)}"
        database_info += "\n\n"

        return database_info

    async def async_fetch_sales_data_using_sqlite_query(self: "SalesData", sqlite_query: str) -> str:
        """
        이 함수는 database (데이터베이스)에 대해 SQLite query (쿼리)를 실행하여 Contoso 판매 데이터에 대한 사용자 질문에 답변하는 데 사용됩니다.

        :param sqlite_query: 입력은 사용자의 질문을 기반으로 정보를 추출하기 위한 올바른 형식의 SQLite query (쿼리)여야 합니다. query (쿼리) 결과는 JSON 객체로 반환됩니다.
        :return: JSON 직렬화 가능한 형식으로 데이터를 반환합니다.
        :rtype: str
        """

        print(
            f"\n{tc.BLUE}Function Call Tools: async_fetch_sales_data_using_sqlite_query{tc.RESET}\n")
        print(f"{tc.BLUE}Executing query: {sqlite_query}{tc.RESET}\n")

        try:
            self._ensure_connection()
            assert self.conn is not None
            # query (쿼리)를 비동기적으로 수행
            async with self.conn.execute(sqlite_query) as cursor:
                rows = await cursor.fetchall()
                columns = [description[0]
                           for description in cursor.description]

            if not rows:  # 행이 없으면 DataFrame을 생성할 필요가 없음
                return json.dumps("The query returned no results. Try a different question.")
            data = pd.DataFrame(rows, columns=columns)
            return data.to_json(index=False, orient="split")

        except Exception as e:
            return json.dumps({"SQLite query failed with error": str(e), "query": sqlite_query})
