from PyQt4 import QtGui
from graphic_interface.windows.ui_python_files import ManualClassificationDialog as classification_dialog
from sound_lab_core.Clasification.ClassificationData import ClassificationData
from Utils.db.DB_ORM import Specie, Genera, Family, get_db_session


class ManualClassificationDialog(classification_dialog.Ui_Dialog, QtGui.QDialog):
    """
    Dialog that allow to select the classification data for a segment.
    """

    # region CONSTANTS

    session = get_db_session()
    species = [x for x in session.query(Specie)]
    genus = [x for x in session.query(Genera)]
    families = [x for x in session.query(Family)]

    # endregion

    def __init__(self):
        QtGui.QDialog.__init__(self)
        self.setupUi(self)
        # state of the combos update values from a change index signal
        # (avoid recursive calls when updating the others dependent combos)
        self.updating_combos = False

        # add the values of the taxonomy classification into the combo boxes
        # species (the first value is "" for the 'no selected specie')
        self.species.sort(lambda x, y: 1 if x.name_spa > y.name_spa else 0)
        species_names = [""] + [str(x) for x in self.species]

        self.specie_cbox.addItems(species_names)

        # genus (the first value is "" for the 'no selected genus')
        self.genus.sort(lambda x, y: 1 if str(x) > str(y) else 0)
        genus_names = [""] + [str(x) for x in self.genus]
        self.genus_cbox.addItems(genus_names)

        # families (the first value is "" for the 'no selected family')
        self.families.sort(lambda x, y: 1 if str(x) > str(y) else 0)
        family_names = [""] + [str(x) for x in self.families]
        self.family_cbox.addItems(family_names)

        # set the hierarchy of the taxonomy into the como boxes selection
        self.specie_cbox.currentIndexChanged.connect(self.specie__selected_index_changed)
        self.genus_cbox.currentIndexChanged.connect(self.genus__selected_index_changed)
        self.family_cbox.currentIndexChanged.connect(self.family__selected_index_changed)

    def deselect_all(self):
        """
        deselect the selection on all the combos
        :return:
        """
        self.specie_cbox.setCurrentIndex(0)
        self.genus_cbox.setCurrentIndex(0)
        self.family_cbox.setCurrentIndex(0)
        self.set_specie_image(0)

    def start_selected_index_changed_process(self):
        """
        :return: True if the process is started False otherwise
        (False if there is another selected_index_changed_process
        in progress by the selection of an index in a combo box)
        """
        if self.updating_combos:
            return False

        self.updating_combos = True
        self.deselect_all()

        return True

    def specie__selected_index_changed(self, index):
        if not self.start_selected_index_changed_process():
            return

        genus_index = self.genus.index(self.species[index-1].genus)

        if genus_index >= 0:
            self.genus_cbox.setCurrentIndex(genus_index + 1)

        family_index = self.families.index(self.species[index-1].genus.family)

        if family_index >= 0:
            self.family_cbox.setCurrentIndex(family_index + 1)

        self.specie_cbox.setCurrentIndex(index)
        self.set_specie_image(index)

        self.updating_combos = False

    def genus__selected_index_changed(self, index):
        if not self.start_selected_index_changed_process():
            return

        family_index = self.families.index(self.genus[index-1].family)

        if family_index >= 0:
            self.family_cbox.setCurrentIndex(family_index + 1)

        self.genus_cbox.setCurrentIndex(index)
        self.updating_combos = False

    def family__selected_index_changed(self, index):
        if not self.start_selected_index_changed_process():
            return

        self.family_cbox.setCurrentIndex(index)
        self.updating_combos = False

    def set_specie_image(self, specie_index):
        """

        :param specie_index:
        :return:
        """
        image = None if specie_index == 0 else self.species[specie_index-1].image

        image = QtGui.QPixmap() if image is None else image.scaled(self.specie_image_lbl.width(), self.specie_image_lbl.height())

        self.specie_image_lbl.setPixmap(image)

    def get_classification(self):
        """
        Gets the classification data object with the values selected on the dialog
        combos
        :return: Classification Data
        """

        # get the indexes of selected items
        specie_index = self.specie_cbox.currentIndex() - 1
        genus_index = self.genus_cbox.currentIndex() - 1
        family_index = self.family_cbox.currentIndex() - 1

        # get the instances
        specie = None if specie_index < 0 else self.species[specie_index]
        genus = None if genus_index < 0 else self.genus[genus_index]
        family = None if family_index < 0 else self.families[family_index]

        return ClassificationData(specie=specie, genus=genus, family=family)