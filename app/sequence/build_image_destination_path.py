from pathlib import Path


def build_image_destination_path(month: int, downloads_path: Path) -> Path:
    zfill_month = f"{month}".zfill(2)
    image_destination_path = downloads_path.joinpath('calendar', f'{zfill_month}', 'image.png')
    image_destination_path.parent.mkdir(parents=True, exist_ok=True)
    return image_destination_path
