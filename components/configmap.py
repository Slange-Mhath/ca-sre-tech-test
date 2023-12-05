import cdk8s_plus_26 as kplus
import cdk8s
import os


def create_config_map(app):
    """The configMap is basically an external configuration
    to the application, which gets connected to the pods so
      that the pods can access the configuration and its data.
        In this case for example the site_contents_dict"""
    config_map_chart = cdk8s.Chart(app, "tech-test-configmap")

    # This a dict comprehension which creates a dictionary of
    # the contents of the public folder, which is then used
    # as data for the configmap. The key is the filename of
    # the file in the public folder (if multiple we'd have
    # multiple key value pairs in this case index.html, style.css)
    # and the value is the content of the file which is read using
    # the open function after being joined with the path of
    # the public folder to get the full path.
    site_contents_dict = {
        filename: open(os.path.join("./public", filename)).read()
        for filename in os.listdir("./public")
    }

    config_map = kplus.ConfigMap(
        config_map_chart,
        "configmap",
        data=site_contents_dict,
        metadata=cdk8s.ApiObjectMetadata(name="tech-test-configmap"),
    )

    # The volume component attaches a physical storage on a hard
    # drive to the pod. In this case the volume contains data
    # to make it accessible to the pod as the configmap, which
    # is in the deployment mounted at the path /usr/share/nginx/html.
    # So index.html file is accessible to the container
    # at path /urs/share/nginx/html/.index
    return {"config_map_chart": config_map_chart, "config_map": config_map}
