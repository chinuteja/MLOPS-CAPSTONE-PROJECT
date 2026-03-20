FROM python:3.10-slim
#creating a directory for the app
WORKDIR /app
#copying the requirements file to the working directory
COPY flask_app/ /app/
#copying the model files to the working directory
COPY models/vectorizer.pkl /app/models/vectorizer.pkl

RUN apt-get update && apt-get install -y git
#installing the dependencies
RUN pip install -r requirements.txt
#   downloading the stopwords and wordnet for nltk
RUN python -m nltk.downloader stopwords wordnet
#exposing the port for the flask app
EXPOSE 5000

#local
CMD ["python", "app.py"]  

#Prod
# CMD ["gunicorn", "--bind", "0.0.0.0:5000", "--timeout", "120", "app:app"]