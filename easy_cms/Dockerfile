FROM se1zer/dedecms:latest

COPY run.sh /run.sh
COPY f1Aggg /f1Aggg
COPY tpl.php /tmp/tpl.php

RUN chmod +x /run.sh \
    && chown www-data:www-data /tmp/tpl.php \
    && mv /tmp/tpl.php /var/www/html/dede/tpl.php

EXPOSE 80

ENTRYPOINT ["/bin/sh", "-c", "/run.sh"]