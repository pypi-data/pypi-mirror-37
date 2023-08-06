# CHANGELOG

## v0.6.1 (2018/10/23)

- require py-meta-utils 0.7.0
- fix SessionManager tests

## v0.6.0 (2018/10/23)

- documentation improvements
- rename `DB_URI` to `DATABASE_URI`
- rename the `db_uri` argument of `init_sqlalchemy_unchained` to `database_uri`
- remove the `ModelMetaOptionsFactory._model_repr` property
- remove the `validates` decorator
- discourage the use of Active Record anti-patterns (remove `query` attribute from `BaseModel`)
- add `SessionManager` and `ModelManager` to encourage use of Data Mapper patterns
- add `query_cls` keyword argument to `init_sqlalchemy_unchained` and `scoped_session_factory`
- bugfix for `declarative_base` if a custom base model is passed in without a constructor
- configure the `MetaData` naming convention if none is provided

## v0.5.1 (2018/10/20)

- bugfix: cannot automatically determine if relationship/association_proxy attributes should be required

## v0.5.0 (2018/10/16)

- configure tox & travis
- make compatible with Python 3.5
- fix `ReprMetaOption` to pull default primary key name from `_ModelRegistry()`
- `ColumnMetaOption` values should only be `str` or `None`
- bump required `py-meta-utils` to v0.6.1
- `ColumnMetaOption.check_value` should raise `TypeError` or `ValueError`, not `AssertionError`
- Move declaration of factory meta options from `ModelMetaOptionsFactory._get_meta_options()` to `ModelMetaOptionsFactory._options`
- bugfix: use correct foreign key for the primary key on joined polymorphic models
- publish documentation on read the docs

## v0.4.0 (2018/10/09)

- fix automatic required validators
- rename `ModelRegistry` to `_ModelRegistry`

## v0.3.1 (2018/10/04)

- set default primary key as a class attribute on the `ModelRegistry`

## v0.3.0 (2018/09/30)

- update to py-meta-utils 0.3

## v0.2.2 (2018/09/29)

- update to py-meta-utils 0.2

## v0.2.1 (2018/09/26)

- fix automatic Required validation (should not raise if the column has a default value)

## v0.2.0 (2018/09/26)

- implement validation for models
- wrap `sqlalchemy.orm.relationship` with the configured `Query` class
- override the `alembic` command to customize the generated migrations templates
- export `ColumnMetaOption` from the top-level `sqlalchemy_unchained` package
- export `association_proxy`, `declared_attr`, `hybrid_method`, and `hybrid_property` from the top-level `sqlalchemy_unchained` package
- add documentation
- add tests

## v0.1.0 (2018/09/24)

- initial release
