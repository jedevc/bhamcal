FROM python:3.8

RUN git clone https://github.com/jedevc/bhamcal.git && \
    cd bhamcal && \
    pip install .

ENTRYPOINT ["bhamcal"]
