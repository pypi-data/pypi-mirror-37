import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="Complex Operations",
    version="1.0.2",
    author="Swag Exp",
    author_email="swagexp@gmail.com",
    description="Python Package for the addition, subtraction, multiplication and division of two complex objects with a real number or an integer",
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)

def conjugate(self):
    return Complex(self._re, -self._im)


def __add__(self, other):
    if type(other) == int or type(other) == float:
        return Complex(self._re + other, self._im)

    re = self._re + other._re
    im = self._im + other._im
    return Complex(re, im)


def __radd__(self, other):
    return Complex(self._re + other, self._im)


def __sub__(self, other):
    if type(other) == int or type(other) == float:
        return Complex(self._re - other, self._im)

    re = self._re - other._re
    im = self._im - other._im
    return Complex(re, im)


def __rsub__(self, other):
    return Complex(-self._re + other, -1 * self._im)


def __mul__(self, other):
    if type(other) == int or type(other) == float:
        return Complex(self._re * other, self._im * other)

    re = self._re * other._re - self._im * other._im
    im = self._re * other._im + self._im * other._re
    return Complex(re, im)


def __rmul__(self, other):
    return Complex(self._re * other, self._im * other)


def __truediv__(self, other):
    if type(other) == int or type(other) == float:
        return Complex(self._re / other, self._im / other)

    conjugate = other.conjugate()
    numerator = self * conjugate
    multiple = conjugate * other
    multiple = multiple.re()

    numerator._re /= multiple
    numerator._im /= multiple

    return numerator


def __rtruediv__(self, other):
    conjugate = self.conjugate()

    multiple = conjugate * self
    conjugate._re *= other
    conjugate._im *= other

    conjugate._re /= multiple._re
    conjugate._im /= multiple._re
    return conjugate
