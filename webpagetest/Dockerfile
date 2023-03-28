FROM vijayhotti/webpagetestserver:v2

COPY flag /flag
COPY run.sh /run.sh

RUN chmod +x /run.sh

EXPOSE 80

ENTRYPOINT ["/bin/sh", "-c", "/run.sh"]