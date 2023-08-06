from omxware import omxware
from omxware.Connect import Connection

"""
OMXWare Genome Entity Class
"""

class Genome:
    """Genome Class"""
    __omx_token = ''


    def __init__(self, connecthdr: Connection, genome):
        """Constructor"""

        if not ("ACCESSION_NUMBER" in genome):
            raise Exception("The Accession number is missing in the given Genome object.")

        self._jobj = genome
        self._genomeAccessionNumber = genome['ACCESSION_NUMBER']
        self._genusName = genome['GENUS_NAME']
        self._connecthdr = connecthdr

        config = self._connecthdr.getConfig()
        self.__omx_token = config.getOMXToken()

    def __str__(self):
        return "{ 'type': 'genome', 'name': '" + self.get_genus_name() + "', 'accession': '" + self.get_accession() + "', 'tax_id': '"+self.get_tax_id()+"'}"

    def get_name(self):
        return str(self._genusName)

    def get_genus_name(self):
        return str(self._jobj['GENUS_NAME'])

    def get_tax_id(self):
        return str(self._jobj['GENUS_TAX_ID'])

    def get_accession(self):
        return str(self._genomeAccessionNumber)

    def genes(self):
        omx = omxware.omxware(self.__omx_token)
        return omx.genes_by_genome(self._genomeAccessionNumber)

    def resistant_genes(self):
        omx = omxware.omxware(self.__omx_token)
        return omx.resistant_genes_by_genome(self._genomeAccessionNumber)

    def genera_with_resistant_genes(self):
        omx = omxware.omxware(self.__omx_token)
        return omx.genera_with_resistant_genes_by_genome(self._genomeAccessionNumber)

    def genomes_with_resistant_genes(self):
        omx = omxware.omxware(self.__omx_token)
        return omx.genomes_with_resistant_genes_by_genome(self._genomeAccessionNumber)

    def proteins(self):
        omx = omxware.omxware(self.__omx_token)
        return omx.proteins_by_genome(self._genomeAccessionNumber)
