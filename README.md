# Drilling
POC carried out on February 27, 2025, by Kévin Abdellah Anatole.

# Description of the Implementation Process

Morning session:
In the morning, we explored the data and tried to understand the different states of a drilling operation, i.e., illustrating the thresholds and drilling states.

![photo_seuils](https://github.com/user-attachments/assets/30d097bf-8186-4ba1-8241-7eaa1b21a99f)

Process:
Given that we had a list of business logic rules, we decided to start by implementing them while also creating data visualizations. This allowed us to visually assess progress and receive feedback from the domain expert. The business logic is implemented in Python in a way that makes it easy to modify and adapt, enabling rapid incorporation of the expert’s feedback.

<img width="2464" height="1530" alt="image" src="https://github.com/user-attachments/assets/f1233b76-5d8f-4d6e-b917-c3cb5ab79ab1" />

Result:
We now have a Dash interface presenting the labeled data and allowing visualization, with a textual description of the state associated with each point.

Next steps:

- Proper display of the classified data remains to be implemented. We could add various filtering options to identify curves based on different parameters and their characteristics, using different colors or symbols.

- Error identification: A filtering system could be added to detect potentially impossible classifications (e.g., a point being both increasing and decreasing at the same time).

Dataset Description

Correspondence of drilling measurements
| Code      | Description                               | Unit of Measurement               |
| --------- | ----------------------------------------- | --------------------------------- |
| TIME      | Data recording time                       | hh\:mm\:ss or s                   |
| DBTM      | Measured depth                            | m (meters)                        |
| DMEA      | True vertical depth (TVD)                 | m (meters)                        |
| SPPA      | Surface pressure                          | psi or bar                        |
| BPOS      | Bit position                              | m (meters)                        |
| SPM1      | Pump 1 speed                              | spm (strokes per minute)          |
| SPM2      | Pump 2 speed                              | spm (strokes per minute)          |
| MFIA      | Drilling fluid flow rate                  | L/min or gpm (gallons per minute) |
| WOBA      | Weight on bit (WOB)                       | klbf (kilopounds-force) or daN    |
| HKLA      | Hook load                                 | klbf (kilopounds-force) or daN    |
| RPMA      | Bit rotation speed                        | tr/min (RPM)                      |
| TQA       | Applied torque                            | kNm (kilonewton-meter)            |
| TV01-TV06 | Temperature measured at different sensors | °C                                |
| TTV1      | Drilling mud temperature                  | °C                                |
| ROPA      | Rate of penetration (ROP)                 | m/h or ft/h                       |

