FROM weboftrust/keri:1.2.0-rc4

WORKDIR /usr/local/var

RUN mkdir reg-pilot-filer
COPY . /usr/local/var/reg-pilot-filer

WORKDIR /usr/local/var/reg-pilot-filer/

RUN pip install -r requirements.txt

ENTRYPOINT reg-pilot-filer server start --config-dir scripts --config-file "${FILER_CONFIG_FILE:-reg-pilot-filer-config.json}"