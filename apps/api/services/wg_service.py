from pydantic_settings import BaseSettings, SettingsConfigDict
from apps.api.services.ssh_service import run_ssh_command


class WGSettings(BaseSettings):
    WG_CONFIG_DIR: str
    WG_INTERFACE: str

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore"
    )


settings = WGSettings()


def create_client_keys():
    private_key = run_ssh_command("wg genkey")
    public_key = run_ssh_command(f"echo '{private_key}' | wg pubkey")
    return private_key.strip(), public_key.strip()


def add_peer(public_key: str, ip: str):
    cmd = f"sudo wg set {settings.WG_INTERFACE} peer {public_key} allowed-ips {ip}/32"
    run_ssh_command(cmd)


def get_server_public_key():
    cmd = f"cat {settings.WG_CONFIG_DIR}/server_public.key"
    return run_ssh_command(cmd)