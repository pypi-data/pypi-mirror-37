"""A module that uses the TypedColumnReader utility (a csv-like file reader)
to extract SMILES and properties from a SMILES file, exposing the
service as an iterator.
"""

from rdkit import Chem

from pipelines_utils.TypedColumnReader import TypedColumnReader


class MolFromTypedColumnReader(object):
    """Creates molecules from a typed column file, exposing the results
    as an iterator.
    """

    def __init__(self, smiles_file):
        """Initialises the module with a smiles_file.

        :param smiles_file: The typed column file. smiles_file can be any object
                            which supports the iterator protocol and returns a
                            string each time its next() method is called
        """

        self._smiles_file = smiles_file
        self._smiles_column_name = None
        # Other object members, set on initialisation.
        self._tcr = None

    def initialise(self,
                   column_sep='\t',
                   type_sep=':',
                   header=None,
                   smiles_column_name='smiles'):
        """Initialises the object. Here we can provide additional material
        like the file column separator, type separator and header for files
        that do not have one.

        This method must be called prior to iterating through the file.

        :param column_sep: The column separator
        :param type_sep: The separator of column name and its type definition
        :param header: A header (for files that do not have one)
        :param smiles_column_name: The name of the SMILES column in the file
        """

        self._smiles_column_name = smiles_column_name
        # Create the TypedColumnReader (a generator)
        # and convert to an iterator.
        self._tcr = iter(TypedColumnReader(self._smiles_file,
                                           column_sep=column_sep,
                                           type_sep=type_sep,
                                           header=header))

    def __iter__(self):
        """Basic iterator requirements.
        """
        return self

    def next(self):
        """Creates the next molecule from the SMILES file.

        Additional columns in the file are added as suitably typed
        properties of the molecule that's created.

        :returns: A molecule object or None if one could not be created.
        """
        # We must have been initialised!
        if not self._tcr:
            raise AssertionError('Not initialised')

        # Get the next entry in the file.
        # We are given a dictionary of type-converted values.
        # The column names and types are defined in the header.
        # We expect a column called 'smiles'.
        row_content = next(self._tcr)
        if not row_content:
            # The end
            raise StopIteration

        # Create a MOL from the smiles string.
        smiles = row_content[self._smiles_column_name]
        mol = Chem.MolFromSmiles(smiles)
        if mol:
            # Now set molecule properties
            # based on all the other parts of the row.
            # These can be floats, ints, strings etc.
            for name in row_content:
                if name != self._smiles_column_name:
                    value = row_content[name]
                    if type(value) is float:
                        mol.SetDoubleProp(name, value)
                    elif type(value) is int:
                        mol.SetIntProp(name, value)
                    elif type(value) is str:
                        mol.SetProp(name, value)

        # Molecule and properties ready for release...
        # But it might also be 'None'
        return mol

    def __del__(self):
        self._tcr = None
