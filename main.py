import cdk8s
from components.configmap import create_config_map
from components.deployment import create_deployment
from components.service import create_service
from components.volumes import create_volumes

app = cdk8s.App()

if __name__ == "__main__":
    config_map_dict = create_config_map(app)
    volumes_dict = create_volumes(config_map_dict)
    deployment = create_deployment(app, volumes_dict)
    create_service(app, deployment)
    app.synth()
