## [0.4.0] - 2026-03-17

### Added

- Added automated tests to verify core dashboard logic and user interactions (PR: #85)

### Changed

- Added trend line to scatter plots (in class feedback from Ilya and Issue #90) via (PR #89)

- Added legend to temperature time series on main dashboard (Issue #90) via (PR #94)

- Aligned x-axis labels on plots horizontally rather than vertically (Issue #93) via (PR #94) 


### Fixed

- Updated system prompt for LLM to not break (Issue #75) via (PR #95)

- Ensured plot titles are consistent between pages (Issue #83, #90) via (PR #94)

- Fixed AI page UI to show chat portion at all times (Issue #69) via (PR ?)

- **Feedback prioritization issue link:** #75

### Known Issues

- Default filter: The dashboard defaults to the most recent terrestrial month rather than the current day since weather data is seasonal and month-level periods provide a more stable view of trends.
- KPI comparisons: KPIs compare the selected period with the same calendar period in the previous year to provide a seasonal baseline. A comparison is not included for Std Air Pressure since variability metrics are less meaningful for quick year-over-year comparison.
- Since the filters on the first page of the dashboard are reactive to each other, the user will need hit the "Reset" button in order to be able to change the Martian Month and Season filters.

### Release Highlight: RAG: Custom Knowledge Base for Querychat

Previously, our chatbot used an LLM that only had access to the dataset schema (column names and types) and general guidelines, without real context. To improve this, we created a folder rag/docs containing three documents with information about Mars, a data dictionary, and details about the rover itself. With RAG (Retrieval-Augmented Generation), the system searches this context bank for relevant information for each user query and provides it to the LLM, ensuring it has the necessary context to answer accurately and improving overall response quality.

- **Option chosen:** C 
- **PR:** #84
- **Why this option over the others:** <!-- 1–2 sentences; link to your feature prioritization issue -->
- **Feature prioritization issue link:**: ?

### Collaboration

Since M3, our collaboration has become more structured and balanced. All members have contributed to coding throughout the project. Task planning through GitHub issues and our branching strategy have minimized merge conflicts and clarified dependencies, improving both efficiency and overall team coordination.

- **CONTRIBUTING.md:** #96
- **M3 retrospective:** After M3, we made a conscious effort to distribute coding tasks more evenly so all group members contributed. Additionally, we attempted to treat design doc updates as a pre-merge step to keep documentation aligned with code changes, though this was not consistently achieved.
- **M4:** For M4, we focused on maintaining meaningful PR reviews: all PRs received feedback from at least one external reviewer, and we aimed to ensure these reviews evaluated the PR content thoroughly rather than serving as a mere formality. In addition, we carefully checked and followed the rubric and instructions to avoid missing requirements, ensuring our work aligned closely with milestone expectations.

### Reflection

The dashboard effectively visualizes key Mars weather data and supports related user stories, allowing users to explore trends and KPI comparisons. In addition, the LLM page provides interactive AI-assisted querying of the dataset, giving context-aware responses. Although the targeted users are experts with a strong knowledge of Mars, current limitations, such as the complexity of translating between Martian and terrestrial dates can make some timeline interpretations less intuitive. Another limitation is that the filters on the main dashboard are interdependent; users must hit the "Reset" button before changing these filters from default, which can make exploration less seamless.

Trade-offs: We prioritized addressing critical UI and LLM issues, improving dashboard clarity, and adding context-aware features (e.g., trend lines, legends) over less urgent visual refinements to ensure both functionality and meaningful user feedback were incorporated.

Most useful: The feedback related to the LLM UI, such as ensuring the chat portion is always visible and preventing system prompt errors—shaped our work most this milestone. Other feedback on maintaining consistent and clear visualizations, including trend lines, legends, and axis labels, also guided our improvements. Additional coverage on best practices for integrating RAG with dashboards and providing richer dataset context to the LLM would have been particularly helpful.

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
