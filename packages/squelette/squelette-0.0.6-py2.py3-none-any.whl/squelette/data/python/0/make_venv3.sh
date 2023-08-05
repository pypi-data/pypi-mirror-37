python3 -m venv venv && \
    . venv/bin/activate && \
    pip install pip setuptools wheel -U && \
    pip install -r requirements.txt && \
    pip install ipython && \
    pip install -e .
