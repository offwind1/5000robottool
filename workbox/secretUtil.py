import base64
import hashlib

secretKey = "3b98c334898a49b19e59b62ea2d9f624"



def _secure(data, kwargs):
    value = get_sign(data)
    if "headers" not in kwargs:
        kwargs["headers"] = {}
    kwargs["headers"].update({
        "mizhu": value
    })


def md5(content):
    return hashlib.md5(content.encode(encoding="utf-8")).hexdigest()


def rc4(data, key):
    """RC4 encryption and decryption method."""
    S, j, out = list(range(256)), 0, bytearray()

    for i in range(256):
        j = (j + S[i] + ord(key[i % len(key)])) % 256
        S[i], S[j] = S[j], S[i]

    i = j = 0
    for ch in data:
        i = (i + 1) % 256
        j = (j + S[i]) % 256
        S[i], S[j] = S[j], S[i]

        x = ord(ch) ^ S[(S[i] + S[j]) % 256]
        out.append(x)

    return out


def get_sign_conntent(data):
    content = ""
    for key in sorted(data.keys()):
        value = str(data.get(key, ""))
        if value and not value.isspace():
            content += key + value
    return content


def get_sign(data):
    content = get_sign_conntent(data)
    md_content = md5(content)
    buf = rc4(md_content, secretKey)
    return str(base64.b64encode(buf), 'utf-8')
