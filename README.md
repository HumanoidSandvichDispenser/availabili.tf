# availabili.tf

Scheduling for TF2

## Setup (dev)

### Frontend

```sh
# first time setup
npm install

npm run dev
```

### Backend

In virtual environment:

```sh
# first time setup
pip install -r requirements.txt
flask db migrate

flask run --debug
```

### OpenAPI

The backend will automatically serve its OpenAPI-compliant spec at
`/apidoc/openapi.json` which can also be viewed at `/apidoc/redoc` or
`/apidoc/swagger` or `/apidoc/scalar`.

To generate the frontend client:

```sh
npx openapi --input 'http://localhost:5000/apidoc/openapi.json' --output src/client
```
