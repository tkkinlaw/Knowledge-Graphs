MATCH (a:Aircraft)-[v:Visits]->(g:Grid50m)
WITH a, COLLECT(v.Date_time) AS visitingTimes
UNWIND visitingTimes AS visitDate
WITH a, date(visitDate) AS visitDate
ORDER BY a, visitDate
WITH a, COLLECT(visitDate) AS sortedVisitDates
WITH a, [date IN sortedVisitDates WHERE 
    date IN sortedVisitDates AND 
    date + duration('P1D') IN sortedVisitDates AND 
    date + duration('P2D') IN sortedVisitDates] AS consecutiveDates
WHERE SIZE(consecutiveDates) > 0
RETURN a, consecutiveDates

// Explanation:
// MATCH Clause:
// (a:Aircraft)-[v:Visits]->(g:Grid50m): Matches Aircraft nodes that have Visits relationships to Grid50m nodes.
// WITH Clause:
// COLLECT(v.Date_time) AS visitingTimes: Collects all visit times for each aircraft.
// UNWIND Clause:
// UNWIND visitingTimes AS visitDate: Unwinds the collected visit times into individual rows.
// Date Conversion:
// WITH a, date(visitDate) AS visitDate: Converts the visit times to date objects.
// Ordering:
// ORDER BY a, visitDate: Orders the visit dates for each aircraft.
// Collecting Sorted Dates:
// WITH a, COLLECT(visitDate) AS sortedVisitDates: Collects the sorted visit dates back into a list.
// Finding Consecutive Dates:
// WITH a, [date IN sortedVisitDates WHERE date IN sortedVisitDates AND date + duration('P1D') IN sortedVisitDates AND date + duration('P2D') IN sortedVisitDates] AS consecutiveDates: Checks for sequences of 3 consecutive days within the sorted visit dates.
// Filtering:
// WHERE SIZE(consecutiveDates) > 0: Filters out aircraft that do not have any sequences of 3 consecutive days.
// RETURN Clause:
// RETURN a, consecutiveDates: Returns the aircraft and the list of starting dates for the 3 consecutive days.
// This query assumes that the Date_time property in the Visits relationship is in a format that can be converted to a date object. You may need to adjust the query based on your specific data model and date format.