# reg-pilot-filer
The file processor for reg-pilot.

This requires a running Vlei-Verifier service.

The service can be launched from the command-line with:

```
reg-pilot-filer server start --config-dir scripts --config-file reg-pilot-filer-config.json
```

Or from docker-compose with:

```
docker-compose build --no-cache
docker-compose down
docker-compose up deps
```


## Filer Endpoints:

### POST /reports/{aid}/{digest}
    This endpoint is responsible for report uploads. Report itself(upload) must be passed as a multipart/form-data request body.
### GET /reports/{aid}/{digest}
    Using the AID and Report file Digest from the request responds with the actual report upload status.

