import pandas as pd
from bokeh.io import output_file
from bokeh.layouts import row
from bokeh.models import (
    ColumnDataSource,
    CustomJS,
    Div,
    HoverTool,
    TapTool,
    WheelZoomTool,
)
from bokeh.plotting import figure, show

# --- 1. Setup Data ---
# Define the categorical risk levels and the numerical exposure range (0-100)
RISK_CATEGORIES = [f"Risk {i}" for i in range(1, 8)]
EXPOSURE_TICKER = list(range(0, 101, 10))

# Data for the 14-segment breakdown with structured table data
segments_data_a = [
    {
        "segment": "Manufacturing A-1",
        "capital": 3000000,
        "risk_level": "Medium",
        "allocation": "15%",
    },
    {
        "segment": "Manufacturing A-2",
        "capital": 6000000,
        "risk_level": "High",
        "allocation": "30%",
    },
    {
        "segment": "Supply Chain A-3",
        "capital": 9000000,
        "risk_level": "Low",
        "allocation": "45%",
    },
    {
        "segment": "Technology A-4",
        "capital": 12000000,
        "risk_level": "Medium",
        "allocation": "60%",
    },
    {
        "segment": "Operations A-5",
        "capital": 15000000,
        "risk_level": "High",
        "allocation": "75%",
    },
    {
        "segment": "Finance A-6",
        "capital": 18000000,
        "risk_level": "Low",
        "allocation": "90%",
    },
    {
        "segment": "Strategic A-7",
        "capital": 21000000,
        "risk_level": "Critical",
        "allocation": "100%",
    },
]
segments_data_b = [
    {
        "segment": "Development B-1",
        "capital": 2000000,
        "risk_level": "Low",
        "allocation": "10%",
    },
    {
        "segment": "Marketing B-2",
        "capital": 4000000,
        "risk_level": "Medium",
        "allocation": "20%",
    },
    {
        "segment": "Sales B-3",
        "capital": 6000000,
        "risk_level": "High",
        "allocation": "30%",
    },
    {
        "segment": "Distribution B-4",
        "capital": 8000000,
        "risk_level": "Medium",
        "allocation": "40%",
    },
    {
        "segment": "Compliance B-5",
        "capital": 10000000,
        "risk_level": "Critical",
        "allocation": "50%",
    },
    {
        "segment": "Research B-6",
        "capital": 12000000,
        "risk_level": "Low",
        "allocation": "60%",
    },
    {
        "segment": "Innovation B-7",
        "capital": 14000000,
        "risk_level": "High",
        "allocation": "70%",
    },
]

# LAYER 1: Square boxes (always visible)
square_source = ColumnDataSource(
    data={
        "x": ["Risk 1", "Risk 1"],
        "y": [8, 18],
        "width": [0.25, 0.25],
        "height": [5, 5],
        "fill_color": ["#3b82f640", "#ef444440"],
        "line_color": ["#3b82f6", "#ef4444"],
        "tooltip_label": ["Focus Area Alpha", "Focus Area Beta"],
        "sector_info": [
            "Lower risk exposure zone - Contains 2 clusters",
            "Higher risk exposure zone - Contains 2 clusters",
        ],
        "alpha": [0.5, 0.5],
        "line_width": [2.0, 2.0],
    }
)

# LAYER 2: Cluster dots (visible at medium zoom) - 4 clusters total
cluster_source = ColumnDataSource(
    data={
        "x": ["Risk 1", "Risk 1", "Risk 1", "Risk 1"],
        "y": [6.8, 9.2, 16.8, 19.2],  # 2 clusters per square
        "label": [
            "Cluster Alpha-1",
            "Cluster Alpha-2",
            "Cluster Beta-1",
            "Cluster Beta-2",
        ],
        "fill_color": ["#3b82f6", "#3b82f6", "#ef4444", "#ef4444"],
        "parent_square": [
            "Alpha (Lower)",
            "Alpha (Lower)",
            "Beta (Higher)",
            "Beta (Higher)",
        ],
        "sector_count": [
            "Contains 2 sectors",
            "Contains 2 sectors",
            "Contains 2 sectors",
            "Contains 2 sectors",
        ],
    }
)

