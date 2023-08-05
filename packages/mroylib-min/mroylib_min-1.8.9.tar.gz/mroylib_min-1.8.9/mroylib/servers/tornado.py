import tornado
import tornado.web
from tornado.websocket import WebSocketHandler
from mroylib.config import Config
import re
import time
import ssl
import os
import logging
import logging.config

import inspect
import importlib
import sys
import argparse
import json
from functools import partial, wraps

J = os.path.join
E = os.path.exists

CC_HEADER = """## written by Mroylib
from mroylib.servers.tornado import Base, Manifest,check

"""
controlll_tmp = """

class -[name]-(Base):
    @check
    def get(self):
        return "Hello"

    def post(self, name):
        return "i got" + name
"""
UI_HEADER = """import tornado
"""
ui_temp = """
class -[name]-(tornado.web.UIModule):
    def render(self, **kwargs):
        return self.render_string('_-[namel]-.html', 
            **kwargs
        )

"""

temp_html = """

<!DOCTYPE html>
<html lang="en">
<head>      
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0, minimum-scale=1.0, maximum-scale=1.0, user-scalable=no" />
    <title>-[name]-</title>     
    <link href="/static/bootstrap-4/css/bootstrap.css" rel="stylesheet"></link>
    {% block head_css %}
         <link href="/static/css/-[name]-.css" rel="stylesheet"></link>
    {% end %}
    {% block extends_css %}
    {% end %}
</head>     
<body style="background: #ddd">      
    <div class="main" class='main'>
        <input name="search" type="text" class="form-control" id="id-search" value="" placeholder="search's value " style="width: 300px; left: 100px; margin: 20px">
        <div class="body col-md-8 col-lg-9 col-xl-10" style="display: flex ;display: flex;align-items: flex-end;flex-wrap: wrap;">
            {% block content %}
            {% end %}
        </div>
        
            
        </div>
        <div class="tail">
        {% block tail %}
        {% end %}
        </div>
    </div>
    
    <div class="modal fade" id="progressbar" tabindex="-1" role="dialog" aria-labelledby="exampleModalCenterTitle" aria-hidden="true" data-backdrop="static" data-keyboard="false" >
      <div class="modal-dialog modal-dialog-centered" role="document">
        <div class="modal-content">
            <div class="modal-header">
                <h5 class="modal-title" id="modal-title">wait ...</h5>
            </div>
            <div class="modal-body">
                <div class="progress" style="height: 1px;">
                  <div id='p-bar' class="progress-bar" role="progressbar" style="width: 0%;" aria-valuenow="25" aria-valuemin="0" aria-valuemax="100"></div>
                </div>
            </div>
        </div>
      </div>
    </div>

    <script src="/static/jquery/dist/jquery.min.js"></script>
    <script src="/static/bootstrap-4/js/bootstrap.js"></script>
    <script src="/static/js/websocket.js"></script>
    {% block body_js %}
        <script src="/static/js/-[name]-.js"></script>
    {% end %}

    {% block extends_js %}
    {% end %}
</body>     
</html>
"""

extend_html = """
{% extends "template/-[extend]-.html"  %}
    {% block extends_css %}
        <link href="/static/css/template/-[name]-.css" rel="stylesheet"></link>
    {% end  %}

    {% block content %}
    {% end %}

    {% block tail %}
    {% end %}

    {% block extends_js %}
    <script src="/static/js/template/-[name]-.js"></script>
    {% end %}

"""

def check(func):

    @wraps(func)
    def _func(*args):
        f = inspect.getfullargspec(func)
        self = args[0]
        val = [args[0]]
        
        try:
            for k in f.args[1:]:
                val.append(self.get_argument(k))
        except :
            for k in f.args[1:]:
                val.append(json.loads(self.requests.body).get(k))
        res = func(*val)
        # print("return : ",res)
        # print(func.__name__.upper())
        if func.__name__ == 'get':
            tmp = self.load_page()
            if isinstance(res, str):
                self.write(res)
                self.finish()
                return 
            elif isinstance(res, (list, tuple)):
                return self.render(tmp, args=res)
            elif isinstance(res, dict):
                return self.render(tmp, **res)
            else:

                logging.error("must return str, list, dict!")
                self.write("Handler return error!")
                self.finish()
                return 

        else:
            if isinstance(res, str):
                self.write(res)
            else:
                self.write(json.dumps(res))
            self.finish()

    return _func


