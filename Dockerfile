FROM jupyter/base-notebook:python-3.10.6
USER root
COPY examples/*.ipynb /home/jovyan/
RUN chown -R jovyan /home/jovyan/*.ipynb
USER jovyan
RUN pip install tptp-lark-parser
