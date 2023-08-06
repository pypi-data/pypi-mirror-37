import click
import logging
from modo.services import SowRose, GrowRose

log = logging.getLogger(__name__)

class RoseCLI(click.MultiCommand):
    """
    Modo Cli Class
    """
  
    CONTEXT_SETTINGS = dict(
        default_map={'sow_cls': SowRose,
                    'grow_cls': GrowRose
        }
    )

    def __init__(self, sow_cls, grow_cls):
        click.MultiCommand.__init__(self, help='sow and grow roses on a compost heap', context_settings=self.CONTEXT_SETTINGS)
        self.sow_rose = self._build_sow_command(sow_cls)
        self.grow_rose = self._build_grow_command(grow_cls)

    class RoseCommand(click.Command):
        def __init__(self, name, rose, **kwargs):
            click.Command.__init__(self, name, **kwargs)
            self.rose = rose
            self.callback = self._run

        def _run(self, **kwargs):
            self.rose(**kwargs).run()    

    def _build_sow_command(self, callback):
        options=[
            click.Option(param_decls=['--bucket-name'],
                         default='modo-basic',
                         show_default=True,
                         help='s3 bucket where modo context is stored'
            ),
            click.Option(param_decls=['--key'],
                default='modo.yml',
                show_default=True,
                help='object key for modo context'
            ),    
            click.Option(param_decls=['--version'],
                help='version of modo context object'  
            )                  
        ]
        return self.RoseCommand('sow', callback, params=options)

    def _build_grow_command(self, callback):
        return self.RoseCommand('grow', callback)

    def list_commands(self, ctx):
        """
        list commands
        """
        return ['sow', 'grow']

    def get_command(self, ctx, name):
        commands = dict(sow='sow_rose',
                        grow='grow_rose'
        )
        if not name in commands.keys():
            click.Abort()
        return getattr(self, commands[name])