
## Grounding with Bing Search (Bing 검색을 통한 그라운딩)

이 랩에는 Grounding with Bing Search 서비스가 필요하며, Azure 구독에서 사용할 수 없을 수 있습니다. 액세스 권한이 있는지 확인하려면 랩 지침에 따라 리소스를 생성하세요. 액세스 권한이 없으면 오류 메시지가 표시됩니다. 서비스를 사용할 수 없더라도 Grounding with Bing Search의 작동 방식을 이해하기 위해 랩을 반드시 읽어보세요.

## 랩 실습

이 랩에서는 Bing Grounding (Bing 그라운딩)을 활성화하여 Contoso 제품 및 카테고리에 대한 경쟁적 판매 분석을 제공합니다.

## Grounding with Bing Search 리소스 만들기

Azure Portal에서 **Grounding with Bing Search Service** 리소스를 만들고 Azure AI Foundry Portal에 연결해야 합니다.

다음 단계에 따라 Grounding with Bing Search 리소스를 만드세요:

1. [클릭하여 Grounding with Bing Search 리소스 만들기](https://portal.azure.com/#view/Microsoft_Azure_Marketplace/GalleryItemDetailsBladeNopdl/id/Microsoft.BingGroundingSearch){:target="_blank"}.

    !!! Warning
        Azure 계정에 로그인하거나 환영 화면을 지워야 Azure Portal에 액세스할 수 있습니다.

1. **Create**를 선택합니다.
1. 드롭다운 목록에서 **rg-agent-workshop-****** 리소스 그룹을 선택합니다.
1. 리소스 이름을 다음과 같이 지정합니다:

    ```text
    groundingwithbingsearch
    ```

1. **Grounding with Bing Search** 가격 책정 계층을 선택합니다.
1. **I confirm I have read and understood the notice above**를 확인합니다.
1. **Review + create**를 선택합니다.
1. **Create**를 선택합니다.
1. 배포가 완료될 때까지 기다린 다음 **Go to resource**를 클릭합니다.
1. 사이드바 메뉴에서 **Overview**를 선택합니다.
1. **Go to Azure AI Foundry Portal** 버튼을 선택합니다.
<!-- 1. Select **Sign in** and enter your Azure account credentials. -->

## AI Foundry에서 Bing Search 연결 만들기

다음으로 Azure AI Foundry Portal에서 Bing Search 연결을 만듭니다. 이 연결을 통해 에이전트 앱이 에이전트 **Grounding-with-Bing-Search**를 사용하여 Bing Search 서비스에 액세스할 수 있습니다.

Azure AI Foundry Portal에서 Bing Search 연결을 만들려면 다음 단계를 따르세요:

1. Foundry **project-******이 선택되어 있는지 확인합니다.
2. 사이드바 메뉴에서 **Management Center** 버튼을 클릭합니다. 버튼은 사이드바 **하단**에 고정되어 있습니다.
3. 사이드바 메뉴에서 **Connected resources**를 선택합니다.
4. **+ New connection**을 클릭합니다.
5. Knowledge 섹션으로 스크롤하여 **Grounding with Bing Search**를 선택합니다.
6. `groundingwithbingsearch` 리소스 오른쪽의 **Add connection** 버튼을 클릭합니다.
7. **Close**를 클릭합니다.

자세한 내용은 [Grounding with Bing Search](https://learn.microsoft.com/en-us/azure/ai-services/agents/how-to/tools/bing-grounding){:target="_blank"} 설명서를 참조하세요.

### 에이전트 앱에서 Grounding with Bing Search 활성화

1. `main.py` 파일을 엽니다.

1. **"# "** 문자를 제거하여 다음 줄의 **주석을 해제**합니다.

    ```python


    # bing_grounding = BingGroundingTool(connection_id=AZURE_BING_CONNECTION_ID)
    # toolset.add(bing_grounding)
    ```

    !!! warning
        주석을 해제할 줄은 인접하지 않습니다. # 문자를 제거할 때 그 뒤에 오는 공백도 삭제하세요.

1. `main.py` 파일의 코드를 검토합니다.

    주석 해제 후 코드는 다음과 같아야 합니다:

    ```python
    INSTRUCTIONS_FILE = "instructions/function_calling.txt"
    INSTRUCTIONS_FILE = "instructions/file_search.txt"
    INSTRUCTIONS_FILE = "instructions/code_interpreter.txt"
    INSTRUCTIONS_FILE = "instructions/bing_grounding.txt"
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

        # Add the Bing grounding tool
        bing_grounding = BingGroundingTool(connection_id=AZURE_BING_CONNECTION_ID)
        toolset.add(bing_grounding)

        # Add multilingual support to the code interpreter
        # font_file_info = await utilities.upload_file(agents_client, utilities.shared_files_path / FONTS_ZIP)
        # code_interpreter.add_file(file_id=font_file_info.id)

        return font_file_info
    ```

### 지침 검토

1. **shared/instructions/bing_grounding.txt** 파일을 엽니다. 이 파일은 이전 랩에서 사용한 지침을 대체합니다.
2. **Tools** 섹션에는 이제 "Competitive Insights for Products and Categories" 기능이 포함되어 있으며, 에이전트가 다음을 수행할 수 있습니다:

    - Bing Search를 사용하여 경쟁업체 제품 이름, 회사 이름 및 가격을 수집합니다.
    - 야외 캠핑 및 스포츠 장비와 관련된 주제로 응답을 제한합니다.
    - 검색 결과가 간결하고 쿼리와 직접 관련이 있는지 확인합니다.

### 에이전트 앱 실행

먼저 이전과 같이 터미널에서 앱을 시작합니다:

1. <kbd>F5</kbd>를 눌러 앱을 실행합니다.

### 에이전트와 대화 시작

에이전트는 Contoso 판매 데이터베이스, Tents Data Sheet 및 Bing Search의 데이터를 결합하여 포괄적인 응답을 제공하므로 쿼리에 따라 결과가 달라집니다.

1. **What beginner tents do we sell?**

    !!! info
        이 정보는 주로 vector information store (벡터 정보 저장소)에 제공한 파일에서 가져옵니다.

2. **What beginner tents do our competitors sell? Include prices.**

    !!! info
        이 정보는 인터넷에서 가져오며 실제 제품 이름과 가격을 포함합니다.

3. **Show as a bar chart**

    !!! info
        AI Agent Service (AI 에이전트 서비스)는 다시 Code Interpreter (코드 인터프리터)를 사용하여 차트를 만들지만 이번에는 이전 쿼리에서 가져온 실제 데이터를 사용합니다. 이전과 마찬가지로 `shared/files`에서 차트를 확인하세요.

4. **Show the tents we sell by region that are a similar price to our competitors beginner tents.**

    !!! info
        이 쿼리는 Function Calling (함수 호출)에서 반환된 데이터와 함께 기본 LLM (대규모 언어 모델)의 추론 기능에 의존합니다.

5. **Download the data as a human-readable JSON file**

    !!! info
        이 쿼리는 다시 Code Interpreter (코드 인터프리터)를 사용하여 이전 쿼리의 컨텍스트에서 파일을 만듭니다.

### 에이전트 앱 중지

1. **save**를 입력하여 에이전트 앱 상태를 저장합니다. 이렇게 하면 에이전트 앱의 상태를 삭제하지 않고 중지하여 Azure AI Foundry의 Agents Playground에서 에이전트를 탐색할 수 있습니다.
2. <kbd>Shift</kbd>+<kbd>F5</kbd>를 눌러 에이전트 앱 **디버깅을 중지**합니다.
3. 터미널 출력에서 Agent ID를 **복사**합니다. Agent ID는 Azure AI Foundry Portal에서 에이전트를 탐색하는 데 필요합니다. Agent ID는 다음 예제와 유사합니다:

    ```text
    Agent ID: asst_pskNeFYuoCPogDnmfaqIUwoU
    ```

## Azure AI Foundry에서 에이전트 탐색

Azure AI Foundry에는 에이전트 앱과 상호 작용하고 다양한 쿼리에 어떻게 응답하는지 테스트할 수 있는 Playground가 포함되어 있습니다. 이 Playground는 완전한 챗봇 경험이 아니라 테스트 도구라는 점을 명심하세요. 또한 Contoso 판매 데이터베이스에 대한 실시간 액세스 권한이 없습니다. 해당 리소스는 로컬에서만 사용할 수 있기 때문입니다.

1. 브라우저에서 [Azure AI Foundry Portal](https://ai.azure.com/){:target="_blank"}로 이동합니다.
2. 왼쪽 탐색 메뉴에서 **Playgrounds**를 선택합니다.
3. **Try the Agents playground**를 선택합니다.
4. 이전에 복사한 **Agent ID**를 **Agent id** 필드에 붙여넣습니다.

### 에이전트의 지침 검토

`instructions_bing_grounding.txt` 파일의 지침을 인식할 수 있을 것입니다. 이러한 지침은 에이전트가 쿼리에 응답하도록 안내하는 데 사용됩니다.

### Playground에서 에이전트와 대화 시작

Playground를 사용하여 다양한 쿼리를 테스트하고 에이전트가 어떻게 응답하는지 관찰하세요. 터미널에서 사용한 것과 동일한 쿼리를 재사용하거나 새로운 쿼리를 시도할 수 있습니다. 에이전트는 Tents Data Sheet 및 Bing Search에서 정보를 가져오지만 로컬 앱 버전과 달리 Contoso 판매 데이터베이스에는 액세스할 수 없다는 점을 명심하세요.

![Azure AI Foundry Playground](../media/agents-playground.png)
