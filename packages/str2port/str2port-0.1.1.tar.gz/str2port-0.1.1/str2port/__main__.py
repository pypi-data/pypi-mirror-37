import click

from . import str2port


@click.command()
@click.argument('string')
@click.option('--use-iana', is_flag=True, help='Exclude used ports from IANA list (default: false)')
def cli(string, use_iana):
    click.echo(' '.join(str(i) for i in str2port(string, use_iana=use_iana)))


if __name__ == '__main__':
    cli()
