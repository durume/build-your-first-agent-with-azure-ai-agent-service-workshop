# 보안 고려사항

이 워크숍 애플리케이션은 교육 및 적응을 위해 설계되었으며, 그대로 프로덕션 환경에 사용하기 위한 것이 아닙니다. 그럼에도 불구하고 보안을 위한 몇 가지 모범 사례를 시연합니다.

## 악의적인 SQL 공격

LLM에 의해 동적으로 생성되는 SQL과 관련된 일반적인 우려는 보안, 특히 SQL injection(SQL 인젝션)이나 데이터베이스를 삭제하거나 변조하는 것과 같은 악의적인 행위의 위험입니다. 이러한 우려는 타당하지만 데이터베이스 액세스 권한을 적절히 구성함으로써 효과적으로 완화될 수 있습니다.

이 앱은 읽기 전용으로 구성된 SQLite 데이터베이스를 사용합니다. PostgreSQL이나 Azure SQL과 같은 데이터베이스 서비스의 경우, 앱에 읽기 전용(SELECT) 역할을 할당해야 합니다. 안전한 환경에서 앱을 실행하면 보호가 더욱 강화됩니다.

엔터프라이즈 시나리오에서는 일반적으로 데이터가 운영 시스템에서 추출되어 사용자 친화적인 스키마를 가진 읽기 전용 데이터베이스 또는 데이터 웨어하우스로 변환됩니다. 이 접근 방식은 데이터가 안전하고 성능과 접근성에 최적화되어 있으며 앱이 제한된 읽기 전용 액세스 권한을 갖도록 보장합니다.

## Sandboxing(샌드박스)

이는 [Azure AI Agents Service Code Interpreter](https://learn.microsoft.com/azure/ai-services/agents/how-to/tools/code-interpreter?view=azure-python-preview&tabs=python&pivots=overview){:target="_blank"}를 사용하여 필요에 따라 코드를 생성하고 실행합니다. 코드는 Agent의 범위를 벗어난 작업을 수행하는 것을 방지하기 위해 샌드박스 실행 환경에서 실행됩니다.
