# Genetic Algorithm with Wisdom of Crowds for Vertex Cover Problem

A hybrid genetic algorithm combining Wisdom of Crowds (WoC) aggregation to approximate solutions for the NP-hard Minimum Vertex Cover problem.

![Python](https://img.shields.io/badge/Python-3776AB?style=flat&logo=python&logoColor=white)
![NetworkX](https://img.shields.io/badge/NetworkX-4C8CBF?style=flat)
![Tkinter](https://img.shields.io/badge/Tkinter-GUI-blue)
![License](https://img.shields.io/badge/License-MIT-green)

---

## Overview

The Vertex Cover problem asks for the smallest set of vertices that cover all edges in a graph. This project implements a hybrid approach combining:

- **Genetic Algorithm (GA):** Evolves candidate solutions using selection, crossover, and mutation
- **Wisdom of Crowds (WoC):** Aggregates top-performing individuals to guide future generations

---

## Key Results

| Metric | Standard GA | GA + WoC |
|--------|-------------|----------|
| Average Cover Size | 9.1 | 8.5 |
| Best Cover Size | 8 | 7 |
| Improvement | — | **7%** |

- Validated across **150+ trials**
- Tested with **15 controlled experiments**
- Consistent convergence with reduced variance

---

## Features

- **Interactive GUI** with 7 adjustable parameters
- **Real-time visualization** of graph evolution
- **Erdős-Rényi random graph generation**
- **CSV export** for experiment logging and analysis

---

## Installation
```bash
# Clone the repository
git clone https://github.com/justinp42/GA-WoC-for-Vertex-Cover.git
cd GA-WoC-for-Vertex-Cover

# Install dependencies
pip install networkx matplotlib

# Run the application
python main.py
```

---

## Usage

1. Launch the GUI
2. Adjust parameters:
   - Number of vertices
   - Edge probability
   - Population size
   - Number of generations
   - Mutation rate
   - Top-K fraction (for WoC)
3. Toggle "Use Wisdom of Crowds" on/off
4. Click "Run Experiment"
5. View results in real-time and export to CSV

---

## Project Structure
```
GA-WoC-for-Vertex-Cover/
├── main.py              # Main application with GUI
├── results.csv          # Experiment results output
├── README.md
└── A Hybrid Genetic Algorithm with Wisdom-of-Crowds Aggregation for Approximating Minimum Vertex Covers.pdf   # Research paper 
```

---

## Research Paper

This project includes an **8-page IEEE-format research paper** documenting:
- Algorithm design and methodology
- Experimental setup and results
- Analysis of 16 peer-reviewed sources

---

## Technologies Used

- **Python** — Core language
- **NetworkX** — Graph generation and manipulation
- **Tkinter** — GUI framework
- **Matplotlib** — Data visualization

---

## Contact

**Justin Pham**  
- LinkedIn: [linkedin.com/in/justinpham](your-linkedin-url)
- Email: jhpham05@gmail.com

---

## License

This project is licensed under the MIT License.
