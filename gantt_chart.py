from dataclasses import dataclass
from pathlib import Path
from typing import List

SVG_WIDTH = 1300
SVG_HEIGHT = 720
LEFT_MARGIN = 200
RIGHT_MARGIN = 60
TOP_MARGIN = 80
BOTTOM_MARGIN = 80
WEEK_COUNT = 13
ROW_HEIGHT = 42
ROW_GAP = 8
TITLE = "DENIM PRODUCTION CRITICAL PATH (12 WEEKS CYCLE)"


@dataclass
class Task:
    name: str
    start_week: float
    duration: float
    color: str

    @property
    def end_week(self) -> float:
        return self.start_week + self.duration


TASKS: List[Task] = [
    Task("Final Inspection & Ex-Factory", 11.5, 0.5, "#e74c3c"),
    Task("Finishing & Packaging", 10.5, 1, "#34495e"),
    Task("Shadeband Approval", 10, 0.5, "#f39c12"),
    Task("Washing Process", 8.5, 2, "#3498db"),
    Task("Inline Inspection", 8, 0.5, "#2ecc71"),
    Task("Production Start (Sewing)", 6.5, 2, "#3498db"),
    Task("Cutting & Risk Review", 6, 0.5, "#95a5a6"),
    Task("Fabric & Trims In-house", 4, 1, "#8e44ad"),
    Task("PP Sample Approval", 5, 1, "#e67e22"),
    Task("Size Set Sample", 3.5, 1, "#95a5a6"),
    Task("Fit Sample", 2, 1.5, "#95a5a6"),
    Task("Fabric Booking", 1.5, 0.5, "#95a5a6"),
    Task("Development Sample", 0, 1.5, "#95a5a6"),
]


def _week_to_x(week: float) -> float:
    usable_width = SVG_WIDTH - LEFT_MARGIN - RIGHT_MARGIN
    return LEFT_MARGIN + (week / WEEK_COUNT) * usable_width


def _svg_header() -> str:
    return (
        f"<svg xmlns='http://www.w3.org/2000/svg' width='{SVG_WIDTH}' height='{SVG_HEIGHT}' "
        f"viewBox='0 0 {SVG_WIDTH} {SVG_HEIGHT}'>\n"
        "  <style>"
        "    .title { font: bold 20px sans-serif; fill: #111; }"
        "    .label { font: 13px sans-serif; fill: #333; }"
        "    .task { rx: 6; ry: 6; stroke: #fff; stroke-width: 1.5; }"
        "    .duration { font: bold 11px sans-serif; fill: #fff; }"
        "  </style>\n"
    )


def _draw_grid() -> str:
    lines = []
    usable_height = SVG_HEIGHT - TOP_MARGIN - BOTTOM_MARGIN
    for week in range(WEEK_COUNT + 1):
        x = _week_to_x(week)
        lines.append(
            f"  <line x1='{x:.2f}' y1='{TOP_MARGIN}' x2='{x:.2f}' y2='{TOP_MARGIN + usable_height}' "
            "stroke='#e0e0e0' stroke-dasharray='4 4' />\n"
        )
        lines.append(
            f"  <text x='{x:.2f}' y='{SVG_HEIGHT - BOTTOM_MARGIN / 2:.2f}' class='label' text-anchor='middle'>Week {week}</text>\n"
        )
    return "".join(lines)


def _draw_tasks() -> str:
    blocks = []
    y = TOP_MARGIN
    for task in TASKS:
        bar_y = y
        bar_height = ROW_HEIGHT
        x_start = _week_to_x(task.start_week)
        x_end = _week_to_x(task.end_week)
        bar_width = x_end - x_start

        blocks.append(
            f"  <rect class='task' x='{x_start:.2f}' y='{bar_y:.2f}' width='{bar_width:.2f}' height='{bar_height}' "
            f"fill='{task.color}' opacity='0.9' />\n"
        )
        blocks.append(
            f"  <text x='{x_start - 12:.2f}' y='{bar_y + bar_height / 2 + 4:.2f}' class='label' text-anchor='end'>{task.name}</text>\n"
        )
        blocks.append(
            f"  <text x='{x_start + bar_width / 2:.2f}' y='{bar_y + bar_height / 2 + 4:.2f}' class='duration' text-anchor='middle'>{task.duration}w</text>\n"
        )
        y += ROW_HEIGHT + ROW_GAP
    return "".join(blocks)


def create_custom_gantt(output_path: Path = Path("custom_critical_path.svg")) -> Path:
    """Create a lightweight SVG Gantt chart without third-party dependencies."""
    content = [
        _svg_header(),
        f"  <text x='{LEFT_MARGIN}' y='{TOP_MARGIN - 30}' class='title'>{TITLE}</text>\n",
        _draw_grid(),
        _draw_tasks(),
        "</svg>\n",
    ]
    output_path.write_text("".join(content), encoding="utf-8")
    return output_path


def create_test_plot(output_path: Path = Path("test_plot.svg")) -> Path:
    """Create a tiny SVG line plot as a sanity check."""
    start_x = LEFT_MARGIN
    start_y = TOP_MARGIN
    width = SVG_WIDTH - LEFT_MARGIN - RIGHT_MARGIN
    height = 220

    points = [
        (0, height - 20),
        (width * 0.5, height * 0.2),
        (width, height - 40),
    ]

    svg = [
        _svg_header(),
        f"  <text x='{start_x}' y='{start_y - 30}' class='title'>Test Plot</text>\n",
        f"  <polyline fill='none' stroke='#2980b9' stroke-width='3' "
        f"points='{start_x},{start_y + points[0][1]} {start_x + points[1][0]},{start_y + points[1][1]} "
        f"{start_x + points[2][0]},{start_y + points[2][1]}' />\n",
        f"  <line x1='{start_x}' y1='{start_y + height}' x2='{start_x + width}' y2='{start_y + height}' stroke='#555' />\n",
        f"  <line x1='{start_x}' y1='{start_y}' x2='{start_x}' y2='{start_y + height}' stroke='#555' />\n",
        f"  <text x='{start_x + width / 2}' y='{start_y + height + 30}' class='label' text-anchor='middle'>X</text>\n",
        f"  <text x='{start_x - 20}' y='{start_y + height / 2}' class='label' text-anchor='end' transform='rotate(-90 {start_x - 20},{start_y + height / 2})'>Y</text>\n",
        "</svg>\n",
    ]

    output_path.write_text("".join(svg), encoding="utf-8")
    return output_path


if __name__ == "__main__":
    chart_path = create_custom_gantt()
    print(f"Saved Gantt chart to {chart_path.resolve()}")

    test_plot_path = create_test_plot()
    print(f"Saved test plot to {test_plot_path.resolve()}")
