# Registry Backlog

## Landing Page
- Add a 'data quality' section showing recent activity and data quality errors; see [Data Quality](#Data-Quality-Checks) 
- ~~Add a list of non-discharged patients, grouped by centre, to the bottom of the page (below the fold).~~
- ~~Add a reporting tools panel to export data~~; does nothing for now.

## Patient Details
- Add additional fields to capture: 
  - ~~Hospital Number~~
  - ~~An automatically generated id (as unique serial number)~~
  - ~~Date of birth OR Year of birth~~
  - ~~Phone #1 + Comments & Phone #2 + Comments~~ (Phone number formatting??)
  - Antibiotics
- ~~Record New Surgery shows drop-down with different hernia repair.~~
- Add type-ahead search box (Google style) that searches across all patient fields

## Follow-Up
- ~~Use Tri-state bools [None, Yes, No] as buttons for follow-up observations.~~

## Discharge
- ~~Create new event type, discharge~~
- Add additional fields to capture:
  - ~~Perioperative Complications: Bool + TextBox.~~
  - ~~Post-Operative Antibiotics Given: bool with text-field on true.~~
  - ~~IV for how many days / oral for how many days~~

## Mesh Herina Repair
Select boxes to default to empty and force to choose one.
Information icon next to choices.
Side == Both / Record “both” as two separate hernia surgeries.
Bi-Lateral bool; with comment that if true “Please record as two separate repairs”.

Primary / recurrent / re-recurrent radio buttons
(recurrent and re-recurrent creates a box with ‘previous suture repair’ / ‘previous mesh repair’, re-recurrent has a numerical box with ‘number of previous repairs’).

Complexity: Simple, Sliding, Incarcerated, Obstructed, Strangulated
Hernia Type: Direct, Indiect, Pantaloon
Size: Small / Medium / Large / Massive

Mesh Type (drop down box, prepopulated with TNMHP Mesh): TNMHP Mesh, KCMC/Northumbria Generic Mesh, Commercial Mesh [If commercial mesh can we have a free text box that appears with the heading ‘brand’].
Diathermy User? Tri-state bool [None, Yes, No]
Primary Surgeon: Blank not ‘(Any)’, Secondary & Tertiary add a ‘(none)’ option - at the top.
Surgeon global and type ahead 

Additional procedure – choice of ‘None’, ‘orchidectomy’, ‘scrotoplasty’ ‘other’. Other creates a free text box.
Antibiotics Given: bool with text-field on true.

Make Complications into a multi-item list box with palette.
Antibiotics Picker

## Data Quality Checks
Dupes + Missing Data on Patients?
