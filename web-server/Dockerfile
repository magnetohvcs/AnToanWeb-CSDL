from tadeorubio/pyodbc-msodbcsql17
RUN useradd -m webuser

WORKDIR /application
COPY Application /application/

RUN /usr/local/bin/python -m pip install --upgrade pip

RUN chown -R root:webuser /application && \
    chmod 655 /application && \
    chmod 644 /application/app.py

USER webuser
RUN pip3 install --upgrade --no-cache-dir -r requirements.txt
CMD ["/usr/local/bin/python", "/application/app.py"]
