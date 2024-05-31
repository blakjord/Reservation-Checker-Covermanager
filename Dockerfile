FROM python
WORKDIR /app
COPY . /app 
ADD ./requirements.txt ./
RUN python3 -m pip install -r requirements.txt
CMD ["python3", "main.py"]