class Manifest(type):
    _route = {}
    _config = {
        "base_dir": None,
        'static_path' : None,
        'port': None,
        'db':None,
        'cookie_secret':'This is a cookie',
        'debug':True,
        'autoreload':True,

    }

    def __new__(cls ,name, bases, attrs):
        if name == "Base":
            return super(Manifest, cls).__new__(cls, name, bases, attrs)
        
        Ocl = super(Manifest, cls).__new__(cls, name, bases, attrs)
        if 'route' in attrs:
            _rout = attrs['route']
            if not _rout.startswith("/"):
                _rout = "/" + _rout
        else:
            _rout = '/' + name.lower()
            if name == 'Index':
                _rout = '/'
        Manifest._route[_rout] = Ocl
        for _name in attrs:
            if _name == 'get' or _name == 'post':
                fun = attrs[_name]
                attrs[_name] = tornado.web.asynchronous(check(fun))
        return Ocl


    @classmethod
    def init(cls, name, path):
        if not E(path):
            os.mkdir(path)
        if not E(J(path,'static')):
            os.mkdir(J(path,'static'))
            src = J(os.path.dirname(__file__), 'res')
            res = os.popen("cp -a %s  %s " % (src + "/*" , J(path, 'static'))).read()
            print(res)

        if not E(J(path,'template')):
            os.mkdir(J(path,'template'))
            with open(J(J(path,"template"), 'index.html'), 'w') as fp:
                fp.write(temp_html)

        config = J(path,'config.ini')
        if not E(config):
            with open(config, 'w') as fp:
                pass
        if not E(J(path, 'controller.py')):
            with open(J(path, 'controller.py'), 'w') as fp:
                fp.write(CC_HEADER)

        if not E(J(path, 'ui_modules.py')):
            with open(J(path, 'ui_modules.py'), 'w') as fp:
                fp.write(UI_HEADER)

        if not E(J(path,'db.sql')):
            with open(J(path, 'db.sql'), 'w') as fp:
                pass

        con = Config(file=config)
        con.section = 'server-config'
        con['base_dir'] = path
        con['port'] = '18080'
        con['db_path'] = J(path,'db.sql')
        con['static_path'] = J(path,'static')
        con['keyfile'] = ''
        con['certfile'] = ''

        con.section = 'loggers'
        
        con['keys'] = 'root'

        con.section = 'logger_root'
        

        con['level']= 'DEBUG'
        con['handlers'] = 'hand01,hand02'
        
        con.section = 'handlers'

        con['keys'] = 'hand01,hand02'

        con.section = 'formatters'
        con['keys'] = 'simple'

        con.section = 'handler_hand01'

        con['class']= 'StreamHandler'
        con['level'] = 'INFO'
        con['formatter'] = 'simple'
        con['args'] = '(sys.stderr,)'
        
        con.section = 'handler_hand02'

        con['class'] = 'handlers.RotatingFileHandler'
        con['level'] = 'INFO'
        con['args'] = "('/tmp/%s.log', 'a', 10*1024*1024, 5)" % name

        con.section = 'program:%s' % name

        con['command'] = '/usr/local/bin/m-server -c %s' % J(path, 'config.ini')
        con['stdout_logfile'] = '/tmp/%s.log' % name
        con['stderr_logfile'] = '/tmp/%s.err.log' % name

        con.section = 'formatter_simple'
        con['format'] = """%(asctime)s | %(levelname)s [%(filename)s:%(lineno)s]: %(message)s  """
        con.save()

        cls.add_controller(path, 'Index')


    @classmethod
    def add_ui(cls, path, name):
        if not E(J(path,"ui_modules.py")):
            logging.error("no ui_modules.py found !")
            return 
        with open(J(path,"ui_modules.py"), "a+") as fp:
            nc = name[0].upper() + name[1:].lower()
            ncl = name.lower()
            cc = ui_temp.replace("-[name]-", nc)
            cc = cc.replace("-[namel]-", ncl)
            fp.write("\n"+cc)
            with open(J(J(path, 'template'), '_' + ncl + ".html"), "w") as fp:
                pass
        print("[+]", 'add ui module: ', name)

    @classmethod
    def add_controller(cls, path, namec, extend=None):

        if not E(J(path,"controller.py")):
            logging.error("no controller.py found !")
            return 

        if not re.match(r'\w+', namec):
            logging.error("must charset [a-Z0-9]")
            return

        name = namec[0].upper() + namec[1:]
        namel = name.lower()
        print("[+]", 'add controller: ', name)
        

        with open(J(path,"controller.py"), "a+") as fp:
            cc = controlll_tmp.replace("-[name]-", name)
            fp.write("\n"+cc)

        

        with open(J(J(path,"template"), namel + ".html"), 'w') as fp:
            if extend:
                html_cc = extend_html.replace("-[name]-", namel)
                html_cc = html_cc.replace("-[extend]-", extend)
            else:
                html_cc = temp_html.replace("-[name]-", namel)
            fp.write(html_cc)

        with open(J(J(J(path,"static"),"js"), namel + ".js"), 'w') as fp:
            pass

        with open(J(J(J(path,"static"),"css"), namel + ".css"), 'w') as fp:
            pass


    @classmethod
    def run(cls, config):
        if not E(config):
            logging.error('not found config: %s' % config)
            return
        c = Config(file=config)
        c.section = 'server-config'
        logging.config.fileConfig(config)
        B = c.get('base_dir', J('/tmp',str(time.time())) )
        cls._config['base_dir'] = B
        cls._config['port'] = c.get('port', 18080)
        cls._config['db_path'] = c.get('db_path', J(B,'db.sql'))
        cls._config['static_path'] = c.get('static_path', J(B,'static'))
        cls._config['template_path'] = J(B,'template')
        cak = c.get('keyfile')
        cac = c.get('certfile')        
        

        port = cls._config.get('port')       
        cls._config['log'] = logging.getLogger('root')

        sys.path += [B]
        importlib.import_module("controller")
        uis = importlib.import_module("ui_modules")

        ui_m = {i:uis.__dict__[i] for i in uis.__dict__.keys() if not i.startswith('_')}
        cls._config['ui_modules'] = ui_m
        appication = tornado.web.Application(cls._route.items(),**cls._config)
        


        if cak:

            ssl_ctx = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
            ssl_ctx.load_cert_chain(cac,keyfile=cak, password='hello')
            http_server = tornado.httpserver.HTTPServer(appication, ssl_options=ssl_ctx)
            http_server.listen(port)
        else:
            appication.listen(port)

        tornado.ioloop.IOLoop.instance().start()






