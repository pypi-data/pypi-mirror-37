from omxware import omxware
from omxware.Connect import Connection

"""
OMXWare Gene Entity Class
"""


class Gene:
    """Gene Class"""

    __omx_token = ''

    def __init__(self, connecthdr: Connection, gene):
        """Constructor"""

        if not ("GENE_UID_KEY" in gene):
            raise Exception("The GENE_UID_KEY is missing in the given Gene object.")

        self._jobj = gene

        self._geneUidKey = gene['GENE_UID_KEY']
        self._geneName = gene['GENE_FULLNAME']

        if 'GENE_SEQUENCE' in gene:
            self._geneSequence = gene['GENE_SEQUENCE']
        else:
            self._geneSequence = ''

        self._connecthdr = connecthdr

        config = self._connecthdr.getConfig()
        self.__omx_token = config.getOMXToken()

    def __str__(self):
        return "{'type': 'gene', 'uid': '" + self.get_uid() + "', 'name': '" + self.get_name() + "', 'sequence: '"+self.get_sequence()+"'}"

    def get_name(self):
        return str(self._geneName)

    def get_sequence(self):
        return str(self._jobj['GENE_SEQUENCE'])

    def get_uid(self):
        return str(self._geneUidKey)

    def toFasta(self):
        if(len(self.get_sequence().strip()) == 0):
            return ''
        else:
            fasta_content = '>omx|gene_' + self.get_uid() + ' ' + self.get_name() + '\n' + self.get_sequence() + '\n'
            return fasta_content
