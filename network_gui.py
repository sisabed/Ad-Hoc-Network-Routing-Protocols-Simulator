#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import tkinter as tk
from tkinter import ttk, messagebox
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from network import Network
from protocols.aodv import AODV
from protocols.dsr import DSR
from protocols.olsr import OLSR
from mobility import random_waypoint, random_direction
from visualize import visualize_network
import time
import random
import csv

class NetworkSimulatorGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Ad Hoc Network Simulator")
        self.protocol_name = tk.StringVar(value="AODV")
        self.mobility_model = tk.StringVar(value="waypoint")
        self.metrics = {
            "throughput": 0,
            "end_to_end_delay": [],
            "packet_delivery_ratio": 0,
            "control_overhead": 0
        }

        # Setup main frames
        
        self.network = None
        self.figure = None   # Initialize `self.figure` as None here
        self.canvas = None   # Initialize `self.canvas` as None here
        self.protocol = None
        self.simulation_running = False
        self.setup_gui()
        
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)

    def setup_gui(self):
        # Protocol Selection
        ttk.Label(self.root, text="Select Protocol:").grid(row=0, column=0, padx=5, pady=5)
        protocol_menu = ttk.Combobox(self.root, textvariable=self.protocol_name, values=["AODV", "DSR", "OLSR"])
        protocol_menu.grid(row=0, column=1, padx=5, pady=5)

        # Mobility Model Selection
        ttk.Label(self.root, text="Select Mobility Model:").grid(row=1, column=0, padx=5, pady=5)
        mobility_menu = ttk.Combobox(self.root, textvariable=self.mobility_model, values=["waypoint", "direction"])
        mobility_menu.grid(row=1, column=1, padx=5, pady=5)

        # Control Buttons
        ttk.Button(self.root, text="Start Simulation", command=self.start_simulation).grid(row=2, column=0, padx=5, pady=5)
        ttk.Button(self.root, text="Pause Simulation", command=self.pause_simulation).grid(row=2, column=1, padx=5, pady=5)
        #ttk.Button(self.root, text="Export Results", command=self.export_results).grid(row=2, column=2, padx=5, pady=5)
        self.export_button = ttk.Button(self.root, text="Export Results", command=self.export_results)
        self.export_button.grid(row=2, column=2, padx=5, pady=5)
        self.export_button.config(state="disabled")  # Disable initially, enable after simulation starts


        # Metric Display
        self.metrics_display = tk.Text(self.root, height=10, width=40, state="disabled")
        self.metrics_display.grid(row=3, column=0, columnspan=3, padx=5, pady=5)

        # Matplotlib Figure for Network Visualization
        self.figure = visualize_network(self.network, self.metrics, self.protocol_name.get())
        self.canvas = FigureCanvasTkAgg(self.figure, self.root)
        self.canvas.get_tk_widget().grid(row=0, column=3, rowspan=4, padx=5, pady=5)

    def start_simulation(self):
        self.simulation_running = True
        self.network = Network(num_nodes=10, area_size=500)
        self.protocol = self.select_protocol()  # Initialize protocol here
        self.run_simulation()
        self.export_button.config(state="normal") 

    def pause_simulation(self):
        self.simulation_running = False
        self.export_button.config(state="normal")

    def export_results(self):
        filename = "simulation_metrics.csv"
        with open(filename, mode='w', newline='') as csv_file:
            writer = csv.writer(csv_file)
            writer.writerow(["Metric", "Value"])
            writer.writerow(["Throughput", self.metrics["throughput"]])
            writer.writerow(["Average Delay (s)", self.calculate_average_delay(self.metrics["end_to_end_delay"])])
            writer.writerow(["Packet Delivery Ratio", self.metrics["packet_delivery_ratio"]])
            writer.writerow(["Control Overhead", self.metrics["control_overhead"]])
        messagebox.showinfo("Export Complete", f"Metrics exported to {filename}")

    def run_simulation(self):
        if not self.simulation_running:
            return

        # Perform a single step in the simulation
        self.protocol = self.select_protocol()
        self.network.update_all_neighbors()
        self.update_metrics_display()

        # Generate random traffic
        src, dest = random.randint(0, self.network.num_nodes - 1), random.randint(0, self.network.num_nodes - 1)
        if src != dest:
            packet = self.network.generate_packet(src, dest)
            route = self.calculate_route(src, dest)

            if route:
                start_time = time.time()
                self.deliver_packet(packet, route)
                end_time = time.time()
                self.metrics["throughput"] += 1
                self.metrics["end_to_end_delay"].append(end_time - start_time)

        # Move nodes based on mobility model
        for node in self.network.nodes:
            if self.mobility_model.get() == "waypoint":
                random_waypoint(node)
            elif self.mobility_model.get() == "direction":
                random_direction(node)

        # Calculate additional metrics
        total_packets = self.network.get_total_packets()
        self.metrics["packet_delivery_ratio"] = self.calculate_packet_delivery_ratio(self.metrics["throughput"], total_packets)
        self.metrics["control_overhead"] += self.calculate_control_overhead()

        # Update visualization
        if self.network and self.network.nodes:
            self.update_visualization()
        else:
            print("Error: Network or network.nodes is not properly initialized for visualization.")

        self.root.after(1000, self.run_simulation)  # Schedule the next simulation step
        

    def select_protocol(self):
        protocol_name = self.protocol_name.get()
        if protocol_name == "AODV":
            return AODV(self.network)
        elif protocol_name == "DSR":
            return DSR(self.network)
        elif protocol_name == "OLSR":
            protocol = OLSR(self.network)
            protocol.update_routes()
            return protocol

    def calculate_route(self, src, dest):
        if self.protocol_name.get() == "AODV" or self.protocol_name.get() == "DSR":
            return self.protocol.find_route(src, dest)
        elif self.protocol_name.get() == "OLSR":
            return self.protocol.routes.get(src, {}).get(dest, None)
        return None

    def deliver_packet(self, packet, route):
        for node_id in route:
            print(f"Packet {packet['packet_id']} forwarded to Node {node_id}")

    def update_visualization(self):
        # Only visualize after the network has been created
        if not self.network:
            return

        # Clear and recreate figure if it already exists
        if self.figure:
            self.figure.clear()
        self.figure = visualize_network(self.network, self.metrics, self.protocol_name.get())

        # Update the Tkinter canvas with the new figure
        if self.canvas:
            self.canvas.get_tk_widget().destroy()
        self.canvas = FigureCanvasTkAgg(self.figure, master=self.root)
        self.canvas.draw()
        self.canvas.get_tk_widget().grid(row=0, column=2, rowspan=4)

    def update_metrics_display(self):
        self.metrics_display.config(state="normal")
        self.metrics_display.delete(1.0, tk.END)
        avg_delay = self.calculate_average_delay(self.metrics["end_to_end_delay"])
        metrics_text = (
            f"Throughput: {self.metrics['throughput']}\n"
            f"Average Delay: {avg_delay:.2f} s\n"
            f"Packet Delivery Ratio: {self.metrics['packet_delivery_ratio']:.2f}\n"
            f"Control Overhead: {self.metrics['control_overhead']}\n"
        )
        self.metrics_display.insert(tk.END, metrics_text)
        self.metrics_display.config(state="disabled")

    def calculate_packet_delivery_ratio(self, successful_deliveries, total_packets):
        return successful_deliveries / total_packets if total_packets > 0 else 0

    def calculate_average_delay(self, delays):
        return sum(delays) / len(delays) if delays else 0

    def calculate_control_overhead(self):
        if self.protocol_name.get() == "AODV":
            return 2  # Example control overhead per step
        elif self.protocol_name.get() == "DSR":
            return 1.5
        elif self.protocol_name.get() == "OLSR":
            return 1
        return 0
    def on_closing(self):
#         """Custom handler for closing the Tkinter window."""
        # Set a flag indicating that the simulation has ended
        self.simulation_running = False  # Stop the simulation
        self.export_button.config(state="normal")

        # Check if there are any active canvas widgets and destroy them safely
        if self.canvas:
            try:
                self.canvas.get_tk_widget().destroy()
            except tk.TclError:
                print("Canvas already destroyed.")

        # Destroy the main Tkinter window
        self.root.destroy()


# Run the GUI application
if __name__ == "__main__":
    root = tk.Tk()
    app = NetworkSimulatorGUI(root)
    root.mainloop()

