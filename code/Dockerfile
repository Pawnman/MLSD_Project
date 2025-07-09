FROM python:3.9

ADD main.py .
ADD modelpipelinefinal.pickle .
ADD flats_Ekat.csv .
ADD flats_Novosib.csv .
ADD flats_SaintP.csv .
ADD flats_Moscow.csv .
ADD flats_Kazan.csv .
ADD score.csv .

COPY ./requirements.txt ./requirements.txt

RUN pip install -r requirements.txt

CMD ["python", "./main.py"]