# LAYER 3: Individual sector dots (visible at high zoom) - 8 sectors total
sector_source = ColumnDataSource(
    data={
        "x": [
            "Risk 1",
            "Risk 1",
            "Risk 1",
            "Risk 1",
            "Risk 1",
            "Risk 1",
            "Risk 1",
            "Risk 1",
        ],
        "y": [6.5, 7.1, 8.9, 9.5, 16.5, 17.1, 18.9, 19.5],  # 2 sectors per cluster
        "label": [
            "Sector A-1",
            "Sector A-2",
            "Sector A-3",
            "Sector A-4",
            "Sector B-1",
            "Sector B-2",
            "Sector B-3",
            "Sector B-4",
        ],
        "fill_color": [
            "#000000",
            "#000000",
            "#000000",
            "#000000",
            "#000000",
            "#000000",
            "#000000",
            "#000000",
        ],
        "parent_cluster": [
            "Alpha-1",
            "Alpha-1",
            "Alpha-2",
            "Alpha-2",
            "Beta-1",
            "Beta-1",
            "Beta-2",
            "Beta-2",
        ],
        "parent_square": [
            "Alpha",
            "Alpha",
            "Alpha",
            "Alpha",
            "Beta",
            "Beta",
            "Beta",
            "Beta",
        ],
        "segment_breakdown": [
            segments_data_a,
            segments_data_b,
            segments_data_a,
            segments_data_b,
            segments_data_a,
            segments_data_b,
            segments_data_a,
            segments_data_b,
        ],
    }
)


# --- 2. Create Plot and Elements ---

p = figure(
    x_range=RISK_CATEGORIES,
    y_range=(0, 100),
    height=550,
    width=800,
    title="Interactive Risk Exposure Matrix: Multi-Layer Zoom View",
    tools="pan,save,reset,hover,tap",  # Removed wheel_zoom to add custom one
    toolbar_location="above",
    background_fill_color="#f5f7fa",
)

# Customize axes and grid
p.yaxis.axis_label = "exposure %"
p.yaxis.major_label_text_color = None
p.yaxis.major_tick_line_color = None
p.yaxis.minor_tick_line_color = None

p.xaxis.axis_label = "Risk Category"
p.y_range.bounds = (0, 100)

# Remove y-axis grid lines
p.ygrid.grid_line_color = None
p.grid.grid_line_color = "#e0e0e0"

# Add custom wheel zoom with faster speed
wheel_zoom = WheelZoomTool(
    zoom_on_axis=False,  # Zoom on both axes
    speed=0.002,  # Default is 0.0005, higher = faster zoom (try 0.002-0.005)
)
p.add_tools(wheel_zoom)
p.toolbar.active_scroll = wheel_zoom  # Make it the active scroll tool

# LAYER 1: Draw squares (always visible)
r = p.rect(
    x="x",
    y="y",
    width="width",
    height="height",
    source=square_source,
    fill_color="fill_color",
    line_color="line_color",
    fill_alpha="alpha",
    line_width="line_width",
    legend_label="Focus Areas",
)

p.add_tools(
    HoverTool(
        renderers=[r],
        tooltips=[
            ("Area", "@tooltip_label"),
            ("Info", "@sector_info"),
        ],
        mode="mouse",
    )
)

# LAYER 2: Draw cluster dots (medium zoom visibility)
clusters = p.circle(
    x="x",
    y="y",
    size=15,
    source=cluster_source,
    fill_color="fill_color",
    line_color="white",
    line_width=2,
    legend_label="Clusters",
    name="clusters",
    alpha=0,  # Start invisible
    visible=True,
)

