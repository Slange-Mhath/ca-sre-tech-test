import cdk8s_plus_26 as kplus
import cdk8s
import os

app = cdk8s.App()

chart = cdk8s.Chart(app, "tech-test")

# This a dict comprehension which creates a dictionary
# of the contents of the public folder, which is then
# used as data for the configmap. The key is the 
# filename of the file in the public folder (if 
# multiple we'd have multiple key value pairs in this
# case index.html, style.css) and the value is the 
# content of the file which is read using the open 
# function after being joined with the path of the 
# public folder to get the full path.
site_contents_dict = {
    filename: open(os.path.join("./public", filename)).read()
    for filename in os.listdir("./public")
}

# The configMap is basically an external configuration
# to the application, which gets connected to the pods
# so that the pods can access the configuration and
# its data. In this case for example the site_contents_dict
config_map = kplus.ConfigMap(
    chart,
    "configmap",
    data=site_contents_dict,
    metadata=cdk8s.ApiObjectMetadata(name="tech-test-configmap"),
)

# The volume component attaches a physical storage on a
# hard drive to the pod. In this case the volume contains
# data to make it accessible to the pod as the configmap,
# which is in the deployment mounted at the path 
# /usr/share/nginx/html. So index.html file is accessible
# to the container at path /urs/share/nginx/html/.index 
volume = kplus.Volume.from_config_map(chart, "volume", config_map=config_map)
nginx_client_cash = kplus.Volume.from_empty_dir(chart, id="nginx-client-cash", name="nginx-client-cash")
nginx_pid = kplus.Volume.from_empty_dir(chart, id="nginx-pid", name="nginx-pid")

# The Deployment component serves as a blueprint to create
#  pods. In this case it defines for example the number
#  of replicas.
deployment = kplus.Deployment(
    chart,
    "deployment",
    metadata=cdk8s.ApiObjectMetadata(
        name="tech-test-deployment",
    ),
    replicas=5,
)

# This adds the container definition (for the container which
# is run inside the pod) to the blueprint (deployment). 
# It defines the image, the port, the name, the security
# context, the volume mount and the cpu ressources for 
# the container which is necessary if we want to run 5 
# instead of 2 replicas.  
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
    resources=kplus.ContainerResources(
        # Defines the resources required by the container, which is necessary if we want to run 5 instead of 2 replicas.
        # https://cdk8s.io/docs/latest/reference/cdk8s-plus-26/python/#resourcesoptional
        cpu=kplus.CpuResources(
            # https://cdk8s.io/docs/latest/reference/cdk8s-plus-26/python/#cpuresources
            limit=kplus.Cpu.millis(400),  # Docker Container has 2 cores = 2000m. 2000 / 5 pods = 400m per pod  
            request=kplus.Cpu.millis(250), 
        ),
    ),
)

# Every pod has an IP address, which is not static.
# Which is problematic if pods die and get recreated
# as the IP address would also change. The service
# component defines a static IP address for the pods
# to make them accessible from outside the cluster.
# The service component is independent so won't die
# if the pod dies.
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
