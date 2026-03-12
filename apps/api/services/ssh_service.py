import paramiko
from pydantic_settings import BaseSettings, SettingsConfigDict


class SSHSettings(BaseSettings):
    VPS_HOST: str
    VPS_USER: str
    VPS_KEY_PATH: str

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore"

    )


settings = SSHSettings()


def run_ssh_command(command: str) -> str:
    key = paramiko.Ed25519Key.from_private_key_file(settings.VPS_KEY_PATH)

    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect(
        hostname=settings.VPS_HOST,
        username=settings.VPS_USER,
        pkey=key,
    )

    stdin, stdout, stderr = client.exec_command(command)
    output = stdout.read().decode().strip()
    error = stderr.read().decode().strip()
    client.close()

    if error:
        raise RuntimeError(error)

    return output