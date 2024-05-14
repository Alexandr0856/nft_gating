FROM python:3.11
WORKDIR api
COPY api/requirements.txt .
RUN pip install -r requirements.txt
CMD ["fastapi", "run", "main.py"]