p.add_tools(
    HoverTool(
        renderers=[clusters],
        tooltips=[
            ("Cluster", "@label"),
            ("Parent", "@parent_square"),
            ("Details", "@sector_count"),
        ],
        point_policy="snap_to_data",
        mode="mouse",
    )
)

# LAYER 3: Draw sector dots (high zoom visibility)
sectors = p.circle(
    x="x",
    y="y",
    size=8,
    source=sector_source,
    fill_color="fill_color",
    line_color="white",
    line_width=1,
    legend_label="Sectors",
    name="sectors",
    alpha=0,  # Start invisible
    visible=True,
)

p.add_tools(
    HoverTool(
        renderers=[sectors],
        tooltips=[
            ("Sector", "@label"),
            ("Cluster", "@parent_cluster"),
            ("Area", "@parent_square"),
            ("Action", "Click for breakdown"),
        ],
        point_policy="snap_to_data",
        mode="mouse",
    )
)


# --- 3. Implement Zoom-Based Visibility ---

zoom_callback = CustomJS(
    args=dict(clusters_renderer=clusters, sectors_renderer=sectors, y_range=p.y_range),
    code="""
    // Get the current y-axis range span (zoom level indicator)
    const y_span = y_range.end - y_range.start;
    
    // Define zoom thresholds
    const CLUSTER_THRESHOLD = 60;  // Show clusters when zoomed to < 60% of y-axis
    const SECTOR_THRESHOLD = 30;   // Show sectors when zoomed to < 30% of y-axis
    
    // Calculate opacity based on zoom level
    let cluster_alpha = 0;
    let sector_alpha = 0;
    
    if (y_span < CLUSTER_THRESHOLD) {
        // Fade in clusters as you zoom past threshold
        cluster_alpha = Math.min(1, (CLUSTER_THRESHOLD - y_span) / 20);
    }
    
    if (y_span < SECTOR_THRESHOLD) {
        // Fade in sectors as you zoom past threshold
        sector_alpha = Math.min(1, (SECTOR_THRESHOLD - y_span) / 15);
    }
    
    // Update the alpha (visibility) of each layer
    clusters_renderer.glyph.fill_alpha = cluster_alpha;
    clusters_renderer.glyph.line_alpha = cluster_alpha;
    
    sectors_renderer.glyph.fill_alpha = sector_alpha;
    sectors_renderer.glyph.line_alpha = sector_alpha;
""",
)

# Attach zoom callback to range changes
p.y_range.js_on_change("start", zoom_callback)
p.y_range.js_on_change("end", zoom_callback)


# --- 4. Implement Click-to-Table (for Layer 3 sectors only) ---

breakdown_div = Div(
    text="""
    <div style="
        background: #ffffff;
        padding: 20px;
        border-radius: 12px;
        box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.1), 0 4px 6px -4px rgba(0, 0, 0, 0.1);
        min-width: 320px;
        font-family: Inter, sans-serif;
        border: 2px solid #e0e7ff;
    ">
        <h3 style="font-size: 1.5rem; font-weight: 700; color: #1e40af; margin-bottom: 12px;">Segment Breakdown</h3>
        <p style="color: #6b7280; font-size: 0.95rem;">
            <strong>Zoom in</strong> to reveal clusters and sectors.<br/>
            Click on any <strong>Sector</strong> dot to see detailed breakdown table.
        </p>
    </div>
    """,
    sizing_mode="fixed",
    width=400,
    height=500,
)

