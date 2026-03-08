## [0.3.0] - 2026-03-08

### Added

- New AI page with chatbot, visualizations, displayed data, and option to download filtered data (PRs #58, #59, #62, #63 #65)

### Changed

- Added KPI comparisons for Average Min + Max Temperatures and Air Pressure
- Updated default dashboard view to show current terrestrial month compared over the years
- Both of these changes address Ilya's feedback per Issue #57 and are merged in PR #64

### Fixed

- There were no known bugs going into this milestone
- Addressed TA feedback (Issue #56) by justifying choice of dropdown filter for Seasons

### Known Issues/Usage Notes

- Default filter: The dashboard defaults to the most recent terrestrial month rather than the current day since weather data is seasonal and month-level periods provide a more stable view of trends.
- KPI comparisons: KPIs compare the selected period with the same calendar period in the previous year to provide a seasonal baseline. A comparison is not included for Std Air Pressure since variability metrics are less meaningful for quick year-over-year comparison.
- Since the filters on the first page of the dashboard are reactive to each other, the user will need hit the "Reset" button in order to be able to change the Martian Month and Season filters.

### Reflection

Most importantly, at this stage, our dashboard does a very good job of addressing each of the Job Stories that we defined during Milestone 1 and revised in Milestone 2. In particular, including the comparison visualizations between Air Pressure and Temperature on both the first page and the AI page are useful for addressing Job Story #3. Furthermore, the time series plots are useful to address Job Story #4. The updated KPIs with comparisons are helpful for Job Stories #1 and #2. Alongside this, we were careful to maintain consistent style choices across the dashboard and visualizations as laid out in the visualization best practices that we learned in DSCI 531.

While the addition of the Chat Bot feature does not directly address any of our Job Stories it will be useful for users who are less familiar with the particular schema of our dataset. Furthermore, the data download option will allow the user to explore the underlying data further, should they have questions not currently being addressed by the dashboard. If this were a real-world product, we would want to set up a way to record and gather feedback from users to see what they are querying often or seeking to uncover in the exported data. That way we could update and upgrade the dashboard to better address user needs.

## [0.2.0] - 2026-02-27

### Added

- Season-based filtering (in addition to Martian month) to support broader time-period exploration.
- “Recent data” control to view the most recent segment of the historical dataset.
- Time-window filtering via terrestrial date control.
- KPI cards computed from the filtered dataset: average min temp, average max temp, average pressure, and pressure standard deviation.
- Core plots driven by the same filtered dataset: pressure vs min temp, pressure vs max temp, temperature time series, and pressure time series.

### Changed

- Job Story #1 revised from “filter by Martian months” to “filter by months or seasons” to better match planning needs across broader periods.
- Job Story #2 revised from “current” to “recent” to reflect the historical nature of the dataset rather than real-time telemetry.
- Filtering logic consolidated into a single `filtered_df` reactive used consistently across KPIs and plots.

### Fixed

- Filters were not correctly tied to KPI cards and graphs, which caused NA displays; this is now fixed.

### Known Issues

- Some plots are not very informative and can look odd for certain filter selections (flat, sparse, or visually misleading due to small sample sizes or axis scaling); workaround: broaden the date range or reset filters; planned fix: revise aggregations and add empty or low-data guards.

### Reflection

#### Implementation Status

- Fully implemented job stories:
  - #1 (revised): month/season filtering for temperature and pressure exploration.
  - #2 (revised): recent-conditions view (historical “recent” slice).
  - #3: pressure vs temperature relationship exploration via scatter plots.
  - #4: temperature and pressure over time via time-series plots and date filtering.
- Partially implemented: None.
- Pending M3: None.

#### Deviations

- Compared to the proposal sketch, the app is now centered on a single filtered dataset powering KPI cards plus relationship and time-series plots, rather than focusing primarily on a landing page of univariate distributions; this better aligns the UI directly to the four job stories (filtering, recent conditions, relationships, trends).

#### Final Layout vs M1 Sketch and M2 Spec

- Matches: KPI-style summaries and interactive filtering remain central to the experience.
- Differences: the final layout emphasizes interconnected filters and job-story-driven plots (relationship plus time series) as the primary outputs; updates are documented under **### Changed** above.

#### Best Practices (DSCI 531)

- We prioritized a clear, usable layout that reduces cognitive load: filters are grouped logically, KPIs summarize the filtered subset, and plots are organized to support the job stories (relationships and trends).
- Where the filtered dataset becomes small, visual interpretation can be weaker; we documented this limitation explicitly under Known Issues so outputs are not misread as implementation gaps.
- We also treated documentation as part of the deliverable: we kept the proposal aligned with the implemented dashboard intent, and captured design changes and constraints in the changelog to support collaboration and reviewer clarity.

#### Self-Assessment

- Strengths:
  - We collaborated smoothly, stayed on schedule, and divided work in a way that ensured each team member contributed meaningfully.
  - Our implementation is cohesive: one reactive dataset drives all outputs, reducing inconsistencies between filters, KPIs, and plots.
- Limitations:
  - Due to the structure and timing of the work across milestones, we could not always ensure every team member had an equally “integral” role in both milestones so far.
- Future improvements (M3):
  - Maintain strong collaboration and role rotation so contributions stay balanced.
  - Continue supporting each other with reviews, testing, and documentation so the app remains consistent and polished as features expand.
