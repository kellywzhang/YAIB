![YAIB logo](docs/figures/yaib_logo.png)

# Yet Another ICU Benchmark

[![CI](https://github.com/rvandewater/YAIB/actions/workflows/ci.yml/badge.svg?branch=development)](https://github.com/rvandewater/YAIB/actions/workflows/ci.yml)
[![Black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
![Platform](https://img.shields.io/badge/platform-linux--64%20|%20win--64%20|%20osx--64-lightgrey)
[![License](https://img.shields.io/badge/license-MIT-green)](LICENSE)

[//]: # (TODO: add coverage once we have some tests )

Yet another ICU benchmark (YAIB) provides a framework for doing clinical machine learning experiments on (ICU) EHR data.
We support the following datasets out of the box:

| Dataset                 | [MIMIC-III](https://physionet.org/content/mimiciii/) / [IV](https://physionet.org/content/mimiciv/) | [eICU-CRD](https://physionet.org/content/eicu-crd/) | [HiRID](https://physionet.org/content/hirid/1.1.1/) | [AUMCdb](https://doi.org/10.17026/dans-22u-f8vd) |
|-------------------------|-----------------------------------------------------------------------------------------------------|-----------------------------------------------------|-----------------------------------------------------|--------------------------------------------------|
| Admissions              | 40k / 50k                                                                                           | 200k                                                | 33k                                                 | 23k                                              |
| Frequency (time-series) | 1 hour                                                                                              | 5 minutes                                           | 2 / 5 minutes                                       | up to 1 minute                                   |
| Origin                  | USA                                                                                                 | USA                                                 | Switzerland                                         | Netherlands                                      |

The benchmark is designed for operating on preprocessed parquet files. We include five tasks by default:
<!-- We refer to  PyICU (in development)
or [ricu package](https://github.com/eth-mds/ricu) for generating these parquet files for particular cohorts and endpoints. -->

We provide several common tasks for clinical prediction by default:

| No  | Task Theme                | Frequency        | Type                                | 
|-----|---------------------------|--------------------|-------------------------------------|
| 1   | ICU Mortality             | Once per Stay (after 24H) | Binary Classification  |
| 2   | Acute Kidney Injury (AKI) | Hourly (within 6H) | Binary Classification |
| 3   | Sepsis                    | Hourly (within 6H) | Binary Classification |
| 4   | Kidney Function(KF)       | Once per stay | Regression |
| 5   | Length of Stay (LoS)      | Hourly (within 7D) | Regression |

For the purposes of getting started right away, we include the eICU and MIMIC-III demo datasets in our repository. 

## Paper

If you use this code in your research, please cite the following publication:

```
```

This paper can also be found on arxiv: TBD

# Installation

YAIB can be installed using conda or pip. Below you will find the three CLI commands to install YAIB using conda.
The

The first command will install an environment based on Python 3.10 (currently).

```
conda env update -f <environment.yml|environment_mps.yml>
```

> Use `environment.yml` on x86 hardware and `environment_mps.yml` on Macs with Metal Performance Shaders.

We then activate the environment and install a package called `icu-benchmarks`, after which YAIB should be operational.

```
conda activate yaib
pip install -e .
```

If you want to install the icu-benchmarks package with pip, execute the command below:

```
pip install torch numpy && pip install -e .
```

If you are on a Mac with Metal Performance Shader, install the package with the following command:

```
pip install torch numpy && pip install -e .[mps]
```

# Usage

## Getting the Datasets

HiRID, eICU, and MIMIC IV can be accessed through [PhysioNet](https://physionet.org/). A guide to this process can be
found [here](https://eicu-crd.mit.edu/gettingstarted/access/).
AUMCdb can be accessed through a separate access [procedure](https://github.com/AmsterdamUMC/AmsterdamUMCdb). We do not have
involvement in the access procedure and can not answer to any requests for data access.

## Data Conversion

Since the datasets were created independently of each other, they do not share the same data structure or data identifiers. In
order to make them interoperable, use the preprocessing utilities
provided by the [ricu package](https://github.com/eth-mds/ricu).
Ricu pre-defines a large number of clinical concepts and how to load them from a given dataset, providing a common interface to
the data, that is used in this
benchmark.

### Extracting cohorts

Please refer to our [cohort definition](https://github.com/rvandewater/YAIB-cohorts) code for generating the cohorts to run our benchmark once you have gained access to the datasets. 

# Data

Users can supply their own datasets in specific format. 

Adding a new dataset type can be easily done by providing it in a `.gin`
task definition file, see. Note, however, that any datasets formatted in the default way do not require any changes to be
used by YAIB. By
default, we have chosen to work with the Apache
parquet file format, which is a modern,
open-source column-oriented format that does not require a lot of
storage due to efficient data compression. We separate the data into
three separate files: `DYNAMIC`, `STATIC`, and `OUTCOME`; this is
defined for dynamic variables (that change during the stay), constant
parameters, and the prediction task label respectively. Our [cohort
definition code](https://github.com/rvandewater/YAIB-cohorts) produces
the files exactly in this format. Furthermore, we see the concept of
`roles` with the definition of the `vars` dictionary. These roles are
assigned as defined in [ReciPys](https://github.com/rvandewater/ReciPys), the preprocessing package developed
alongside YAIB.
The `GROUP` variable defines which internal dataset variable should be
used to "group by" for, e.g., aggregating patient vital signs. The
`SEQUENCE` variable defines the sequential dimension of the dataset (in
the common case, time). The other keys in this dictionary define the
feature columns and outcome variables to be used for prediction.

## Demo Data

In the folder `demo_data` we provide processed publicly available demo datasets from eICU and MIMIC with the necessary labels
for `Mortality at 24h`,`Sepsis`, `Akute Kidney Injury`, `Kidney Function`, `Length of Stay`.

# Running the Benchmark

## Preprocessing and Training

The following command will run training and evaluation on the MIMIC demo dataset for (Binary) Mortality prediction at 24h with
the
LGBMClassifier. Child samples are reduced due to the small amount of training data. We load available cache and, if available,
load
existing cache files.

```
icu-benchmarks train \
    -d demo_data/mortality24/mimic_demo \
    -n mimic_demo \
    -t BinaryClassification \
    -tn Mortality24 \
    -m LGBMClassifier \
    -hp LGBMClassifier.min_child_samples=10 \
    --generate_cache
    --load_cache \
    --seed 2222 \
    -s 2222 \
    -l ../yaib_logs/ \
    --tune
```

> For a list of available flags, run `icu-benchmarks train -h`.

> Run with `PYTORCH_ENABLE_MPS_FALLBACK=1` on Macs with Metal Performance Shaders.

[//]: # (> Please note that, for Windows based systems, paths need to be formatted differently, e.g: ` r"\..\data\mortality_seq\hirid"`.)
> For Windows based systems, the next line character (\\)  needs to be replaced by (^) (Command Prompt) or (`) (Powershell)
> respectively.


## Evaluate

It is possible to evaluate a model trained on another dataset. In this case, the source dataset is the demo data from MIMIC and
the target is the eICU demo:

```
icu-benchmarks evaluate \
    -d demo_data/mortality24/eicu_demo \
    -n eicu_demo \
    -t BinaryClassification \
    -tn Mortality24 \
    -m LGBMClassifier \
    --generate_cache \
    --load_cache \
    -s 2222 \
    -l ../yaib_logs \
    -sn mimic \
    --source-dir ../yaib_logs/mimic_demo/Mortality24/LGBMClassifier/2022-12-12T15-24-46/fold_0
```

## Imputation

Below is an example call for training an imputation model

```
icu-benchmarks train \
    -d demo_data/mortality24/mimic_demo \
    -n mimic_demo \
    -t DatasetImputation \
    -m Mean \
    -lc -gc \
    -s 2222 \
    -l ../yaib_logs/ 
```

For more details on how to implement new imputation methods, visit [this document](docs/imputation_methods.md).

## Training a Classification model using a pretrained imputation model

Below is an example call to train a classification model using a pretrained imputation model:

``` bash
icu-benchmarks train \
    -d demo_data/mortality24/mimic_demo \
    -n mimic_demo \
    -t BinaryClassificationPretrainedImputation \
    -tn Mortality24 \
    -m LGBMClassifier \
    -hp LGBMClassifier.min_child_samples=10 \
    -gc \
    -lc \
    -s 2222 \
    -l ../yaib_logs/ \
    --use_pretrained_imputation path/to/pretrained/imputation_model.ckpt
    --tune
```

Where `path/to/pretrained/imputation_model.ckpt` is the path to the `model.ckpt` created by training an imputation model with
our framework.

## Metrics

Several metrics are defined for this benchmark:

- Binary Classification: Because our tasks are all highly imbalanced, we use both ROC and PR Area Under the Curve
  using [sklearn.metrics.roc_auc_score](https://scikit-learn.org/stable/modules/generated/sklearn.metrics.roc_auc_score.html)
  and [sklearn.metrics.average_precision_score](https://scikit-learn.org/stable/modules/generated/sklearn.metrics.average_precision_score.html#sklearn.metrics.average_precision_score)
- Regression : The Mean Absolute Error (MAE) is used
  with [sklearn.metrics.mean_absolute_error](https://scikit-learn.org/stable/modules/generated/sklearn.metrics.mean_absolute_error.html)

## Models

We provide several existing machine learning models that are commonly used for multivariate time-series data.
`pytorch` is used for the deep learning models, `lightgbm` for the boosted tree approaches, and `sklearn` for the logistic
regression model and metrics.
The benchmark provides the following built-in models:

- [Logistic Regression](https://scikit-learn.org/stable/modules/generated/sklearn.linear_model.LogisticRegression.html?highlight=logistic+regression):
  Standard regression approach.
- [LightGBM](https://proceedings.neurips.cc/paper/2017/file/6449f44a102fde848669bdd9eb6b76fa-Paper.pdf): Efficient gradient
  boosting trees.
- [Long Short-term Memory (LSTM)](https://ieeexplore.ieee.org/document/818041): The most commonly used type of Recurrent Neural
  Networks for long sequences.
- [Gated Recurrent Unit (GRU)](https://arxiv.org/abs/1406.1078) : A extension to LSTM which showed improvement over them in the
  context of polyphonic music modeling and speech signal modeling ([paper](https://arxiv.org/abs/1412.3555)).
- [Temporal Convolutional Networks (TCN)](https://arxiv.org/pdf/1803.01271 ): 1D convolution approach to sequence data. By
  using dilated convolution to extend the receptive field of the network it has shown great performance on long-term
  dependencies.
- [Transformers](https://papers.nips.cc/paper/2017/file/3f5ee243547dee91fbd053c1c4a845aa-Paper.pdf): The most common Attention
  based approach.

# Development

To adapt YAIB to your own use case, you can use the [development information](docs/development.md) document as a reference.

# Acknowledgements

We do not own any of the datasets used in this benchmark. This project uses adapted components of
the [HiRID benchmark](https://github.com/ratschlab/HIRID-ICU-Benchmark/). We thank the authors for providing this codebase and
encourage further development to benefit the scientific community.

# License

This source code is released under the MIT license, included [here](LICENSE).