js_code = """
const data = sector_source.data;
const indices = cb_data.source.selected.indices;
const div = breakdown_div.child_views[0].el; 

if (indices.length > 0) {
    const index = indices[0];
    const sector = data['label'][index];
    const segments = data['segment_breakdown'][index];
    
    let totalCapital = 0;
    if (Array.isArray(segments)) {
        segments.forEach(seg => totalCapital += seg.capital);
    }

    let html_content = `
    <div style="background: #ffffff; padding: 20px; border-radius: 12px; box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.1); font-family: Inter, sans-serif; border: 2px solid #e0e7ff;">
        <h3 style="font-size: 1.5rem; font-weight: 700; color: #1e40af; margin-bottom: 12px;">
            ${sector} - Detailed Breakdown
        </h3>
        <p style="color: #6b7280; font-size: 0.9rem; margin-bottom: 16px;">
            Total Capital at Risk: <strong>$${(totalCapital/1000000).toFixed(1)}M USD</strong>
        </p>
        
        <table style="width: 100%; border-collapse: collapse; font-size: 0.85rem;">
            <thead>
                <tr style="background: #f8fafc; border-bottom: 2px solid #e2e8f0;">
                    <th style="text-align: left; padding: 8px 6px; font-weight: 600; color: #374151;">Segment</th>
                    <th style="text-align: right; padding: 8px 6px; font-weight: 600; color: #374151;">Capital ($M)</th>
                    <th style="text-align: center; padding: 8px 6px; font-weight: 600; color: #374151;">Risk Level</th>
                    <th style="text-align: right; padding: 8px 6px; font-weight: 600; color: #374151;">Allocation</th>
                </tr>
            </thead>
            <tbody>`;
    
    if (Array.isArray(segments)) {
        segments.forEach((segment, i) => {
            let riskColor = '#6b7280';
            if (segment.risk_level === 'Low') riskColor = '#10b981';
            else if (segment.risk_level === 'Medium') riskColor = '#f59e0b';
            else if (segment.risk_level === 'High') riskColor = '#dc2626';
            else if (segment.risk_level === 'Critical') riskColor = '#7c2d12';
            
            const rowBg = i % 2 === 0 ? '#ffffff' : '#f9fafb';
            
            html_content += `
                <tr style="background: ${rowBg}; border-bottom: 1px solid #e5e7eb;">
                    <td style="padding: 6px; color: #1f2937; font-weight: 500;">${segment.segment}</td>
                    <td style="padding: 6px; text-align: right; color: #1f2937;">$${(segment.capital/1000000).toFixed(1)}</td>
                    <td style="padding: 6px; text-align: center;">
                        <span style="background: ${riskColor}20; color: ${riskColor}; padding: 2px 6px; border-radius: 4px; font-size: 0.75rem; font-weight: 600;">
                            ${segment.risk_level}
                        </span>
                    </td>
                    <td style="padding: 6px; text-align: right; color: #6b7280;">${segment.allocation}</td>
                </tr>
            `;
        });
    }

    html_content += `
            </tbody>
        </table>
    </div>`;
    
    div.innerHTML = html_content;
    
    setTimeout(() => {
        cb_data.source.selected.indices = [];
        cb_data.source.change.emit();
    }, 500);

} else {
    div.innerHTML = `
        <div style="background: #ffffff; padding: 20px; border-radius: 12px; box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.1); min-width: 320px; font-family: Inter, sans-serif; border: 2px solid #e0e7ff;">
            <h3 style="font-size: 1.5rem; font-weight: 700; color: #1e40af; margin-bottom: 12px;">Segment Breakdown</h3>
            <p style="color: #6b7280; font-size: 0.95rem;">
                <strong>Zoom in</strong> to reveal clusters and sectors.<br/>
                Click on any <strong>Sector</strong> dot to see detailed breakdown table.
            </p>
        </div>
    `;
}
"""

callback = CustomJS(
    args=dict(sector_source=sector_source, breakdown_div=breakdown_div), code=js_code
)
sectors.js_on_event("tap", callback)


# --- 5. Layout and Output ---

plot_layout = row(p, breakdown_div, sizing_mode="scale_width")

output_file("risk_exposure_analysis.html", title="Interactive Risk Exposure Plot")
show(plot_layout)
