# Azure AI Foundry로 코드 우선(code-first) Agent 구축하기

## 75분 인터랙티브 워크숍

여러분이 아웃도어 장비를 판매하는 다국적 소매 회사인 Contoso의 영업 관리자라고 상상해 보세요. 트렌드를 파악하고, 고객 선호도를 이해하며, 정보에 기반한 비즈니스 의사결정을 내리기 위해 판매 데이터를 분석해야 합니다. 이를 돕기 위해 Contoso는 판매 데이터에 대한 질문에 답변할 수 있는 대화형 Agent(에이전트)를 개발했습니다.

![Contoso Sales Analysis Agent](../../../docs/docs/media/persona.png)

## LLM 기반 AI Agent란 무엇인가요?

Large Language Model(LLM, 대규모 언어 모델) 기반 AI Agent는 사전에 정의된 단계나 프로세스 없이 주어진 목표를 달성하도록 설계된 반자율적 소프트웨어입니다. 명시적으로 프로그래밍된 지침을 따르는 대신, Agent는 instructions(지시사항)과 context(맥락)를 사용하여 작업을 수행하는 방법을 스스로 결정합니다.

예를 들어, 사용자가 "**지역별 총 판매액을 원형 차트로 표시해줘**"라고 요청하면, 앱은 이 요청에 대해 미리 정의된 로직에 의존하지 않습니다. 대신, LLM이 요청을 해석하고, 대화 흐름과 맥락을 관리하며, 지역별 판매 원형 차트를 생성하는 데 필요한 작업을 조율(orchestrate)합니다.

비즈니스 프로세스를 지원하기 위해 개발자가 로직과 워크플로우를 정의하는 전통적인 애플리케이션과 달리, AI Agent는 이 책임을 LLM에 전가합니다. 이러한 시스템에서는 prompt engineering(프롬프트 엔지니어링), 명확한 instructions(지시사항), 그리고 tool development(도구 개발)가 앱이 의도한 대로 작동하도록 보장하는 데 매우 중요합니다.

## Azure AI Foundry 소개

[Azure AI Foundry](https://azure.microsoft.com/products/ai-foundry/){:target="_blank"}는 AI 앱과 Agent를 설계, 커스터마이징 및 관리하기 위한 Microsoft의 안전하고 유연한 플랫폼입니다. 모델, Agent, 도구 및 observability(관찰 가능성) 등 모든 것이 단일 포털, SDK 및 REST endpoint 뒤에 있어, 첫날부터 거버넌스와 비용 통제를 갖춘 상태로 클라우드나 엣지에 배포할 수 있습니다.

![Azure AI Foundry Architecture](../../../docs/docs/media/azure-ai-foundry.png)

## Foundry Agent Service란 무엇인가요?

Foundry Agent Service는 [Python](https://learn.microsoft.com/azure/ai-services/agents/quickstart?pivots=programming-language-python-azure){:target="_blank"}, [C#](https://learn.microsoft.com/azure/ai-services/agents/quickstart?pivots=programming-language-csharp){:target="_blank"}, [TypeScript](https://learn.microsoft.com/en-us/azure/ai-foundry/agents/quickstart?pivots=programming-language-typescript){:target="_blank"}용 SDK를 제공하는 완전 관리형 클라우드 서비스입니다. 이는 AI Agent 개발을 단순화하여 function calling(함수 호출)과 같은 복잡한 작업을 몇 줄의 코드로 줄입니다.

!!! info
    Function calling(함수 호출)을 사용하면 LLM을 외부 도구 및 시스템에 연결할 수 있습니다. 이는 AI Agent에 기능을 부여하거나 애플리케이션과 LLM 간의 깊은 통합을 구축하는 등 여러 가지에 유용합니다.

Foundry Agent Service는 전통적인 Agent 플랫폼에 비해 여러 가지 장점을 제공합니다:

- **신속한 배포**: 빠른 배포를 위해 최적화된 SDK로, 개발자가 Agent 구축에 집중할 수 있게 합니다.
- **확장성**: 성능 문제 없이 다양한 사용자 로드를 처리하도록 설계되었습니다.
- **커스텀 통합**: Agent 기능을 확장하기 위한 Function Calling을 지원합니다.
- **내장 도구**: 빠른 개발을 위해 Fabric, SharePoint, Azure AI Search, Azure Storage를 포함합니다.
- **RAG 스타일 검색**: 효율적인 파일 및 의미론적 검색을 위한 내장 vector store(벡터 저장소)를 제공합니다.
- **대화 상태 관리**: 여러 상호작용에 걸쳐 context(맥락)을 유지합니다.
- **AI 모델 호환성**: 다양한 AI 모델과 함께 작동합니다.

Foundry Agent Service에 대한 자세한 내용은 [Foundry Agent Service 문서](https://learn.microsoft.com/azure/ai-services/agents/overview){:target="_blank"}에서 확인하세요.

## AI Agent Frameworks(프레임워크)

인기 있는 Agent 프레임워크에는 LangChain, Semantic Kernel, CrewAI가 있습니다. Foundry Agent Service를 구별하는 것은 원활한 통합 기능과 신속한 배포에 최적화된 SDK입니다. 복잡한 멀티 Agent 시나리오에서는 Semantic Kernel 및 AutoGen과 같은 SDK를 Foundry Agent Service와 결합하여 견고하고 확장 가능한 시스템을 구축합니다.
