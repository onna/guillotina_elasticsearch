
run-postgres:
	docker run \
		-e POSTGRES_DB=guillotina \
		-e POSTGRES_USER=postgres \
		-p 127.0.0.1:5432:5432 postgres:9.6

run-opensearch:
	docker run -p 9200:9200 \
		-e "plugin.security.enabled=false" \
		-e "cluster.name=docker-cluster" \
		-e "bootstrap.memory_lock=true" \
		-e "ES_JAVA_OPTS=-Xms1512m -Xmx1512m" \
		-e "http.host=0.0.0.0" \
		-e "transport.host=127.0.0.1" \
		opensearchproject/opensearch:2.0.0

run-opendistro:
	docker run -p 9200:9200 -p 9600:9600 \
		-e "discovery.type=single-node" \
		-e "bootstrap.memory_lock=true" \
		-e "ES_JAVA_OPTS=-Xms1512m -Xmx1512m" \
		-e "http.host=0.0.0.0" \
		-e "transport.host=127.0.0.1" \
		amazon/opendistro-for-elasticsearch:0.7.1
