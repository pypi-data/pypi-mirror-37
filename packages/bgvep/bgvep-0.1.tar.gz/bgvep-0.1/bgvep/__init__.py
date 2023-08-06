from .readers import Tabix, BGPack


def get(genome_reference, vep_build, chr_, start, stop):
    with Tabix(genome_reference, vep_build) as reader:
        yield from reader.get(chr_, start, stop)


def get_most_severe(genome_reference, vep_build, chr_, start, stop):
    with BGPack(genome_reference, vep_build) as reader:
        yield from reader.get(chr_, start, stop)
