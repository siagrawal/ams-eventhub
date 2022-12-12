FROM mcr.microsoft.com/azure-functions/python:3.0-python3.9

ENV AzureWebJobsScriptRoot=/home/site/wwwroot \
    AzureFunctionsJobHost__Logging__Console__IsEnabled=true

COPY requirements.txt /

# FROM base AS python-deps

# RUN pip install pipenv

RUN apt-get update \
  && apt-get -y install gcc \
  && apt-get -y install g++ \
  && apt-get -y install unixodbc unixodbc-dev \
  && apt-get clean

# RUN apt install pipenv -y
RUN pip install -r /requirements.txt
# RUN  pip install pipenv
# RUN pipenv lock
# # COPY Pipfile .
# # COPY Pipfile.lock .
# RUN cd /home/site/wwwroot && pipenv install --system

# FROM base AS runtime

# COPY --from=python-deps /.venv /.venv
# ENV PATH ="/.venv/bin:$PATH"

COPY . /home/site/wwwroot
# COPY Pipfile .
# COPY Pipfile.lock .
# RUN  pip install pipenv
# RUN cd /home/site/wwwroot && python -m pipenv install
# ENV PATH="/.venv/bin:$PATH"


# To enable ssh & remote debugging on app service change the base image to the one below
# FROM mcr.microsoft.com/azure-functions/python:3.0-python3.9-appservice


