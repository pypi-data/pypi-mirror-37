#all imports
from webbrowser import open_new
from datetime import datetime
from  os import  path,makedirs
from sunlite.db import connect
from  flask import  Flask , render_template , url_for
from flask_restful import  Resource,Api
import  logging
import json




class Serve(object):
       def __init__(self,name='',logs=True,logfolder=''):
              self.name = ":memory:" if name == '' else name
              if logs:
                     self.logs = True
                     logfolder = path.realpath(__file__) + "logs/{0}".format(str(datetime.today().date())) if logfolder=='' else logfolder
                     try:
                            makedirs(logfolder)
                     except:
                            pass
                     logtime = "time-{0}-{1}".format(datetime.now().time().hour,datetime.now().time().minute)
                     logfile = "{1}/database-{0}-{2}.log".format(self.name.replace(":",''),logfolder , logtime)
                     if path.exists(logfile):
                            logging.basicConfig(filename=logfile ,
                                         format='%(asctime)s %(message)s',
                                         filemode='a')
                     else:
                            logging.basicConfig(filename=logfile,
                                                format='%(asctime)s %(message)s',
                                                filemode='w')
                     self.logger = logging.getLogger()
                     self.logger.setLevel(logging.DEBUG)
                     self.logger.info("Sucess !  Logger Started. Writing logs on '{0}'".format(logfile))
              else:
                     self.logs = False
              with open("dump",'w') as f:
                     f.write(json.dumps({'name':self.name , 'logs':False}))
                     f.close()
              self.APP = Flask(__name__)
              self.API = Api(self.APP)
       def build_links(self):
              class MyDataManager(Resource):
                     def __init__(self):
                            with open('dump', 'r') as f:
                                   d = json.loads(f.read())
                                   f.close()
                            self.co = connect(d['name'], logs=d['logs'])
                     def get(self, topic):
                            try:
                                   return {topic: str(self.co.pull(topic))}
                            except:
                                   return {topic: "doesn't exists"}
              class MyDataAddManager(Resource):
                     def __init__(self):
                            with open('dump', 'r') as f:
                                   d = json.loads(f.read())
                                   f.close()
                            self.co = connect(d['name'], logs=d['logs'])
                            with open("Config",'r') as f:
                                   self.header = f.read()
                                   f.close()
                     def get(self, name , data,header=''):
                            header = self.header if header=='' else header
                            try:
                                   self.co.push(name,data,header)
                                   return {name: "Set Sucessfully"}
                            except:
                                   return {name: "Failed . Recheck data"}
              class MyFullData(Resource):
                     def __init__(self):
                            with open('dump', 'r') as f:
                                   d = json.loads(f.read())
                                   f.close()
                            self.co = connect(d['name'], logs=d['logs'])
                     def get(self):
                            return  self.co.List()
              class MyAddHeader(Resource):
                     def __init__(self):
                            with open('dump', 'r') as f:
                                   d = json.loads(f.read())
                                   f.close()
                            self.co = connect(d['name'], logs=d['logs'])

                     def get(self, name):
                            try:
                                   self.co.new(name)
                                   return {name: "Created New Header"}
                            except:
                                   return {name: "Failed . Recheck data"}
              class MyAllHeader(Resource):
                     def __init__(self):
                            with open('dump', 'r') as f:
                                   d = json.loads(f.read())
                                   f.close()
                            self.co = connect(d['name'], logs=d['logs'])

                     def get(self):
                            try:
                                   return {'headers': self.co.headers()}
                            except:
                                   return {'headers' :"Failed . Recheck data"}
              class MyGet(Resource):
                     def __init__(self):
                            with open('dump', 'r') as f:
                                   d = json.loads(f.read())
                                   f.close()
                            self.co = connect(d['name'], logs=d['logs'])
                     def get(self, name):
                                   try:
                                          return {name: self.co.get(name)}
                                   except:
                                          return {name: "Failed to fetch data"}
              self.API.add_resource(MyGet,'/g/<string:name>')
              self.API.add_resource(MyAllHeader,'/h/')
              self.API.add_resource(MyAddHeader,'/new/<string:name>')
              self.API.add_resource(MyFullData,'/a/')
              self.API.add_resource(MyDataAddManager,'/add/<string:name>/<string:data>/<string:header>')
              self.API.add_resource(MyDataManager, '/p/<string:topic>')

       def invoke(self,ip="127.0.0.1",port=5000):
              if self.logs:
                     self.logger.info("Sucess ! Api decleared.")
              if self.logs:
                     self.logger.info("Sucess ! Connected to {0}".format(self.name))
                     self.build_links()
              with open('dump', 'r') as f:
                     d = json.loads(f.read())
                     f.close()
              @self.APP.route('/')
              def HomePage():
                     return  render_template('main.html' , DBname=d['name'])
              if ip=='127.0.0.1' and port ==5000 :
                     open_new('http://localhost:5000/')
                     self.APP.run()
              else:
                     try:
                            open_new('http://127.0.0.1:5000/')
                            self.APP.run(host=ip,port=port , template_folder=path.realpath(__file__) +"/templates" , static_folder=path.realpath(__file__) +'/static')

                     except:
                            raise Exception('Invalied IP and Host : '+ip+':'+str(port))



