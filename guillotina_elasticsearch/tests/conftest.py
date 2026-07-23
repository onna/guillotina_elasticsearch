from pytest_docker_fixtures import images


image_version = "2.0.0"

images.configure(
    "elasticsearch",
    "opensearchproject/opensearch",
    image_version,
    max_wait_s=90,
    env={
        "xpack.security.enabled": None,
        "plugins.security.disabled": "true",
        "discovery.type": "single-node",
        "http.host": "0.0.0.0",
        "transport.host": "127.0.0.1",
        "OPENSEARCH_JAVA_OPTS": "-Xms512m -Xmx512m -XX:-UseContainerSupport",
    },
)


pytest_plugins = [
    "pytest_docker_fixtures",
    "guillotina.tests.fixtures",
    "guillotina_elasticsearch.tests.fixtures",
]
