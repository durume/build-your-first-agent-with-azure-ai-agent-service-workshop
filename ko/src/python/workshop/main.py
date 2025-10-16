import asyncio
import logging

from azure.ai.agents.aio import AgentsClient
from azure.ai.agents.models import (
    Agent,
    AgentThread,
    AsyncFunctionTool,
    AsyncToolSet,
    CodeInterpreterTool,
    FileSearchTool,
)
from azure.identity.aio import DefaultAzureCredential


from config import Config
from sales_data import SalesData
from stream_event_handler import StreamEventHandler
from terminal_colors import TerminalColors as tc
from utilities import Utilities

logging.basicConfig(level=logging.ERROR)
logger = logging.getLogger(__name__)

INSTRUCTIONS_FILE = None


toolset = AsyncToolSet()
utilities = Utilities()
sales_data = SalesData(utilities)


agents_client = AgentsClient(
    credential=DefaultAzureCredential(),
    endpoint=Config.PROJECT_ENDPOINT,
)

functions = AsyncFunctionTool(
    {
        sales_data.async_fetch_sales_data_using_sqlite_query,
    }
)

# INSTRUCTIONS_FILE = "instructions/function_calling.txt"
# INSTRUCTIONS_FILE = "instructions/file_search.txt"
# INSTRUCTIONS_FILE = "instructions/code_interpreter.txt"
# INSTRUCTIONS_FILE = "instructions/code_interpreter_multilingual.txt"


async def add_agent_tools():
    """Agent에 도구(tools)를 추가합니다."""
    font_file_info = None

    # functions tool 추가
    # toolset.add(functions)

    # 텐트 데이터 시트를 새로운 vector data store(벡터 데이터 저장소)에 추가
    # vector_store = await utilities.create_vector_store(
    #     agents_client,
    #     files=[Config.TENTS_DATA_SHEET_FILE],
    #     vector_store_name="Contoso Product Information Vector Store",
    # )
    # file_search_tool = FileSearchTool(vector_store_ids=[vector_store.id])
    # toolset.add(file_search_tool)

    # code interpreter tool 추가
    # code_interpreter = CodeInterpreterTool()
    # toolset.add(code_interpreter)

    # code interpreter에 다국어 지원 추가
    # font_file_info = await utilities.upload_file(agents_client, utilities.shared_files_path / Config.FONTS_ZIP)
    # code_interpreter.add_file(file_id=font_file_info.id)

    return font_file_info


async def initialize() -> tuple[Agent | None, AgentThread | None]:
    """판매 데이터 스키마(schema)와 instructions(지시사항)로 Agent를 초기화합니다."""

    if not INSTRUCTIONS_FILE:
        return None, None

    if not Config.API_DEPLOYMENT_NAME:
        logger.error("MODEL_DEPLOYMENT_NAME environment variable is not set")
        return None, None

    font_file_info = await add_agent_tools()

    await sales_data.connect()
    database_schema_string = await sales_data.get_database_info()

    try:
        instructions = utilities.load_instructions(INSTRUCTIONS_FILE)
        # placeholder를 데이터베이스 스키마 문자열로 대체
        instructions = instructions.replace(
            "{database_schema_string}", database_schema_string)

        if font_file_info:
            # placeholder를 폰트 파일 ID로 대체
            instructions = instructions.replace(
                "{font_file_id}", font_file_info.id)

        print("Creating agent...")
        agent = await agents_client.create_agent(
            model=Config.API_DEPLOYMENT_NAME,
            name=Config.AGENT_NAME,
            instructions=instructions,
            toolset=toolset,
            temperature=Config.TEMPERATURE,
        )
        print(f"Created agent, ID: {agent.id}")

        agents_client.enable_auto_function_calls(tools=toolset)
        print("Enabled auto function calls.")

        print("Creating thread...")
        thread = await agents_client.threads.create()
        print(f"Created thread, ID: {thread.id}")

        return agent, thread

    except Exception as e:
        logger.error("An error occurred initializing the agent: %s", str(e))
        logger.error("Please ensure you've enabled an instructions file.")
        return None, None


async def cleanup(agent: Agent, thread: AgentThread) -> None:
    """리소스를 정리합니다."""
    existing_files = await agents_client.files.list()
    for f in existing_files.data:
        await agents_client.files.delete(f.id)
    await agents_client.threads.delete(thread.id)
    await agents_client.delete_agent(agent.id)
    await sales_data.close()


async def post_message(thread_id: str, content: str, agent: Agent, thread: AgentThread) -> None:
    """Foundry Agent Service에 메시지를 게시합니다."""
    try:
        await agents_client.messages.create(
            thread_id=thread_id,
            role="user",
            content=content,
        )

        async with await agents_client.runs.stream(
            thread_id=thread.id,
            agent_id=agent.id,
            event_handler=StreamEventHandler(
                functions=functions, agent_client=agents_client, utilities=utilities),
            max_completion_tokens=Config.MAX_COMPLETION_TOKENS,
            max_prompt_tokens=Config.MAX_PROMPT_TOKENS,
            temperature=Config.TEMPERATURE,
            top_p=Config.TOP_P,
            # instructions=agent.instructions,
        ) as stream:
            await stream.until_done()

    except Exception as e:
        utilities.log_msg_purple(
            f"An error occurred posting the message: {e!s}")


async def main() -> None:
    """
    예제 질문: 지역별 판매, 가장 많이 팔린 제품, 지역별 총 배송비, 원형 차트로 표시.
    """
    async with agents_client:
        agent, thread = await initialize()
        if not agent or not thread:
            print(f"{tc.BG_BRIGHT_RED}초기화 실패. 실습을 위한 instructions 파일의 주석을 해제했는지 확인하세요.{tc.RESET}")
            print("종료 중...")
            return

        cmd = None

        while True:
            prompt = input(
                f"\n\n{tc.GREEN}쿼리를 입력하세요 (종료하려면 exit 또는 save 입력): {tc.RESET}").strip()
            if not prompt:
                continue

            cmd = prompt.lower()
            if cmd in {"exit", "save"}:
                break

            await post_message(agent=agent, thread_id=thread.id, content=prompt, thread=thread)

        if cmd == "save":
            print("Agent가 삭제되지 않았으므로 Azure AI Foundry에서 계속 실험할 수 있습니다.")
            print(
                f"https://ai.azure.com으로 이동하여 프로젝트를 선택한 다음 playgrounds, agents playground를 선택하고 agent id: {agent.id}를 선택하세요"
            )
        else:
            await cleanup(agent, thread)
            print("Agent 리소스가 정리되었습니다.")


if __name__ == "__main__":
    print("비동기 프로그램 시작 중...")
    asyncio.run(main())
    print("프로그램 종료.")
