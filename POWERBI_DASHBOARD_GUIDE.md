# Power BI Dashboard Creation Guide
## Sentiment Intelligence System — Dynamic Visualization Dashboard

---

## Part 1: Prerequisites

1. ✓ **Power BI Desktop** installed (download from [powerbi.microsoft.com](https://powerbi.microsoft.com))
2. ✓ **API running** — Start it with: `cd api && python app.py`
3. ✓ **CSV file ready**: `api/predictions_log.csv`
4. ✓ (Optional) **Word Cloud** custom visual from AppSource

---

## Part 2: Import Data into Power BI

### Step 1: Open Power BI Desktop
- Launch **Power BI Desktop** on your computer

### Step 2: Load the CSV File
1. Click **Home** tab → **Get Data** → **Text/CSV**
2. Navigate to:
   ```
   C:\Users\Asus\OneDrive\Desktop\STUDY\2nd SEM\LAB PRACTICE - II\Assignment 1\Sentiment-Intelligence-System\api\predictions_log.csv
   ```
3. Click **Load**

### Step 3: Transform Data in Power Query
1. After loading, click **Transform Data** to open Power Query Editor
2. **Fix Timestamp Column:**
   - Select the `timestamp` column
   - Click **Data Type** → change to **Date/Time**
3. **Add Date Column (for slicing):**
   - Select `timestamp` → Right-click → **Duplicate Column**
   - Rename to `Date`
   - Change Data Type to **Date** (strips out time)
4. **Add Hour Column (for time-of-day analysis):**
   - Go to **Add Column** → **Custom Column**
   - Name: `Hour`
   - Formula: `Time.Hour([timestamp])`
5. **Add Sentiment Score Column (numeric):**
   - Go to **Add Column** → **Conditional Column**
   - Name: `sentiment_score`
   - If `sentiment` equals `Positive` then output `1`, else output `0`
6. **Add Confidence Category Column:**
   - Go to **Add Column** → **Conditional Column**
   - Name: `confidence_category`
   - If `confidence` >= 0.8 then `High Confidence`
   - Else if `confidence` >= 0.5 then `Medium Confidence`
   - Else `Low Confidence`
7. **Add Word Count Bucket Column:**
   - Go to **Add Column** → **Conditional Column**
   - Name: `length_bucket`
   - If `review_length` <= 5 then `Short (1-5)`
   - Else if `review_length` <= 10 then `Medium (6-10)`
   - Else `Long (11+)`
8. Click **Close & Apply**

---

## Part 3: Create DAX Measures (for dynamic KPIs)

Click on **Model** view, then create these measures:

### Essential DAX Measures
```dax
-- 1. Total Reviews Count
Total Reviews = COUNTROWS(predictions_log)

-- 2. Positive Count
Positive Count = CALCULATE(COUNTROWS(predictions_log), predictions_log[sentiment] = "Positive")

-- 3. Negative Count
Negative Count = CALCULATE(COUNTROWS(predictions_log), predictions_log[sentiment] = "Negative")

-- 4. Positive Percentage
Positive % = DIVIDE([Positive Count], [Total Reviews], 0) * 100

-- 5. Negative Percentage
Negative % = DIVIDE([Negative Count], [Total Reviews], 0) * 100

-- 6. Average Confidence Score
Avg Confidence = AVERAGE(predictions_log[confidence])

-- 7. Average Review Length
Avg Review Length = AVERAGE(predictions_log[review_length])

-- 8. Sentiment Ratio (Positive/Negative)
Sentiment Ratio = DIVIDE([Positive Count], [Negative Count], 0)
```

---

## Part 4: Add SLICERS (Dynamic Filtering)

Slicers make your dashboard **interactive and dynamic** — users can filter all visuals at once.

### Slicer 1: Sentiment Filter (Dropdown)
1. Go to **Home** → **Visualizations** pane → Click **Slicer** icon
2. Drag `sentiment` field into the slicer
3. Click the ▼ arrow on the slicer → Select **Dropdown** style
4. **Format:**
   - Title: "Filter by Sentiment"
   - Background: Light gray
   - Selection: Single select or Multi-select (your preference)

### Slicer 2: Date Range Slicer (Between)
1. Insert another **Slicer**
2. Drag `Date` field into the slicer
3. It will auto-detect as a date slicer with a **slider**
4. Click the ▼ → Choose **Between** style (shows start & end date pickers)
5. **Format:**
   - Title: "Select Date Range"
   - This allows filtering reviews by time period

### Slicer 3: Confidence Level Filter (Dropdown)
1. Insert another **Slicer**
2. Drag `confidence_category` field into the slicer
3. Click the ▼ → Select **Dropdown**
4. **Format:**
   - Title: "Confidence Level"
   - Users can filter by High / Medium / Low confidence predictions

### Slicer 4: Review Length Bucket (Buttons)
1. Insert another **Slicer**
2. Drag `length_bucket` field into the slicer
3. Click the ▼ → Select **Tile** style (shows as clickable buttons)
4. **Format:**
   - Title: "Review Length"
   - Layout: Horizontal
   - Users can filter by Short / Medium / Long reviews

### Slicer Placement
```
┌──────────┬──────────┬────────────┬───────────┐
│Sentiment │Date Range│Confidence  │Rev. Length │
│ Dropdown │ Between  │  Dropdown  │  Buttons  │
└──────────┴──────────┴────────────┴───────────┘
```

### Configure Slicer Interactions
1. Select a slicer → Go to **Format** tab → **Edit Interactions**
2. For each other visual, choose:
   - **Filter** (funnel icon) — slicer filters this visual ✅
   - **None** — slicer doesn't affect this visual
3. Ensure all slicers affect all charts for full interactivity

---

## Part 5: Create Visualizations

### 5A: KPI Cards Row (Key Metrics)

Create **4 Card visuals** across the top:

#### Card 1 — Total Reviews
1. **Insert** → **Card** visual
2. Drag `Total Reviews` measure into Value
3. Format: Title = "Total Reviews", Font size = 28

#### Card 2 — Positive %
1. **Insert** → **Card** visual
2. Drag `Positive %` measure into Value
3. Format: Title = "Positive %", Color = Green, Font size = 28

#### Card 3 — Negative %
1. **Insert** → **Card** visual
2. Drag `Negative %` measure into Value
3. Format: Title = "Negative %", Color = Red, Font size = 28

#### Card 4 — Average Confidence
1. **Insert** → **Card** visual
2. Drag `Avg Confidence` measure into Value
3. Format: Title = "Avg Confidence", Data label format = Percentage

---

### 5B: Gauge Chart (Sentiment Health Score)

1. **Insert** → **Gauge** visual
2. Configure:
   - **Value**: `Positive %` measure
   - **Minimum**: 0
   - **Maximum**: 100
   - **Target**: 70 (or your desired goal)
3. Format:
   - Title: "Sentiment Health Score"
   - Gauge axis → Color bands:
     - 0–40: Red (Poor sentiment)
     - 40–70: Yellow (Average sentiment)
     - 70–100: Green (Good sentiment)
   - Data labels: Show
4. This gauge responds to **all slicers** — it dynamically updates!

---

### 5C: Donut Chart (Sentiment Distribution)

1. **Insert** → **Donut Chart**
2. Configure:
   - **Legend**: `sentiment`
   - **Values**: `Total Reviews` measure (or Count of `review`)
3. Format:
   - Title: "Sentiment Distribution"
   - Colors: Positive = `#2ecc71` (Green), Negative = `#e74c3c` (Red)
   - Data labels: Show Category + Percentage
   - Inner radius: 60%
4. **Why Donut over Pie**: Donut charts are more modern and leave room for a center label

---

### 5D: Line Chart (Sentiment Trend Over Time)

1. **Insert** → **Line Chart**
2. Configure:
   - **X-Axis**: `timestamp` (set to Day or Hour granularity)
   - **Y-Axis**: `Avg Confidence` measure
   - **Legend**: `sentiment` (creates separate lines for Positive/Negative)
3. Format:
   - Title: "Sentiment Confidence Trend Over Time"
   - X-axis label: "Date"
   - Y-axis: Min = 0, Max = 1, Label = "Confidence Score"
   - Line colors: Positive = Green, Negative = Red
   - Show data points: Yes
   - Enable **Forecast** (Analytics pane → Forecast → Add) for trend prediction

---

### 5E: Clustered Bar Chart (Sentiment Count)

1. **Insert** → **Clustered Bar Chart**
2. Configure:
   - **Y-Axis**: `sentiment`
   - **X-Axis**: Count of `review`
   - **Legend**: `confidence_category`
3. Format:
   - Title: "Sentiment Count by Confidence Level"
   - Colors: High = Dark Blue, Medium = Medium Blue, Low = Light Blue
   - Data labels: Show values
   - Sort: Descending by count

---

### 5F: Histogram (Confidence Score Distribution)

1. **Insert** → **Clustered Column Chart**
2. Configure:
   - **X-Axis**: `confidence` (binned — see step below)
   - **Y-Axis**: Count of `review`
3. To create bins:
   - Go to **Data** view → Right-click `confidence` field
   - Select **New Group** → Bin type = **Bin**, Bin size = `0.1`
4. Format:
   - Title: "Confidence Score Distribution"
   - Gradient colors from Red (0) to Green (1)
   - Data labels: Show

---

### 5G: Word Cloud (Top Words in Reviews)

> ⚠️ Word Cloud is a **custom visual** — install it from AppSource first

#### Install Word Cloud:
1. In Visualizations pane → Click **"..."** (three dots) → **Get more visuals**
2. Search for **"Word Cloud"** → Click **Add**

#### Create Word Cloud:
1. Insert the **Word Cloud** visual
2. Drag `review` field into **"Category"**
3. Format:
   - Title: "Most Frequent Words in Reviews"
   - Max number of words: 50
   - **Stop words**: Enable → Add common words: `the, a, an, is, it, to, and, of, in, for, was, this, that, i, my, we, you, they, are`
   - Rotation: Some rotation for visual appeal
   - Colors: Use theme colors or sentiment-based colors
4. **Pro Tip**: Duplicate the word cloud, use **Edit Interactions** to link one to Positive slicer and another to Negative — see which words associate with each sentiment!

---

### 5H: Table Visual (Detailed Review Log)

1. **Insert** → **Table**
2. Add columns: `timestamp`, `review`, `sentiment`, `confidence`, `review_length`
3. Format:
   - Title: "Recent Predictions Log"
   - Sort by `timestamp` descending (newest first)
   - **Conditional formatting** on `sentiment` column:
     - Right-click `sentiment` column header → **Conditional Formatting** → **Background color**
     - Rules: If value is "Positive" → Green background
     - If value is "Negative" → Red background
   - **Conditional formatting** on `confidence`:
     - Right-click → **Conditional Formatting** → **Data bars**
     - Color: Blue gradient
   - Column widths: Review = wider, others = compact
   - Style: Alternating rows

---

### 5I: Stacked Area Chart (Cumulative Sentiment Over Time)

1. **Insert** → **Stacked Area Chart**
2. Configure:
   - **X-Axis**: `Date`
   - **Y-Axis**: Count of `review`
   - **Legend**: `sentiment`
3. Format:
   - Title: "Cumulative Sentiment Over Time"
   - Colors: Positive = Green (transparent), Negative = Red (transparent)
   - This shows how the volume of reviews by sentiment accumulates over time

---

### 5J: Scatter Plot (Confidence vs Review Length)

1. **Insert** → **Scatter Chart**
2. Configure:
   - **X-Axis**: `review_length`
   - **Y-Axis**: `confidence`
   - **Legend**: `sentiment`
   - **Size**: Fixed
3. Format:
   - Title: "Confidence vs Review Length"
   - Colors: Positive = Green, Negative = Red
   - X-axis label: "Word Count"
   - Y-axis label: "Confidence Score"
   - This reveals if shorter/longer reviews have different confidence patterns

---

## Part 6: Dashboard Layout

### Recommended Layout (3-Page Dashboard)

#### Page 1: Overview Dashboard
```
┌──────────────────────────────────────────────────────────────────┐
│ 🔶 SLICERS ROW                                                  │
│ [Sentiment ▼] [Date Range ━━━━━] [Confidence ▼] [Length: S|M|L] │
├──────────┬──────────┬──────────┬───────────────────────────────── │
│ Card:    │ Card:    │ Card:    │ Card:                           │
│ Total    │ Positive │ Negative │ Avg                             │
│ Reviews  │   %      │   %      │ Confidence                     │
├──────────┴──────────┼──────────┴──────────────────────────────── │
│  Gauge Chart        │  Donut Chart                               │
│  (Sentiment Health) │  (Sentiment Distribution)                  │
├─────────────────────┴──────────────────────────────────────────── │
│  Line Chart (Sentiment Confidence Trend)                         │
└──────────────────────────────────────────────────────────────────┘
```

#### Page 2: Deep Analysis
```
┌──────────────────────────────────────────────────────────────────┐
│ [Sentiment ▼] [Date Range ━━━━━]                                │
├─────────────────────┬────────────────────────────────────────── │
│  Bar Chart          │  Word Cloud                               │
│  (Sentiment by      │  (Top Keywords)                           │
│   Confidence Level) │                                           │
├─────────────────────┼──────────────────────────────────────────── │
│  Histogram          │  Scatter Plot                             │
│  (Confidence        │  (Confidence vs                           │
│   Distribution)     │   Review Length)                          │
└─────────────────────┴──────────────────────────────────────────┘
```

#### Page 3: Review Details
```
┌──────────────────────────────────────────────────────────────────┐
│ [Sentiment ▼] [Date Range ━━━━━] [Confidence ▼]                 │
├──────────────────────────────────────────────────────────────────│
│  Stacked Area Chart (Cumulative Sentiment Over Time)             │
├──────────────────────────────────────────────────────────────────│
│  Table (Full Prediction Log with conditional formatting)         │
│  timestamp | review | sentiment | confidence | review_length     │
└──────────────────────────────────────────────────────────────────┘
```

---

## Part 7: Sync Slicers Across Pages

1. Go to **View** tab → Enable **Sync Slicers** pane
2. For each slicer:
   - Check which pages it should appear on (all 3 pages)
   - Check which pages it should filter (all 3 pages)
3. This ensures when you switch pages, your filters stay applied!

---

## Part 8: Apply Theme and Polish

### Set Professional Theme
1. Go to **View** → **Themes**
2. Choose a dark or professional theme (e.g., "Executive", "Innovation", or "City park")
3. Or create custom theme JSON:
   ```json
   {
     "name": "Sentiment Dashboard",
     "dataColors": ["#2ecc71", "#e74c3c", "#3498db", "#f39c12", "#9b59b6"],
     "background": "#f8f9fa",
     "foreground": "#2c3e50"
   }
   ```
4. **File** → **Import Theme** → Select your JSON file

### Add Title
1. **Insert** → **Text Box**
2. Type: **"Sentiment Intelligence Dashboard"**
3. Font: Segoe UI Bold, Size: 22, Color: Dark

### Add Company Logo / Branding (Optional)
1. **Insert** → **Image** → Select your logo
2. Place in top-left corner

---

## Part 9: Save and Publish

### Save Locally:
1. Click **File** → **Save As**
2. Name: `Sentiment_Dashboard.pbix`
3. Location: `Sentiment-Intelligence-System` folder

### Publish to Cloud (Optional):
1. Click **File** → **Publish** → **Publish to Power BI**
2. Select your workspace
3. Share dashboard link with team

---

## Part 10: Real-Time Updates

### Manual Refresh:
- Click **Refresh** button (top ribbon) to reload CSV data

### Auto-Refresh (Power BI Service):
1. Publish to Power BI Service
2. Go to **Dataset Settings** → **Scheduled Refresh**
3. Set refresh frequency (e.g., every 30 minutes)

### Live Connection to API:
1. Use **Web connector**: Home → Get Data → Web
2. Enter: `http://127.0.0.1:8000/analytics/summary`
3. Power BI will fetch real-time data from the API endpoint

---

## Troubleshooting

| Issue | Solution |
|-------|----------|
| Data not showing | Re-import CSV, check file path |
| Timestamp not recognized | Change data type to Date/Time in Power Query |
| Charts look blank | Verify fields are in correct areas (Values, Axis, Legend) |
| Slicers not filtering | Check Edit Interactions — ensure Filter mode is on |
| Word Cloud not available | Install from AppSource: Visualizations → ... → Get more visuals |
| Gauge not moving | Check that the Value is a measure, not a column |
| DAX measure errors | Ensure table name matches exact name (case-sensitive) |
| Cross-filter not working | Select visual → Format → Edit Interactions → Enable |

---

## Summary: Visualization Checklist

| # | Visual Type | Purpose | Data Fields |
|---|-------------|---------|-------------|
| 1 | **Slicer (Dropdown)** | Filter by Sentiment | `sentiment` |
| 2 | **Slicer (Between)** | Filter by Date Range | `Date` |
| 3 | **Slicer (Dropdown)** | Filter by Confidence Level | `confidence_category` |
| 4 | **Slicer (Tile)** | Filter by Review Length | `length_bucket` |
| 5 | **Card** (×4) | KPI metrics | Total, Positive%, Negative%, Avg Confidence |
| 6 | **Gauge** | Sentiment Health Score | `Positive %`, target = 70 |
| 7 | **Donut Chart** | Sentiment Distribution | `sentiment`, Count of `review` |
| 8 | **Line Chart** | Confidence Trend Over Time | `timestamp`, `Avg Confidence`, `sentiment` |
| 9 | **Clustered Bar** | Sentiment by Confidence Level | `sentiment`, `confidence_category` |
| 10 | **Column Chart** | Confidence Histogram | `confidence` (binned), Count |
| 11 | **Word Cloud** | Top Keywords | `review` text |
| 12 | **Table** | Detailed Review Log | All fields with conditional formatting |
| 13 | **Stacked Area** | Cumulative Sentiment Over Time | `Date`, `sentiment`, Count |
| 14 | **Scatter Plot** | Confidence vs Review Length | `review_length`, `confidence`, `sentiment` |

---

**Last Updated**: 2026-03-10
**Author**: Kashyap Barad — Lab Practice II (2026)
**Status**: Ready for Dashboard Creation ✅
