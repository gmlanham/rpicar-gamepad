import io
import picamera
import logging
import socketserver
from threading import Condition
from http import server
import os
fd = os.open(__file__, os.O_RDWR)
blocking = False
os.set_blocking(fd, blocking) # change the blocking mode
print("Blocking mode changed")
print("Blocking Mode:", os.get_blocking(fd))

PAGE="""\
<html>
<head>
<title>RPI Car MJPEG Streaming</title>
</head>
<body>
<h1>RPICar MJPEG Streaming</h1>
<img src="stream.mjpg" width="640" height="480" />
</body>
</html>
"""

class StreamingOutput(object):
    def __init__(self):
        self.frame = None
        self.buffer = io.BytesIO()
        self.condition = Condition()

    def write(self, buf):
        if buf.startswith(b'\xff\xd8'):
            # New frame, copy the existing buffer's content and notify all
            # clients it's available
            self.buffer.truncate()
            with self.condition:
                self.frame = self.buffer.getvalue()
                self.condition.notify_all()
            self.buffer.seek(0)
        return self.buffer.write(buf)

class StreamingHandler(server.BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/':
            self.send_response(301)
            self.send_header('Location', '/index.html')
            self.end_headers()
        elif self.path == '/index.html':
            content = PAGE.encode('utf-8')
            self.send_response(200)
            self.send_header('Content-Type', 'text/html')
            self.send_header('Content-Length', len(content))
            self.end_headers()
            self.wfile.write(content)
        elif self.path == '/stream.mjpg':
            self.send_response(200)
            self.send_header('Age', 0)
            self.send_header('Cache-Control', 'no-cache, private')
            self.send_header('Pragma', 'no-cache')
            self.send_header('Content-Type', 'multipart/x-mixed-replace; boundary=FRAME')
            self.end_headers()
            try:
                while True:
                    with output.condition:
                        output.condition.wait()
                        frame = output.frame
                    self.wfile.write(b'--FRAME\r\n')
                    self.send_header('Content-Type', 'image/jpeg')
                    self.send_header('Content-Length', len(frame))
                    self.end_headers()
                    self.wfile.write(frame)
                    self.wfile.write(b'\r\n')
            except Exception as e:
                logging.warning(
                    'Removed streaming client %s: %s',
                    self.client_address, str(e))
        else:
            self.send_error(404)
            self.end_headers()

class StreamingServer(socketserver.ThreadingMixIn, server.HTTPServer):
    allow_reuse_address = True
    daemon_threads = True
    print(daemon_threads)

with picamera.PiCamera(resolution='640x480', framerate=24) as camera:
    output = StreamingOutput()
    
    camera.start_recording(output, format='mjpeg')
    print(format)
    try:
        address = ('192.168.0.11', 8000)
        print(address)
        server = StreamingServer(address, StreamingHandler)
        server.serve_forever()
#     except Exception as ex:
#         print(ex)
#         pass       
    except KeyboardInterrupt:
        print('ctrl')
        pass
    finally:
        # Clean-up server (close socket, etc.)
        server.server_close()
        #sys.stdout.flush()
        #os.execv(sys.argv[0], sys.argv)
        #camera_close()
        #print("break on CTRL+c")
        #os._exit(0)
        #break # if CTRL+C is pressed
#     finally:
#         camera.stop_recording()
#         os._exit(0)
#         camera.close()

