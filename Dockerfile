FROM shvedfun/algoritmika:v0.01

WORKDIR /usr/src/app

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

#EXPOSE 8080
CMD ["python", "asgi.py"]