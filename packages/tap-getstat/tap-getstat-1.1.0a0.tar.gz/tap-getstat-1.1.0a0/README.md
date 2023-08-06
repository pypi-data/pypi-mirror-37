# tap-getstat

This is a [Singer](https://singer.io) tap that produces JSON-formatted data following the [Singer spec](https://github.com/singer-io/getting-started/blob/master/SPEC.md).

This tap:
- Pulls raw data from getstat's [REST API](https://help.getstat.com/knowledgebase/requests-and-responses/)
- Extracts the following resources from getstat.com:
  - [Projects](https://help.getstat.com/knowledgebase/requests-and-responses/#projects-list)
  - [Sites](https://help.getstat.com/knowledgebase/requests-and-responses/#sites-list)
  - [Tags](https://help.getstat.com/knowledgebase/requests-and-responses/#tags-list)
  - [Keywords](https://help.getstat.com/knowledgebase/requests-and-responses/#keywords-list)
  - [Rankings](https://help.getstat.com/knowledgebase/requests-and-responses/#rankings-list)
- Rankings uses the bulk data api
- Outputs the schema for each resource
- Incrementally pulls data based on the input state


## Quick start

1. Install

    ```bash
    > git clone http://github.com/realself/tap-getstat
    > cd tap-getstat
    > python setup.py install
    ```

2. Get your getstat.com access token

    - Login to your getstat.com account
    - Navigate to your profile page
    - Create an access token

3. Create the config file

    Create a JSON file called `config.json` containing:
    - Access token you just created
    - API URL for your getstat account. 
    - your getstat subdomain
    - Projects to track (space separated)

    ```json
    {"subdomain": "your-subdomain",
     "api_key": "your-access-token",
     "project_id": "your project id",
     "site_id": "your site id",
     "start_date": "first date for keyword extractions",
     "end_date": "last date for keyword extractions"
     }
    ```

4. [Optional] Create the initial state file

    tap-getstat accepts an initial state file in JSON format to restrict
    dates on which data is fetched for the API endpoints. Without this 
    file all of your getstat.com data will be fetched.

    ```json
    {"projects": "2017-01-17T00:00:00Z",
    "sites": "2017-01-17T00:00:00Z",
    "tags": "2017-01-17T00:00:00Z",
    "keywords": "2017-01-17T00:00:00Z",
    "rankings": "2017-01-17T00:00:00Z"
    ```

5. Run the application

    `tap-getstat` can be run with:

    ```bash
    tap-getstat --config config.json [--state state.json]
    ```

---

Copyright &copy; 2018 Realself
