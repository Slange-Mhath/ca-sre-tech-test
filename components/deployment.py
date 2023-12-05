import cdk8s_plus_26 as kplus
import cdk8s


def create_deployment(app, volumes_dict):
    """The Deployment component serves as a blueprint
    to create pods. In this case it defines for
    example the number of replicas."""
    deployment_chart = cdk8s.Chart(app, "tech-test-deployment")
    deployment = kplus.Deployment(
        deployment_chart,
        "deployment",
        metadata=cdk8s.ApiObjectMetadata(
            name="tech-test-deployment",
        ),
        replicas=5,
    )
    # This adds the container definition (for the container
    # which is run inside the pod) to the
    # blueprint (deployment). It defines the image,
    # the port, the name, the security context, the
    # volume mount and the cpu ressources for the container
    # which is necessary if we want to run 5 instead of 2 replicas.
    deployment.add_container(
        image="nginx:latest",
        port=80,
        name="nginx",
        security_context=kplus.ContainerSecurityContextProps(
            ensure_non_root=False, read_only_root_filesystem=True
        ),
        volume_mounts=[
            kplus.VolumeMount(
                path="/usr/share/nginx/html",
                volume=volumes_dict["volume"],
            ),
            kplus.VolumeMount(
                path="/var/cache/nginx",
                volume=volumes_dict["nginx_client_cash"],
            ),
            kplus.VolumeMount(
                path="/var/run",
                volume=volumes_dict["nginx_pid"],
            ),
        ],
        resources=kplus.ContainerResources(
            # Defines the resources required by the container,
            # which is necessary if we want to run 5 instead
            # of 2 replicas.
            # https://cdk8s.io/docs/latest/reference/cdk8s-plus-26/python/#resourcesoptional
            cpu=kplus.CpuResources(
                # https://cdk8s.io/docs/latest/reference/cdk8s-plus-26/python/#cpuresources
                # Docker Container has 2 cores = 2000m.
                # 2000 / 5 pods = 400m per pod
                limit=kplus.Cpu.millis(400),
                request=kplus.Cpu.millis(250),
            ),
        ),
        liveness=kplus.Probe.from_http_get(
            path="/",
            failure_threshold=1,
            initial_delay_seconds=cdk8s.Duration.seconds(10),
            period_seconds=cdk8s.Duration.seconds(10),
            timeout_seconds=cdk8s.Duration.seconds(5),
            port=80,
        ),
    )
    return deployment
