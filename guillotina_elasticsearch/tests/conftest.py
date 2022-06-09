from pytest_docker_fixtures import images


image_version = "7.5.1"

images.configure(
    "opensearch",
    "opensearchproject/opensearch",
    image_version,
    max_wait_s=90,
    env={
        "plugins.security.disabled": "true",
        "discovery.type": "single-node",
        "http.host": "0.0.0.0",
        "transport.host": "127.0.0.1",
    },
)


pytest_plugins = [
    "pytest_docker_fixtures",
    "guillotina.tests.fixtures",
    "guillotina_elasticsearch.tests.fixtures",
]
