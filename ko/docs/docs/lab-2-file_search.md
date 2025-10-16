## 소개

문서를 통한 대화 grounding(접지)은 운영 데이터베이스에서 사용할 수 없는 제품 세부 정보를 검색하는 데 특히 효과적입니다. Foundry Agent Service에는 [File Search tool](https://learn.microsoft.com/en-us/azure/ai-services/agents/how-to/tools/file-search){:target="_blank"}이 포함되어 있어, Agent가 사용자가 제공한 문서나 제품 데이터와 같은 업로드된 파일에서 직접 정보를 검색하여 [RAG-style](https://learn.microsoft.com/azure/ai-studio/concepts/retrieval-augmented-generation){:target="_blank"} 검색 경험을 가능하게 합니다.

이 실습에서는 문서 검색을 활성화하고 Tents Data Sheet를 Agent용 vector store(벡터 저장소)에 업로드하는 방법을 배웁니다. 활성화되면 도구를 통해 Agent가 파일을 검색하고 관련 응답을 제공할 수 있습니다. 문서는 모든 사용자를 위해 Agent에 업로드되거나 특정 사용자 thread(스레드)에 연결되거나 Code Interpreter에 연결될 수 있습니다.

앱이 시작되면 vector store가 생성되고, Contoso tents datasheet PDF 파일이 vector store에 업로드되며, Agent가 사용할 수 있게 됩니다.

일반적으로는 앱이 시작될 때마다 새 vector store를 만들고 문서를 업로드하지 않습니다. 대신 vector store를 한 번 만들고 잠재적으로 수천 개의 문서를 업로드한 다음 store를 Agent에 연결합니다.

[vector store](https://en.wikipedia.org/wiki/Vector_database){:target="_blank"}는 vectors(벡터, 텍스트 데이터의 수치 표현)를 저장하고 검색하는 데 최적화된 데이터베이스입니다. File Search tool은 업로드된 문서에서 관련 정보를 검색하기 위해 [semantic search](https://en.wikipedia.org/wiki/Semantic_search){:target="_blank"}(의미론적 검색)를 위한 vector store를 사용합니다.

## 실습 과제

1. VS Code에서 **shared/datasheet/contoso-tents-datasheet.pdf** 파일을 엽니다. PDF 파일에는 Contoso가 판매하는 텐트에 대한 상세한 제품 설명이 포함되어 있습니다.

2. 파일 내용을 **검토**하여 포함된 정보를 이해하세요. 이는 Agent의 응답을 grounding하는 데 사용됩니다.

=== "Python"

      1. `main.py` 파일을 엽니다.

      2. **"# "** 문자를 제거하여 다음 줄의 **주석을 해제**합니다.

        ```python
        # INSTRUCTIONS_FILE = "instructions/file_search.txt"

        # vector_store = await utilities.create_vector_store(
        #     agent_client,
        #     files=[TENTS_DATA_SHEET_FILE],
        #     vector_name_name="Contoso Product Information Vector Store",
        # )
        # file_search_tool = FileSearchTool(vector_store_ids=[vector_store.id])
        # toolset.add(file_search_tool)
        ```

        !!! warning
            주석을 해제할 줄은 인접하지 않습니다. # 문자를 제거할 때 그 뒤에 있는 공백도 삭제해야 합니다.

      3. `main.py` 파일의 코드를 검토합니다.

        주석 해제 후 코드는 다음과 같아야 합니다:

        ```python
        INSTRUCTIONS_FILE = "instructions/function_calling.txt"
        INSTRUCTIONS_FILE = "instructions/file_search.txt"
        # INSTRUCTIONS_FILE = "instructions/code_interpreter.txt"
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
            # code_interpreter = CodeInterpreterTool()
            # toolset.add(code_interpreter)

            # Add multilingual support to the code interpreter
            # font_file_info = await utilities.upload_file(agents_client, utilities.shared_files_path / FONTS_ZIP)
            # code_interpreter.add_file(file_id=font_file_info.id)

            return font_file_info
        ```

=== "C#"

      1. `Program.cs` 파일을 엽니다.
      2. `Lab3` 클래스를 사용하도록 lab 생성을 **업데이트**합니다.

          ```csharp
          await using Lab lab = new Lab2(projectClient, apiDeploymentName);
          ```

      3. `Lab3.cs` 클래스를 검토하여 `InitialiseLabAsync`가 PDF를 vector store에 추가하고 Agent에 File Search tool을 추가하는 방법과 `InitialiseToolResources`가 Agent에 File Search tool을 추가하는 방법을 확인하세요. 이러한 메서드는 프로세스를 관찰하기 위한 breakpoint를 설정하기 좋은 위치입니다.

## Instructions 검토하기

1. **utilities.py** 파일의 **create_vector_store** 함수를 검토합니다. create_vector_store 함수는 Tents Data Sheet를 업로드하고 vector store에 저장합니다.

    VS Code 디버거 사용에 익숙하다면, **create_vector_store** 함수에 [breakpoint](https://code.visualstudio.com/Docs/editor/debugging){:target="_blank"}를 설정하여 vector store가 생성되는 방법을 관찰하세요.

2. **shared/instructions/file_search.txt** 파일을 엽니다.

    이전 단계에서 사용한 것과 비교하여 instructions 파일의 **Tools** 섹션의 업데이트를 검토합니다.


## Agent 앱 실행하기

1. <kbd>F5</kbd>를 눌러 앱을 실행합니다.
1. 터미널에서 앱이 시작되며, Agent 앱이 **Enter your query**(쿼리 입력)를 요청할 것입니다.

### Agent와 대화 시작하기

다음 대화는 Contoso sales database와 업로드된 Tents Data Sheet의 데이터를 모두 사용하므로 쿼리에 따라 결과가 달라집니다.

1. **What brands of tents do we sell?**

    Agent는 Tents Data Sheet에 언급된 고유한 텐트 브랜드 목록으로 응답합니다.

    !!! info
        이전 실습과 비교하여 Agent의 동작이 어떻게 변경되었는지 관찰하세요. Agent는 이제 제공된 데이터 시트를 참조하여 브랜드, 설명, 제품 유형 및 카테고리와 같은 세부 정보에 액세스하고 이 데이터를 Contoso sales database와 연결할 수 있습니다.

1. **What brands of hiking shoes do we sell?**

    !!! info
        하이킹 신발에 대한 정보를 포함하는 파일을 Agent에 제공하지 않았습니다. Agent가 vector store에서 검색할 수 없는 정보에 대한 질문을 어떻게 처리하는지 관찰하세요.

1. **What product type and categories are these brands associated with?**

    Agent는 텐트 브랜드와 관련된 제품 유형 및 카테고리 목록을 제공합니다.

1. **What were the sales of tents in 2024 by product type? Include the brands associated with each.**

    !!! info
        Agent가 이를 잘못 처리하여 AlpineGear에 Family Camping 텐트가 있다고 잘못 제안할 수 있습니다. 이를 해결하려면 instructions나 datasheet에 추가 context를 제공하거나 다음 프롬프트와 같이 Agent에 직접 context를 제공할 수 있습니다. 예를 들어 다음을 시도해 보세요:
        "**Contoso does not sell Family Camping tents from AlpineGear. Try again.**"

1. **What were the sales of AlpineGear in 2024 by region?**

    Agent는 Contoso sales database의 판매 데이터로 응답합니다.

    !!! info
        Agent는 이를 "CAMPING & HIKING" 카테고리의 모든 텐트 판매를 찾는 요청으로 해석합니다. 이는 이제 Alpine Gear가 backpacking tent의 브랜드라는 정보에 액세스할 수 있기 때문입니다.

1. **Show sales by region as a pie chart**

    우리 Agent는 아직 차트를 만들 수 없습니다... 다음 실습에서 이를 수정하겠습니다.

## Agent 앱 중지하기

완료되면 **exit**를 입력하여 Agent 리소스를 정리하고 앱을 중지하세요.
