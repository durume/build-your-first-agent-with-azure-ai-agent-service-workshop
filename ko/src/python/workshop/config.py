import os
from dotenv import load_dotenv

load_dotenv()


class Config:
    """Contoso Sales Agent (에이전트)의 구성 클래스입니다."""

    AGENT_NAME = "Contoso Sales Agent"
    TENTS_DATA_SHEET_FILE = "datasheet/contoso-tents-datasheet.pdf"
    FONTS_ZIP = "fonts/fonts.zip"
    API_DEPLOYMENT_NAME = os.getenv("MODEL_DEPLOYMENT_NAME")
    PROJECT_ENDPOINT = os.environ["PROJECT_ENDPOINT"]
    MAX_COMPLETION_TOKENS = 10240
    MAX_PROMPT_TOKENS = 20480
    # LLM은 SQL query (쿼리)를 생성하는 데 사용됩니다.
    # 보다 결정론적인 결과를 얻기 위해 temperature와 top_p를 낮게 설정합니다.
    TEMPERATURE = 0.1
    TOP_P = 0.1
