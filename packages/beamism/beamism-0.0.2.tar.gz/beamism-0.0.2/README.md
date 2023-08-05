# beamism

beamism is a tiny framework to run apache beam based software.

### Motivation
- Implement Mongo Sink
- Schema Validation
- Flow Control

### Installation

```
pip install beamism
```

### Quick Start(Examples)
```
# run locally
python examples/wordcount_streaming.py

# deploy to Google Cloud Dataflow
python examples/wordcount_streaming.py --runner DataflowRunner --project {YOUR_PROJECT}--setup_file {ABSOLUTE_PATH_TO_SETUP.PY} --requirements_file {ABSOLUTE_PATH_TO_REQUIREMENTS.TXT} --temp_location {GCP_STORAGE_PATH} --staging_location {GCP_STORAGE_PATH}
```

※ This module is inspired by [Apache Beam](https://github.com/apache/beam), and some codes are modified based on it.