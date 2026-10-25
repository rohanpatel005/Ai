"""
Interactive Visualization Module.
Builds Plotly charts and graphical reasoning diagrams for reasoning pipelines,
backward chaining goal trees, and empirical complexity benchmarks.
"""

from typing import List, Dict, Any, Optional
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

from src.models import InferenceResult, BackwardGoalNode


class Visualizer:
    """
    Constructs modern, interactive Plotly visualizations for the Medical Expert System.
    """

    # Academic & Professional Theme Palette
    COLOR_PRIMARY = "#2563EB"    # Royal Blue
    COLOR_SECONDARY = "#0D9488"  # Teal
    COLOR_ACCENT = "#F59E0B"     # Amber
    COLOR_DANGER = "#EF4444"     # Crimson
    COLOR_SUCCESS = "#10B981"    # Emerald
    COLOR_BG_CARD = "#F8FAFC"    # Soft Slate Light

    @staticmethod
    def plot_algorithm_comparison(results_map: Dict[str, InferenceResult]) -> go.Figure:
        """
        Creates a dual-axis or side-by-side bar chart comparing runtime, rules evaluated, and rules fired.
        """
        algos = []
        runtimes = []
        evaluated = []
        fired = []

        for name, res in results_map.items():
            algos.append(name)
            runtimes.append(round(res.execution_time_ms, 3))
            evaluated.append(res.evaluated_rules_count)
            fired.append(len(res.fired_rules))

        fig = go.Figure()

        # Rules Evaluated
        fig.add_trace(go.Bar(
            name="Rules Evaluated",
            x=algos,
            y=evaluated,
            marker_color="#94A3B8",
            yaxis="y1",
        ))

        # Rules Fired
        fig.add_trace(go.Bar(
            name="Rules Fired",
            x=algos,
            y=fired,
            marker_color="#10B981",
            yaxis="y1",
        ))

        # Execution Time (ms) on Secondary Y-Axis
        fig.add_trace(go.Scatter(
            name="Execution Time (ms)",
            x=algos,
            y=runtimes,
            mode="lines+markers+text",
            text=[f"{t:.2f} ms" for t in runtimes],
            textposition="top center",
            marker=dict(size=10, color="#2563EB"),
            line=dict(width=3, color="#2563EB"),
            yaxis="y2",
        ))

        fig.update_layout(
            title="Reasoning Performance Across Paradigms",
            xaxis=dict(title="Inference Algorithm"),
            yaxis=dict(title="Rule Count", side="left", showgrid=True),
            yaxis2=dict(
                title="Execution Time (ms)",
                side="right",
                overlaying="y",
                showgrid=False,
            ),
            legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
            barmode="group",
            margin=dict(l=40, r=40, t=60, b=40),
            template="plotly_white",
            height=450,
        )

        return fig

    @staticmethod
    def plot_benchmark_runtimes(summary_df: pd.DataFrame) -> go.Figure:
        """
        Bar chart of average execution time per algorithm in benchmark runs.
        """
        fig = px.bar(
            summary_df,
            x="Algorithm",
            y="Avg Execution Time (ms)",
            color="Algorithm",
            text_auto=".3f",
            title="Benchmark: Average Execution Time per Case (ms)",
            color_discrete_sequence=["#3B82F6", "#10B981", "#8B5CF6", "#F59E0B"],
            template="plotly_white",
        )
        fig.update_layout(
            showlegend=False,
            yaxis_title="Time (ms)",
            height=400,
            margin=dict(l=40, r=40, t=50, b=40),
        )
        return fig

    @staticmethod
    def plot_kb_scaling(scaling_df: pd.DataFrame) -> go.Figure:
        """
        Line chart illustrating Knowledge Base Size vs Execution Time.
        """
        fig = px.line(
            scaling_df,
            x="KB_Size",
            y="Avg_Execution_Time_ms",
            color="Algorithm",
            markers=True,
            title="Empirical Complexity: Knowledge Base Size vs. Execution Time (ms)",
            template="plotly_white",
            color_discrete_sequence=["#3B82F6", "#10B981", "#8B5CF6", "#F59E0B"],
        )
        fig.update_layout(
            xaxis_title="Knowledge Base Size (Number of Rules)",
            yaxis_title="Execution Time (ms)",
            height=420,
            margin=dict(l=40, r=40, t=50, b=40),
        )
        return fig

    @staticmethod
    def plot_load_scaling(load_df: pd.DataFrame) -> go.Figure:
        """
        Line chart illustrating Number of Test Cases vs Total Wall Execution Time.
        """
        fig = px.line(
            load_df,
            x="Test_Cases_Count",
            y="Total_Execution_Time_ms",
            color="Algorithm",
            markers=True,
            title="Scalability: Test Case Load vs. Cumulative Execution Time (ms)",
            template="plotly_white",
            color_discrete_sequence=["#3B82F6", "#10B981", "#8B5CF6", "#F59E0B"],
        )
        fig.update_layout(
            xaxis_title="Number of Test Cases",
            yaxis_title="Total Execution Time (ms)",
            height=420,
            margin=dict(l=40, r=40, t=50, b=40),
        )
        return fig

    @staticmethod
    def render_backward_tree_graph(root: BackwardGoalNode) -> go.Figure:
        """
        Generates an interactive hierarchical tree visualization for Backward Chaining.
        """
        nodes_x = []
        nodes_y = []
        nodes_text = []
        nodes_color = []
        nodes_hover = []

        edge_x = []
        edge_y = []

        def traverse(node: BackwardGoalNode, x: float, y: float, spread: float):
            nodes_x.append(x)
            nodes_y.append(y)
            label = node.goal
            if node.rule_id:
                label = f"{node.goal} ({node.rule_id})"
            nodes_text.append(label)

            # Node color by status
            color_map = {
                "PROVEN_FACT": "#10B981",    # Emerald
                "PROVEN_RULE": "#2563EB",    # Royal Blue
                "FAILED": "#EF4444",         # Red
                "CYCLE_DETECTED": "#DC2626", # Dark Red
                "EVALUATING": "#F59E0B",     # Amber
                "ROOT": "#6366F1",           # Indigo
            }
            nodes_color.append(color_map.get(node.status, "#94A3B8"))
            nodes_hover.append(f"<b>{node.goal}</b><br>Status: {node.status}<br>Depth: {node.depth}<br>{node.message}")

            if not node.children:
                return

            step_x = spread / max(1, len(node.children))
            start_x = x - (spread / 2) + (step_x / 2)

            for idx, child in enumerate(node.children):
                cx = start_x + (idx * step_x)
                cy = y - 1.0

                edge_x.extend([x, cx, None])
                edge_y.extend([y, cy, None])

                traverse(child, cx, cy, spread * 0.5)

        traverse(root, 0.0, 0.0, 8.0)

        fig = go.Figure()

        # Draw connecting edges
        fig.add_trace(go.Scatter(
            x=edge_x,
            y=edge_y,
            mode="lines",
            line=dict(color="#CBD5E1", width=2),
            hoverinfo="none",
        ))

        # Draw nodes
        fig.add_trace(go.Scatter(
            x=nodes_x,
            y=nodes_y,
            mode="markers+text",
            text=nodes_text,
            textposition="bottom center",
            hoverinfo="text",
            hovertext=nodes_hover,
            marker=dict(
                size=22,
                color=nodes_color,
                line=dict(width=2, color="#FFFFFF"),
            ),
        ))

        fig.update_layout(
            title="Backward Chaining Goal Resolution Tree",
            showlegend=False,
            hovermode="closest",
            xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
            yaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
            template="plotly_white",
            height=480,
            margin=dict(l=20, r=20, t=50, b=20),
        )

        return fig
