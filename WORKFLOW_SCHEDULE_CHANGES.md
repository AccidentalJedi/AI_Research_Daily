# Workflow Schedule Changes

## Summary
Updated the GitHub Actions workflows to align with the requested schedule:
- **Data Ingestion**: Changed from every 6 hours to every 4 hours
- **Report Publishing**: Changed from 16:00 CST to 08:00 CST (8:00 AM Central)

## Changes Made

### 1. Ingest Workflow (`ingest.yml`)
**Purpose**: Gathers research data from arXiv, HuggingFace, and Papers with Code

**Schedule Change**:
- **Before**: `0 */6 * * *` (Every 6 hours: 00:00, 06:00, 12:00, 18:00 UTC)
- **After**: `0 */4 * * *` (Every 4 hours: 00:00, 04:00, 08:00, 12:00, 16:00, 20:00 UTC)

**Impact**: 
- Data is now collected 6 times per day instead of 4 times
- More frequent data gathering ensures fresher content for the 08:00 CST report
- The report at 08:00 CST (14:00 UTC) will have data from the 12:00 UTC ingestion run

### 2. Daily Report Workflow (`daily_report.yml`)
**Purpose**: Generates and publishes "The Scholar" research intelligence report

**Schedule Changes**:
- **Before**: 
  - `0 21 * * *` (21:00 UTC = 16:00 CDT / 15:00 CST)
  - `0 22 * * *` (22:00 UTC = 17:00 CDT / 16:00 CST)
- **After**:
  - `0 13 * * *` (13:00 UTC = 08:00 CDT during Daylight Saving Time)
  - `0 14 * * *` (14:00 UTC = 08:00 CST during Standard Time)

**Time Gate Change**:
- **Before**: Checked for hour == 16 (4:00 PM)
- **After**: Checks for hour == 08 (8:00 AM)

**Impact**:
- Report now publishes at 08:00 AM Central Time instead of 4:00 PM
- Automatically handles Daylight Saving Time transitions
- Publishes in the morning for better visibility during work hours

## Timeline Example (Central Time Zone)

### Data Ingestion (Every 4 Hours)
- **18:00 CST** (00:00 UTC) - Ingestion Run 1
- **22:00 CST** (04:00 UTC) - Ingestion Run 2
- **02:00 CST** (08:00 UTC) - Ingestion Run 3
- **06:00 CST** (12:00 UTC) - Ingestion Run 4 ← **Most recent before report**
- **10:00 CST** (16:00 UTC) - Ingestion Run 5
- **14:00 CST** (20:00 UTC) - Ingestion Run 6

### Report Generation
- **08:00 CST** (14:00 UTC) - Daily Report Published

The report at 08:00 CST uses data gathered from:
- Yesterday's evening ingestion runs
- Overnight ingestion runs
- The 06:00 CST ingestion run (most recent, 2 hours before report)

## How to Manually Trigger Workflows

Since the workflows have `workflow_dispatch` enabled, you can trigger them manually:

### To Trigger Data Ingestion:
1. Go to: https://github.com/AccidentalJedi/AI_Research_Daily/actions/workflows/ingest.yml
2. Click "Run workflow"
3. Select the branch (e.g., `main` or `copilot/set-reporting-time-and-frequency`)
4. Click "Run workflow"

### To Trigger Report Generation:
1. Go to: https://github.com/AccidentalJedi/AI_Research_Daily/actions/workflows/daily_report.yml
2. Click "Run workflow"
3. Select the branch
4. Click "Run workflow"

**Note**: The report generation has a time gate that checks for 08:00 local time. When triggered manually via `workflow_dispatch`, if the current time is not 08:00 CST, the workflow will exit without generating a report. To bypass this for testing, you would need to temporarily comment out the time gate step.

## Verification

To verify the changes are working:

1. **Check Workflow Files**:
   ```bash
   cat .github/workflows/ingest.yml | grep "cron:"
   cat .github/workflows/daily_report.yml | grep "cron:"
   ```

2. **Monitor Next Scheduled Runs**:
   - Go to: https://github.com/AccidentalJedi/AI_Research_Daily/actions
   - Check when the next scheduled runs are for each workflow

3. **Check Generated Reports**:
   - Reports are saved to: `docs/reports/lab-{date}.md`
   - View on GitHub Pages: https://accidentaljedi.github.io/AI_Research_Daily

## Files Modified
- `.github/workflows/ingest.yml` - Changed ingestion frequency from 6 hours to 4 hours
- `.github/workflows/daily_report.yml` - Changed report time from 16:00 to 08:00 CST
