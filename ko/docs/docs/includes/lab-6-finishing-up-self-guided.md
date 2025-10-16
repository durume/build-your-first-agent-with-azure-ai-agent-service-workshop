워크숍의 실습 부분은 여기까지입니다. 주요 요점과 추가 리소스를 계속 읽어보세요. 하지만 먼저 정리해 봅시다.

## GitHub 리포지토리에 Star 표시하기

GitHub 계정이 있다면 이 리포지토리에 "star"를 표시하여 나중에 쉽게 다시 찾을 수 있습니다.

* GitHub 리포지토리 방문: [microsoft/build-your-first-agent-with-azure-ai-agent-service-workshop](https://github.com/microsoft/build-your-first-agent-with-azure-ai-agent-service-workshop){:target="_blank"}
* GitHub 계정에 로그인
* 오른쪽 상단의 **Star**를 클릭

나중에 이 워크숍을 다시 찾으려면 오른쪽 상단의 GitHub 프로필 사진을 클릭하고 **Your stars**를 클릭하세요.

## GitHub CodeSpaces 정리하기

### GitHub에 변경 사항 저장하기

워크숍 중에 파일에 대한 변경 사항을 개인 GitHub 리포지토리에 fork로 저장할 수 있습니다. 이렇게 하면 커스터마이징한 워크숍을 쉽게 다시 실행할 수 있으며, 워크숍 콘텐츠가 항상 GitHub 계정에 남아있습니다.

* VS Code에서 왼쪽 창의 "Source Control" 도구를 클릭합니다. 세 번째 아이콘이거나 키보드 단축키 <kbd>Control-Shift-G</kbd>를 사용할 수 있습니다.
* "Source Control" 아래 필드에 `Agents Lab`을 입력하고 **✔️Commit**을 클릭합니다.
  * "There are no staged changes to commit." 프롬프트에 **Yes**를 클릭합니다.
* **Sync Changes**를 클릭합니다.
  * "This action will pull and push commits from and to origin/main" 프롬프트에 **OK**를 클릭합니다.

이제 커스터마이징한 워크숍의 복사본을 GitHub 계정에 가지고 있습니다.

### GitHub codespace 삭제하기

GitHub CodeSpace는 자동으로 종료되지만 삭제될 때까지 compute 및 storage 할당량의 작은 부분을 소비합니다. (사용량은 [GitHub Billing summary](https://github.com/settings/billing/summary)에서 확인할 수 있습니다.) 이제 codespace를 안전하게 삭제할 수 있습니다:

* [github.com/codespaces](https://github.com/codespaces){:target="_blank"} 방문
* 페이지 하단에서 활성 codespace 오른쪽에 있는 "..." 메뉴 클릭
* **Delete** 클릭
  * "Are you sure?" 프롬프트에서 **Delete** 클릭

## Azure 리소스 삭제하기

이 실습에서 생성한 대부분의 리소스는 사용한 만큼만 지불하는(pay-as-you-go) 리소스이므로 사용한 것에 대한 추가 요금이 청구되지 않습니다. 그러나 AI Foundry에서 사용하는 일부 스토리지 서비스는 작은 지속적인 요금이 발생할 수 있습니다. 모든 리소스를 삭제하려면 다음 단계를 따르세요:

* [Azure Portal](https://portal.azure.com){:target="_blank"} 방문
* **Resource groups** 클릭
* 리소스 그룹 `rg-agent-workshop-****` 클릭
* **Delete Resource group** 클릭
* 하단의 "Enter resource group name to confirm deletion" 필드에 `rg-agent-workshop-****` 입력
* **Delete** 클릭
  * Delete Confirmation 프롬프트에서 "Delete" 클릭
