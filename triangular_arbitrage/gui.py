import asyncio
import threading
import time
import tkinter as tk
from tkinter import ttk

from . import detector


class ArbitrageGUI:
    """Basic Tkinter interface for running the arbitrage detector."""

    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Triangular Arbitrage Detector")

        self.exchange_var = tk.StringVar(value="binanceus")
        self._build_widgets()

        self.running = False
        self.thread = None

    def _build_widgets(self):
        top = ttk.Frame(self.root)
        top.pack(padx=10, pady=10, fill=tk.X)

        ttk.Label(top, text="Exchange:").pack(side=tk.LEFT)
        ttk.Entry(top, textvariable=self.exchange_var, width=15).pack(side=tk.LEFT, padx=5)
        ttk.Button(top, text="Start", command=self.start).pack(side=tk.LEFT, padx=5)
        ttk.Button(top, text="Stop", command=self.stop).pack(side=tk.LEFT)

        columns = ("step", "action", "pair", "price")
        self.tree = ttk.Treeview(self.root, columns=columns, show="headings")
        for col in columns:
            self.tree.heading(col, text=col.capitalize())
        self.tree.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

    def start(self):
        if self.running:
            return
        self.running = True
        self.thread = threading.Thread(target=self._detection_loop, daemon=True)
        self.thread.start()

    def stop(self):
        self.running = False

    def _detection_loop(self):
        while self.running:
            exchange = self.exchange_var.get()
            best_opps, profit = asyncio.run(detector.run_detection(exchange))
            self.root.after(0, self._update_table, best_opps, profit, exchange)
            time.sleep(5)  # avoid hitting the API too often

    def _update_table(self, opportunities, profit, exchange):
        for row in self.tree.get_children():
            self.tree.delete(row)
        if opportunities is None:
            self.root.title(f"Triangular Arbitrage Detector - {exchange} (no opportunity)")
            return
        for i, opp in enumerate(opportunities, 1):
            action = "buy" if opp.reversed else "sell"
            self.tree.insert("", "end", values=(i, action, str(opp.symbol), f"{opp.last_price:.5f}"))
        self.root.title(
            f"Triangular Arbitrage Detector - {exchange} ({(profit - 1) * 100:.2f}% profit)"
        )

    def run(self):
        self.root.mainloop()


def main():
    gui = ArbitrageGUI()
    gui.run()


if __name__ == "__main__":
    main()