class Base(tornado.web.RequestHandler, metaclass=Manifest):
    def prepare(self):
        self.db = self.settings['db_path']
        self.L = self.settings['log']
        self.base_path = self.settings['base_dir']
        self.tloop = tornado.ioloop.IOLoop.current()
    def get_current_user(self):
        return (self.get_cookie('user'),self.get_cookie('passwd'))
    def get_current_secure_user(self):
        return (self.get_cookie('user'),self.get_secure_cookie('passwd'))
    def set_current_seccure_user_cookie(self,user,passwd):
        self.set_cookie('user',user)
        self.set_secure_cookie("passwd",passwd)

    def load_page(self):
        name = J(os.path.join(self.base_path, 'template'), self.__class__.__name__.lower() + ".html")
        self.L.info("loading from : %s" % name)
        if not name.endswith('.html'):
            name += '.html'
        return name

    def json_reply(self,data):
        self.write(json.dumps(data))


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-c", "--load-config", default=None,help="load config to run")
    parser.add_argument("-n", "--new-controller",default=None, help="add new controller")
    parser.add_argument("-u", "--new-ui-module",default=None, help="add new ui_module")
    parser.add_argument("-I", "--Init", nargs='*', default=None, help="new web initializtion")
    parser.add_argument("-e", "--extend", default=None, help="new route create extend to .. exp: -e index")


    args = parser.parse_args()

    if args.Init:
        name , path = args.Init
        Manifest.init(name, path)

    elif args.load_config:
        Manifest.run(args.load_config)

    elif args.new_controller:
        if re.match(r'\w+', args.new_controller):
            Manifest.add_controller(os.getcwd(), args.new_controller, extend=args.extend)
    elif args.new_ui_module:
        if re.match(r'\w+', args.new_ui_module):
            Manifest.add_ui(os.getcwd(), args.new_ui_module)
