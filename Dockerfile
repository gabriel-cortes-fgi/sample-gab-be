# Ref: https://gallery.ecr.aws/docker/library/python
FROM public.ecr.aws/docker/library/python:3.10-bullseye
ENV PORT=5000

ARG AWS_ACCESS_KEY_ID
ARG AWS_SECRET_ACCESS_KEY
ENV AWS_DEFAULT_REGION="ap-southeast-1"
ENV AWS_ACCESS_KEY_ID=$AWS_ACCESS_KEY_ID
ENV AWS_SECRET_ACCESS_KEY=$AWS_SECRET_ACCESS_KEY

ADD https://github.com/mikefarah/yq/releases/download/v4.34.1/yq_linux_amd64.tar.gz .
RUN tar -xzf yq_linux_amd64.tar.gz
RUN mv yq_linux_amd64 /usr/bin/yq
RUN pip install pipenv
COPY app/scripts/aws-ca-auth.sh ./app/scripts/aws-ca-auth.sh
RUN chmod +x ./app/scripts/aws-ca-auth.sh
RUN ./app/scripts/aws-ca-auth.sh
#ARG PIPENV_PYPI_MIRROR
#RUN pip config set global.index-url $PIPENV_PYPI_MIRROR
COPY Pipfile* ./
RUN yq -i -p json -o json '._meta.sources = []' Pipfile.lock
# Ref: https://www.giladpeleg.com/blog/package-aws-lambda-python-code-with-docker/
RUN pipenv requirements > requirements.txt
RUN pip install -r ./requirements.txt
COPY . .
CMD ["gunicorn", "-b=:5000", "-w=3", "-t=0", "wsgi:create_app()"]
