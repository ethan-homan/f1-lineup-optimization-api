FROM python:3.9

RUN apt-get update -y && apt-get install -y \
	wget \
	build-essential \
	--no-install-recommends \
	&& rm -rf /var/lib/apt/lists/*

WORKDIR /user/local/
RUN wget http://ftp.gnu.org/gnu/glpk/glpk-4.57.tar.gz \
	&& tar -zxvf glpk-4.57.tar.gz

WORKDIR /user/local/glpk-4.57
RUN ./configure \
	&& make \
	&& make check \
	&& make install \
	&& make distclean \
	&& ldconfig \
	&& rm -rf /user/local/glpk-4.57.tar.gz \
	&& apt-get clean

ENV PYTHONUNBUFFERED True
ENV PORT 5000

WORKDIR /
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY ./app app
CMD exec uvicorn app.main:app --proxy-headers --host 0.0.0.0 --port $PORT
