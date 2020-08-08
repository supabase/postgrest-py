## CHANGELOG

### Unreleased

#### Added

- Support basic authentication
- Support stored procedures (RPC)
- `RequestBuilder.select()` now accepts `columns` as variable-length arguments
- Add `RequestBuilder.not_` getter
- Add `RequestBuilder.ov()`

#### Changed

- Rename `Client` to `PostgrestClient` and deprecate the old name

#### Removed

- Remove `RequestBuilder.not_()`
- Remove `RequestBuilder.ova()` and `RequestBuilder.ovr()`

### v0.1.1

#### Fixed

- Fix a typo in `Client.from_()`

### v0.1.0

#### Added

- Add basic features
