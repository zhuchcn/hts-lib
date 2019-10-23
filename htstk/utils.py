from datetime import datetime


def log(msg):
    print(
        '[ ' + datetime.now().strftime("%Y-%m-%d %H:%M:%S") + 
        " ] " + msg,
        flush=True
    )

class CommandConfig():
    name = None
    args = []
    func = None
    mapper = {}
    help = None
    description = None

    def __init__(self, argparser):
        if not self.name:
            raise ValueError('Command name not set')
        if not self.func:
            raise ValueError('Commnad func not set')
        parser = argparser.add_parser(
            self.name, help=self.help, description=self.description
        )
        for arg in self.args:
            parser.add_argument(*arg[0], **arg[1])
        parser.set_defaults(func=self.map_args)
        self.parser = parser
    
    def map_args(self, args):
        kwargs = {key: getattr(args, val) for key,val in self.mapper.items()}
        self.func.__func__(**kwargs)

