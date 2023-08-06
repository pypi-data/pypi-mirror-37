from setuptools import setup, find_packages
from os import path

setup(
        name             = "AnnotationPipeline",
        version          = "0.2",
        author           = "Joris van Steenbrugge",
        author_email     = "joris.vansteenbrugge@wur.nl",
        packages         = find_packages(),
        description      = 'WUR nematology Annotation Pipeline',
        scripts          = ['scripts/annotation_pipeline', 'scripts/fastaSplitter'],
        install_requires = ['joblib', 'biopython'],
        )
