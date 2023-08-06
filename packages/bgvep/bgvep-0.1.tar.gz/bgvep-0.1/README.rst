
BGVEP
=====

Read data generated within the **bgvep** project.
Within that project there are two datasets, both identified by
the reference genome (e.g. hg19) and the VEP version (e.g. 88):

- a tabix file with the run of vep for all positions in the genome
- a bgpack file with only the most severe consequence type.


Installation
------------

This project is a Python package
and can be installed with ``pip``.
Download the source code, get into this
project directory and execute:

.. code:: bash

   pip install .


Usage
-----

To request the output of 1 or more positions, simply indicate the
chromosome, the initial and the final positions you are interested.



Commad line usage
*****************

Execute :code:`bgvep --help` for getting all the information.

The output is printed to the screen using tabs as separators for the indexes:

.. code:: bash

   bgvep --genome hg19 --vep 88 --chromosome chr1 --begin 100000 --end 100004


Adding the ``--most-severe`` flags, returns the most severe consequence type
for the 3 possible changes of the allele in that position.



Python usage
************

The easiest way to use **bgvep** is to make use of the generators **get** and
**get_most_severe**.

.. code:: python

   from bgvep import get
   for data in get('hg19', '88', 'chr1', 100000, 100004):
       ...

However, the *best* way to use **bgvep** is using directly the readers:
the *Tabix* and the *BGPack* readers, which are context managers.

.. code:: python

   from bgvep.readers import Tabix

   with Tabix('hg19', '88') as reader:
        for data in reader.get('chr1', 100000, 100004):
             ...


The advantage of using directly the readers is that they are not instantiated
on every call.


The output
----------


The format of the output is:

- Chromosome
- Position
- Reference
- Alternate
- Gene
- Feature
- Feature_type
- Consequence
- cDNA_position
- CDS_position
- Protein_position
- Amino_acids
- Codons
- Existing_variation
- Impact
- Distance
- Strand
- Flags
- Symbol
- Symbol source
- HGNC_ID
- Canonical
- ENSP


When asking for the **most-severe** consquence type, the output is formed
by the most severe consequente type of all the possible changes of the reference
allele. The order is always ACGT, and if the refernce allele changes to itself,
nothing is returned for it.


Support
-------

If you are having issues, please let us know.
You can contact us at: bbglab@irbbarcelona.org
