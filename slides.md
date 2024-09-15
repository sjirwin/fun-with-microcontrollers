## Fun With Microcontrollers
### Building a digital sundial using Python

<center>
<br/>Scott Irwin
<p>&nbsp;
<img src="images/BBGEngineering_black.png"
     style="border: none; box-shadow: none; height: 100px"
     alt="Bloomberg Engineering logo"
/>
<br/>
<p>&nbsp;
https://sjirwin.github.io/fun-with-microcontrollers/
</center>

------

## About Me

- Bloomberg Engineering
  - Joined in 2014 as Senior Engineer and Team Lead
  - Python educator
  - Python Guild Leader since 2018
    - Co-chair since 2021

===

# Digital Sundial

------

## What We Are Building

<img src="images/sundial-photo.png"
     style="border: none; box-shadow: none; height: 500px"
     alt="Small TFT LED screen displaying a circle divided into 8 segments with each segment representing a portion of the day. Also displayed is a single clock hand indicating the current time."
/>

------

## What We Need To Get There

- Data
- Hardware
- Python !

===

# Data

------

## Sun Event Times

- Using API provided by https://sunrise-sunset.org/
  - They have a simple, free REST API
  - Usage limited to "reasonable volume"
  - **They require that you show attribution to them with a link to their site**

------

## Using The API

- Send a GET request to https://api.sunrise-sunset.org/json
- Request parameters
  - Latitude and longitude as decimal degrees
  - Date (YYYY-MM-DD)
  - Timezone identifier (e.g., Asia/Tokyo)
  - Format option

------

## Sample data

```text
{
  'astronomical_twilight_begin': '2024-08-24T04:36:51-04:00',
  'astronomical_twilight_end': '2024-08-24T21:19:26-04:00',
  'civil_twilight_begin': '2024-08-24T05:47:25-04:00',
  'civil_twilight_end': '2024-08-24T20:08:51-04:00',
  'day_length': 48430,
  'nautical_twilight_begin': '2024-08-24T05:13:06-04:00',
  'nautical_twilight_end': '2024-08-24T20:43:11-04:00',
  'solar_noon': '2024-08-24T12:58:08-04:00',
  'sunrise': '2024-08-24T06:14:33-04:00',
  'sunset': '2024-08-24T19:41:43-04:00'
}
```

------

## Mapping The Data

<img src="images/sundial-annotated.png"
     style="border: none; box-shadow: none"
     alt="A circle divided into 8 segments with each segment representing a portion of the day. At the boundry point of each segment is an annotation labeling which part of the solar day it represents."
/>

===

# Hardware

------

## Working Title

===

# Python

------

## Working Title

===

## References

  - This talk: [https://sjirwin.github.io/fun-with-microcontrollers](https://sjirwin.github.io/fun-with-microcontrollers)
  - Project Repo: [https://github.com/sjirwin/fun-with-microcontrollers](https://github.com/sjirwin/fun-with-microcontrollers)
    - Code: `main` branch
    - Slides: `gh-pages` branch
