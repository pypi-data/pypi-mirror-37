import  os, tarfile


def tar(dst, *args):
    with tarfile.open(dst, "w:gz") as tar:
        for src in args:
            tar.add(src, arcname=os.path.basename(src))

