FROM python:3.6
MAINTAINER Amalie Trewartha "amalietrewartha@lbl.gov"
WORKDIR /user/src/app
COPY requirements.txt ./
RUN pip install -r requirements.txt
COPY search_api /user/src/app/search_api
RUN groupadd nginx
RUN chgrp nginx /user/src/app/search_api
RUN chmod -R g+wrx /user/src/app/search_api
ENV COVID_HOST mongodb05.nersc.gov
ENV COVID_USER dummy
ENV COVID_PASS dummy
ENV COVID_DB COVID-19-text-mining
EXPOSE 8080
COPY setup.py ./
COPY README.md ./
COPY LICENSE ./
RUN python setup.py install
COPY wsgi.py ./

RUN pip install uvicorn
CMD [ "uvicorn", "wsgi:covidscholar_search_api", "--host", "0.0.0.0", "--port", "8080", "--reload"]
