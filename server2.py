# Uses SimpleHTTPServer that runs and handles all the get and post requests 

import SimpleHTTPServer
from BaseHTTPServer import HTTPServer, BaseHTTPRequestHandler
import SocketServer
import cgi
import logging

import sys
import json
import summarize as Summ
import allhtmldata as _HTML

PORT = 3000
inputtext = ""
class ServerHandler(BaseHTTPRequestHandler):

  def _set_headers(self):
    self.send_response(200)
    self.send_header('Content-Type', 'text/html')
    self.end_headers()
  def do_GET(self):

    logging.warning("=== get started ===")
    logging.warning(self.headers)
    self._set_headers()
    F = open("text.txt", "r")
    thetext = F.read()

    # f = open("index.html", "r")
    contentdata = _HTML.htmlcontenthome.format(type_of_request = 'get', already_text = thetext)
    self.wfile.write(contentdata)
  def do_POST(self):
    global inputtext
    logging.warning("=== post started ===")
    logging.warning(self.headers)
    form = cgi.FieldStorage(
      fp = self.rfile,
      headers = self.headers,
      environ = {'REQUEST_METHOD': 'POST',
      'CONTENT_TYPE': self.headers['Content-Type'],
      })
    logging.warning("=== post values ===")
    # for item in form.list:
    #   logging.warning(item)
    inputtext = form.list[0].value
    # print form.list[0].key
    print form.list[0].value
    FF = open("temp.html", "w")
    FF.write("<html><body><p>"+inputtext+"</p></body></html>")

    # logging.warning(str(inputtext)+"\n")
    summary = ""
    self._set_headers()
    
    print "calling summary"
    # 
    # summary += Summ.merafunc("http://127.0.0.1:3000")
    sumobj = Summ.merafunc(inputtext)
    for item in  sumobj.summaries:
      summary += item+"\n"
    print sumobj.summaries
    # 
    
    contentdata = _HTML.htmlcontentsummary.format(input_text = inputtext, summary_generated = summary)
    self.wfile.write(contentdata)
    

def main():
  try:
    Handler = ServerHandler
    print "starting.."
    httpd = HTTPServer(("", PORT), Handler)
    httpd.serve_forever()
  except KeyboardInterrupt:
    print '^C stop'
    httpd.socket.close()

if __name__ == '__main__':
  main()
