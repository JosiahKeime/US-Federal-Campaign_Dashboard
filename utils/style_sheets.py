COLORS = {
    'primary': '#2c3e50',
    'secondary': '#3498db',
    'accent': '#e74c3c',
    'background': '#ffffff',
    'sidebar_bg': '#f8f9fa',
    'text_primary': '#2c3e50',
    'text_secondary': '#7f8c8d',
    'text_muted': '#95a5a6',
    'border': '#dee2e6',
    'hover': '#e9ecef'
}

# Header styles
HEADER_CONTAINER = {
    'width': '100%',
    'maxHeight': '10%',
    'backgroundColor': '#ecf0f1',
    'padding': 'auto',
    'marginBottom': 'auto',
    'borderBottom': f'3px solid {COLORS["primary"]}'
}

HEADER_TITLE = {
    'textAlign': 'center',
    'color': COLORS['primary'],
    #'margin': '0 0 10px 0',
    'fontSize': '1.5rem',
    #'fontWeight': '600',
    'fontFamily': 'Arial, sans-serif'
}

HEADER_SUBTITLE = {
    'textAlign': 'center',
    'color': COLORS['text_secondary'],
    'fontSize': '1.2rem',
    'margin': '0',
    'fontFamily': 'Arial, sans-serif'
}

FOOTER_CONTAINER = {
    'width': '100%',
    'maxHeight': '10%',
    'backgroundColor': '#ecf0f1',
    #'padding': '25px 20px',
    #'marginTop': '40px',
    'borderTop': f'3px solid {COLORS["primary"]}'
}

# Main container styles
MAIN_CONTAINER = { 
    'minWidth': '100%',
    'maxHeight': '60%',
    'display': 'flex',
    'margin': '0',
    'backgroundColor': COLORS['background']
}

# Sidebar styles
SIDEBAR_CONTAINER = {
    'minWidth': '15%',
    'minHeight': '100%',
    'backgroundColor': COLORS['sidebar_bg'],
    'padding': '5px',
    'borderRight': f'2px solid {COLORS["border"]}',
    'boxShadow': '2px 0 5px rgba(0,0,0,0.1)',
    #'minHeight': '600px'
}

# Map container styles
MAP_CONTAINER = {
    'minWidth': '75%',
    'height': '100%',
    'flex': '1',
    'padding': '0',
    'backgroundColor': COLORS['background']
}

MAP_STYLE = {
    'height': '100%',
    'width': '100%'
}

# Info container
INFO_CONTAINER = {
    'width': '100%',
    'maxHeight': '20%',
    'margin': '10px 5px',
    'padding': '5px',
    'backgroundColor': COLORS['sidebar_bg'],
    'borderRadius': '8px',
    'border': f'1px solid {COLORS["border"]}',
    'boxShadow': '0 2px 8px rgba(0,0,0,0.1)',
    #'height': '500px',
    'overflowY': 'scroll',
    'border': '1px solid #ddd'
}

INFO_TITLE = {
    'color': COLORS['primary'],
    'marginBottom': '5px',
    'fontSize': '1.4rem',
    'fontWeight': '600'
}

# Control group styles
CONTROL_GROUP = {
    'marginBottom': '25px'
}

LABEL_STYLE = {
    'fontWeight': '600',
    'marginBottom': '8px',
    'display': 'block',
    'color': COLORS['text_primary'],
    'fontSize': '14px'
}

DROPDOWN_STYLE = {
    'backgroundColor': COLORS['background'],
    'border': f'1px solid {COLORS["border"]}',
    'borderRadius': '6px',
    'fontSize': '14px'
}

# Footer styles
FOOTER_HR = {
    'border': 'none',
    'height': '1px',
    'backgroundColor': COLORS['border'],
    'margin': '0 0 20px 0'
}

FOOTER_TEXT = {
    'textAlign': 'center',
    'color': COLORS['text_secondary'],
    'margin': '10px 0',
    'fontSize': '14px',
    'fontFamily': 'Arial, sans-serif'
}

FOOTER_SUBTEXT = {
    'textAlign': 'center',
    'color': COLORS['text_muted'],
    'fontSize': '12px',
    'margin': '5px 0',
    'fontFamily': 'Arial, sans-serif'
}
