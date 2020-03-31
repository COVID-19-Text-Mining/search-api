FROM python:3.6
MAINTAINER Amalie Trewartha "amalietrewartha@lbl.gov"
ARG COVID_HOST
ARG COVID_USER
ARG COVID_PASS
ARG COVID_DB
WORKDIR /user/src/app
COPY requirements.txt ./
RUN pip install -r requirements.txt
COPY search_api /user/src/app/search_api
RUN groupadd nginx
RUN chgrp nginx /user/src/app/search_api
RUN chmod -R g+wrx /user/src/app/search_api
EXPOSE 8080
COPY setup.py ./
COPY README.md ./
COPY LICENSE ./
RUN python setup.py install
COPY wsgi.py ./
RUN pip install uvicorn
ENV COVID_HOST $COVID_HOST
ENV COVID_USER $COVID_USER
ENV COVID_PASS $COVID_PASS
ENV COVID_DB $COVID_DB
CMD [ "uvicorn", "wsgi:covidscholar_search_api", "--host", "0.0.0.0", "--port", "8080", "--reload"]
