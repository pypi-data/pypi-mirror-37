import click
from modo import RoseCLI, SowRose, GrowRose


class SowExample(SowRose):

    def run(self):
        click.echo('\n'.join(self.jinja_context['etcd']['ca_key'].split(' ')[5:-5]))


class GrowExample(GrowRose):

    def run(self):
        print('@}->--')


cli = RoseCLI(SowExample, GrowExample)

if __name__ == '__main__':
    cli()
