import logging
import sys

def AlwaysOnline(app):
  log = logging.getLogger("werkzeug")
  class InterceptHandler(logging.Handler):
    def emit(self, record):
      try:
        val = str(record.args[0])
      except:
        val = ""
      if "/ping" not in val:
        sys.stderr.write(logging.Handler().format(record)+"\n")
        sys.stderr.flush()
  logging.basicConfig(handlers=[InterceptHandler()], level=logging.NOTSET)
  log.handlers = [InterceptHandler(level=logging.NOTSET)]
  log.propagate = False
  @app.route("/ping")
  def ping():
    return "pong"