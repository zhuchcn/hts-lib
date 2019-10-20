from datetime import datetime


def log(msg):
    print(
        '[ ' + datetime.now().strftime("%Y-%m-%d %H:%M:%S") + 
        " ] " + msg
    )

class CommandConfig():
    name = None
    args = None
    func = None
    mapper = None
    help = None
    description = None

    def __init__(self, argparser):
        if not self.name:
            raise ValueError('Command name not set')
        if not self.args:
            raise ValueError('Command args not set')
        if not self.func:
            raise ValueError('Commnad func not set')
        if not self.mapper:
            raise ValueError('Command mapper not set')
        parser = argparser.add_parser(
            self.name, help=self.help, description=self.description
        )
        for arg in self.args:
            parser.add_argument(*arg[0], **arg[1])
        parser.set_defaults(func=self.map_args)
    
    def map_args(self, args):
        kwargs = {key: getattr(args, val) for key,val in self.mapper.items()}
        self.func.__func__(**kwargs)

