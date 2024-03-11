#
FROM python:3.9

#
WORKDIR /code

#
COPY ./requirements.txt /code/requirements.txt

#
RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

#
COPY ./inventory_app /code/app

#
CMD ["uvicorn", "inventory_app.main:app", "--host", "0.0.0.0", "--port", "80"]