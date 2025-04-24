from consul import Consul
import requests
import base64

def get_kv(consul_host: str, key: str) -> str:
    url = f"http://{consul_host}:8500/v1/kv/{key}"
    response = requests.get(url)
    response.raise_for_status()
    data = response.json()
    value_b64 = data[0]['Value']
    return base64.b64decode(value_b64).decode('utf-8')

def register_service(consul_host, service_name, service_id, service_port):
    """
    Register a service with Consul.

    :param consul_host: The host of the Consul agent.
    :param service_name: The name of the service to register.
    :param service_id: The unique ID for the service instance.
    :param service_port: The port on which the service is running.
    """
    consul = Consul(host=consul_host)
    
    # Register the service
    consul.agent.service.register(
        name=service_name,
        service_id=service_id,
        port=service_port
    )
    print(f"Service {service_name} with ID {service_id} registered on port {service_port}.")

def discover_service(consul_host, service_name):
    """
    Discover a service using Consul.

    :param consul_host: The host of the Consul agent.
    :param service_name: The name of the service to discover.
    :return: A list of available service instances.
    """
    consul = Consul(host=consul_host)
    
    # Discover the service
    services = consul.catalog.service(service_name)[1]
    
    return services

def deregister_service(consul_host, service_id):
    """
    Deregister a service from Consul.

    :param consul_host: The host of the Consul agent.
    :param service_id: The unique ID for the service instance to deregister.
    """
    consul = Consul(host=consul_host)
    
    # Deregister the service
    consul.agent.service.deregister(service_id)
    print(f"Deregistered service with ID: {service_id}")