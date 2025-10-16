from typing import Any

from azure.ai.agents.aio import AgentsClient
from azure.ai.agents.models import (
    AsyncAgentEventHandler,
    AsyncFunctionTool,
    MessageDeltaChunk,
    MessageStatus,
    RunStatus,
    RunStep,
    RunStepDeltaChunk,
    RunStepStatus,
    ThreadMessage,
    ThreadRun,
)

from utilities import Utilities


class StreamEventHandler(AsyncAgentEventHandler[str]):
    """LLM 스트리밍 이벤트와 토큰을 처리합니다."""

    def __init__(self, functions: AsyncFunctionTool, agent_client: AgentsClient, utilities: Utilities) -> None:
        self.functions = functions
        self.agent_client = agent_client
        self.util = utilities
        super().__init__()

    async def on_message_delta(self, delta: MessageDeltaChunk) -> None:
        """메시지 델타 이벤트를 처리합니다. 스트리밍된 토큰이 됩니다."""
        self.util.log_token_blue(delta.text)

    async def on_thread_message(self, message: ThreadMessage) -> None:
        """스레드 메시지 이벤트를 처리합니다."""
        pass
        # if message.status == MessageStatus.COMPLETED:
        #     print()
        # self.util.log_msg_purple(f"ThreadMessage created. ID: {message.id}, " f"Status: {message.status}")

        await self.util.get_files(message, self.agent_client)

    async def on_thread_run(self, run: ThreadRun) -> None:
        """스레드 실행 이벤트를 처리합니다."""

        if run.status == RunStatus.FAILED:
            print(f"Run failed. Error: {run.last_error}")
            print(f"Thread ID: {run.thread_id}")
            print(f"Run ID: {run.id}")

    async def on_run_step(self, step: RunStep) -> None:
        pass
        # if step.status == RunStepStatus.COMPLETED:
        #     print()
        # self.util.log_msg_purple(f"RunStep type: {step.type}, Status: {step.status}")

    async def on_run_step_delta(self, delta: RunStepDeltaChunk) -> None:
        pass

    async def on_error(self, data: str) -> None:
        print(f"An error occurred. Data: {data}")

    async def on_done(self) -> None:
        """스트림 완료를 처리합니다."""
        pass
        # self.util.log_msg_purple(f"\nStream completed.")

    async def on_unhandled_event(self, event_type: str, event_data: Any) -> None:
        """처리되지 않은 이벤트를 처리합니다."""
        # print(f"Unhandled Event Type: {event_type}, Data: {event_data}")
        print(f"Unhandled Event Type: {event_type}")
