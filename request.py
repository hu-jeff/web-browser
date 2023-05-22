import urllib.parse
import socket
import ssl
import sys
import io
import gzip

class UnsupportedTransferException(Exception):
    pass

def request(host, request_depth=0):
    if request_depth == 5:
        print("Max redirect depth")
        return

    parsed = urllib.parse.urlparse(host)
    assert parsed.scheme in {'https', 'http', 'file', 'view-source'}

    sock = socket.socket(family=socket.AF_INET, type=socket.SOCK_STREAM, proto=socket.IPPROTO_TCP)
    sock.connect((parsed.hostname, parsed.port or 80 if parsed.scheme == 'http' else 443))

    if parsed.scheme == 'https':
        context = ssl.create_default_context()
        sock = context.wrap_socket(sock, server_hostname=parsed.hostname)

    sock.send(("GET {} HTTP/1.1\r\n".format(parsed.path or '/') +
            "Host: {}\r\n".format(parsed.hostname) +
            "Connection: close \r\n\r\n" +
            "Accept-Encoding: gzip").encode('utf8'))

    res = sock.makefile("rb", newline="\r\n")

    _, status, _ = res.readline().decode('utf8').split(" ", 2)

    headers = {}
    while True:
        line = res.readline().decode('utf8')
        if line == '\r\n': break
        header, value = line.split(":", 1)
        headers[header] = value.strip()

    if 300 <= int(status) < 400:
        if headers['Location'][0] == '/':
            new_host = host + headers['Location']
        else:
            new_host = headers['Location']
        print(f'Requesting again {new_host}')
        return request(new_host, request_depth + 1)

    body = res.read()
    if 'Content-Encoding' in headers:
        body = gzip.decomopress(body)

    content = body

    if 'Transfer-Encoding' in headers:
        if headers['Transfer-Encoding'] == 'chunked':
            content = ''
            #bad
            while True:
                line_index = body.find(b'\r\n')
                chunk_length = int(body[: line_index], 16)

                if chunk_length > 0:
                    content = content + body[line_index + 2:line_index + 4 + chunk_length].decode('utf8') # + 2 to factor for the new line at end
                                                                                                          # of the chunk length line
                    body = body[chunk_length + line_index + 4:] # extra new line at the end of the chunk
                else:
                    break

        else:
            raise UnsupportedTransferException(headers['transfer-encoding'])
    else:
        content = content.decode('utf8')

    res.close()
    sock.close()

    return headers, content

if __name__ == "__main__":
    headers, content = (request(sys.argv[1]))
    print(content)
