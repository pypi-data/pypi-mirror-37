import os
import shutil


def makefolder(path, folder):
    if not os.path.exists(f"{path}/{folder}"):
        os.makedirs(f"{path}/{folder}")


def files(path):
    for root, dirs, filenames in os.walk(path):
        for filename in filenames:
            if filename.endswith(".org"):
                yield root + os.sep + filename


def images(root, path, doc):
    print("## Images")
    for item in doc.images():
        image = item.value[0]
        if image.startswith("http://") or image.startswith("https://"):
            continue
        print(root)
        print(path)
        print(image)
        current_path = os.path.abspath(root + os.sep + image)
        if not os.path.exists(current_path):
            print(f"Missing image {current_path}")
            continue
        new_path = current_path[len(root) + 1 :]
        folder = os.path.dirname(new_path)
        item.value[0] = f"../images{new_path}"
        makefolder(path, f"images{folder}")
        shutil.copy(current_path, f"{path}/images{new_path}")
