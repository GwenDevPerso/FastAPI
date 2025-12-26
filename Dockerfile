#Build stage
FROM python:3.14-slim AS build

WORKDIR /app

#Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

#Copy the build stage
COPY /src /src

#Expose
EXPOSE 8000

#Run the application
CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8000"]