import cdk8s_plus_26 as kplus
import cdk8s


def create_service(app, deployment):
    """Every pod has an IP address, which is not static.
    Which is problematic if pods die and get recreated as
    the IP address would also change. The service component
    defines a static IP address for the pods to make them
    accessible from outside the cluster. The service component
    is independent so won't die if the pod dies."""
    service_chart = cdk8s.Chart(app, "tech-test-service")

    _ = kplus.Service(
        service_chart,
        "service",
        ports=[kplus.ServicePort(port=80, target_port=80)],
        type=kplus.ServiceType.NODE_PORT,
        selector=deployment,
        metadata=cdk8s.ApiObjectMetadata(name="tech-test-service"),
    )
    return service_chart
