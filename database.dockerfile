FROM docker.io/postgis/postgis:14-3.2
RUN localedef -i pt_PT -c -f UTF-8 -A /usr/share/locale/locale.alias pt_PT.UTF-8
ENV LANG pt_PT.utf8