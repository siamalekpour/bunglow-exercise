# bunglow-exercise

This is my submission for the Bungalow hiring challenge

> Sorry about the typo in the repo name. Rushing through the challenge as fast as I can

## How to run the project

Clone the repo to your local directory and install the requirements in your virtualenv:

```
$ git clone  https://github.com/siamalekpour/bunglow-exercise.git
$ cd bunglow-exercise
$ workon bunglow -- assuming you've already created this environement
$ pip install -r requirements.txt
```

> As of now, I don't have docker installed on my systems. That's why I've defaulted to using `virutalenvwrapper` for this challenge

This should setup a project with all necessary requirements. Next step is to migrate data from the csv file.

```
$ python manage.py migrate
$ python manage.py migrate_data_from_csv
```
The last line will take a few minutes. At the end you should see a success message:

```
Processed 449 homes.
``` 

#### Management Command vs Data Migration
Since this is a one off migration a Django Data Migration could've also been used. The management command however, is reusable in the future;

## Things for the future
- Move project to a docker container
- Add tests
- Move off of Sqlite