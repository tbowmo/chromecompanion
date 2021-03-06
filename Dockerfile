FROM python:3.7.4-slim
WORKDIR /usr/src/app
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY . .
COPY chromecompanion/ chromecompanion/

EXPOSE 8181
ENTRYPOINT [ "python", "-m", "chromecompanion" ]

