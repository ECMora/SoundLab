# -*- coding: utf-8 -*-
from utils.db.DB_ORM import Genera, Family, Specie


class ClassificationData:
    """
    Class that represents the classification or identification
    of a detected segment.
    Contains the (partial if identification) taxonomic classification of
    the segment.
    """

    def __init__(self, specie=None, genus=None, family=None):
        """
        create the classification-identification object.
        :param specie: The specie of the segment
        :param genus: The genus of the specie of the segment
        :param family: The family of the specie of the segment
        :param taxa: The taxa of the specie of the segment
        :return:
        """
        if specie is not None and not isinstance(specie, Specie):
            raise Exception("Invalid argument type (specie must be of tye Specie).")
        if genus is not None and not isinstance(genus, Genera):
            raise Exception("Invalid argument type (genus must be of tye Genera).")
        if family is not None and not isinstance(family, Family):
            raise Exception("Invalid argument type (family must be of tye Family).")

        self.specie = None
        self.genus = None
        self.family = None

        if specie is not None:
            self.specie = specie
            self.genus = self.specie.genus
            self.family = self.genus.family

        elif genus is not None:
            self.genus = genus
            self.family = self.genus.family

        else:
            self.family = family

        if self.specie != specie or \
           (family is not None and self.family != family) or \
           (genus is not None and self.genus != genus):

            raise Exception("Invalid arguments. The relationship between the classification taxonomy is incorrect")

    def get_image(self):
        """
        :return: the image associated with the specie of the classification
        """
        if self.specie is None:
            return None
        return self.specie.image

    def __str__(self):
        if self.specie:
            return self.specie.name_spa
        if self.genus:
            return "Genus: " + str(self.genus)
        if self.family:
            return "Family: " + str(self.family)
        return "No Classified"

    def get_full_description(self):
        desc = ""
        if self.specie:
            desc += "Specie: " + str(self.specie) + "\n"
        if self.genus:
            desc += "Genus: " + str(self.genus) + "\n"
        if self.family:
            desc += "Family: " + str(self.family) + "\n"

        if not desc:
            desc = "No identified"

        return desc