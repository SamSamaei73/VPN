from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from apps.api.services.qr_service import generate_qr_image
import os
from apps.api.db.session import get_db
from apps.api.models.device import Device
from apps.api.services.wg_service import (
    create_client_keys,
    add_peer,
    get_server_public_key,
)

router = APIRouter()


@router.post("/devices")
def create_device(user_id: int, device_name: str, public_key: str, db: Session = Depends(get_db)):
    device = Device(
        user_id=user_id,
        device_name=device_name,
        public_key=public_key,
        status="active"
    )

    db.add(device)
    db.commit()
    db.refresh(device)

    return device


@router.post("/create-vpn")
def create_vpn(user_id: int, device_name: str, db: Session = Depends(get_db)):
    client_private_key, client_public_key = create_client_keys()

    device = Device(
        user_id=user_id,
        device_name=device_name,
        public_key=client_public_key,
        status="active"
    )

    db.add(device)
    db.commit()
    db.refresh(device)

    client_ip = f"10.0.0.{device.id + 1}"

    add_peer(client_public_key, client_ip)

    server_public_key = get_server_public_key()

    config = f"""[Interface]
    PrivateKey = {client_private_key}
    Address = {client_ip}/24
    DNS = 1.1.1.1

    [Peer]
    PublicKey = {server_public_key}
    Endpoint = 13.53.214.109:51820
    AllowedIPs = 0.0.0.0/0
    PersistentKeepalive = 25
    """

    os.makedirs("vpn_configs", exist_ok=True)

    config_path = f"vpn_configs/device_{device.id}.conf"
    qr_path = f"vpn_configs/device_{device.id}.png"

    with open(config_path, "w") as f:
        f.write(config)

    generate_qr_image(config, qr_path)
    
    return {
    "device_id": device.id,
    "device_name": device.device_name,
    "client_ip": client_ip,
    "config_path": config_path,
    "qr_path": qr_path
}