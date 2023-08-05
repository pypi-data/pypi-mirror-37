# -*- coding: utf-8 -*-
#
# This class was auto-generated from the API references found at
# https://epayments-api.developer-ingenico.com/s2sapi/v1/
#
from ingenico.connect.sdk.data_object import DataObject


class PaymentProductFilter(DataObject):

    __groups = None
    __products = None

    @property
    def groups(self):
        """
        | List containing all payment product groups that should either be restricted to in or excluded from the payment context.
        
        Type: list[str]
        """
        return self.__groups

    @groups.setter
    def groups(self, value):
        self.__groups = value

    @property
    def products(self):
        """
        | List containing all payment product ids that should either be restricted to in or excluded from the payment context.
        
        Type: list[int]
        """
        return self.__products

    @products.setter
    def products(self, value):
        self.__products = value

    def to_dictionary(self):
        dictionary = super(PaymentProductFilter, self).to_dictionary()
        self._add_to_dictionary(dictionary, 'groups', self.groups)
        self._add_to_dictionary(dictionary, 'products', self.products)
        return dictionary

    def from_dictionary(self, dictionary):
        super(PaymentProductFilter, self).from_dictionary(dictionary)
        if 'groups' in dictionary:
            if not isinstance(dictionary['groups'], list):
                raise TypeError('value \'{}\' is not a list'.format(dictionary['groups']))
            self.groups = []
            for groups_element in dictionary['groups']:
                self.groups.append(groups_element)
        if 'products' in dictionary:
            if not isinstance(dictionary['products'], list):
                raise TypeError('value \'{}\' is not a list'.format(dictionary['products']))
            self.products = []
            for products_element in dictionary['products']:
                self.products.append(products_element)
        return self
