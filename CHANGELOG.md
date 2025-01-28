# Changelog

## [v0.1.0] - 2025-01-28

### Added

- **Role Validation Business Logic**:  
  - The Filer now incorporates role validation, ensuring that users have the correct roles for specific operations.  
  - Validation logic previously handled by the Verifier has been migrated to the Filer.

- **Integration with `vlei-verifier-client`**:  
  - Replaced direct requests to the vLEI Verifier with the official [vlei-verifier-client](https://pypi.org/project/vlei-verifier-client/), improving maintainability and abstraction.


## [v0.0.2] - 2025-01-06

### Added

#### Configurable Parameters
The **Filer** now supports the following configuration options:
- **`admin_role_name`**:  
  The name of the Data Admin role. This parameter is used to check the Engagement Context Role (ECR) credential, ensuring it corresponds to the Data Admin credential.
- **`admin_lei`**:  
  The Legal Entity Identifier (LEI) of the Data Admin credential. This parameter is used to verify that the ECR credential has the expected LEI linked to the Data Admin.

#### New Endpoints
- **`/reports/status/{aid}/{lei}`**:  
  Allows Data Admins to retrieve upload statuses for all submitted reports.  
  - **Parameters**:
    - `aid`: The Admin Identifier (AID) of the Data Admin.  
    - `lei` (optional): The LEI of the organization for which the upload statuses are requested. If no LEI is provided, statuses for all uploads will be returned.

---

### Summary

This release focuses on adding support for **Data Admin roles**. Users with a credential that grants Data Admin role permissions can now access upload statuses for all submitted reports.



## [v0.0.1] - 2024-12-26

### Added

- **Environment Variables**:
    - `KERI_BASER_MAP_SIZE`: Defines the maximum size of the LMDB database. Defaults to `104857600` (100 MB).
    - `FILER_CHUNK_SIZE`: Defines the size of the chunks used for file processing. This allows fine-tuning of memory
      usage when handling large files.
    - `VLEI_VERIFIER`: Base URL of the Vlei Verifier.

- **Automatic LMDB Cleanup**:
    - Processed reports are now automatically removed from the LMDB database after verification, preventing database
      size issues.

### Example Command

To run the Reg-Pilot-Filer service, specify the configuration file as follows:

```bash
reg-pilot-filer server start --config-dir scripts --config-file reg-pilot-filer-config.json
```


