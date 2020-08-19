## CHANGELOG

### v0.3.0

#### Added

- Add some basic test cases for `PostgrestClient`
- Use Travis CI

#### Changed

- Change behavior of `RequestBuilder.filter()`
- Change signature of general filters

#### Removed

- Remove `RequestBuilder.filter_in()` and `RequestBuilder.filter_out()`

#### Fixed

- Fix `PostgrestClient.schema()` not actually work

### v0.2.0

#### Added

- Support basic authentication
- Support stored procedures (RPC)
- `RequestBuilder.select()` now accepts `columns` as variable-length arguments
- Add `RequestBuilder.not_` getter
- Add `RequestBuilder.ov()`

#### Changed

- Rename `Client` to `PostgrestClient` and deprecate the old name
- Deprecate `PostgrestClient.from_table()`

#### Removed

- Remove `RequestBuilder.not_()`
- Remove `RequestBuilder.ova()` and `RequestBuilder.ovr()`

### v0.1.1

#### Fixed

- Fix a typo in `Client.from_()`

### v0.1.0

#### Added

- Add basic features
