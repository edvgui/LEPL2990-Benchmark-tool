# LEPL2990-Benchmark-tool
This repository hosts my benchmarking tool for comparing different containerization and virtualization solutions.

## Structure
This repository containers the source code of the benchmark tool created to compare different containerization solutions
as well as the source code of the of the different plots made based on the results and also the different resources
associated with the containers manipulated and some deployment playbooks to make the use easier.

```
.
├── measurements                # Measurements for all the tested configurations
├── ops                         # Playbooks and script to launch the benchmark tool
│   ├── cleanup-playbooks
│   ├── config-playbooks
│   ├── deploy-playbooks
│   └── run-playbooks
├── plots                       # Some plots of the results I obtained
├── resources
│   ├── common                  # Resources needed to create testing containers
│   │   ├── http-server
│   │   ├── io
│   │   ├── network
│   │   └── sqlite
│   ├── contingious             # Utilities to import contingious container images
│   ├── docker                  # Utilities to import/build docker container images
│   ├── lxd                     # Utilities to import/build lxd container images
│   └── podman                  # Utilities to import podman container images
└── src
    ├── benchmark               # Source of the benchmark tool
    │   ├── api                 # Api to interface with the different tools compared
    │   ├── contingious         # Basic mplementation of continigious
    │   ├── exceptions
    │   └── procedure           # Implementation of different tests
    └── plot
```

## License
The content of this repository is under MIT License, use it at your convenience.