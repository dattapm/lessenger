import cgi
import json
import urllib
import urllib2

from common import exceptions

class Base(object):

  def __init__(self):
    self.server_url = "http://localhost:9000"
    self.api_headers = {
                        'Content-Type': 'application/json'
                       }

  def GetFormData(self, environ):
      # When the method is POST the variable will be sent
      # in the HTTP request body which is passed by the WSGI server
      # in the file like wsgi.input environment variable.

      form_data = {}

      content_type = environ.get("CONTENT_TYPE")
      if content_type:
        content_type_value, content_type_dict = cgi.parse_header(content_type)
        if content_type_value == "multipart/form-data":
          form_data = cgi.parse_multipart(environ["wsgi.input"], content_type_dict)
        elif content_type_value == "application/json":

          try:
            request_body_size = int(environ.get("CONTENT_LENGTH", 0))
          except (ValueError):
            request_body_size = 0
          
          try:
            request_body = environ["wsgi.input"].read(request_body_size)
            request_body = cgi.parse_qs(request_body)
            form_data = json.loads(request_body["json"][0])
          except:
            raise exceptions.InvalidJSONResponseException("Invalid JSON message received by API.")  
        else:
          raise exceptions.UnsupportedMediaTypeException("%s Content-Type not supported." %(content_type_value))
      else:
        raise exceptions.HTTPRequestException("Content-Type header not found in HTTP environment.")

      return form_data

  def GetHTTPResponse(self, url_data, api_name):
    try:
      print "in GETHTTPRSP TRY"
      data = urllib.urlencode({"json": json.dumps(url_data)})
      url = self.server_url + api_name
      req = urllib2.Request(url, data, self.api_headers)
      response = urllib2.urlopen(req)
      response = json.loads(cgi.parse_qs(response.read())["json"][0])
      print "GETHTTPRSP: ",response
    except:
      print "in GETHTTPRSP EXCEPT"

    return response

  def __del__(self):
    pass
