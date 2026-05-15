# How to Install the Recoup Catalog Diligence Plugin in Claude Desktop

The Recoup Catalog Diligence Plugin is a collection of ready-made
workflows that turn Claude into a music catalog analyst. Install it
once and you can ask Claude to ingest a messy seller data room,
normalize the royalty statements, flag rights issues, build a
valuation bracket, and hand you back a polished dashboard, an
investment memo, and a shareable PDF — all source-cited, all in one
place.

This guide is written for catalog operators, A&R, and business teams.
**You don't need to know how to code.** It takes about 5 minutes.

---

## Before you begin

You'll need:

- **Claude Desktop** installed on your Mac or Windows computer.
  ([Download here](https://claude.ai/download) if you haven't yet.)
- A **Claude Pro, Team, or Enterprise** account signed in.
- The plugin's web link (copy this — you'll paste it in Step 3):

  ```text
  https://github.com/recoupable/recoup-catalog-diligence
  ```

That's it. No Terminal. No installs. No coding.

---

## Step 1 — Open the plugins panel

Open Claude Desktop. In the left sidebar, look for the **puzzle-piece
icon** (the plugin marketplace).

Click it.

> 📸 *Screenshot: the Claude Desktop sidebar, with an arrow pointing at the puzzle-piece icon.*

**You'll know you're in the right place when:** a panel slides open
showing "Plugins" at the top, with tabs like *Featured*, *Installed*,
and a search bar.

---

## Step 2 — Add a custom plugin

At the top of the plugins panel, look for the button that says
**Add custom plugin** (sometimes labelled **Install from URL** or
**Add plugin manually**).

Click it.

> 📸 *Screenshot: the Plugins panel with the "Add custom plugin" button highlighted.*

A small dialog box will open with a single text field, asking for a
plugin URL.

---

## Step 3 — Paste the plugin link

Paste this link into the dialog:

```text
https://github.com/recoupable/recoup-catalog-diligence
```

Then click **Add** (or **Install** — the button name may vary).

> 📸 *Screenshot: the dialog with the URL pasted in and the Add button highlighted.*

Claude will spend a few seconds downloading the plugin. **Don't close
the window** while it works. When it's ready, you'll see a permissions
prompt (Step 4).

---

## Step 4 — Approve the permissions

Claude will show you a list of things the plugin needs permission to
do. For the Recoup Catalog Diligence Plugin, you'll see three:

- **Read files** — so it can look at the seller's royalty statements
  and rights documents you give it.
- **Write files** — so it can save the normalized data, the dashboard,
  the memo, and the PDF report.
- **Run commands** — so it can run the small checks that confirm every
  number on the dashboard ties back to a real source file.

These are all expected. Click **Approve** (or **Allow**, **Trust this
plugin**, etc.).

> 📸 *Screenshot: the permissions dialog with the three permissions visible and the Approve button highlighted.*

**Tip:** Claude only ever touches files inside a folder you create for
the deal. It does not read or modify anything else on your computer.

---

## Step 5 — Restart Claude Desktop

This is the most important step. **The plugin won't fully work until
you restart Claude.**

1. Close Claude Desktop completely. (On Mac: ⌘ + Q. On Windows: right-click
   the Claude icon in the system tray → Quit.)
2. Open Claude Desktop again.

> 📸 *Screenshot: the Claude Desktop window before quitting, with the Quit menu visible.*

---

## Step 6 — Confirm the plugin is installed

In a new conversation, type a forward slash:

```text
/
```

A menu of commands will appear. Scroll through — you should see
commands beginning with **`/recoup-catalog-…`**, like:

- `/recoup-catalog-demo`
- `/recoup-catalog-diligence`
- `/recoup-catalog-report`

If you see those, **you're done.** The plugin is installed and ready.

> 📸 *Screenshot: the slash-command menu with the /recoup-catalog-* commands visible.*

---

## Your first run (the 60-second confidence check)

Before you point Claude at a real seller's data room, let's prove the
plugin works using a fake catalog that's bundled in. In a new chat,
type:

```text
/recoup-catalog-demo
```

Then press Enter.

Claude will work for 2–4 minutes. It will:

1. Set up a sample deal workspace called `demo-catalog`.
2. Pretend you handed it a messy seller data room.
3. Normalize the royalty statements.
4. Flag the rights issues, valuation drivers, and missing files.
5. Build an interactive dashboard.
6. Draft an investment-committee memo.

When it's done, Claude will give you a file path to open. Click it,
and the **dashboard opens in your browser**. That's the deliverable
your buyer / IC / lender would see.

> 📸 *Screenshot: the dashboard rendered in a browser, with KPIs and the value bracket visible.*

If you got here, the plugin works. You're ready for a real deal.

---

## Using it on a real catalog

When you have a real seller data room:

1. Create a new chat in Claude Desktop.
2. Type:

   ```text
   /recoup-catalog-diligence
   ```

3. Claude will ask what kind of deal it is (buy-side, seller-prep,
   financing) and what you want to call it. Answer in plain English.
4. **Drag and drop** the seller's files into the chat — royalty
   statements, contracts, metadata exports, anything they sent you.
5. Wait. Claude runs the full workflow end-to-end and lands on the
   dashboard.
6. When you're ready to send the deal to a buyer, IC, or lender,
   type:

   ```text
   /recoup-catalog-report
   ```

   That produces a single shareable PDF you can attach to an email.

---

## Troubleshooting

**I don't see the `/recoup-catalog-…` commands after restarting.**

Quit Claude Desktop **completely** (not just close the window) and
reopen. On Mac, use ⌘ + Q. If that still doesn't work, restart your
computer.

**The "Add custom plugin" button isn't in my Plugins panel.**

You may need to enable custom plugins in Claude's settings. Click
the gear icon → **Plugins** → toggle **Allow custom plugins** on. Then
try Step 2 again.

**Claude says "permission denied" when I run a command.**

You probably skipped Step 4. Open the Plugins panel, find
*Recoup Catalog Diligence* under *Installed*, click it, and approve
the three permissions (Read, Write, Run commands).

**My seller sent me a PDF royalty statement and Claude says it can't
read it.**

This is the one optional thing that needs a tiny bit of setup —
**have your tech team set up two helper libraries for you** (it's a
one-time, 30-second install). Send them this link:
[Optional: handling PDF and Excel files](#optional-handling-pdf-and-excel-files).

If you don't have a tech team, you can also ask the seller to send
royalty statements as **CSV or Excel** instead of PDF. Most providers
can do that on request.

**Something else is wrong.**

Email <support@recoupable.com> with a screenshot. We respond fast.

---

## Optional: handling PDF and Excel files

The plugin's core works out of the box. If your seller sends royalty
statements as **PDF** or large **Excel (.xlsx)** files, two small
helper libraries make those readable. Anyone on your tech team can
install them in about 30 seconds:

1. Open Terminal (Mac) or Command Prompt (Windows).
2. Run:

   ```bash
   pip3 install pdfplumber openpyxl
   ```

3. Restart Claude Desktop.

If your data room is CSV-only, **skip this step entirely.**

---

## What you can do now

| Type this in chat | What happens |
| ----------------- | ------------ |
| `/recoup-catalog-demo` | Runs a full demo on a synthetic catalog. Great for showing teammates what the plugin does. |
| `/recoup-catalog-diligence` | The main command. End-to-end diligence on a real seller's data room. |
| `/recoup-catalog-report` | Exports the deal as a shareable PDF you can email. |

You don't need to memorize the rest. Just type `/` in any Claude chat
and the menu shows you everything.

---

## Help & support

- **Plugin home:** [recoupable.com](https://recoupable.com)
- **Email:** <support@recoupable.com>
- **Plugin source:**
  [github.com/recoupable/recoup-catalog-diligence](https://github.com/recoupable/recoup-catalog-diligence)

Welcome to faster, more honest catalog diligence.
