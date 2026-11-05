# Dashboard Example

Complex layout with 12-column grid, tabs, cards, and data grids.

## Pattern: Responsive Dashboard

Demonstrates:
- 12-column responsive grid
- Metric cards with statistics
- Tab-based sections
- Data grid with sorting/filtering
- Master layout with toolbar
- Flexible spacing and alignment

## Layout Structure

```
Header (full width)
└── Tabs (full width)
    ├── Overview
    │   └── Grid 12 columns
    │       ├── Metric card (3 cols)
    │       ├── Metric card (3 cols)
    │       ├── Metric card (3 cols)
    │       ├── Metric card (3 cols)
    │       └── Data grid (12 cols)
    ├── Analytics
    │   └── Cards with charts
    └── Settings
        └── Checkboxes, radio groups
```

## Implementation

```eiffel
-- Create 12-column grid
grid := sv.grid_sized (12, 1)
  .gap (10)

-- Add metric card (3 columns)
grid.add_child (create_metric_card ("Users", "1,234"), 3)
grid.add_child (create_metric_card ("Sessions", "456"), 3)
grid.add_child (create_metric_card ("Revenue", "$45K"), 3)
grid.add_child (create_metric_card ("Conversion", "3.4%"), 3)

-- Add data grid (full width - 12 columns)
grid.add_child (create_data_grid, 12)
```

## Key Patterns

1. **12-Column Grid**: Flexible, responsive layout
2. **Cards**: Grouped, themed containers
3. **Tabs**: Section navigation
4. **Data Tables**: Sortable, filterable data
5. **Metric Display**: KPI cards with large text
6. **Responsive Design**: Adapts to window size

## Related Examples

- [layout_patterns](../../LAYOUT_PATTERNS.md) - Grid systems
- [crud_application](../crud_application/) - Complex master-detail

---

**Files:**
- `dashboard.json` - JSON specification
- `screens.svg` - Screen mockups
- `README.md` - This file
