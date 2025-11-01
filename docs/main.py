import json
import smtplib
import ssl
from email.mime.text import MIMEText
from email.header import Header
from http.server import BaseHTTPRequestHandler, HTTPServer
import re


def is_valid_email(email: str) -> bool:
    pattern = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
    return re.fullmatch(pattern, email) is not None


with open("./config/smtp_config.json", "r", encoding="utf-8") as f:
    smtp_config = json.load(f)

with open("./config/server_config.json", "r", encoding="utf-8") as f:
    server_config = json.load(f)


# handle api
class api_handler(BaseHTTPRequestHandler):
    # set header
    def _set_header(self):
        self.send_response(200)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "POST, GET, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
        self.end_headers()

    # handle pretest
    def do_OPTIONS(self):
        self._set_header()

    def do_POST(self):
        if self.path == "/send_mail":
            try:
                # recive post data

                content_length = int(self.headers.get("Content-Length", 0))
                post_body = self.rfile.read(content_length)
                data = json.loads(post_body.decode("utf-8"))

                # format data
                name = data.get("name", "")
                email = data.get("email", "")
                message = data.get("message", "")

                # check not null
                if not name or not email:
                    self._set_header()
                    self.wfile.write(
                        json.dumps(
                            {
                                "success": False,
                                "code": 1001,
                                "error": "name or email connot be null",
                            }
                        ).encode("utf-8")
                    )
                    return
                # check email
                if not is_valid_email(email):
                    self._set_header()
                    self.wfile.write(
                        json.dumps(
                            {
                                "success": False,
                                "code": 1001,
                                "error": "the email address type is error",
                            }
                        ).encode("utf-8")
                    )
                    return

                # send email
                data = {"name": name, "email": email, "message": message}
                result = send(data)
                if result["success"]:
                    self._set_header()
                    self.wfile.write(
                        json.dumps({"success": True, "code": 200}).encode("utf-8")
                    )
                    return
                else:
                    self._set_header()
                    self.wfile.write(
                        json.dumps(
                            {
                                "success": False,
                                "code": 1003,
                                "error": str(result["error"]),
                            }
                        ).encode("utf-8")
                    )
                    return

            except Exception as e:
                self._set_header()
                self.wfile.write(
                    json.dumps(
                        {"success": False, "code": 1002, "error": str(e)}
                    ).encode("utf-8")
                )

    def do_GET(self):
        if self.path == "/":
            print("server is already up")
            self.send_response(200)
            self.send_header("Content-Type", "text/plain; charset=utf-8")
            self.send_header("Access-Control-Allow-Origin", "*")
            self.end_headers()
            self.wfile.write(b"server is already up")


# set up sever
def run(server_class=HTTPServer, handler_class=api_handler):
    server_address = (server_config["server"], server_config["port"])
    httpd = server_class(server_address, handler_class)
    print(f"host:http://localhost:{server_config["port"]}")
    httpd.serve_forever()


# send smtp
def send(data):
    body = f"""
    姓名：{data['name']}
    邮箱：{data['email']}
    消息内容：
    {data['message']}
     """
    msg = MIMEText(body, "plain", "utf-8")
    msg["From"] = Header(smtp_config["smtp_user"], "utf-8")
    msg["To"] = Header(smtp_config["smtp_user"], "utf-8")
    msg["Subject"] = Header("新网站留言", "utf-8")

    context = ssl.create_default_context()

    try:
        with smtplib.SMTP_SSL(
            smtp_config["smtp_server"],
            smtp_config["smtp_port"],
            context=context,
            local_hostname="localhost",
        ) as server:
            server.login(smtp_config["smtp_user"], smtp_config["smtp_pass"])
            server.sendmail(
                smtp_config["smtp_user"],
                [smtp_config["smtp_user"]],
                msg.as_string(),
            )
            return {"success": True}
    except Exception as e:
        return {"success": False, "error": e}


if __name__ == "__main__":
    run()


# password - "advance@biotech123"
# email - "advancebiotech0@gmail.com"
