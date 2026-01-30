import os
import gradio as gr
import pandas as pd
import matplotlib.pyplot as plt

# ---------- Helpers ----------

def get_available_symbols():
    try:
        return sorted(
            f.replace(".csv", "")
            for f in os.listdir("archive/stocks")
            if f.endswith(".csv")
        )
    except Exception:
        return []

def get_available_date_range(symbol):
    df = pd.read_csv(f"archive/stocks/{symbol}.csv")
    df["Date"] = pd.to_datetime(df["Date"])
    return df["Date"].min().date(), df["Date"].max().date()

def update_date_range(symbol):
    if not symbol:
        return "Select a stock"
    start, end = get_available_date_range(symbol)
    return f"{start} → {end}"

# ---------- Core Logic ----------

def predict_and_plot(symbol, initial_capital, start_date, end_date):
    if not symbol or not start_date or not end_date:
        return "Missing inputs", None

    df = pd.read_csv(f"archive/stocks/{symbol}.csv")
    df["Date"] = pd.to_datetime(df["Date"])
    df = df[(df["Date"] >= start_date) & (df["Date"] <= end_date)]

    if df.empty:
        return "No data for selected range", None

    # Simple fake prediction for demo
    final_capital = initial_capital * 1.05

    # ----- PLOT -----
    fig, ax = plt.subplots(figsize=(8, 4))
    ax.plot(df["Date"], df["Close"], label="Close Price")
    ax.set_title(f"{symbol} Price History")
    ax.set_xlabel("Date")
    ax.set_ylabel("Price")
    ax.legend()
    ax.grid(True)

    result = (
        f"Symbol: {symbol}\n"
        f"Initial Capital: ${initial_capital:,.2f}\n"
        f"Final Capital (demo): ${final_capital:,.2f}"
    )

    return result, fig

# ---------- UI ----------

def create_app():
    symbols = get_available_symbols()

    with gr.Blocks(title="Stock Trading Bot") as app:
        gr.Markdown("# 📈 Stock Trading Bot")
        gr.Markdown("Interactive stock visualization demo")

        with gr.Row():
            with gr.Column():
                symbol = gr.Dropdown(
                    label="Stock Symbol",
                    choices=symbols,
                    interactive=True
                )
                date_range = gr.Textbox(
                    label="Available Date Range",
                    interactive=False
                )
                capital = gr.Number(
                    label="Initial Capital ($)",
                    value=10000
                )
                start_date = gr.Textbox(
                    label="Start Date (YYYY-MM-DD)"
                )
                end_date = gr.Textbox(
                    label="End Date (YYYY-MM-DD)"
                )
                run = gr.Button("Predict")

            with gr.Column():
                output_text = gr.Textbox(
                    label="Results",
                    lines=4,
                    interactive=False
                )
                plot = gr.Plot(label="Stock Price Chart")

        symbol.change(
            fn=update_date_range,
            inputs=symbol,
            outputs=date_range
        )

        run.click(
            fn=predict_and_plot,
            inputs=[symbol, capital, start_date, end_date],
            outputs=[output_text, plot]
        )

    return app

# ---------- Launch ----------

if __name__ == "__main__":
    app = create_app()
    app.launch(server_port=8888)