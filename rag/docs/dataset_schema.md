# Mars Curiosity Rover Dataset Schema

## Dataset Overview

This dataset contains environmental measurements collected by NASA's Curiosity Rover on Mars.

- Total rows: 1894
- Each row represents measurements recorded during a Martian sol.
- A sol is a Martian day (~24h 39m).

---

## Columns

### id

- Type: integer
- Description: The identification number of a single transmission.

### terrestrial_date

- Type: string (ISO date)
- Description: The date on Earth (formatted as month/day/year or m/dd/yy).

### sol

- Type: integer
- Description: The number of elapsed sols (Martian days) since Curiosity landed on Mars.

### ls

- Type: integer
- Description: The solar longitude or the Mars-Sun angle, measured from the Northern Hemisphere. In the Northern Hemisphere, the spring equinox is when ls = 0. Since Curiosity is in the Southern Hemisphere, the following ls values are of importance:
  - ls = 0: autumnal equinox
  - ls = 90 : winter solstice
  - ls = 180 : spring equinox
  - ls = 270 : summer solstice
- Used to approximate Martian seasons.

### month

- Type: categorical (string)
- Description: The Martian Month. Similarly to Earth, Martian time can be divided into 12 months. A martian year is 668.6 sols (martian solar days) long and a sol is 88775.245 seconds long. Martian months are defined as spanning 30 degrees in solar longitude. Due to the eccentricity of Mars' orbit, martian months are thus from 46 to 67 sols long.

### min_temp

- Type: float (°C)
- Missing values: 27
- Description: The minimum temperature (in °C) observed during a single Martian sol.

### max_temp

- Type: float (°C)
- Missing values: 27
- Description: The maximum temperature (in °C) observed during a single Martian sol.

### pressure

- Type: float (Pa)
- Missing values: 27
- Description: The atmospheric pressure (Pa) in Curiosity's location on Mars.

### wind_speed

- Type: float (m/s)
- Missing values: 1894 (currently unavailable)
- Description: The average wind speed (m/s) measured in a single sol. Note: Wind Speed data has not be transmitted to Earth since Sol 1485. Missing values are coded as NaN. No recorded values in this dataset.

### atmo_opacity

- Type: categorical (string)
- Description: Description of the overall weather conditions on Mars for a given sol based on atmospheric opacity (e.g., Sunny). All values in this column are "Sunny".

## Query Guidance

- **What is this?**: Data representing the weather conditions on Mars from Sol 1 (August 7, 2012 on Earth) to Sol 1895 (February 27, 2018 on Earth).
- **Source(s) & Methodology**: This data was measured and transmitted via the Rover Environmental Monitoring Station (REMS)on-board the Curiosity Rover. The data was made publicly available by NASA’s Mars Science Laboratory and the Centro de Astrobiología (CSIC-INTA). The Centro de Astrobiología offers a widget and a disclaimer regarding the data collected by Curiosity.
- **Last Modified**: March 2, 2018.
- **Spatial Applicability**: Gale Crater, Mars (just south of Mars' equator). More information on Curiosity's location.
- **Temporal Applicability**: Sol 1 (August 7, 2012 on Earth) to Sol 1895 (February 27, 2018 on Earth)
- **Observations (Rows)**: Each row represents the weather information collected at some point on a single sol (Martian day).
