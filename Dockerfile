FROM python:3.8

RUN mkdir /code
WORKDIR /code
ADD . /code/
RUN pip install --trusted-host pypi.org --trusted-host pypi.python.org --trusted-host=files.pythonhosted.org -r requirements.txt

EXPOSE 5000
CMD ["python", "/code/app.py"]
