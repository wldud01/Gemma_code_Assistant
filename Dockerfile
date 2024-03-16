FROM amd64/python:3.10-slim

WORKDIR /usr/app

RUN pip install -U pip && pip install poetry && pip install huggingface-cli

# 프로젝트 의존성 파일 복사
COPY pyproject.toml poetry.lock* ./

# 의존성 설치
RUN poetry config virtualenvs.create false && poetry install --no-dev

# 애플리케이션 코드 복사
COPY Gemma_streamlit.py .
COPY ignore.json .

RUN huggingface-cli login --token {YOUR_HUGGING_FACE_TOKEN}
# Streamlit 애플리케이션 실행
CMD ["streamlit", "run", "Gemma_streamlit.py", "--server.address", "0.0.0.0"]
 