<img src="./systemtest/static/images/logos/rebus_h_black.png" alt="IBM rebus Logo" title="IBM" align="right" height="55">


# PowerTest WebApps

![python] ![flask] ![pandas]

![postgres] ![mongo]

![aws] ![heroku]

<!-- <details>
<summary>Index</summary> -->

## Content table

- [Requirements](#![requirements]-Requirements)
- [Installation](#![installation]-Installation)
- [Usage](#![usage]-Basic-Usage)
  - [Linear](#Linear)
    - [Schema](#schema)
    - [E.G.](#E.G.)
  - [Pie](#Pie)
    - [Schema](#schema)
    - [E.G.](#E.G.)
  - [Bar](#Bar)
    - [Schema](#schema)
    - [E.G.](#E.G.)
- [Documentation](#![documentation]-Documentation)
  - [API](#API)
    - [Document endpoints](#Document-endpoints)
  - [Charts](#Charts)
- [Technologies](#![technologies]-Technologies)
- [Links](#![links]-Links-&-References)
- [License](#![license]-License)
- [Author](#![author]-Author)

<!-- </details> -->

This API process and format data usage from [P-Maker] to generate useful graphics for the administration of the platform.
Charts based on [highcharts]

<br/>

## ![requirements] Requirements

>Python >= 3.8 <br/>
>Pip >= 20.2.3 <br/>
>MongoDB >= 4.0 <br/>
>PostgreSQL >=12.4

## ![installation] Installation

Install dependencies

```bash
pip install -r requirements.txt
```

<details>
<summary>Dependencies</summary>

> APScheduler==3.6.3 <br/>
> flasgger==0.9.5 <br/>
> Flask==1.1.2 <br/>
> Flask-Cors==3.0.9 <br/>
> Flask-RESTful==0.3.8 <br/>
> gunicorn==20.0.4 <br/>
> numpy==1.19.2 <br/>
> pandas==1.1.3 <br/>
> psycopg2==2.8.6 <br/>
> psycopg2-binary==2.8.6 <br/>
> requests==2.24.0 <br/>
> SQLAlchemy==1.3.19 <br/>

</details> <br/>

Set env variables

```bash
PG_HOST # Host of PstgreSQL [ e.g. localhost ]
PG_PORT # Port of host [ e.g. 5432 ]
PG_DATABASE # Database name [ e.g. postgres ]
PG_USER # User with read permissions [ e.g. postgres ]
PG_PASSWORD # Password of user

FLASK_APP = api.py # Change entrypoint of flask to api.py instead app.py
```

    ❗ Depending on the console changes the way of exporting the variables
<br/>
Run

```bash
flask run
```

## ![usage] Basic Usage

The API is made up of two basic components. The type of graph and the information to graph it is based on the data collected from the DB

### **Linear**

A *line chart* is a graphical representation of an asset's **historical action** that connects a series of data points with a continuous line.

Two main objects *'Series'* [ Array of data ] and *'Categories'* [ Array of main categories ]

<details>
<summary>Responses</summary>

**Schema**

```YAML
{
  categories: [ string ] # Array with range of datesstring
  series: [ # Objects array with the name of its category and an array with its data
    {
    data: [ number ] # Number Length of array is the same in all categories andAnd this is dynamic depending on the range of time available in the selected range
    name: string
    }
  ]
}
```

**E.G.**

```JSON
{
  "categories": [
    "2020-03",
    "2020-06",
    "2020-09",
    "2020-12"
  ],
  "series": [
    {
      "data": [
        13,
        20,
        20,
        17
      ],
      "name": "Total"
    },
    {
      "data": [
        4,
        4,
        7,
        0
      ],
      "name": "Backend"
    },
    {
      "data": [
        9,
        16,
        13,
        17
      ],
      "name": "Frontend"
    }
  ]
}
```

</details>

> *[Highcharts line example][linear]*

### **Pie**

A *Pie Chart* a special chart that uses "pie slices" to show **relative sizes of data**.
It is a really good way to show relative sizes: it is easy to see which movie types are **most liked**, and which are **least liked**, at a glance.

<details>
<summary>Responses</summary>

**Schema**

```YAML
{
  data: [
    {
      name: string
      y: number
    }
  ]
}
```

**E.G.**

```JSON
{
  "data": [
    {
      "name": "Mexico",
      "y": 45.5
    },
    {
      "name": "Colombia",
      "y": 54.5
    }
  ]
}
```

</details>

> *[Highcharts pie example][pie]*

### **Bar**

A *bar chart* is a way of summarizing a set of categorical data (continuous data can be made categorical by auto-binning). The bar chart displays data using a number of bars, each representing a particular category.

<details>
<summary>Responses</summary>

**Schema**

```YAML
{
  categories: [ string ] # Array with first group [ category ]
  series: [ # Objects array with the name of its category and an array with its data
    {
      data: [ number ] # Length of array is the same of the array of main categories
      name: string
    }
  ]
}
```

**E.G.**

```JSON
{
  "categories": [
    "spanish",
    "english"
  ],
  "series": [
    {
      "data": [
        13,
        20
      ],
      "name": "Male"
    },
    {
      "data": [
        4,
        4
      ],
      "name": "Female"
    }
  ]
}
```

</details>


> *[Highcharts bar example][bar]*

## ![documentation] Documentation

### API

The documentation is based on the specification of **OpenAPI 3.0** *[ [Swagger] ]* which in fact is the standard for what API documentation refers to.

The documentation is generated by the *[flasgger]* module. The **OAS** *[ OpenAPI Specification ]* is used through YAML formats which in turn are referenced in the code with the *[python docstrings][docstring]*

<details>
<summary>Document endpoints</summary>

**YAML [ docs/pie.yml ]**

```YAML
Returns the data in the format necessary for pie chart
Support any categorical data from Database
---
parameters:
  - in: path
    name: group
    type: string
    enum: [gender, country, profession, city, social_networks, users_tags, language, social_networks] 
    required: true
responses:
  200:
    description: Array of objects with data and name
    schema: 
      type: array
      items:
        type: object
        properties:
          name:
            type: string
          y:
            type: number    
      example:
        data:
          - name: Mexico
            y: 45.5
          - name: Colombia
            y: 54.5
```

**Python / Docstring**

```python
class Pie(Resource):
    def get(self, group: str) -> dict:
        '''file: docs/pie.yml'''
        . . .
```

</details>

> [API Docs][api doc]
>> [OAS 3.0][swagger] <br/>
>> [flasgger][flasgger] <br/>
>> [Python PEP257][docstring]

### Charts

Because the API was designed for a specific fronted library for greater efficiency and not to overload the frontend, it is necessary to check how each specific graph receives the information.

> [Highcharts Demos][highcharts]
>> [Basic line][linear] <br/>
>> [Pie with legend][pie] <br/>
>> [Basic bar][bar]

## ![technologies] Main Technologies

<a style="float:left;">![python logo]</a>
<a style="float:left;">![flask logo]</a>
<a style="float: left">![swagger logo]</a>
<a style="">![postgres logo]</a>

## ![links] Links & References

- [P-Maker web][p-maker]
- [Highcharts demos][highcharts]
- [API DOCS][api doc]
- [OpenAPI Specification][swagger]
- [Flask Home][flask home]
- [PostgeSQL Home][postgresql home]

## ![license] License

![mit license]

P-Maker *Dashboard API* is [MIT licenced][MIT]

## ![author] Author

### @AlanVazquez

<a href="https://github.com/AlanVazquez99" style="float: left;"> ![github] </a>
<a href="https://www.linkedin.com/in/alan-isaac-vazquez/" style="padding: 100px"> ![LinkedIn] </a>

<!-- All links for document -->
<!-- Basic Links -->
<!-- Reference links -->
[postgresql home]: https://www.postgresql.org/ "PostgreSQL Home"
<!-- Aditional reference links -->
<!-- IMGs Links -->
<!-- badges -->
[python]: https://img.shields.io/badge/python%20-%2314354C.svg?&style=for-the-badge&logo=python&logoColor=white
[postgres]: https://img.shields.io/badge/postgres-%23316192.svg?&style=for-the-badge&logo=postgresql&logoColor=white
<!-- Icons Links -->
<!-- Other Links -->
[MIT]: https://tldrlegal.com/license/mit-license "MIT License"
[docstring]: https://www.python.org/dev/peps/pep-0257/ "Python Docstrings PEP257"
