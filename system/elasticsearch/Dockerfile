FROM docker.elastic.co/elasticsearch/elasticsearch:7.6.2

# Install kuromoji plugin
RUN elasticsearch-plugin  install analysis-kuromoji
RUN elasticsearch-plugin install analysis-icu
