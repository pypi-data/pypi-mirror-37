import click
from modo import RoseCLI, SowRose, GrowRose

class SowExample(SowRose):

    def run(self):
        click.echo(self.jinja_context)

class GrowExample(GrowRose):

    def run(self):
       print('@}->--')

cli = RoseCLI(SowExample, GrowExample)

if __name__ == '__main__':
    cli()