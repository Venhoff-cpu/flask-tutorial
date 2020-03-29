from setuptools import find_packages, setup

setup(
    name='flaskr',
    version='1.0.0',
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        'flask',
    ],
)
# WAŻNE! Większość projektów zaczynamy od ustawieniu steupu, żeby wskazac jakie pakiety sa wymagne do uzycia aplikacji.
# Pyhton bedzie potrzebował informacji które pakiety powinnien uwzlednić. Do tego słuzy plik MANIFEST.in.
# W nim wskazaliśmy, by skopiować foldery: static (style.css), templates; Uwzgledniliśmy konstrukcję bazy schema.sql;
# Kazaliśmy pomijać wszelkie pliki z bytecodem -> global -exclude *.pyc