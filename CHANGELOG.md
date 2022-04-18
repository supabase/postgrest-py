# Changelog

<!--next-version-placeholder-->

## v0.10.2 (2022-04-18)
### Fix
* Include source directory name ([#116](https://github.com/supabase-community/postgrest-py/issues/116)) ([`18334f8`](https://github.com/supabase-community/postgrest-py/commit/18334f880d5e4e769a9e843007bc2f46b597a777))

### Documentation
* Remove rtd config file ([`14100a1`](https://github.com/supabase-community/postgrest-py/commit/14100a15a7d9c526df3e504a676d2d1018be3e04))

**[See all commits in this version](https://github.com/supabase-community/postgrest-py/compare/v0.10.1...v0.10.2)**

## v0.10.1 (2022-04-07)
### Fix
* Escape chars only when necessary ([#108](https://github.com/supabase-community/postgrest-py/issues/108)) ([`53f7d18`](https://github.com/supabase-community/postgrest-py/commit/53f7d18807aa292aa7326af573bd55828a3bb6e4))

**[See all commits in this version](https://github.com/supabase-community/postgrest-py/compare/v0.10.0...v0.10.1)**

## v0.10.0 (2022-03-13)
### Feature
* Add .contains and .contained_by operators to match JS client ([#100](https://github.com/supabase-community/postgrest-py/issues/100)) ([`7189e09`](https://github.com/supabase-community/postgrest-py/commit/7189e095bd792fcbc5b89e4f03ef7174e1dd30b7))

**[See all commits in this version](https://github.com/supabase-community/postgrest-py/compare/v0.9.2...v0.10.0)**

## v0.9.2 (2022-03-12)
### Fix
* Make api error properties optionals ([#101](https://github.com/supabase-community/postgrest-py/issues/101)) ([`eb92326`](https://github.com/supabase-community/postgrest-py/commit/eb92326db0088fbf2d96bb68b206160b03e63747))

**[See all commits in this version](https://github.com/supabase-community/postgrest-py/compare/v0.9.1...v0.9.2)**

## v0.9.1 (2022-03-08)
### Fix
* Fix APIError ([#97](https://github.com/supabase-community/postgrest-py/issues/97)) ([`ff29024`](https://github.com/supabase-community/postgrest-py/commit/ff290240cf9364902ffca19e854604d6a40770f9))

**[See all commits in this version](https://github.com/supabase-community/postgrest-py/compare/v0.9.0...v0.9.1)**

## v0.9.0 (2022-02-19)
### Feature
* Export APIError and APIResponse ([`83e7799`](https://github.com/supabase-community/postgrest-py/commit/83e77991101c8e8aec42552344b02ce8db6bd04a))

**[See all commits in this version](https://github.com/supabase-community/postgrest-py/compare/v0.8.2...v0.9.0)**

## v0.8.2 (2022-01-30)
### Fix
* Add-response-model ([`4c0259d`](https://github.com/supabase-community/postgrest-py/commit/4c0259d1658c07bf3e78fe03d98b304f7a6f0c7a))

**[See all commits in this version](https://github.com/supabase-community/postgrest-py/compare/v0.8.1...v0.8.2)**

## v0.8.1 (2022-01-22)
### Fix
* Order filter ([`094dbad`](https://github.com/supabase-community/postgrest-py/commit/094dbadb26bef4238536579ede71d46a4ef67899))

**[See all commits in this version](https://github.com/supabase-community/postgrest-py/compare/v0.8.0...v0.8.1)**

## v0.8.0 (2022-01-16)
### Feature
* Add timeout as a parameter of clients ([#75](https://github.com/supabase-community/postgrest-py/issues/75)) ([`1ea965a`](https://github.com/supabase-community/postgrest-py/commit/1ea965a6cb32dacb5f41cd1198f8a970a24731b6))

**[See all commits in this version](https://github.com/supabase-community/postgrest-py/compare/v0.7.1...v0.8.0)**

## v0.7.1 (2022-01-04)
### Performance
* Sync configurations with gotrue-py ([#66](https://github.com/supabase-community/postgrest-py/issues/66)) ([`d5a97da`](https://github.com/supabase-community/postgrest-py/commit/d5a97daad42a431b2d36f16e3969b38b9dded288))

**[See all commits in this version](https://github.com/supabase-community/postgrest-py/compare/v0.7.0...v0.7.1)**

## v0.5.0

### Features

* Allow setting headers in `PostgrestClient`'s constructor
* Improve `PostgrestClient.auth()` behavior

### Internal

* Require Poetry >= 1.0.0
* Update CI workflow
* Use Dependabot
* Update httpx to v0.19.0

## v0.4.0

### Added

* Add some tests
* Allow multivalued query parameters

### Changed

* Internal changes & improvements

## v0.3.2

### Added

* Use Github Actions

### Changed

* Move to a new home: [supabase/postgrest-py](https://github.com/supabase/postgrest-py)

### Removed

* Remove Travis CI

## v0.3.1

### Removed

* Remove dummy test cases
* Remove PyPy3 from Travis CI

## v0.3.0

### Added

* Add some basic test cases for `PostgrestClient`
* Use Travis CI

### Changed

* Change behavior of `RequestBuilder.filter()`
* Change signature of general filters

### Removed

* Remove `RequestBuilder.filter_in()` and `RequestBuilder.filter_out()`

### Fixed

* Fix `PostgrestClient.schema()` not actually work

## v0.2.0

### Added

* Support basic authentication
* Support stored procedures (RPC)
* `RequestBuilder.select()` now accepts `columns` as variable-length arguments
* Add `RequestBuilder.not_` getter
* Add `RequestBuilder.ov()`

### Changed

* Rename `Client` to `PostgrestClient` and deprecate the old name
* Deprecate `PostgrestClient.from_table()`

### Removed

* Remove `RequestBuilder.not_()`
* Remove `RequestBuilder.ova()` and `RequestBuilder.ovr()`

## v0.1.1

### Fixed

* Fix a typo in `Client.from_()`

## v0.1.0

### Added

* Add basic features
