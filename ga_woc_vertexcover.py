import tkinter as tk
from tkinter import ttk
import random
import csv
import datetime
import time
import networkx as nx
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

#Genetic Algorithm with WoC
def vertex_cover_ga(num_vertices, edge_prob, pop_size, generations, mutation_rate, top_k_frac, use_woc, update_plot=None):
    #Creates random graph using erdos-renyi model
    G = nx.erdos_renyi_graph(num_vertices, edge_prob)

    #Precomputes edges
    edges = list(G.edges())

    #Fitness
    def fitness(cover):
        uncovered = sum(1 for (u, v) in edges if not (cover[u] or cover[v]))
        return uncovered + sum(cover) / num_vertices

    #Initializes population to 0 or 1   
    population = [[random.choice([0, 1]) for _ in range(num_vertices)] for _ in range(pop_size)]

    for gen in range(generations):
        fitnesses = [fitness(ind) for ind in population]
        ranked = sorted(zip(fitnesses, population), key=lambda x: x[0])
        new_pop = []

        #WoC selection
        if use_woc:
            top_k = int(top_k_frac * pop_size)
            best_inds = [ind for (_, ind) in ranked[:max(1, top_k)]]
            consensus = [1 if sum(ind[i] for ind in best_inds) > top_k / 2 else 0 for i in range(num_vertices)]
            new_pop.append(consensus)

        #Elitism
        new_pop.append(ranked[0][1])

        #Crossover and mutation
        while len(new_pop) < pop_size:
            p1, p2 = random.choices(population, k=2)
            point = random.randint(1, num_vertices - 1)
            child = p1[:point] + p2[point:]
            for i in range(num_vertices):
                if random.random() < mutation_rate:
                    child[i] = 1 - child[i]
            new_pop.append(child)

        population = new_pop

        
        if update_plot:
            best_cover = ranked[0][1]
            update_plot(G, best_cover, gen, ranked[0][0])

    best_fit, best_cover = min(zip(fitnesses, population), key=lambda x: x[0])
    uncovered = sum(1 for (u, v) in edges if not (best_cover[u] or best_cover[v]))

    return {
        "cover_size": sum(best_cover),
        "uncovered": uncovered,
        "fitness": best_fit,
        "graph": G,
        "cover": best_cover,
    }

#GUI
class VertexCoverGUI:
    def __init__(self, root):
        self.root = root
        root.title("Vertex Cover GA + WoC (Visual Experiment)")
        root.geometry("1200x700")

        #Left panel
        controls = ttk.Frame(root)
        controls.pack(side="left", fill="y", padx=10, pady=10)
        

        #sliders here
        self.sliders = {}
        params = [
            ("Num Vertices", "NUM_VERTICES", 5, 30, 1),
            ("Edge Probability", "EDGE_PROB", 0.1, 0.9, 0.05),
            ("Population Size", "POP_SIZE", 10, 200, 10),
            ("Generations", "GENERATIONS", 10, 200, 10),
            ("Mutation Rate", "MUTATION_RATE", 0.01, 0.3, 0.01),
            ("Top-K Fraction", "TOP_K_FRAC", 0.1, 0.5, 0.05),
            ("Trials", "TRIALS", 1, 100, 1),
        ]
        for label, key, frm, to, step in params:
            self.create_slider(controls, label, key, frm, to, step)

        self.use_woc = tk.BooleanVar(value=True)
        ttk.Checkbutton(controls, text="Use Wisdom of Crowds", variable=self.use_woc).pack(anchor="w", pady=5)

        ttk.Button(controls, text="Run Experiment", command=self.run_experiment).pack(pady=15)

        #Graph
        self.fig, self.ax = plt.subplots(figsize=(6, 6))
        self.ax.axis("off")
        self.canvas = FigureCanvasTkAgg(self.fig, master=root)
        self.canvas.get_tk_widget().pack(side="right", fill="both", expand=True)

    def create_slider(self, parent, label, key, frm, to, step):
        ttk.Label(parent, text=label).pack()
        var = tk.DoubleVar(value=frm)
        slider = ttk.Scale(parent, from_=frm, to=to, variable=var, orient="horizontal")
        slider.pack(fill="x")
        entry = ttk.Entry(parent, textvariable=var)
        entry.pack()
        self.sliders[key] = var

    def update_plot(self, G, cover, gen, fit):
        self.ax.clear()
        self.ax.set_title(f"Generation {gen} | Fitness: {fit:.3f}")
        pos = nx.spring_layout(G, seed=42)
        nx.draw_networkx_edges(G, pos, ax=self.ax, edge_color="gray")
        node_colors = ["red" if cover[i] else "lightgray" for i in G.nodes()]
        nx.draw_networkx_nodes(G, pos, ax=self.ax, node_color=node_colors, node_size=300)
        nx.draw_networkx_labels(G, pos, ax=self.ax, font_color="black")
        self.canvas.draw()
        self.root.update()

    def run_experiment(self):
        use_woc = self.use_woc.get()
        params = {k: v.get() for k, v in self.sliders.items()}

        trials = int(params["TRIALS"])
        with open("results.csv", "a", newline="") as f:
            writer = csv.writer(f)
            for trial in range(trials):
                start = time.time()
                res = vertex_cover_ga(
                    int(params["NUM_VERTICES"]),
                    params["EDGE_PROB"],
                    int(params["POP_SIZE"]),
                    int(params["GENERATIONS"]),
                    params["MUTATION_RATE"],
                    params["TOP_K_FRAC"],
                    use_woc,
                    update_plot=self.update_plot,
                )
                elapsed = time.time() - start
                writer.writerow([
                    datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    use_woc,
                    int(params["NUM_VERTICES"]),
                    params["EDGE_PROB"],
                    int(params["POP_SIZE"]),
                    int(params["GENERATIONS"]),
                    params["MUTATION_RATE"],
                    params["TOP_K_FRAC"],
                    trial + 1,
                    res["cover_size"],
                    res["uncovered"],
                    res["fitness"],
                    round(elapsed, 3),
                ])
        print("✅ Experiments complete. Results saved to results.csv")

#main

if __name__ == "__main__":
    root = tk.Tk()
    app = VertexCoverGUI(root)
    root.mainloop()
