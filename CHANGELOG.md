# CHANGELOG

### _Unreleased_

#### Features

- Allow setting headers in `PostgrestClient`'s constructor
- Improve `PostgrestClient.auth()` behavior

#### Internal

- Require Poetry >= 1.0.0
- Update CI workflow
- Use Dependabot
- Update httpx to v0.19.0

### v0.4.0

#### Added

- Add some tests
- Allow multivalued query parameters

#### Changed

- Internal changes & improvements

### v0.3.2

#### Added

- Use Github Actions

#### Changed

- Move to a new home: [supabase/postgrest-py](https://github.com/supabase/postgrest-py)

#### Removed

- Remove Travis CI

### v0.3.1

#### Removed

- Remove dummy test cases
- Remove PyPy3 from Travis CI

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
