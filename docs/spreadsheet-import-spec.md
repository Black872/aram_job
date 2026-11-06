# Existing spreadsheet import specification

Source workbook: `Jobsuche Befund.xlsx` (user-provided export).

## Workbook inventory

- `Sheet1`: application tracker, headers in row 5, application records start at row 7.
- `Sheet2`: dropdown dictionaries.
- `Sheet3`: empty.
- `Sheet1` has 31 populated candidate rows (rows 7–37). Row 7 is the template's
  `Example Firm` demonstration record and must be excluded by default. Rows 8–37
  contain 30 actual application records.
- Rows 38–200 are not application records; many contain only a prefilled Contact
  template (`Name - / Email - / Tel -`). Never import those as applications.

## Column mapping (Sheet1)

| Excel column | Header | ARAM field | Import handling |
|---|---|---|---|
| A | Company | `company` | Required for a normal row |
| B | Role Title | `role_title` | Preserve original text; normalize soft hyphen for matching only |
| C | Salary/Rate | `salary_rate` | Preserve as text (e.g. `55-70k`, `35k`) |
| D | Link to Job Advert | `job_advert_url` | Preserve URL or formula hyperlink target |
| E | Application Date | `application_date` | Parse Excel date or `dd.mm.yyyy`; retain source value if parse fails |
| F | Contact | contact fields | Parse `Name -`, `Email -`, `Tel -`; also preserve full raw contact text |
| G | Response | `response_status_raw` | Preserve exact dropdown value |
| H | Interview Stage | `interview_stage` | Preserve exact dropdown value |
| I | Interview Time, Date & Interviewer Name | interview details | Preserve complete raw text; structured parsing is best-effort |
| J | Offer | `offer_status_raw` | Preserve exact dropdown value |

## Dropdown dictionaries (Sheet2)

- Response: `Nothing Yet`, `Positive Email`, `Positive Phone Call`,
  `Rejection Email/Call`.
- Interview: `Telephone`, `1st Face-to-face`, `2nd Face-to-face`,
  `3rd Face-to-face`, `4th Face-to-face`, `Interview Declined`.
- Offer: `Yes`, `No`.

Do not replace these user-facing values in the spreadsheet. ARAM's normalized
internal status is separate from the raw dropdown values.

## Initial status mapping

- Response `Rejection Email/Call` -> `REJECTED`.
- Response `Positive Email` or `Positive Phone Call` -> `IN_REVIEW`, unless a
  more advanced interview/offer field provides a later stage.
- Interview stage other than empty or `Interview Declined` -> `INTERVIEW`.
- Offer `Yes` -> `OFFER`.
- Response `Nothing Yet` or blank, with no later-stage evidence -> `APPLIED`.
- `Interview Declined` alone does not prove the employer rejected the application;
  keep raw value and flag for review rather than assigning `REJECTED`.
- Conflicting fields must be flagged for review; precedence: OFFER > REJECTED only
  when an explicit current rejection event is confirmed > INTERVIEW > IN_REVIEW > APPLIED.
  Historical contradictory spreadsheet fields are not silently overwritten.

## Import safety and identity

- Exclude row 7 (example record) unless the user explicitly asks to import it.
- Ignore rows with only the prefilled contact template.
- Use `(workbook_id, sheet_name, row_number)` as the initial external row identity.
- Store source row number and tab name in `spreadsheet_row_id` / `spreadsheet_tab`.
- Before writing, produce a dry-run report with imported, skipped, and flagged rows.
- Do not write to the original Google Sheet during initial import.
- Import must be idempotent: re-running the same workbook must update/match the
  same external row identity rather than create duplicates.
- Keep raw source values for date, contact, response, interview, and offer fields.
