FROM python:3.12.3-slim 

WORKDIR /app

COPY ./requirements.txt ./
RUN pip install --no-cache-dir --upgrade -r requirements.txt

COPY . .

ENV DATABASE_URL=postgresql+asyncpg://postgres:082004@feedbackdb?host=/cloudsql/multitude-assessment:asia-southeast2:feedback-db

EXPOSE 8080

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8080"]