import cdk8s_plus_26 as kplus


def create_volumes(config_map_dict):
    volume = kplus.Volume.from_config_map(
        config_map_dict["config_map_chart"],
        "volume",
        config_map=config_map_dict["config_map"],
    )
    nginx_client_cash = kplus.Volume.from_empty_dir(
        config_map_dict["config_map_chart"],
        id="nginx-client-cash",
        name="nginx-client-cash",
    )
    nginx_pid = kplus.Volume.from_empty_dir(
        config_map_dict["config_map_chart"], id="nginx-pid", name="nginx-pid"
    )
    return {
        "volume": volume,
        "nginx_client_cash": nginx_client_cash,
        "nginx_pid": nginx_pid,
    }
