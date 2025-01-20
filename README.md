# reg-pilot-filer
The file processor for reg-pilot.

This requires a running Vlei-Verifier service.

# Compatibility Matrix


| Service  | Version | Compatible Verifier Versions | Compatible API Versions | Compatible Filer Versions |
|----------|---------|------------------------------|--------------------------|---------------------------|
| Verifier | 0.0.3   | -                            | 0.0.2                   | 0.0.1, 0.0.2              |
| Verifier | 0.0.4   | -                            | 0.0.2                   | 0.0.1, 0.0.2              |
| API      | 0.0.2   | 0.0.3, 0.0.4                | -                        | 0.0.1, 0.0.2              |
| Filer    | 0.0.1   | 0.0.3, 0.0.4                | 0.0.2                   | -                         |
| Filer    | 0.0.2   | 0.0.3, 0.0.4                | 0.0.2                   | -                         |


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

