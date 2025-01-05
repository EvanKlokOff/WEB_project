import base64
from pathlib import Path


main_path = Path().cwd().parent / "app"
default_path = "static/image/menu/"

def store_image_in(base64str: str,
                   image_name: str,
                   directory:str = default_path,
                   photo_extension: str = "png")->str:

    image_data = base64.b64decode(base64str)
    image_path = main_path / directory / f"{image_name}.{photo_extension}"
    print(image_path)
    directory_ = main_path / directory
    directory_.mkdir(parents=True, exist_ok=True)

    image_path.write_bytes(image_data)
    return "/" + directory + f"{image_name}.{photo_extension}"

def delete_image_in(image_path:str) -> None:
    try:
        # Создаем объект Path
        path = main_path / image_path[1:]
        print(path)
        # Проверяем, существует ли файл
        if path.exists() and path.is_file():
            # Удаляем файл
            path.unlink()
            return
    except Exception as e:
        print(e.__class__, e)

if __name__ == "__main__":
    print(main_path / default_path)