import hvac


def get_secret_from_kv_v1(vc, mount_point, secret_path, key):
    return vc.kv.v1.read_secret(
        path=secret_path,
        mount_point=mount_point
    )['data'][key]