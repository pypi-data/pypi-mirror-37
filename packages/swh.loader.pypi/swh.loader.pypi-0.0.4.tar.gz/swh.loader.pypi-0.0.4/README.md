swh-loader-pypi
====================

SWH PyPI loader's source code repository

# What does the loader do?

The PyPI loader visits and loads a PyPI project [1].

Each visit will result in:
- 1 snapshot (which targets n revisions ; 1 per release artifact)
- 1 revision (which targets 1 directory ; the release artifact uncompressed)

[1] https://pypi.org/help/#packages

## First visit

Given a PyPI project (origin), the loader, for the first visit:

- retrieves information for the given project (including releases)
- then for each associated release
- for each associated source distribution (type 'sdist') release
  artifact (possibly many per release)
- retrieves the associated artifact archive (with checks)
- uncompresses locally the archive
- computes the hashes of the uncompressed directory
- then creates a revision (using PKG-INFO metadata file) targeting
  such directory
- finally, creates a snapshot targeting all seen revisions
  (uncompressed PyPI artifact and metadata).

## Next visit

The loader starts by checking if something changed since the last
visit.  If nothing changed, the visit's snapshot is left
unchanged. The new visit targets the same snapshot.

If something changed, the already seen release artifacts are skipped.
Only the new ones are loaded. In the end, the loader creates a new
snapshot based on the previous one. Thus, the new snapshot targets
both the old and new PyPI release artifacts.

## Terminology

- 1 project: a PyPI project (used as swh origin). This is a collection
             of releases.

- 1 release: a specific version of the (PyPi) project. It's a
             collection of information and associated source release
             artifacts (type 'sdist')

- 1 release artifact: a source release artifact (distributed by a PyPI
                      maintainer). In swh, we are specifically
                      interested by the 'sdist' type (source code).

## Edge cases

- If no release provides release artifacts, those are skipped

- If a release artifact holds no PKG-INFO file (root at the archive),
  the release artifact is skipped.

- If a problem occurs during a fetch action (e.g. release artifact
  download), the load fails and the visit is marked as 'partial'.

# Development

## Configuration file

### Location

Either:
- /etc/softwareheritage/
- ~/.config/swh/
- ~/.swh/

Note: Will call that location $SWH_CONFIG_PATH

### Configuration sample

$SWH_CONFIG_PATH/loader/pypi.yml:
```
storage:
  cls: remote
  args:
    url: http://localhost:5002/

```

## Local run

The built-in command-line will run the loader for a project in the
main PyPI archive.

For instance, to load arrow:
``` sh
python3 -m swh.loader.pypi.loader arrow
```

If you need more control, you can use the loader directly. It expects
three arguments:
- project: a PyPI project name (f.e.: arrow)
- project_url: URL of the PyPI project (human-readable html page)
- project_metadata_url: URL of the PyPI metadata information
  (machine-parsable json document)

``` python
import logging
logging.basicConfig(level=logging.DEBUG)

from swh.loader.pypi.tasks import LoadPyPI

project='arrow'

LoadPyPI().run(project, 'https://pypi.org/pypi/%s/' % project, 'https://pypi.org/pypi/%s/json' % project)
```
