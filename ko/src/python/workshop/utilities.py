from pathlib import Path

from azure.ai.agents.aio import AgentsClient
from azure.ai.agents.models import ThreadMessage

from terminal_colors import TerminalColors as tc


class Utilities:
    # 공유 파일의 상대 경로를 가져오는 속성
    @property
    def shared_files_path(self) -> Path:
        """공유 파일 디렉토리 경로를 가져옵니다."""
        return Path(__file__).parent.parent.parent.resolve() / "shared"

    def load_instructions(self, instructions_file: str) -> str:
        """파일에서 지시사항을 로드합니다."""
        file_path = self.shared_files_path / instructions_file
        with file_path.open("r", encoding="utf-8", errors="ignore") as file:
            return file.read()

    def log_msg_green(self, msg: str) -> None:
        """녹색으로 메시지를 출력합니다."""
        print(f"{tc.GREEN}{msg}{tc.RESET}")

    def log_msg_purple(self, msg: str) -> None:
        """보라색으로 메시지를 출력합니다."""
        print(f"{tc.PURPLE}{msg}{tc.RESET}")

    def log_token_blue(self, msg: str) -> None:
        """파란색으로 토큰을 출력합니다."""
        print(f"{tc.BLUE}{msg}{tc.RESET}", end="", flush=True)

    async def get_file(self, agents_client: AgentsClient, file_id: str, attachment_name: str) -> None:
        """파일을 검색하여 로컬 디스크에 저장합니다."""
        self.log_msg_green(f"Getting file with ID: {file_id}")

        attachment_part = attachment_name.split(":")[-1]
        file_name = Path(attachment_part).stem
        file_extension = Path(attachment_part).suffix
        if not file_extension:
            file_extension = ".png"
        file_name = f"{file_name}.{file_id}{file_extension}"

        folder_path = Path(self.shared_files_path) / "files"
        folder_path.mkdir(parents=True, exist_ok=True)
        file_path = folder_path / file_name

        # 동기 컨텍스트 관리자를 사용하여 파일 저장
        with file_path.open("wb") as file:
            async for chunk in await agents_client.files.get_content(file_id):
                file.write(chunk)

        self.log_msg_green(f"File saved to {file_path}")

    async def get_files(self, message: ThreadMessage, agent_client: AgentsClient) -> None:
        """메시지에서 이미지 파일을 가져와 다운로드를 시작합니다."""
        if message.image_contents:
            for index, image in enumerate(message.image_contents, start=0):
                attachment_name = (
                    "unknown" if not message.file_path_annotations else message.file_path_annotations[index].text + ".png"
                )
                await self.get_file(agent_client, image.image_file.file_id, attachment_name)
        elif message.attachments:
            for index, attachment in enumerate(message.attachments, start=0):
                attachment_name = (
                    "unknown" if not message.file_path_annotations else message.file_path_annotations[index].text
                )
                if attachment.file_id:
                    await self.get_file(agent_client, attachment.file_id, attachment_name)

    async def upload_file(self, agents_client: AgentsClient, file_path: Path, purpose: str = "assistants"):
        """프로젝트에 파일을 업로드합니다."""
        self.log_msg_purple(f"Uploading file: {file_path}")
        file_info = await agents_client.files.upload(file_path=str(file_path), purpose=purpose)
        self.log_msg_purple(f"File uploaded with ID: {file_info.id}")
        return file_info

    async def create_vector_store(
        self, agents_client: AgentsClient, files: list[str], vector_store_name: str
    ):
        """프로젝트에 파일을 업로드합니다."""

        file_ids = []
        prefix = self.shared_files_path

        # 파일들을 업로드
        for file in files:
            file_path = prefix / file
            file_info = await self.upload_file(agents_client, file_path=file_path, purpose="assistants")
            file_ids.append(file_info.id)

        self.log_msg_purple("Creating the vector store")

        # vector store (벡터 저장소)를 생성
        vector_store = await agents_client.vector_stores.create_and_poll(
            file_ids=file_ids, name=vector_store_name
        )

        self.log_msg_purple(f"Vector store created and files added.")
        return vector_store
