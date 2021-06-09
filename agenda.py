#!/usr/bin/env python3
""" Agenda telefonica - OOP """

import argparse
import os


class Contact:

    def __init__(self, nume, numar_telefon, email):
        self.nume = nume
        self.numar_telefon = numar_telefon
        self.email = email

    def afiseaza(self):
        print('-' * 30)
        print("Nume: %s" % self.nume)
        print("Telefon: %s" % self.numar_telefon)
        print("E-mail: %s" % self.email)

    def to_csv_string(self):
        return "%s,%s,%s" % (self.nume, self.numar_telefon, self.email)

    @classmethod
    def from_csv_string(cls, csv_string):
        csv_string = csv_string.strip()
        fields = csv_string.split(',')
        if len(fields) != 3:
            print("Invalid string for contact: %s" % csv_string)
            return None
        return cls(fields[0], fields[1], fields[2])


class Agenda:

    def __init__(self):
        self.lista_contacte = []

    def adauga_contact(self, *args):
        """Adauga contacte in agenda"""
        for item in args:
            if isinstance(item, Contact):
                self.lista_contacte.append(item)
            else:
                print("Skipping %s " % item)

    def cauta_contacte(self, criteriu, valoare):
        lista_contacte = []
        for contact in self.lista_contacte:
            # contact - referinta catre fiecare obiect
            # de tip Contact, la fiecare iteratie
            if hasattr(contact, criteriu) and getattr(contact, criteriu) == valoare:
                lista_contacte.append(contact)
        return lista_contacte

    def sterge_contact(self, criteriu, valoare):
        """ Sterge contact dupa un anumit criteriu.
        Criteriu - [ 'nume', 'numar_telefon', 'email' ]
        Valoare - vine de la utilizator
        """
        for contact in self.cauta_contacte(criteriu, valoare):
            self.lista_contacte.remove(contact)

    def importa_fisier(self, cale_fisier):
        if os.path.isfile(cale_fisier):
            handler = open(cale_fisier, 'r')
            for csv_line in handler.readlines():
                self.adauga_contact(Contact.from_csv_string(csv_line))
            handler.close()
        else:
            print("Calea %s nu reprezinta un fisier" % cale_fisier)

    def exporta_fisier(self, cale_fisier):
        if os.path.isfile(cale_fisier):
            handler = open(cale_fisier, 'w')
            for contact in self.lista_contacte:
                handler.write(contact.to_csv_string())
                handler.write("\r\n")
            handler.close()

    @classmethod
    def from_csv_file(cls, cale_fisier):
        agenda = cls()
        agenda.importa_fisier(cale_fisier)
        return agenda

    def afiseaza(self):
        """Afiseaza detalii despre toate contactele din agenda"""
        for contact in self.lista_contacte:
            contact.afiseaza()


def main():
    parser = argparse.ArgumentParser(description="Agenda Telefonica")
    parser.add_argument("--file", type=str, default="agenda.csv")
    args = parser.parse_args()
    agenda = Agenda.from_csv_file(args.file)
    agenda.sterge_contact('email', 'daniel.popescu@email.ro')
    agenda.exporta_fisier(args.file)



if __name__ == "__main__":
    main()