"""
SWISSMODEL
==========
"""

import json
import logging
import requests
import ssbio.utils
import os.path as op
from collections import defaultdict

log = logging.getLogger(__name__)


class SWISSMODEL():
    """Methods to parse through a SWISS-MODEL metadata set.

    Download a particular organism's metadata from SWISS-MODEL here: https://swissmodel.expasy.org/repository

    Args:
        metadata_dir (str): Path to the extracted SWISS-MODEL_Repository folder

    """

    def __init__(self, metadata_dir):
        self.metadata_dir = metadata_dir
        """str: Path to the extracted SWISS-MODEL_Repository folder"""

        self.all_models = None
        """dict: Dictionary of lists, UniProt ID as the keys"""

        # Parse the INDEX_JSON file and then store all the metadata in all_models
        self.parse_metadata()

    @property
    def metadata_index_json(self):
        """str: Path to the INDEX_JSON file."""
        try:
            return op.join(self.metadata_dir, 'INDEX.json')
        except FileNotFoundError:
            return op.join(self.metadata_dir, 'INDEX_JSON')

    @property
    def uniprots_modeled(self):
        """list: Return all UniProt accession numbers with at least one model"""
        return list(self.all_models.keys())

    def parse_metadata(self):
        """Parse the INDEX_JSON file and reorganize it as a dictionary of lists."""

        all_models = defaultdict(list)

        with open(self.metadata_index_json) as f:
            loaded = json.load(f)

        for m in loaded['index']:
            all_models[m['uniprot_ac']].append(m)

        self.all_models = dict(all_models)

    def get_models(self, uniprot_acc):
        """Return all available models for a UniProt accession number.

        Args:
            uniprot_acc (str): UniProt ACC/ID

        Returns:
            dict: All available models in SWISS-MODEL for this UniProt entry

        """
        if uniprot_acc in self.all_models:
            return self.all_models[uniprot_acc]
        else:
            log.error('{}: no SWISS-MODELs available'.format(uniprot_acc))
            return None

    def get_model_filepath(self, infodict):
        """Get the path to the homology model using information from the index dictionary for a single model.

        Example: use self.get_models(UNIPROT_ID) to get all the models, which returns a list of dictionaries.
            Use one of those dictionaries as input to this function to get the filepath to the model itself.

        Args:
            infodict (dict): Information about a model from get_models

        Returns:
            str: Path to homology model

        """
        u = infodict['uniprot_ac']

        original_filename = '{}_{}_{}_{}'.format(infodict['from'], infodict['to'],
                                                 infodict['template'], infodict['coordinate_id'])
        file_path = op.join(self.metadata_dir, u[:2], u[2:4], u[4:6],
                            'swissmodel', '{}.pdb'.format(original_filename))

        if op.exists(file_path):
            return file_path
        else:
            log.warning('{}: no file {} found for model'.format(u, file_path))
            return None

    def download_models(self, uniprot_acc, outdir='', force_rerun=False):
        """Download all models available for a UniProt accession number.

        Args:
            uniprot_acc (str): UniProt ACC/ID
            outdir (str): Path to output directory, uses working directory if not set
            force_rerun (bool): Force a redownload the models if they already exist

        Returns:
            list: Paths to the downloaded models

        """
        downloaded = []
        subset = self.get_models(uniprot_acc)

        for entry in subset:
            ident = '{}_{}_{}_{}'.format(uniprot_acc, entry['template'], entry['from'], entry['to'])
            outfile = op.join(outdir, ident + '.pdb')

            if ssbio.utils.force_rerun(flag=force_rerun, outfile=outfile):
                response = requests.get(entry['url'])

                if response.status_code == 404:
                    log.error('{}: 404 returned, no model available.'.format(ident))

                else:
                    with open(outfile, 'w') as f:
                        f.write(response.text)

                    log.debug('{}: downloaded homology model'.format(ident))
                    downloaded.append(outfile)
            else:
                downloaded.append(outfile)

        return downloaded

    def organize_models(self, outdir, force_rerun=False):
        """Organize and rename SWISS-MODEL models to a single folder with a name containing template information.

        Args:
            outdir (str): New directory to copy renamed models to
            force_rerun (bool): If models should be copied again even if they already exist

        Returns:
            dict: Dictionary of lists, UniProt IDs as the keys and new file paths as the values

        """
        for u, models in self.all_models:
            for m in models:
                original_filename = '{}_{}_{}_{}'.format(m['from'], m['to'], m['template'], m['coordinate_id'])
                file_path = op.join(self.metadata_dir,
                                    u[:2], u[2:4], u[4:], 'swissmodel',
                                    '{}.pdb'.format(original_filename))
                if op.exists(file_path):
                    uniprot_to_swissmodel[uni].append(file_path)
                else:
                    log.warning('{}: no file {} found for model'.format(u, ))