# Azure AI Foundry로 코드 우선(code-first) Agent 구축하기

이 리포지토리는 75분 워크숍인 "Azure AI Foundry로 코드 우선 Agent 구축하기"의 콘텐츠와 샘플 코드를 포함하고 있습니다. 이 리포지토리를 사용하여 워크숍을 직접 체험해 보실 수 있습니다. [Microsoft AI Tour](https://aitour.microsoft.com/)와 같은 실습 환경에서 이 워크숍을 진행하는 방법에 대한 정보는 [이 리포지토리](https://github.com/microsoft/aitour-build-your-first-agent-with-azure-ai-agent-service)를 참조하세요.

## 워크숍 개요

여러분이 아웃도어 장비를 판매하는 다국적 소매 회사인 Contoso의 영업 관리자라고 상상해 보세요. 트렌드를 파악하고, 고객 선호도를 이해하며, 정보에 기반한 비즈니스 의사결정을 내리기 위해 판매 데이터를 분석해야 합니다. 이를 돕기 위해 Contoso는 판매 데이터에 대한 질문에 답변할 수 있는 대화형 Agent(에이전트)를 개발했습니다.

### 배우게 될 내용

이 워크숍을 마치면, Azure AI Foundry Agent Service를 사용하여 Agent 앱을 구축하고, 다양한 도구를 탐색하며, LLM(대규모 언어 모델)을 효과적으로 가이드하기 위한 instructions(지시사항)을 사용하는 방법을 배우게 됩니다.

## 워크숍 가이드

이 워크숍을 시작하려면 [Azure AI Foundry로 코드 우선 Agent 구축하기](https://aka.ms/agent-service-workshop-docs) 워크숍 가이드를 열어주세요.

워크숍 가이드 수정에 대한 정보는 [docs/README.md](docs/README.md)를 참조하세요.

## 사전 준비사항

이 워크숍에 참여하려면 다음이 필요합니다:

1. Azure 구독에 대한 액세스 권한. Azure 구독이 없다면, 시작하기 전에 [무료 계정](https://azure.microsoft.com/free/)을 만드세요.
1. GitHub 계정과 GitHub Codespaces. GitHub 계정이 없다면 [GitHub](https://github.com/join)에서 계정을 만드세요. 무료 Codespaces 혜택으로도 이 워크숍을 실행하기에 충분합니다.
1. 워크숍 진행 동안 필요한 Azure 리소스를 배포하기에 충분한 Azure 크레딧과 할당량. 일반적인 워크숍 진행 시 USD $1.00 미만의 사용량이 필요합니다. 자세한 내용은 워크숍 가이드의 "솔루션 아키텍처" 섹션에서 확인할 수 있습니다.

## 중요한 보안 공지

이 템플릿, 애플리케이션 코드 및 구성은 Microsoft Azure의 특정 서비스와 도구를 소개하기 위해 만들어졌습니다. 추가 보안 기능을 구현하거나 활성화하지 않고 이 코드를 프로덕션 환경의 일부로 사용하지 않을 것을 강력히 권장합니다.

Intelligent Applications(지능형 애플리케이션)에 대한 모범 사례 및 보안 권장 사항의 포괄적인 목록은 [공식 문서](https://learn.microsoft.com/azure/developer/ai/get-started-securing-your-ai-app)를 참조하세요.

> [!WARNING]
>
> **이 리포지토리에서 사용된 일부 기능은 미리 보기 상태입니다.** 미리 보기 버전은 서비스 수준 계약 없이 제공되며 프로덕션 워크로드에는 권장되지 않습니다. 특정 기능이 지원되지 않거나 제한된 기능을 가질 수 있습니다. 자세한 내용은 [Microsoft Azure 미리 보기에 대한 추가 사용 약관](https://azure.microsoft.com/en-us/support/legal/preview-supplemental-terms/)을 참조하세요.

**이 프로젝트에는 샘플 애플리케이션 코드가 포함되어 있습니다**. 이 앱 코드를 사용하거나 수정할 수 있으며, 또는 제거하고 자신만의 코드를 포함시킬 수도 있습니다.

## 기여하기

이 워크숍에 대한 여러분의 의견과 제안을 환영합니다! 발견한 문제나 개선 제안 사항이 있다면 이 리포지토리에 issue로 보고해 주세요.

이 프로젝트는 기여와 제안을 환영합니다. 대부분의 기여는 여러분이 기여할 권리가 있으며 실제로 기여에 대한 권리를 우리에게 부여한다는 것을 선언하는 기여자 라이선스 계약(CLA)에 동의해야 합니다. 자세한 내용은 https://cla.opensource.microsoft.com을 방문하세요.

Pull Request를 제출하면 CLA 봇이 자동으로 CLA 제공 여부를 결정하고 PR을 적절하게 장식합니다(예: 상태 확인, 코멘트). 봇이 제공하는 지침을 따르기만 하면 됩니다. CLA를 사용하는 모든 리포지토리에서 한 번만 수행하면 됩니다.

이 프로젝트는 [Microsoft 오픈 소스 행동 강령](https://opensource.microsoft.com/codeofconduct/)을 채택했습니다.
자세한 내용은 [행동 강령 FAQ](https://opensource.microsoft.com/codeofconduct/faq/)를 참조하거나
추가 질문이나 의견이 있는 경우 [opencode@microsoft.com](mailto:opencode@microsoft.com)으로 문의하세요.

## 상표

이 프로젝트에는 프로젝트, 제품 또는 서비스에 대한 상표나 로고가 포함될 수 있습니다. Microsoft 상표 또는 로고의 승인된 사용은
[Microsoft의 상표 및 브랜드 가이드라인](https://www.microsoft.com/en-us/legal/intellectualproperty/trademarks/usage/general)을 따라야 합니다.
이 프로젝트의 수정된 버전에서 Microsoft 상표 또는 로고를 사용하는 것은 혼란을 야기하거나 Microsoft의 후원을 암시해서는 안 됩니다.
제3자 상표 또는 로고의 사용은 해당 제3자의 정책을 따릅니다.
