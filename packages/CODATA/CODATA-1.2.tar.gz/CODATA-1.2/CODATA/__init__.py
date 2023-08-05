"""All CODATA constants with units, uncertainty and description."""

import time
import os
import urllib.request
import sys

name = "CODATA"

__author__ = "Jelle Westra, https://github.com/JelleWestra/CODATA"
__version__ = "1.2"
__license__ = "MIT"


class Constant(float):
    """Subclass of float, with some extra atributes and a
       different representation"""
    def __new__(self, value, uncertainty, unit, description):
        return float.__new__(self, value)

    def __init__(self, value, uncertainty, unit, description):
        float.__init__(value)
        self.value = value
        self.uncertainty = uncertainty
        self.unit = unit
        self.description = description

    def __repr__(self):
        if self.uncertainty is not 0:
            if "e" in str(self.uncertainty):
                uncertainty = str(self.uncertainty)
                uncertainty = "(" + uncertainty[:uncertainty.find("e")] \
                              .replace(".", "") + ")"
            else:
                uncertainty = str(self.uncertainty)
                uncertainty = "(" + uncertainty[:uncertainty.find("00")] \
                              .replace(".", "") + ")"
        else:
            uncertainty = ""
        if "e" in str(self.value):
            return str(self.value)[:str(self.value).find("e")] + \
                   uncertainty + " " + \
                   str(self.value)[str(self.value).find("e"):] + \
                   " [ " + self.unit + " ] " + self.description
        else:
            return str(self.value) + uncertainty + " [ " + self.unit + \
                   " ] " + self.description


def update(url="https://physics.nist.gov/cuu/Constants/Table/allascii.txt"):
    """Updates the CODATA.txt"""
    global constants
    try:
        urllib.request.urlretrieve(url, "CODATA.txt")
        constants = load_values()
        make_constants(constants)
    except urllib.error.URLError:
        print("Unable to fetch the data\n")
        print(" [1] Check internet connection.")
        print(" [2] Pherhaps the domain changed check: \n" +
              "     https://physics.nist.gov/cuu/Constants/Table/allascii.txt")
        print("\nIn case of a url change try updating the package or use:")
        print("     update('new_url') instead of update()")


def load_values():
    """Loads the constants from CODATA.txt and returns a dictionary containting
       all the constants found in the file"""
    constants = {}
    with open(r"CODATA.txt", "r") as data:
        for line in range(10):
            data.readline()
        while True:
            dataString = data.readline()
            if dataString == "":
                break
            try:
                value = float(dataString[60:85].replace(" ", ""))
            except ValueError:
                valueString = dataString[60:85].replace(" ", "")
                if valueString.find("...") is not -1:
                    valueString = valueString.replace("...", "")
                try:
                    value = float(valueString.replace(" ", ""))
                except ValueError:
                    value = "NaN"

            try:
                uncertainty = float(dataString[85:110].replace(" ", ""))
            except ValueError:
                uncertaintyString = dataString[85:110].replace(" ", "")
                if uncertaintyString == "(exact)":
                    uncertainty = 0
                else:
                    uncertainty = "NaN"

            unit = dataString[110:].replace("\n", "")
            if unit == "":
                unit = "-"

            description = dataString[:dataString.find("  ")]

            constants[description] = Constant(value, uncertainty, unit,
                                              description)

            quantity = description.replace(" ", "_").replace(".", "") \
                                  .replace("-", "_").replace("/", "") \
                                  .replace(",", "").replace("(", "")  \
                                  .replace(")", "").replace("{", "")  \
                                  .replace("}", "")
            if quantity[0] in "1234567890":
                quantity = "_" + quantity

    return constants


def make_constants(constants):
    """Makes the given constants dictionary in to accesable variables
       of the class Constant."""
    global constant
    for description in constants:
        constant = constants[description]
        quantity = description.replace(" ", "_").replace(".", "") \
                              .replace("-", "_").replace("/", "") \
                              .replace(",", "").replace("(", "")  \
                              .replace(")", "").replace("{", "")  \
                              .replace("}", "")
        if quantity[0] in "1234567890":
            quantity = "_" + quantity
        try:
            exec("""%s = Constant(constant.value, constant.uncertainty,
                    constant.unit, constant.description)"""
                 % quantity, globals())
        except SyntaxError:
            print("Cannot create Constant for: %s" % description)
    constant = None


if "CODATA.txt" not in os.listdir("."):
    update()
    if "CODATA.txt" not in os.listdir("."):
        print("""\nCODATA.txt was not found in path,
                 and was unable to download.""")
        sys.exit()

constants = load_values()
make_constants(constants)
last_update = time.localtime(os.stat("CODATA.txt").st_mtime)


# =================================
#
#  "Short cut values"
#
# =================================

#   Speed of Light
c = speed_of_light_in_vacuum
speed_of_light = c
c0 = c

#   Planck Constant
h = Planck_constant
planck_constant = h

#   Masses of elementary particles
m_e = electron_mass
m_p = proton_mass
m_n = neutron_mass

#   Elementary charge
e = elementary_charge

#   Magnetic constant
mu_0 = mag_constant
magnetic_constant = mu_0

#   Electric constant
epsilon_0 = electric_constant

#   Rydberg constant
Rydberg = Rydberg_constant

#   Boltzman constant
k = Boltzmann_constant

#   Stefan Boltzman constant
sigma = Stefan_Boltzmann_constant

#   Universal gas constant
R = molar_gas_constant
universal_gas_constant = R
ideal_gas_constant = R
gas_constant = R

#   Universal gravitation constant
G = Newtonian_constant_of_gravitation
gravitation_constant = G
universal_gravitation_constant = G

#   Wien
Wien = Wien_wavelength_displacement_law_constant

#   Electron Volt
eV = electron_volt

#   Avogadro constant
N_A = Avogadro_constant
Avogadro = N_A
Avogadro_number = N_A
L = N_A

#   Planck constant over 2pi
hbar = Planck_constant_over_2_pi

#   SI - prefixes
yotta = 1e24
zetta = 1e21
exa = 1e18
peta = 1e15
tera = 1e12
giga = 1e9
mega = 1e6
kilo = 1e3
hecto = 1e2
deka = 1e1
deci = 1e-1
centi = 1e-2
milli = 1e-3
micro = 1e-6
nano = 1e-9
pico = 1e-12
femto = 1e-15
atto = 1e-18
zepto = 1e-21
