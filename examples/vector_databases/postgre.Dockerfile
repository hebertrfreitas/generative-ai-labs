FROM postgres:17.5-bullseye
RUN apt update && apt install git -y
RUN git clone --branch v0.8.0 https://github.com/pgvector/pgvector.git
RUN cd pgvector
RUN make
RUN make install
