## 소개

### Function Calling이란 무엇인가요?

Function calling(함수 호출)은 Large Language Model(LLM, 대규모 언어 모델)이 외부 시스템과 상호작용할 수 있게 합니다. LLM은 instructions(지시사항), function definitions(함수 정의) 및 사용자 프롬프트를 기반으로 언제 함수를 호출할지 결정합니다. 그런 다음 LLM은 Agent 앱이 함수를 호출하는 데 사용할 수 있는 구조화된 데이터를 반환합니다.

Agent 앱 내에서 함수 로직을 구현하는 것은 개발자의 몫입니다. 이 워크숍에서는 함수 로직을 사용하여 LLM에 의해 동적으로 생성된 SQLite 쿼리를 실행합니다.

### Function Calling 활성화하기

[Azure OpenAI Function Calling](https://learn.microsoft.com/azure/ai-services/openai/how-to/function-calling){:target="_blank"}에 익숙하다면, LLM을 위한 function schema(함수 스키마)를 정의해야 한다는 것을 알고 계실 것입니다.

=== "Python"

    Foundry Agent Service와 Python SDK를 사용하면 Python 함수의 docstring(독스트링) 내에서 직접 function schema를 정의할 수 있습니다. 이 접근 방식은 정의와 구현을 함께 유지하여 유지 관리를 단순화하고 가독성을 향상시킵니다.

    예를 들어, **sales_data.py** 파일에서 **async_fetch_sales_data_using_sqlite_query** 함수는 docstring을 사용하여 signature(시그니처), inputs(입력) 및 outputs(출력)을 지정합니다. SDK는 이 docstring을 파싱하여 LLM을 위한 callable function(호출 가능한 함수)을 생성합니다:

    ```python

    async def async_fetch_sales_data_using_sqlite_query(self: "SalesData", sqlite_query: str) -> str:
        """
        This function is used to answer user questions about Contoso sales data by executing SQLite queries against the database.

        :param sqlite_query: The input should be a well-formed SQLite query to extract information based on the user's question. The query result will be returned as a JSON object.
        :return: Return data in JSON serializable format.
        :rtype: str
        """
    ```

=== "C#"

    Foundry Agent Service와 .NET SDK를 사용하면 Agent에 함수를 추가할 때 C# 코드의 일부로 function schema를 정의합니다.

    예를 들어, **Lab.cs** 파일에서 `InitialiseTools` 메서드는 `FetchSalesDataAsync` 함수에 대한 function schema를 정의합니다:

    ```csharp
    new FunctionToolDefinition(
        name: nameof(SalesData.FetchSalesDataAsync),
        description: "This function is used to answer user questions about Contoso sales data by executing SQLite queries against the database.",
        parameters: BinaryData.FromObjectAsJson(new {
            Type = "object",
            Properties = new {
                Query = new {
                    Type = "string",
                    Description = "The input should be a well-formed SQLite query to extract information based on the user's question. The query result will be returned as a JSON object."
                }
            },
            Required = new [] { "query" }
        },
        new JsonSerializerOptions() { PropertyNamingPolicy = JsonNamingPolicy.CamelCase })
    )
    ```

### 동적 SQL 생성

앱이 시작되면 데이터베이스 스키마와 주요 데이터를 Foundry Agent Service의 instructions(지시사항)에 통합합니다. 이 입력을 사용하여 LLM은 자연어로 표현된 사용자 요청에 응답하기 위해 SQLite 호환 SQL 쿼리를 생성합니다.

## 실습 과제

이 실습에서는 SQLite 데이터베이스에 대해 동적 SQL 쿼리를 실행하는 함수 로직을 활성화합니다. 이 함수는 Contoso 판매 데이터에 대한 사용자 질문에 답변하기 위해 LLM에 의해 호출됩니다.

=== "Python"

    1. `main.py`를 엽니다.

    2. **"# "** 문자를 제거하여 다음 줄의 **주석을 해제**합니다

        ```python
        # INSTRUCTIONS_FILE = "instructions/instructions_function_calling.txt"

        # toolset.add(functions)
        ```

        !!! warning
            주석을 해제할 줄은 인접하지 않습니다. # 문자를 제거할 때 그 뒤에 있는 공백도 삭제해야 합니다. **CTRL-K + CTRL-U** 단축키를 사용하여 선택한 코드 섹션의 주석을 더 빠르게 해제할 수 있습니다.

    3. main.py의 코드를 검토합니다.

        주석 해제 후 코드는 다음과 같아야 합니다:

        ``` python
        INSTRUCTIONS_FILE = "instructions/function_calling.txt"
        # INSTRUCTIONS_FILE = "instructions/file_search.txt"
        # INSTRUCTIONS_FILE = "instructions/code_interpreter.txt"
        # INSTRUCTIONS_FILE = "instructions/code_interpreter_multilingual.txt"



        async def add_agent_tools() -> None:
            """Add tools for the agent."""
            font_file_info = None

            # Add the functions tool
            toolset.add(functions)

            # Add the tents data sheet to a new vector data store
            # vector_store = await utilities.create_vector_store(
            #     agents_client,
            #     files=[TENTS_DATA_SHEET_FILE],
            #     vector_store_name="Contoso Product Information Vector Store",
            # )
            # file_search_tool = FileSearchTool(vector_store_ids=[vector_store.id])
            # toolset.add(file_search_tool)

            # Add the code interpreter tool
            # code_interpreter = CodeInterpreterTool()
            # toolset.add(code_interpreter)

            # Add multilingual support to the code interpreter
            # font_file_info = await utilities.upload_file(agents_client, utilities.shared_files_path / FONTS_ZIP)
            # code_interpreter.add_file(file_id=font_file_info.id)

            return font_file_info
        ```

=== "C#"

    1. `Program.cs` 파일을 엽니다.

    2. 다음 코드를 **주석 해제**하고 업데이트합니다:

        ```csharp
        await using Lab lab = new Lab1(projectClient, apiDeploymentName);
        await lab.RunAsync();
        ```

### Instructions 검토하기

 1. **shared/instructions/function_calling.txt** 파일을 엽니다.

    !!! tip "VS Code에서 Alt + Z(Windows/Linux) 또는 Option + Z(Mac)를 눌러 word wrap(단어 줄 바꿈) 모드를 활성화하면 instructions를 더 쉽게 읽을 수 있습니다."

 2. instructions가 Agent 앱의 동작을 어떻게 정의하는지 검토합니다:

     - **Role definition(역할 정의)**: Agent는 정중하고 전문적이며 친근한 방식으로 Contoso 사용자의 판매 데이터 문의를 지원합니다.
     - **Context(맥락)**: Contoso는 캠핑 및 스포츠 장비를 전문으로 하는 온라인 소매업체입니다.
     - **Tool description(도구 설명) – "Sales Data Assistance"**:
         - Agent가 SQL 쿼리를 생성하고 실행할 수 있게 합니다.
         - 쿼리 구축을 위한 데이터베이스 스키마 세부 정보를 포함합니다.
         - 결과를 최대 30행의 집계된 데이터로 제한합니다.
         - 출력을 Markdown 테이블로 포맷합니다.
     - **Response guidance(응답 가이드)**: 실행 가능하고 관련성 있는 답변을 강조합니다.
     - **User support tips(사용자 지원 팁)**: 사용자를 지원하기 위한 제안을 제공합니다.
     - **Safety and conduct(안전 및 행동)**: 불명확하거나 범위를 벗어나거나 악의적인 쿼리를 처리하는 방법을 다룹니다.

     워크숍 동안 새로운 도구를 도입하여 Agent의 기능을 향상시키기 위해 이러한 instructions를 확장할 것입니다.

    !!! info
        instructions의 {database_schema_string} placeholder(플레이스홀더)는 앱이 초기화될 때 데이터베이스 스키마로 대체됩니다.

        === "Python"

            ```python
            # Replace the placeholder with the database schema string
            instructions = instructions.replace("{database_schema_string}", database_schema_string)
            ```

        === "C#"

            ```csharp
            // Replace the placeholder with the database schema string
            instructions = instructions.Replace("{database_schema_string}", databaseSchemaString);
            ```

## Agent 앱 실행하기

1. <kbd>F5</kbd>를 눌러 앱을 실행합니다.
2. 터미널에서 앱이 시작되는 것을 볼 수 있으며, Agent 앱이 **Enter your query**(쿼리 입력)를 요청할 것입니다.

    ![Agent App](../../../docs/docs/media/run-the-agent.png){:width="600"}

### Agent와 대화 시작하기

Contoso 판매 데이터에 대해 질문하기 시작하세요. 예를 들어:

1. **Help**

    다음은 **help** 쿼리에 대한 LLM 응답의 예입니다:

    *I'm here to help with your sales data inquiries at Contoso. Could you please provide more details about what you need assistance with? Here are some example queries you might consider:*

    - *What were the sales by region?*
    - *What was last quarter's revenue?*
    - *Which products sell best in Europe?*
    - *Total shipping costs by region?*

    *Feel free to ask any specific questions related to Contoso sales data!*

    !!! tip
        LLM은 instructions 파일에 정의된 시작 질문 목록을 제공합니다. 예를 들어 `help in Hindi`, `help in Italian` 또는 `help in Korean`과 같이 여러분의 언어로 도움을 요청해 보세요.

2. **Show the 3 most recent transaction details**

    응답에서 SQLite 데이터베이스에 저장된 원시 데이터를 볼 수 있습니다. 각 레코드는 제품, 제품 카테고리, 판매 금액 및 지역, 날짜 등에 대한 정보가 포함된 Contoso의 단일 판매 거래입니다.

    !!! warning
        Agent가 "I'm unable to provide individual transaction details"와 같은 메시지로 이 쿼리에 응답하지 않을 수 있습니다. 이는 instructions가 "기본적으로 집계된 결과를 제공"하도록 지시하기 때문입니다. 이런 경우 다시 시도하거나 쿼리를 다시 표현해 보세요.

        Large Language model은 비결정적 동작을 가지며, 동일한 쿼리를 반복하더라도 다른 응답을 제공할 수 있습니다.

3. **What are the sales by region?**

    다음은 **sales by region** 쿼리에 대한 LLM 응답의 예입니다:

        | Region         | Total Revenue  |
        |----------------|----------------|
        | AFRICA         | $5,227,467     |
        | ASIA-PACIFIC   | $5,363,718     |
        | CHINA          | $10,540,412    |
        | EUROPE         | $9,990,708     |
        | LATIN AMERICA  | $5,386,552     |
        | MIDDLE EAST    | $5,312,519     |
        | NORTH AMERICA  | $15,986,462    |

    !!! info
        그렇다면 이 모든 것을 작동시키기 위해 백그라운드에서 무슨 일이 일어나고 있을까요?

        LLM은 다음 단계를 조율(orchestrate)합니다:

        1. LLM은 사용자의 질문에 답변하기 위한 SQL 쿼리를 생성합니다. **"What are the sales by region?"** 질문에 대해 다음 SQL 쿼리가 생성됩니다:

            **SELECT region, SUM(revenue) AS total_revenue FROM sales_data GROUP BY region;**

        2. 그런 다음 LLM은 Agent 앱에 **async_fetch_sales_data_using_sqlite_query** 함수를 호출하도록 요청하며, 이 함수는 SQLite 데이터베이스에서 필요한 데이터를 검색하여 LLM에 반환합니다.
        3. LLM은 검색된 데이터를 사용하여 Markdown 테이블을 생성한 다음 이를 사용자에게 반환합니다. instructions 파일을 확인하면 Markdown이 기본 출력 형식임을 알 수 있습니다.

4. **Show sales by category in Europe**

    이 경우 Agent 앱에 의해 훨씬 더 복잡한 SQL 쿼리가 실행됩니다.

5. **Breakout sales by footwear**

    Agent가 어떤 제품이 "footwear" 카테고리에 속하는지 파악하고 "**breakout**" 용어의 의도를 이해하는 방법을 주목하세요.

6. **What brands of tents do we sell?**

    !!! info
        제품 브랜드에 대한 정보를 포함하는 데이터를 Agent에 제공하지 않았습니다. 그렇기 때문에 Agent가 이 질문에 제대로 답변할 수 없습니다.

        이전 응답에서 기본 데이터베이스의 거래 내역에도 제품 브랜드나 설명이 포함되어 있지 않다는 것을 알아차렸을 수도 있습니다. 다음 실습에서 이를 수정하겠습니다!

## (선택 사항) 앱 디버깅하기

LLM이 데이터를 요청하는 방법을 관찰하려면 `sales_data.py`에 있는 `async_fetch_sales_data_using_sqlite_query` 함수에 [breakpoint](https://code.visualstudio.com/Docs/editor/debugging){:target="_blank"}를 설정하세요.

!!! info "참고: 디버그 기능을 사용하려면 이전 실행을 종료하세요. 그런 다음 breakpoint를 설정하세요. 그런 다음 사이드바의 디버거 아이콘을 사용하여 애플리케이션을 실행하세요. 이렇게 하면 디버그 사이드바가 열려 스택 트레이스를 보고 실행을 단계별로 진행할 수 있습니다."

![Breakpoint](../../../docs/docs/media/breakpoint.png){:width="600"}

### 더 많은 질문하기

breakpoint를 설정했으므로 함수 로직이 작동하는 것을 관찰하기 위해 Contoso 판매 데이터에 대한 추가 질문을 하세요. 함수를 단계별로 진행하여 데이터베이스 쿼리를 실행하고 결과를 LLM에 반환하세요.

다음 질문을 시도해 보세요:

1. **What regions have the highest sales?**
2. **What were the sales of tents in the United States in April 2022?**

### Breakpoint 비활성화하기

앱을 다시 실행하기 전에 breakpoint를 비활성화하는 것을 잊지 마세요.

### Agent 앱 중지하기

완료되면 **exit**를 입력하여 Agent 리소스를 정리하고 앱을 중지하세요.
