import qrcode


def generate_qr_image(config_text: str, output_path: str):
    img = qrcode.make(config_text)
    img.save(output_path)