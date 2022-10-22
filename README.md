## SETUP

***

1. Create a virtual environment for development

* Create a virtual environment to isolate our package dependencies locally

```bash
 pip install -r dev-requirements.txt 
 python3 -m venv venv
 source venv/bin/activate  # On Windows use `env\Scripts\activate`
```  

* Install all dependencies

```bash
  pip install -r requirements.txt
```

***  

3. Configure python virtual environment with IDE

* Pycharm

  see from the
  following [link](https://www.jetbrains.com/help/pycharm/creating-virtual-environment.html#python_create_virtual_env)


* VSCode  
  create `settings.json` file under directory `.vscode` if directory does not exist create one

```bash
{
    "python.defaultInterpreterPath": "venv/bin/python",  
    "python.linting.enabled": true, 
    "editor. formatOnSave": true
}

```

***

4. Run the application

```bash
    # pull related docker images
    docker-compsoe pull
    
    # build the docker continer
    docker-compose build
    
    # run the docker containers
    docker-compose up
```

6. view application REST documentation

* credentials are

```bash
    # test admin user
     username=test@test.com
     password=test
    
    # test user
    username=admin@admin.com
    password=admin
```

* visit [link](http://localhost:8000/) for django restframework drdf documentation
* visit [link](http://localhost:8000/docs) for swager documentation

***

7. Run manual Tests

##### Jams

* list/view jams `http://localhost:8000/jams/`

```json
{
  "method": "GET"
}
```

* retrieve/view jam `http://localhost:8000/jams/{jam id}`

 ```json
{
  "method": "GET"
}
```

* create jam `http://localhost:8000/jams/`

```json
{
  "method": "POST",
  "paylaod": {
    "description": "string",
    "roles": [
      {
        "description": "string",
        "instrument": "string"
      }
    ]
  }
}
``` 
* join jam `http://localhost:8000/jams/{jam id}/join_jam/`
```json
{
  "method": "GET"
}
```  

##### Profiles

* list/view profiles as an admin `http://localhost:8000/profiles/`

```json
{
  "method": "GET"
}
```

* retrieve/view profiles as an admin or user `http://localhost:8000/profiles/{user/profile id}`

 ```json
{
  "method": "GET"
}
```

* create profile `http://localhost:8000/profiles/`

```json
{
  "method": "POST",
  "paylaod": {
    "role": {
      "description": "string",
      "instrument": "string"
    }
  }
}
``` 
##### performers 

* list/view performers as an admin `http://localhost:8000/performers/`

```json
{
  "method": "GET"
}
```

* retrieve/view performers as an admin or performer `http://localhost:8000/performers/{user/profile id}`

 ```json
{
  "method": "GET"
}
```

* create performer `http://localhost:8000/performers/`

```json
{
  "method": "POST",
  "paylaod": {
      "email": "user@example.com",
      "password": "string",
      "is_superuser": true,
      "is_staff": true,
      "is_active": true
  }
}
``` 
***  

8. Run Unit Tests

```bash
 # to run tests with in python virtual environment
 source venv/bin/activate  # On Windows use `env\Scripts\activate`
 python3 manage.py test --settings=music_jam.settings.test
 
 # to run tests using docker-compose
 docker-compose run backend  ./manage.py test --settings=music_jam.settings.test
```