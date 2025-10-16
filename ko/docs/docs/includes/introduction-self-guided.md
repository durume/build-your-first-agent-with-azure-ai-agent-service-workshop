## 자기 주도 학습자

이 지침은 사전 구성된 랩 환경에 액세스할 수 없는 자기 주도 학습자를 위한 것입니다. 다음 단계에 따라 환경을 설정하고 워크샵을 시작하세요.

## 소개

이 워크샵은 Azure AI Agents Service (에이전트 서비스) 및 관련 SDK에 대해 알려드리기 위해 설계되었습니다. 여러 랩으로 구성되어 있으며 각 랩은 Azure AI Agents Service의 특정 기능을 강조합니다. 각 랩은 이전 랩의 지식과 작업을 기반으로 하므로 순서대로 완료해야 합니다.

## 필수 조건

1. Azure 구독에 대한 액세스 권한. Azure 구독이 없는 경우 시작하기 전에 [무료 계정](https://azure.microsoft.com/free/){:target="_blank"}을 만드세요.
1. GitHub 계정이 필요합니다. 계정이 없는 경우 [GitHub](https://github.com/join){:target="_blank"}에서 만드세요.

## 워크샵 프로그래밍 언어 선택

워크샵은 Python과 C# 모두에서 사용할 수 있습니다. 언어 선택기 탭을 사용하여 선호하는 언어를 선택하세요. 참고: 워크샵 중간에 언어를 전환하지 마세요.

**선호하는 언어의 탭을 선택하세요:**

=== "Python"
    워크샵의 기본 언어는 **Python**으로 설정되어 있습니다.
=== "C#"
    워크샵의 기본 언어는 **C#**으로 설정되어 있습니다.

## 워크샵 열기

이 워크샵을 실행하는 권장 방법은 GitHub Codespaces를 사용하는 것입니다. 이 옵션은 워크샵을 완료하는 데 필요한 모든 도구와 리소스가 포함된 사전 구성된 환경을 제공합니다. 또는 Visual Studio Code Dev Container를 사용하여 로컬에서 워크샵을 열 수 있습니다.

=== "GitHub Codespaces"

    **Open in GitHub Codespaces**를 선택하여 GitHub Codespaces에서 프로젝트를 엽니다.

    [![Open in GitHub Codespaces](https://github.com/codespaces/badge.svg)](https://codespaces.new/microsoft/build-your-first-agent-with-azure-ai-agent-service-workshop){:target="_blank"}

    !!! Warning "Codespace를 빌드하는 데 몇 분이 걸립니다. 빌드하는 동안 지침을 계속 읽을 수 있습니다."

=== "VS Code Dev Container"

    !!! warning "Apple Silicon 사용자"
        곧 실행할 자동화된 배포 스크립트는 Apple Silicon에서 지원되지 않습니다. Dev Container 대신 Codespaces 또는 macOS에서 배포 스크립트를 실행하세요.

    또는 Visual Studio Code Dev Container를 사용하여 프로젝트를 로컬에서 열 수 있습니다. 이렇게 하면 [Dev Containers 확장](https://marketplace.visualstudio.com/items?itemName=ms-vscode-remote.remote-containers){:target="_blank"}을 사용하여 로컬 VS Code 개발 환경에서 프로젝트가 열립니다.

    1. Docker Desktop을 시작합니다 (아직 설치하지 않은 경우 설치하세요)
    2. **Dev Containers Open**을 선택하여 VS Code Dev Container에서 프로젝트를 엽니다.

        [![Open in Dev Containers](https://img.shields.io/static/v1?style=for-the-badge&label=Dev%20Containers&message=Open&color=blue&logo=visualstudiocode)](https://vscode.dev/redirect?url=vscode://ms-vscode-remote.remote-containers/cloneInVolume?url=https://github.com/microsoft/build-your-first-agent-with-azure-ai-agent-service-workshop)

    !!! Warning "Dev Container를 빌드하는 과정(다운로드 및 로컬 시스템에 설정)은 몇 분이 걸립니다. 이 시간 동안 지침을 계속 읽을 수 있습니다."

## Azure 인증

에이전트 앱이 Azure AI Agents Service 및 모델에 액세스할 수 있도록 Azure로 인증해야 합니다. 다음 단계를 따르세요:

1. Codespace가 생성되었는지 확인합니다.
1. Codespace에서 **Terminal** > **New Terminal**을 **VS Code 메뉴**에서 선택하여 새 터미널 창을 엽니다.
1. 다음 명령을 실행하여 Azure로 인증합니다:

    ```shell
    az login --use-device-code
    ```

    !!! note
        브라우저 링크를 열고 Azure 계정에 로그인하라는 메시지가 표시됩니다. 먼저 인증 코드를 복사하세요.

        1. 브라우저 창이 자동으로 열리면 계정 유형을 선택하고 **다음**을 클릭합니다.
        2. Azure 구독 **Username**과 **Password**로 로그인합니다.
        3. 인증 코드를 **붙여넣기**합니다.
        4. **확인**을 선택한 다음 **완료**를 선택합니다.

    !!! warning
        여러 Azure 테넌트가 있는 경우 인증할 때 적절한 테넌트를 선택해야 합니다.

        ```shell
        az login --use-device-code --tenant <tenant_id>
        ```

1. 다음으로 명령줄에서 적절한 구독을 선택합니다.
1. 다음 단계를 위해 터미널 창을 열어 두세요.

## Azure 리소스 배포

다음 리소스는 Azure 구독의 **rg-contoso-agent-workshop-nnnn** 리소스 그룹에 생성됩니다.

- **fdy-contoso-agent-nnnn**이라는 **Azure AI Foundry 허브**
- **prj-contoso-agent-nnnn**이라는 **Azure AI Foundry 프로젝트**
- **gpt-4o-mini**라는 **Serverless (종량제) GPT-4o-mini 모델 배포**. 가격 세부 정보는 [여기](https://azure.microsoft.com/pricing/details/cognitive-services/openai-service/){:target="_blank"}를 참조하세요.

!!! warning "에이전트가 많은 토큰을 사용하기 때문이 아니라 에이전트가 모델에 대해 수행하는 호출 빈도 때문에 gpt-4o-mini Global Standard SKU에 대해 120K TPM 할당량 가용성이 필요합니다. [AI Foundry Management Center](https://ai.azure.com/managementCenter/quota){:target="_blank"}에서 할당량 가용성을 검토하세요."

워크샵에 필요한 리소스 배포를 자동화하는 bash 스크립트를 제공했습니다.

`deploy.sh` 스크립트는 기본적으로 `westus` 지역에 배포합니다. 지역 또는 리소스 이름을 변경하려면 파일을 편집하세요. 스크립트를 실행하려면 VS Code 터미널을 열고 다음 명령을 실행합니다:

```bash
cd infra && ./deploy.sh
```

### 워크샵 구성

=== "Python"

    배포 스크립트는 프로젝트 엔드포인트와 모델 배포 이름이 포함된 **.env** 파일을 생성합니다.

    VS Code에서 Python 작업 공간을 열면 이 파일을 볼 수 있습니다. **.env** 파일은 다음과 유사하지만 본인의 프로젝트 엔드포인트가 포함됩니다.

    ```python
    MODEL_DEPLOYMENT_NAME="gpt-4o-mini"
    PROJECT_ENDPOINT="<your_project_endpoint>"
    ```
=== "C#"

    자동화된 배포 스크립트는 [ASP.NET Core의 개발에서 앱 시크릿의 안전한 저장](https://learn.microsoft.com/aspnet/core/security/app-secrets){:target="_blank"}을 위한 Secret Manager 기능을 사용하여 프로젝트 변수를 안전하게 저장합니다.

    C# 작업 공간을 VS Code에서 연 후 다음 명령을 실행하여 시크릿을 볼 수 있습니다:

    ```bash
    dotnet user-secrets list
    ```

## 언어 작업 공간 선택

워크샵에는 Python용과 C#용 두 개의 작업 공간이 있습니다. 작업 공간에는 각 언어에 대한 랩을 완료하는 데 필요한 소스 코드 및 모든 파일이 포함되어 있습니다. 작업하려는 언어와 일치하는 작업 공간을 선택하세요.

=== "Python"

    1. Visual Studio Code에서 **File** > **Open Workspace from File**로 이동합니다.
    2. 기본 경로를 다음으로 바꿉니다:

        ```text
        /workspaces/build-your-first-agent-with-azure-ai-agent-service-workshop/.vscode/
        ```

    3. **python-workspace.code-workspace**라는 파일을 선택하여 작업 공간을 엽니다.

    ## 프로젝트 구조

    워크샵 전체에서 작업할 주요 **폴더** 및 **파일**을 숙지하세요.

    ### workshop 폴더

    - **main.py** 파일: 앱의 진입점으로 주요 로직이 포함되어 있습니다.
    - **sales_data.py** 파일: SQLite 데이터베이스에 대해 동적 SQL 쿼리를 실행하는 함수 로직입니다.
    - **stream_event_handler.py** 파일: 토큰 스트리밍을 위한 이벤트 핸들러 로직이 포함되어 있습니다.

    ### shared 폴더

    - **files** 폴더: 에이전트 앱에서 생성한 파일이 포함되어 있습니다.
    - **fonts** 폴더: Code Interpreter (코드 인터프리터)에서 사용하는 다국어 글꼴이 포함되어 있습니다.
    - **instructions** 폴더: LLM (대규모 언어 모델)에 전달되는 지침이 포함되어 있습니다.

    ![Lab folder structure](../media/project-structure-self-guided-python.png)

=== "C#"

    1. Visual Studio Code에서 **File** > **Open Workspace from File**로 이동합니다.
    2. 기본 경로를 다음으로 바꿉니다:

        ```text
        /workspaces/build-your-first-agent-with-azure-ai-agent-service-workshop/.vscode/
        ```

    3. **csharp-workspace.code-workspace**라는 파일을 선택하여 작업 공간을 엽니다.

    ## 프로젝트 구조

    워크샵 전체에서 작업할 주요 **폴더** 및 **파일**을 숙지하세요.

    ### workshop 폴더

    - **Lab1.cs, Lab2.cs, Lab3.cs** 파일: 각 랩의 진입점으로 에이전트 로직이 포함되어 있습니다.
    - **Program.cs** 파일: 앱의 진입점으로 주요 로직이 포함되어 있습니다.
    - **SalesData.cs** 파일: SQLite 데이터베이스에 대해 동적 SQL 쿼리를 실행하는 함수 로직입니다.

    ### shared 폴더

    - **files** 폴더: 에이전트 앱에서 생성한 파일이 포함되어 있습니다.
    - **fonts** 폴더: Code Interpreter (코드 인터프리터)에서 사용하는 다국어 글꼴이 포함되어 있습니다.
    - **instructions** 폴더: LLM (대규모 언어 모델)에 전달되는 지침이 포함되어 있습니다.

    ![Lab folder structure](../media/project-structure-self-guided-csharp.png)
