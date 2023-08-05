# Boilerplate Manager

## Table of Contents

- [Boilerplate Manager](#boilerplate-manager)
    - [Table of Contents](#table-of-contents)
    - [About](#about)
        - [Overview](#overview)
            - [Supported Django and Python versions](#supported-django-and-python-versions)
    - [Documentation](#documentation)
        - [Installation](#installation)
        - [Usage](#usage)
    - [Built With](#built-with)
    - [Change Log](#change-log)
        - [v1.0.0](#v1.0.0)
    - [Contributing](#contributing)
    - [Authors](#authors)
    - [License](#license)


## About

Boilerplate Manager is a Django app to generate forms, templates, API, views for apps of your project. For each app in your project, you create the models and after you can generate all the forms, templates, APIs and views of this app, you will only need to take care of the business rule.

Detailed documentation is in the “docs” directory.

### Overview

`boilerplate-manager` is a well tested, documented, and base management app to generate forms, templates, API, views for apps of your project.

#### Supported Django and Python versions

Django \ Python | 3.5 | 3.6
--------------- | --- | ---
2.1  |  *  |  *


## Documentation

### Installation

To install boilerplate-manager:

```shell
    $ pip install boilerplate-manager
```

Add `core` to your `INSTALLED_APPS` setting:

```python
    INSTALLED_APPS = [
        # other apps
        "core",
    ]
```

Add `core.urls` to your project urlpatterns:

```python
    urlpatterns = [
        # other urls
        path('core/', include('core.urls'), name='core'),
    ]
```
Run 
```shell 
    $ python manage.py migrate
```
to create the core models.

Run 
```shell 
    $ python manage.py runserver
```
to run the server

Visit http://127.0.0.1:8000/core/ to list the apps installed in your project.  

### Usage

For generate the files of your model, create one app and write your models. The models should extends `Base`.

Example:

 ```python
 #others imports
 from core.models import Base

#Create your models here.
class NameModel(Base):
    ...
 ```
After this, run the command for generate the files of the app.

 ```shell
    $ python manage.py build <your_app_name> 
 ```
This command will generate all the forms, views, Api Rest and templates for your app based in your models.

To generate the files only one specific model, run this command:


 ```shell
    $ python manage.py build <your_app_name> <your_model_name>
 ```

 This command will generate all the forms, views, Api Rest and templates for your model.

## Built With

* [Django](https://www.djangoproject.com/) - The high-level Python Web framework that encourages rapid development and clean, pragmatic design.
* [Bootstrap 4](https://getbootstrap.com/) - The open source toolkit for developing with HTML, CSS, and JS. 
  
## Change Log

### v1.0.0
- 🎉 first release!


## Contributing

Please read [CONTRIBUTING](CONTRIBUTING.md) for details on our code of conduct, and the process for submitting pull requests to us.

## Authors

* [Lucas Siqueira da Silva](https://github.com/lucas-siqueira)
* [Claysllan Ferreira Xavier](https://github.com/claysllanxavier)
* [Guilherme de Carvalho Carneiro](https://github.com/guilhermecarvalhocarneiro)
* [Salomao Pinheiro Coelho Junior](https://github.com/spcoelhojr)
* [Alecxandra Mesquita](https://github.com/AlecxandraMesquita)
* [André Praça De Almeida Pinheiro](https://github.com/apracapinheiro)
* [Clazzeani Dias Almeida](https://github.com/clazzeani)
* [George Silva Macedo](https://github.com/)
* [Robson Aparecido Ronzani](https://github.com/ronzani)
* [Thales Ribeiro Evangelista](https://github.com/thales-t)
* [Thiago Carvalho Peçanha](https://github.com/carvalhopecanha)
* [Thyago Mendes Neves](https://github.com/thyagomn)
* [Wilber Lacerda De Jesus](https://github.com/wilberlacerda)


See also the list of [contributors](https://github.com/agencia-tecnologia-palmas/boilerplate-manager/contributors) who participated in this project.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details
