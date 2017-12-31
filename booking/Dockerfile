# Use an official Python runtime as self parent image
FROM python:3.6.3

# set working directory
WORKDIR /app

ADD *.py requirements.txt /app/

# install requirements
RUN pip install --trusted-host pypi.python.org -r requirements.txt

ENTRYPOINT ["python", "./booking.py"]
EXPOSE 5003

# Run user.py when the container launches
CMD ["python", "booking.py"]
