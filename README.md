```
  _____    _______   _                  ____    _____    _______ 
 |  __ \  |__   __| | |                / __ \  |  __ \  |__   __|
 | |__) |    | |    | |       ______  | |  | | | |__) |    | |   
 |  _  /     | |    | |      |______| | |  | | |  ___/     | |   
 | | \ \     | |    | |____           | |__| | | |         | |   
 |_|  \_\    |_|    |______|           \____/  |_|         |_|   
```                                                                 
                                                                 
# RTL-OPT: A Benchmark for RTL Code Optimization

**RTL-OPT** is a benchmark designed to evaluate RTL code optimization for improving IC design quality. The dataset consists of 36 digital IC designs, each containing suboptimal and expert-optimized RTL code, enabling the assessment of LLM-generated RTL code. The dataset also includes an integrated evaluation framework for automatic verification of functional correctness and quantification of PPA (Power, Performance, Area) improvements.

This benchmark provides a realistic and comprehensive evaluation method for generative AI models in hardware design optimization.

## Dataset Contents

- **Number of Designs**: 36 digital IC designs
- **Code Types**:
  - Suboptimal RTL code
  - Expert-optimized RTL code (golden reference)

## 📁 Project Structure

```
.
├── Results/                          # Test results and outputs
│   ├── LLM_Test_result/             # Large Language Model testing results
│   ├── RTL-OPT_DC/                  # RTL optimization results using Design Compiler
│   ├── RTL-OPT_FM/                  # RTL optimization results using Formality
│   └── RTL-OPT_Yosys/               # RTL optimization results using Yosys
|
└── benchmarks/                       # Optimal and Sub-optimal designs
│
└── evaluation_framework/             # Core evaluation framework
    ├── DC/                          # Design Compiler scripts and configurations
    ├── Formality/                          # Formality scripts and configurations
    ├── Yosys/                       # Yosys scripts and configurations
    └── lib/                         # Library files and dependencies
```

## 📊 Directory Details

### Results/
- **LLM test results/**: Outputs and logs from Large Language Model integration tests. Also, `llm_gen.py` is included to generate the optimized RTL code for LLMs.
- **RTL-OPT_DC/**: Netlists, reports, and timing analysis from RTL optimization using Synopsys Design Compiler
- **RTL-OPT_FM/**: Formal verification results and equivalence checking reports using Synopsys Formality
- **RTL-OPT_Yosys/**: RTL optimization results using Yosys open-source synthesis tool

### evaluation_framework/
- **DC/**: Auto-run scripts, constraint files, and configuration files for Design Compiler
- **Formality/**: Auto-run scripts and setup files for Formality to verify functional consistency
- **Yosys/**: Auto-run synthesis scripts, strategy configurations, and plugins for Yosys
- **lib/**: Technology libraries, standard cell libraries, and other necessary library files
