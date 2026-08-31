FROM python:3.13.5-slim
WORKDIR /work
COPY environment/requirements.txt /tmp/requirements.txt
RUN pip install --no-cache-dir -r /tmp/requirements.txt
COPY . /work
CMD ["bash","scripts/reproduce_offline.sh"]
