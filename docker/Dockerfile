FROM python:3.7-slim as build

# Create a group and user to run our app
# ARG APP_USER=appuser
# RUN groupadd -r ${APP_USER} && useradd --no-log-init -r -g ${APP_USER} ${APP_USER}

# Working directory where all the setup would take place in the image
WORKDIR /commuters

# The default user that should be used
ARG USER_ID=1000
ARG GROUP_ID=1000

ARG APP_USER=appuser

# Create user and group
RUN groupadd -g ${GROUP_ID} ${APP_USER} && useradd -u ${USER_ID} -g ${APP_USER} -s /bin/sh ${APP_USER}


RUN pip3 install --upgrade pip
RUN apt-get -y update


RUN apt install -y gdal-bin python-gdal python3-gdal
RUN apt-get install -y postgresql-client
RUN apt-get -y install curl
RUN export LC_ALL=C.UTF-8 && export LANG=C.UTF-8


# copy the Pipfile & pipfile.lock which contains dependencies to be installed
COPY requirements.txt .

# RUN pip install
RUN pip install -r requirements.txt


COPY . .

RUN chown -R ${APP_USER}:${APP_USER} /commuters
RUN chmod 755 /commuters

USER ${APP_USER}

RUN mkdir -p app/static

EXPOSE 80
CMD ["/bin/bash", "-c", "docker/start_api.sh"]