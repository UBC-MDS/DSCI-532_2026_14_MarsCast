# Curiosity Rover Mars weather dataset (Sol 1–1895, 2012–2018, Gale Crater)

Collected by the **Rover Environmental Monitoring Station (REMS)** on Curiosity. Released by NASA’s Mars Science Laboratory and CSIC-INTA.

Each row is weather data for a single sol. Key columns:

- sol: Martian day since landing
- terrestrial_date: Earth date
- ls: solar longitude (Mars’ season)
- month: Martian month
- min_temp / max_temp: surface temperature (°C)
- pressure: surface atmospheric pressure (Pa)
- id: record ID

## Notes

- Some temperature and pressure data are missing.
- Supports monitoring conditions, mission planning, and engineering limits.
