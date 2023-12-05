import cdk8s_plus_26 as kplus
import cdk8s
import os

app = cdk8s.App()
chart = cdk8s.Chart(app, "tech-test")

site_contents_dict = {
    filename: open(os.path.join("./public", filename)).read()
    for filename in os.listdir("./public")
}

config_map = kplus.ConfigMap(
    chart,
    "configmap",
    data=site_contents_dict,
    metadata=cdk8s.ApiObjectMetadata(name="tech-test-configmap"),
)

volume = kplus.Volume.from_config_map(chart, "volume", config_map=config_map)
nginx_client_cash = kplus.Volume.from_empty_dir(chart, id="nginx-client-cash", name="nginx-client-cash")
nginx_pid = kplus.Volume.from_empty_dir(chart, id="nginx-pid", name="nginx-pid")

deployment = kplus.Deployment(
    chart,
    "deployment",
    metadata=cdk8s.ApiObjectMetadata(
        name="tech-test-deployment",
    ),
)

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
            volume=volume,
        ),
        kplus.VolumeMount(
            path="/var/cache/nginx",
            volume=nginx_client_cash,
        ),
        kplus.VolumeMount(
            path="/var/run",
            volume=nginx_pid,
        ),
    ],
)

service = kplus.Service(
    chart,
    "service",
    ports=[kplus.ServicePort(port=80, target_port=80)],
    type=kplus.ServiceType.NODE_PORT,
    selector=deployment,
    metadata=cdk8s.ApiObjectMetadata(name="tech-test-service"),
)

if __name__ == "__main__":
    app.synth()
