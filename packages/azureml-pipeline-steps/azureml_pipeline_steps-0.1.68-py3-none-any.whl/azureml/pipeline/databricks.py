# ---------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# ---------------------------------------------------------
"""databricks.py.

Module for creating AutoScale,  MavenLibrary, PyPiLibrary, RCranLibrary, JarLibrary or EggLibrary input
for a Databricks step.
"""


class AutoScale:
    """
    Creates an AutoScale input for a Databricks step.

    :param min_workers: The min number of workers for the databricks run cluster.
    :type min_workers: int
    :param max_workers: The max number of workers for the databricks run cluster.
    :type max_workers: int
    """

    def __init__(self, min_workers=None, max_workers=None):
        """
        Initialize AutoScale.

        :param min_workers: The min number of workers for the databricks run cluster.
        :type min_workers: int
        :param max_workers: The max number of workers for the databricks run cluster.
        :type max_workers: int
        """
        if min_workers is None:
            raise ValueError("min_workers is required")
        if not isinstance(min_workers, int):
            raise ValueError("min_workers must be an int")
        if max_workers is None:
            raise ValueError("max_workers is required")
        if not isinstance(max_workers, int):
            raise ValueError("max_workers must be an int")

        self.min_workers = min_workers
        self.max_workers = max_workers


class MavenLibrary:
    """
    Creates an MavenLibrary input for a Databricks step.

    :param coordinates: Gradle-style maven coordinates. For example: “org.jsoup:jsoup:1.7.2”.
    :type coordinates: str
    :param repo: Maven repo to install the Maven package from. If omitted,
    　　　　both Maven Central Repository and Spark Packages are searched.
    :type repo: str
    :param exclusions: List of dependences to exclude. For example: ["slf4j:slf4j", "*:hadoop-client"].
           Maven dependency exclusions
    　　　　https://maven.apache.org/guides/introduction/introduction-to-optional-and-excludes-dependencies.html.
    :type exclusions: list
    """

    def __init__(self, coordinates=None, repo=None, exclusions=None):
        """
        Initialize MavenLibrary.

        :param coordinates: Gradle-style maven coordinates. For example: “org.jsoup:jsoup:1.7.2”.
        :type coordinates: str
        :param repo: Maven repo to install the Maven package from. If omitted,
        　　　　both Maven Central Repository and Spark Packages are searched.
        :type repo: str
        :param exclusions: List of dependences to exclude. For example: ["slf4j:slf4j", "*:hadoop-client"].
               Maven dependency exclusions
        　　　　https://maven.apache.org/guides/introduction/introduction-to-optional-and-excludes-dependencies.html.
        :type exclusions: list
        """
        if coordinates is None:
            raise ValueError("coordinates is required")
        if not isinstance(coordinates, str):
            raise ValueError("coordinates must be a string")
        if repo is None:
            repo = ""
        if not isinstance(repo, str):
            raise ValueError("repo must be a string")
        if exclusions is None:
            exclusions = []

        self.coordinates = coordinates
        self.repo = repo
        self.exclusions = exclusions


class PyPiLibrary:
    """
    Creates an PyPiLibrary input for a Databricks step.

    :param package: The name of the pypi package to install. An optional exact version specification is also supported.
    :type package: str
    :param repo: The repository where the package can be found. If not specified, the default pip index is used.
    :type repo: str
    """

    def __init__(self, package=None, repo=None):
        """
        Initialize PyPiLibrary.

        :param package: The name of the pypi package to install.
        　　　　An optional exact version specification is also supported.
        :type package: str
        :param repo: The repository where the package can be found. If not specified, the default pip index is used.
        :type repo: str
        """
        if package is None:
            raise ValueError("package is required")
        if not isinstance(package, str):
            raise ValueError("coordinates must be a string")
        if repo is None:
            repo = ""
        if not isinstance(repo, str):
            raise ValueError("repo must be a string")

        self.package = package
        self.repo = repo


class RCranLibrary:
    """
    Creates an RCranLibrary input for a Databricks step.

    :param package: The name of the CRAN package to install.
    :type package: str
    :param repo: The repository where the package can be found. If not specified, the default CRAN repo is used.
    :type repo: str
    """

    def __init__(self, package=None, repo=None):
        """
        Initialize RCranLibrary.

        :param package: The name of the CRAN package to install.
        :type package: str
        :param repo: The repository where the package can be found. If not specified, the default CRAN repo is used.
        :type repo: str
        """
        if package is None:
            raise ValueError("package is required")
        if not isinstance(package, str):
            raise ValueError("coordinates must be a string")
        if repo is None:
            repo = ""
        if not isinstance(repo, str):
            raise ValueError("repo must be a string")

        self.package = package
        self.repo = repo


class JarLibrary:
    """
    Creates an JarLibrary input for a Databricks step.

    :param library: URI of the jar to be installed. Only DBFS and S3 URIs are supported.
    :type library: str
    """

    def __init__(self, library=None):
        """
        Initialize JarLibrary.

        :param library: URI of the jar to be installed. Only DBFS and S3 URIs are supported.
        :type library: str
        """
        if library is None:
            raise ValueError("library is required")
        if not isinstance(library, str):
            raise ValueError("library must be a string")

        self.library = library


class EggLibrary:
    """
    Creates an EggLibrary input for a Databricks step.

    :param library: URI of the egg to be installed. Only DBFS and S3 URIs are supported.
    :type library: str
    """

    def __init__(self, library=None):
        """
        Initialize EggLibrary.

        :param library: URI of the egg to be installed. Only DBFS and S3 URIs are supported.
        :type library: str
        """
        if library is None:
            raise ValueError("library is required")
        if not isinstance(library, str):
            raise ValueError("library must be a string")

        self.library = library
