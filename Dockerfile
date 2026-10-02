FROM python:3.12.3

WORKDIR /main

COPY ./main/requirements.txt /main/requirements.txt

RUN pip install --no-cache-dir --upgrade -r /main/requirements.txt

COPY ./main /main

RUN useradd -m appuser && chown -R appuser /main
USER appuser

HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD python -c "import urllib.request; urllib.request.urlopen('http://localhost:5000')" || exit 1

EXPOSE 5000

CMD ["python", "run.py"]
