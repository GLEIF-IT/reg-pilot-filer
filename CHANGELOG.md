# Changelog

## [v0.0.1] - 2024-12-26

### Added

- **Environment Variables**:
  - `VLEI_VERIFIER`: Base URL of the Vlei Verifier.

- **Automatic LMDB Cleanup**: 
  - Processed reports are now automatically removed from the LMDB database after verification, preventing database size issues.

### Example Command
To run the Reg-Pilot-Filer service, specify the configuration file as follows:
```bash
reg-pilot-filer server start --config-dir scripts --config-file reg-pilot-filer-config.json
```

### Summary

This is the first release of the Reg-Pilot-Filer. The main objective of the release is to separate report uploads functionality from the Vlei-Verifier.
