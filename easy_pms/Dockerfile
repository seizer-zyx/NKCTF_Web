FROM se1zer/zentao:18.0.beta1

COPY src/ /tmp/
COPY flag /flag
COPY run.sh /run.sh

RUN cp /tmp/model.php /var/www/zentaopms/module/repo/model.php \
    && chmod 644 /flag \
    && chmod +x /run.sh


EXPOSE 80

ENTRYPOINT ["/bin/sh", "-c", "/run.sh"]