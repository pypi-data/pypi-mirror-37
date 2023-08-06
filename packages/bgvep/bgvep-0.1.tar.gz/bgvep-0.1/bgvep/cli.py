
import click

from bgvep import get, get_most_severe

CONTEXT_SETTINGS = dict(help_option_names=['-h', '--help'])


def print_tabix(genome, vep, chromosome, begin, end):
    for values in get(genome, vep, chromosome, begin, end):
        print('\t'.join(values))


def print_pack(genome, vep, chromosome, begin, end):
    for pos, values in get_most_severe(genome, vep, chromosome, begin, end):
        print('\t'.join([str(pos)] + [str(v) if v is not None else '-' for v in values]))


@click.command(context_settings=CONTEXT_SETTINGS)
@click.option('--genome', '-g', help='Reference genome', required=True)
@click.option('--vep', '-v', help='VEP version', required=True)
@click.option('--chromosome', '-c', help='Chromosome', required=True)
@click.option('--begin', '-b', type=int, help='Start position', required=True)
@click.option('--end', '-e', type=int, help='Stop position', required=True)
@click.option('--most-severe', default=False, is_flag=True, help='Stop position')
@click.version_option()
def cli(genome, chromosome, begin, end, vep, most_severe):
    """bgvep help"""
    if most_severe:
        print_pack(genome, vep, chromosome, begin, end)
    else:
        print_tabix(genome, vep, chromosome, begin, end)


if __name__ == "__main__":
    cli()