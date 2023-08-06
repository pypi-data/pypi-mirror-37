from omxware import omxware
from omxware.Connect import Connection

"""
OMXWare Protein Entity Class
"""


class Protein:
    """Protein Class"""
    __omx_token = ''

    def __init__(self, connecthdr: Connection, protein):
        """Constructor"""

        if not ("PROTEIN_UID_KEY" in protein):
            raise Exception("The PROTEIN_UID_KEY is missing in the given Protein object.")

        self._jobj = protein

        self._proteinUidKey = protein['PROTEIN_UID_KEY']
        self._proteinName = protein['PROTEIN_FULLNAME']

        if 'PROTEIN_SEQUENCE' in protein:
            self._proteinSequence = protein['PROTEIN_SEQUENCE']
        else:
            self._proteinSequence = ''

        self._connecthdr = connecthdr

        config = self._connecthdr.getConfig()
        self.__omx_token = config.getOMXToken()

    def __str__(self):
        return "{ 'type': 'protein', 'uid': '" + self.get_uid() + "', 'name': '" + self.get_name() + "', 'sequence: '"+self.get_sequence()+"'}"

    def get_name(self):
        return str(self._proteinName)

    def get_sequence(self):
        return str(self._proteinSequence)

    def get_uid(self):
        return str(self._proteinUidKey)
