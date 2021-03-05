FROM python:3.8
ENV PYTHONUNBUFFERED 1

WORKDIR /api_project
COPY requirements.txt /api_project/requirements.txt
RUN pip3 install -r requirements.txt
COPY wait-for-it.sh /wait-for-it.sh
RUN chmod +x /wait-for-it.sh
COPY . /api_project
CMD /bin/bash -c "./wait-for-it.sh db:3306 -- python3 manage.py migrate && python3 manage.py update_youtubevideo_table_data && python3 manage.py runserver 0.0.0.0:8000"