# 솔루션 아키텍처

이 워크숍에서는 판매 데이터에 대한 질문에 답변하고, 차트를 생성하며, 추가 분석을 위한 데이터 파일을 다운로드할 수 있도록 설계된 대화형 Agent인 Contoso Sales Agent를 만들 것입니다.

## Agent 앱의 구성 요소

1. **Microsoft Azure 서비스**

    이 Agent는 Microsoft Azure 서비스를 기반으로 구축되었습니다.

      - **Generative AI 모델**: 이 앱을 구동하는 기본 LLM은 [Azure OpenAI gpt-4o-mini](https://learn.microsoft.com/azure/ai-services/openai/concepts/models?tabs=global-standard%2Cstandard-chat-completions#gpt-4o-mini-and-gpt-4-turbo){:target="_blank"} LLM입니다.

      - **Vector Store(벡터 저장소)**: Agent가 쿼리를 지원할 수 있도록 제품 정보를 PDF 파일로 제공합니다. Agent는 [Foundry Agent Service file search tool](https://learn.microsoft.com/azure/ai-services/agents/how-to/tools/file-search?tabs=python&pivots=overview){:target="_blank"}의 "basic agent setup"을 사용하여 vector search(벡터 검색)로 문서의 관련 부분을 찾고 이를 context(맥락)로 Agent에게 제공합니다.

      - **Control Plane(제어 평면)**: 앱과 아키텍처 구성 요소는 브라우저를 통해 액세스할 수 있는 [Azure AI Foundry](https://ai.azure.com){:target="_blank"} 포털을 사용하여 관리 및 모니터링됩니다.

2. **Azure AI Foundry (SDK)**

    워크숍은 Azure AI Foundry SDK를 사용하여 [Python](https://learn.microsoft.com/python/api/overview/azure/ai-projects-readme?view=azure-python-preview&context=%2Fazure%2Fai-services%2Fagents%2Fcontext%2Fcontext){:target="_blank"}과 [C#](https://learn.microsoft.com/en-us/dotnet/api/overview/azure/ai.projects-readme?view=azure-dotnet-preview&viewFallbackFrom=azure-python-preview){:target="_blank"} 모두에서 제공됩니다. SDK는 [Code Interpreter](https://learn.microsoft.com/azure/ai-services/agents/how-to/tools/code-interpreter?view=azure-python-preview&tabs=python&pivots=overview){:target="_blank"}와 [Function Calling](https://learn.microsoft.com/azure/ai-services/agents/how-to/tools/function-calling?view=azure-python-preview&tabs=python&pivots=overview){:target="_blank"}을 포함한 Azure AI Agents 서비스의 주요 기능을 지원합니다.

3. **Database(데이터베이스)**

    이 앱은 40,000개의 합성 데이터 행을 포함하는 [SQLite 데이터베이스](https://www.sqlite.org/){:target="_blank"}인 Contoso Sales Database를 기반으로 합니다. 시작 시 Agent 앱은 판매 데이터베이스 스키마, 제품 카테고리, 제품 유형 및 보고 연도를 읽은 다음 이 메타데이터를 Foundry Agent Service의 instruction context(지시사항 맥락)에 통합합니다.

## 워크숍 솔루션 확장하기

워크숍 솔루션은 데이터베이스를 수정하고 Foundry Agent Service instructions(지시사항)을 특정 사용 사례에 맞게 조정함으로써 고객 지원과 같은 다양한 시나리오에 매우 적응 가능합니다. 의도적으로 인터페이스에 구애받지 않도록 설계되어 AI Agent Service의 핵심 기능에 집중하고 기본 개념을 적용하여 자신만의 대화형 Agent를 구축할 수 있습니다.

## 앱에서 시연되는 모범 사례

앱은 또한 효율성과 사용자 경험을 위한 몇 가지 모범 사례를 시연합니다.

- **Asynchronous APIs(비동기 API)**:
  워크숍 샘플에서 Foundry Agent Service와 SQLite는 모두 비동기 API를 사용하여 리소스 효율성과 확장성을 최적화합니다. 이러한 설계 선택은 FastAPI, ASP.NET, Chainlit 또는 Streamlit과 같은 비동기 웹 프레임워크로 애플리케이션을 배포할 때 특히 유리합니다.

- **Token Streaming(토큰 스트리밍)**:
  Token streaming은 LLM 기반 Agent 앱의 체감 응답 시간을 줄여 사용자 경험을 개선하기 위해 구현되었습니다.
