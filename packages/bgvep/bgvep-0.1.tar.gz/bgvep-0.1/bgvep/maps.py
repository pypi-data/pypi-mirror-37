
HUMAN_GENOME_SEQUENCE_MAPS = {'chr{}'.format(c): '{}'.format(c) for c in range(1, 23)}
HUMAN_GENOME_SEQUENCE_MAPS.update({'chrX': 'X', '23': 'X', 'chr23': 'X', 'chrY': 'Y', '24': 'Y', 'chr24': 'Y'})
HUMAN_GENOME_SEQUENCE_MAPS.update({'chrM': 'M', 'MT': 'M', 'chrMT': 'M'})


SEQUENCE_NAME_MAPS = {
    'hg19': HUMAN_GENOME_SEQUENCE_MAPS,
    'hg38': HUMAN_GENOME_SEQUENCE_MAPS,
    'hg18': HUMAN_GENOME_SEQUENCE_MAPS
}
