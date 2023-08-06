from distutils.core import setup

setup(
    name="metro_distribution_engine",
    version="0.3.8",
    url="https://getmetro.co",
    description="The distribution engine for moving metrics around the Metro network",
    author="Metro",
    author_email="rory@getmetro.co",
    packages=['metro_distribution_engine', 'metro_distribution_engine/sqs_engine']
)
