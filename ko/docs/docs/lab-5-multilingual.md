## 소개

Grounding with Documents(문서를 통한 접지) 실습에서는 대화의 context(맥락)를 제공하기 위해 PDF 파일을 업로드했습니다. 이제 다국어 시각화를 위한 폰트가 포함된 ZIP 파일을 업로드하여 Code Interpreter를 향상시킬 것입니다. 이는 [file uploads](https://learn.microsoft.com/azure/ai-services/agents/how-to/tools/code-interpreter){:target="_blank"}가 기능을 확장할 수 있는 방법의 한 예입니다.

!!! note
    Code Interpreter에는 기본적으로 라틴 기반 폰트 세트가 포함되어 있습니다. Code Interpreter는 샌드박스 Python 환경에서 실행되므로 인터넷에서 직접 폰트를 다운로드할 수 없습니다.

## 실습 과제

이전 실습에서는 필요한 폰트 ZIP 파일을 업로드하고 Code Interpreter에 연결하는 것이 시간이 많이 걸리기 때문에 다국어 지원이 포함되지 않았습니다. 이 실습에서는 필요한 폰트를 업로드하여 다국어 지원을 활성화합니다. 또한 확장된 instructions를 사용하여 Code Interpreter를 가이드하는 방법에 대한 몇 가지 팁을 배우게 됩니다.

## 이전 실습 재실행하기

먼저 Code Interpreter가 다국어 텍스트를 어떻게 지원하는지 확인하기 위해 이전 실습을 재실행할 것입니다.

1. <kbd>F5</kbd>를 눌러 Agent 앱을 시작합니다.
2. 터미널에서 앱이 시작되며, Agent 앱이 **Enter your query**(쿼리 입력)를 요청할 것입니다.
3. 다음 질문을 시도해 보세요:

      1. **What were the sales by region for 2022**
      2. **In Korean**
      3. **Show as a pie chart**

작업이 완료되면 pie chart 이미지가 **shared/files** 하위 폴더에 저장됩니다. 시각화를 검토하면 텍스트가 올바르게 렌더링되지 않은 것을 볼 수 있습니다. 이는 Code Interpreter에 비라틴 문자를 렌더링하는 데 필요한 폰트가 없기 때문입니다.

![The image shows korean pie chart without Korean text](media/sales_by_region_2022_pie_chart_korean.png){width=75%}

4. 완료되면 **exit**를 입력하여 Agent 리소스를 정리하고 앱을 중지하세요.

## 다국어 폰트 지원 추가하기

=== "Python"

    1. `main.py`를 엽니다.

    2. Agent를 위한 새로운 instructions 파일을 정의합니다: **"# "** 문자를 제거하여 다음 줄의 **주석을 해제**합니다

        ```python
        INSTRUCTIONS_FILE = "instructions/code_interpreter_multilingual.txt"

        font_file_info = await utilities.upload_file(agent_client, utilities.shared_files_path / FONTS_ZIP)
        code_interpreter.add_file(file_id=font_file_info.id)
        ```

        !!! warning
            주석을 해제할 줄은 인접하지 않습니다. # 문자를 제거할 때 그 뒤에 있는 공백도 삭제해야 합니다.

    3. `main.py` 파일의 코드를 검토합니다.

        주석 해제 후 코드는 다음과 같아야 합니다:

        ```python
        INSTRUCTIONS_FILE = "instructions/function_calling.txt"
        INSTRUCTIONS_FILE = "instructions/file_search.txt"
        INSTRUCTIONS_FILE = "instructions/code_interpreter.txt"
        INSTRUCTIONS_FILE = "instructions/code_interpreter_multilingual.txt"


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
            font_file_info = await utilities.upload_file(agents_client, utilities.shared_files_path / FONTS_ZIP)
            code_interpreter.add_file(file_id=font_file_info.id)

            return font_file_info
        ```

=== "C#"

    1. `Program.cs` 파일을 엽니다.

    2. `Lab5` 클래스를 사용하도록 lab 생성을 **업데이트**합니다.

        ``` csharp
        await using Lab lab = new Lab5(projectClient, apiDeploymentName);
        ```

    3. Code Interpreter가 Tools 목록에 추가되는 방법을 확인하려면 `Lab5.cs` 클래스를 검토하세요.

## Instructions 검토하기

1. **shared/instructions/code_interpreter_multilingual.txt** 파일을 엽니다. 이 파일은 이전 실습에서 사용된 instructions를 대체합니다.
2. **Tools** 섹션에는 이제 시각화를 만들고 비라틴 언어를 처리하는 방법을 설명하는 확장된 "Visualization and Code Interpretation"(시각화 및 코드 해석) 섹션이 포함됩니다.

    다음은 Code Interpreter에 제공된 instructions의 요약입니다:

    - **비라틴 스크립트용 폰트 설정 (예: 아랍어, 일본어, 한국어, 힌디어):**
        - 첫 실행 시 `/mnt/data/fonts` 폴더가 있는지 확인합니다. 없으면 폰트 파일을 이 폴더에 압축 해제합니다.
    - **사용 가능한 폰트:**
        - 아랍어: `CairoRegular.ttf`
        - 힌디어: `NotoSansDevanagariRegular.ttf`
        - 한국어: `NanumGothicRegular.ttf`
        - 일본어: `NotoSansJPRegular.ttf`

    - **폰트 사용법:**
        - 올바른 경로를 사용하여 `matplotlib.font_manager.FontProperties`로 폰트를 로드합니다.
        - 다음에 폰트를 적용합니다:
            - `fontproperties` 매개변수를 사용하여 `plt.title()`에 적용.
            - `plt.pie()` 또는 `plt.bar_label()`과 같은 함수에서 `textprops={'fontproperties': font_prop}`을 사용하여 모든 레이블과 텍스트에 적용.
        - 상자나 물음표 없이 모든 텍스트(레이블, 제목, 범례)가 올바르게 인코딩되었는지 확인합니다.

    - **시각화 텍스트:**
        - 항상 데이터를 요청되거나 추론된 언어(예: 중국어, 프랑스어, 영어)로 번역합니다.
        - 모든 차트 텍스트(예: 제목, 레이블)에 `/mnt/data/fonts/fonts`의 적절한 폰트를 사용합니다.

## Agent 앱 실행하기

1. <kbd>F5</kbd>를 눌러 앱을 실행합니다.
2. 터미널에서 앱이 시작되며, Agent 앱이 **Enter your query**(쿼리 입력)를 요청할 것입니다.

### Agent와 대화 시작하기

다음 질문을 시도해 보세요:

1. **What were the sales by region for 2022**
2. **In Korean**
3. **Show as a pie chart**

    작업이 완료되면 pie chart 이미지가 **shared/files** 하위 폴더에 저장됩니다.

    ![The image shows korean pie chart with Korean text](media/sales_by_region_pie_chart_korean_font.png){width=75%}

## Code Interpreter 디버깅하기

Code Interpreter를 직접 디버깅할 수는 없지만, Agent에게 생성하는 코드를 표시하도록 요청하여 동작에 대한 통찰력을 얻을 수 있습니다. 이를 통해 instructions를 어떻게 해석하는지 이해하고 이를 개선하는 데 도움을 받을 수 있습니다.

터미널에서 다음을 입력하세요:

1. **show code**를 입력하여 마지막 시각화에 대해 Code Interpreter가 생성한 코드를 확인합니다.
1. **list files mounted at /mnt/data**를 입력하여 Code Interpreter에 업로드된 파일을 확인합니다.

## Code Interpreter 출력 제한하기

프로덕션 환경에서는 최종 사용자가 Code Interpreter가 생성한 코드를 보거나 업로드되거나 생성된 파일에 액세스하는 것을 원하지 않을 것입니다. 이를 방지하려면 Code Interpreter가 코드를 표시하거나 파일을 나열하지 못하도록 제한하는 instructions를 추가하세요.

예를 들어, `code_interpreter_multilingual.txt` 파일의 `2. Visualization and Code Interpretation` 섹션 시작 부분에 다음 instructions를 삽입할 수 있습니다.

```text
- Never show the code you generate to the user.
- Never list the files mounted at /mnt/data.
```

## Agent 앱 중지하기

완료되면 **exit**를 입력하여 Agent 리소스를 정리하고 앱을 중지하세요.
