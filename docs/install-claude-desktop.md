# How to Install the Recoup Catalog Diligence Plugin in Claude Desktop

The Recoup Catalog Diligence Plugin turns Claude into a music catalog
analyst. Install it once and Claude can ingest a seller's data room,
normalize the royalties, and produce a source-cited dashboard, memo,
and shareable PDF.

**Takes about 2 minutes. No coding.**

You'll need Claude Desktop installed and signed in
([download here](https://claude.ai/download)). Copy this link — you'll
paste it in Step 3:

```text
https://github.com/recoupable/recoup-catalog-diligence
```

---

## 1. Open the plugins panel

Click the **puzzle-piece icon** in the Claude Desktop sidebar.

> 📸 *Screenshot: sidebar with the puzzle-piece icon highlighted.*

## 2. Click "Add custom plugin"

At the top of the Plugins panel.

> 📸 *Screenshot: Plugins panel with the Add custom plugin button highlighted.*

## 3. Paste the link

Paste the URL above and click **Add**.

> 📸 *Screenshot: dialog with the URL pasted in.*

## 4. Approve the permissions

Claude will ask to **Read files**, **Write files**, and **Run commands**.
Click **Approve**.

> 📸 *Screenshot: permissions dialog.*

The plugin only ever touches files inside a folder you create for the
deal. It does not read anything else on your computer.

## 5. Restart Claude Desktop

Quit completely (⌘ + Q on Mac, right-click the system tray icon →
Quit on Windows), then reopen.

> 📸 *Screenshot: Quit menu.*

## 6. Analyze your first catalog

In a new chat, type:

> **Let's analyze a catalog with /recoup-catalog-diligence**

Then drop your seller's files into the chat — royalty statements,
contracts, metadata exports, even messy ones. Claude takes it from
there and lands on a dashboard you can open in your browser.

> 📸 *Screenshot: the dashboard rendered in a browser.*

**No catalog yet?** Type `/recoup-catalog-demo` instead — it runs the
full workflow against a sample catalog so you can see the output.

---

## If something goes wrong

- **Slash commands don't appear?** Quit Claude completely and reopen.
- **No "Add custom plugin" button?** Settings → Plugins → toggle
  **Allow custom plugins** on.
- **Anything else?** Email <support@recoupable.com> with a screenshot.
