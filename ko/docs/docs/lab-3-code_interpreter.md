## 소개

Foundry Agent Service Code Interpreter는 LLM이 차트 생성이나 복잡한 데이터 분석과 같은 작업을 위해 Python 코드를 안전하게 실행할 수 있게 합니다. natural language processing(NLP, 자연어 처리), SQLite 데이터베이스의 판매 데이터 및 사용자 프롬프트를 활용하여 코드 생성을 자동화합니다. LLM이 생성한 Python 코드는 안전한 sandbox 환경 내에서 실행되며, 안전하고 제어된 실행을 보장하기 위해 Python의 제한된 하위 집합에서 실행됩니다.

## 실습 과제 - Python

이 실습에서는 LLM이 생성한 Python 코드를 실행하도록 Code Interpreter를 활성화합니다.

=== "Python"

    1. `main.py`를 엽니다.

    2. Agent를 위한 새로운 instructions 파일을 정의하고 Agent의 toolset(도구 세트)에 code interpreter를 추가합니다. **"# "** 문자를 제거하여 다음 줄의 **주석을 해제**합니다.

        ```python
        # INSTRUCTIONS_FILE = "instructions/code_interpreter.txt

        # code_interpreter = CodeInterpreterTool()
        # toolset.add(code_interpreter)
        ```

        !!! warning
            주석을 해제할 줄은 인접하지 않습니다. # 문자를 제거할 때 그 뒤에 있는 공백도 삭제해야 합니다.

    3. `main.py` 파일의 코드를 검토합니다.

        주석 해제 후 코드는 다음과 같아야 합니다:

        ```python
        INSTRUCTIONS_FILE = "instructions/function_calling.txt"
        INSTRUCTIONS_FILE = "instructions/file_search.txt"
        INSTRUCTIONS_FILE = "instructions/code_interpreter.txt"
        # INSTRUCTIONS_FILE = "instructions/code_interpreter_multilingual.txt"



        async def add_agent_tools() -> None:
            """Add tools for the agent."""
            font_file_info = None

            # Add the functions tool
            toolset.add(functions)

            # Add the tents data sheet to a new vector data store
            vector_store = await utilities.create_vector_store(
                agents_client,
                files=[TENTS_DATA_SHEET_FILE],
                vector_store_name="Contoso Product Information Vector Store",
            )
            file_search_tool = FileSearchTool(vector_store_ids=[vector_store.id])
            toolset.add(file_search_tool)

            # Add the code interpreter tool
            code_interpreter = CodeInterpreterTool()
            toolset.add(code_interpreter)

            # Add multilingual support to the code interpreter
            # font_file_info = await utilities.upload_file(agents_client, utilities.shared_files_path / FONTS_ZIP)
            # code_interpreter.add_file(file_id=font_file_info.id)

            return font_file_info
        ```

=== "C#"

    1. `Program.cs` 파일을 엽니다.

    2. `Lab2` 클래스를 사용하도록 lab 생성을 **업데이트**합니다.

        ``` csharp
        await using Lab lab = new Lab3(projectClient, apiDeploymentName);
        ```

    3. Code Interpreter가 Tools 목록에 추가되는 방법을 확인하려면 `Lab2.cs` 클래스를 검토하세요.

## Instructions 검토하기

1. **shared/instructions/code_interpreter.txt** 파일을 엽니다. 이 파일은 이전 실습에서 사용된 instructions를 대체합니다.
2. **Tools** 섹션에는 이제 "Visualization and Code Interpretation"(시각화 및 코드 해석) 기능이 포함되어 Agent가 다음을 수행할 수 있습니다:

      - code interpreter를 사용하여 LLM이 생성한 Python 코드를 실행합니다(예: 데이터 다운로드 또는 시각화).
      - 레이블, 제목 및 기타 차트 텍스트에 사용자의 언어를 사용하여 차트와 그래프를 생성합니다.
      - 시각화를 PNG 파일로, 데이터를 CSV 파일로 내보냅니다.

## Agent 앱 실행하기

1. <kbd>F5</kbd>를 눌러 앱을 실행합니다.
2. 터미널에서 앱이 시작되며, Agent 앱이 **Enter your query**(쿼리 입력)를 요청할 것입니다.

### Agent와 대화 시작하기

다음 질문을 시도해 보세요:

1. **Show sales by region as a pie chart**

    작업이 완료되면 파일이 **shared/files** 하위 폴더에 저장됩니다. 이 하위 폴더는 이 작업이 처음 실행될 때 생성되며 소스 제어에는 체크인되지 않습니다.

    VS Code에서 폴더를 열고 파일을 클릭하여 확인하세요. (팁: Codespaces에서는 Agent가 응답에 출력하는 링크를 Control-Click하여 파일을 볼 수 있습니다.)

    !!! info
        이것은 마법처럼 느껴질 수 있습니다. 그렇다면 이 모든 것을 작동시키기 위해 백그라운드에서 무슨 일이 일어나고 있을까요?

        Foundry Agent Service는 다음 단계를 조율(orchestrate)합니다:

        1. LLM은 사용자의 질문에 답변하기 위한 SQL 쿼리를 생성합니다. 이 예제에서 쿼리는:

            **SELECT region, SUM(revenue) AS total_revenue FROM sales_data GROUP BY region;**

        2. LLM은 Agent 앱에 **async_fetch_sales_data_using_sqlite_query** 함수를 호출하도록 요청합니다. SQL 명령이 실행되고 결과 데이터가 LLM에 반환됩니다.
        3. 반환된 데이터를 사용하여 LLM은 Pie Chart를 생성하는 Python 코드를 작성합니다.
        4. 마지막으로 Code Interpreter가 Python 코드를 실행하여 차트를 생성합니다.

2. **Download as CSV file**

    작업이 완료되면 **shared/files** 폴더를 확인하여 다운로드된 파일을 확인하세요.

    !!! info
        Agent는 명시적으로 지정하지 않았음에도 불구하고 대화에서 생성하려는 파일을 추론했습니다.

3. Code Interpreter가 작동하는 것을 보기 위해 Contoso 판매 데이터에 대한 질문을 계속하세요. 몇 가지 예:
    - **What would be the impact of a shock event (e.g., 20% sales drop in one region) on global sales distribution? Show as a Grouped Bar Chart.**
        - 이어서 **What if the shock event was 50%?**
    - **Which regions have sales above or below the average? Show as a Bar Chart with Deviation from Average.**
    - **Which regions have discounts above or below the average? Show as a Bar Chart with Deviation from Average.**
    - **Simulate future sales by region using a Monte Carlo simulation to estimate confidence intervals. Show as a Line with Confidence Bands using vivid colors.**

## Code Interpreter 디버깅하기

Code Interpreter를 직접 디버깅할 수는 없지만, Agent에게 생성하는 코드를 표시하도록 요청하여 동작에 대한 통찰력을 얻을 수 있습니다. 이를 통해 instructions를 어떻게 해석하는지 이해하고 이를 개선하는 데 도움을 받을 수 있습니다.

터미널에서 다음을 입력하세요:

1. **show code**를 입력하여 마지막 작업에 대해 Code Interpreter가 생성한 코드를 확인합니다.

## Agent 앱 중지하기

완료되면 **exit**를 입력하여 Agent 리소스를 정리하고 앱을 중지하세요.
