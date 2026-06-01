"""
Generate a PDF deployment guide using ReportLab.
"""
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.colors import HexColor
from reportlab.lib.units import mm, cm
from reportlab.lib.enums import TA_LEFT, TA_CENTER
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle,
    PageBreak, HRFlowable, Preformatted
)
from reportlab.lib import colors
import os

OUTPUT_PATH = os.path.join(os.path.dirname(__file__), "Deployment_Guide.pdf")

# ── Colors ──────────────────────────────────────────────
PRIMARY = HexColor("#1a73e8")
DARK = HexColor("#202124")
GRAY = HexColor("#5f6368")
LIGHT_BG = HexColor("#f8f9fa")
CODE_BG = HexColor("#1e1e1e")
CODE_FG = HexColor("#d4d4d4")
SUCCESS = HexColor("#0d652d")
WARNING = HexColor("#e37400")
TABLE_HEADER_BG = HexColor("#1a73e8")
TABLE_ALT_BG = HexColor("#e8f0fe")

# ── Styles ──────────────────────────────────────────────
styles = getSampleStyleSheet()

styles.add(ParagraphStyle(
    name='DocTitle', fontSize=24, leading=30, alignment=TA_CENTER,
    textColor=PRIMARY, spaceAfter=6, fontName='Helvetica-Bold',
))
styles.add(ParagraphStyle(
    name='DocSubtitle', fontSize=12, leading=16, alignment=TA_CENTER,
    textColor=GRAY, spaceAfter=20, fontName='Helvetica',
))
styles.add(ParagraphStyle(
    name='H1', fontSize=18, leading=24, textColor=PRIMARY,
    spaceAfter=10, spaceBefore=24, fontName='Helvetica-Bold',
))
styles.add(ParagraphStyle(
    name='H2', fontSize=14, leading=18, textColor=DARK,
    spaceAfter=8, spaceBefore=16, fontName='Helvetica-Bold',
))
styles.add(ParagraphStyle(
    name='H3', fontSize=12, leading=16, textColor=HexColor("#333333"),
    spaceAfter=6, spaceBefore=12, fontName='Helvetica-Bold',
))
styles.add(ParagraphStyle(
    name='Body', fontSize=10, leading=15, textColor=DARK,
    spaceAfter=6, fontName='Helvetica',
))
styles.add(ParagraphStyle(
    name='BulletItem', fontSize=10, leading=15, textColor=DARK,
    spaceAfter=4, fontName='Helvetica', leftIndent=20, bulletIndent=8,
))
styles.add(ParagraphStyle(
    name='CodeBlock', fontSize=8.5, leading=12, textColor=CODE_FG,
    backColor=HexColor("#2d2d2d"), fontName='Courier',
    leftIndent=10, rightIndent=10, spaceBefore=6, spaceAfter=8,
    borderWidth=0.5, borderColor=HexColor("#444444"), borderPadding=8,
    borderRadius=4,
))
styles.add(ParagraphStyle(
    name='InlineCode', fontSize=9.5, leading=14, textColor=HexColor("#d63384"),
    fontName='Courier', backColor=HexColor("#f1f3f5"),
))
styles.add(ParagraphStyle(
    name='Note', fontSize=9.5, leading=14, textColor=HexColor("#0c5460"),
    backColor=HexColor("#d1ecf1"), fontName='Helvetica-Oblique',
    leftIndent=12, rightIndent=12, spaceBefore=6, spaceAfter=8,
    borderWidth=0.5, borderColor=HexColor("#bee5eb"), borderPadding=8,
))
styles.add(ParagraphStyle(
    name='Warning', fontSize=9.5, leading=14, textColor=HexColor("#856404"),
    backColor=HexColor("#fff3cd"), fontName='Helvetica-Oblique',
    leftIndent=12, rightIndent=12, spaceBefore=6, spaceAfter=8,
    borderWidth=0.5, borderColor=HexColor("#ffc107"), borderPadding=8,
))
styles.add(ParagraphStyle(
    name='TableCell', fontSize=9, leading=12, textColor=DARK, fontName='Helvetica',
))
styles.add(ParagraphStyle(
    name='TableHeader', fontSize=9, leading=12, textColor=colors.white, fontName='Helvetica-Bold',
))


def hr():
    return HRFlowable(width="100%", thickness=0.5, color=HexColor("#dadce0"), spaceBefore=10, spaceAfter=10)

def spacer(h=6):
    return Spacer(1, h)

def code_block(text):
    """Create a styled code block."""
    lines = text.strip().split('\n')
    formatted = '<br/>'.join(
        line.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;').replace(' ', '&nbsp;')
        for line in lines
    )
    return Paragraph(formatted, styles['CodeBlock'])

def make_table(headers, rows, col_widths=None):
    """Create a styled table."""
    header_cells = [Paragraph(h, styles['TableHeader']) for h in headers]
    data = [header_cells]
    for row in rows:
        data.append([Paragraph(str(c), styles['TableCell']) for c in row])

    if col_widths is None:
        col_widths = [None] * len(headers)

    t = Table(data, colWidths=col_widths, repeatRows=1)
    style_cmds = [
        ('BACKGROUND', (0, 0), (-1, 0), TABLE_HEADER_BG),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 9),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 8),
        ('TOPPADDING', (0, 0), (-1, -1), 6),
        ('BOTTOMPADDING', (0, 1), (-1, -1), 6),
        ('LEFTPADDING', (0, 0), (-1, -1), 8),
        ('RIGHTPADDING', (0, 0), (-1, -1), 8),
        ('GRID', (0, 0), (-1, -1), 0.5, HexColor("#dadce0")),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, TABLE_ALT_BG]),
    ]
    t.setStyle(TableStyle(style_cmds))
    return t

def note_box(text):
    return Paragraph(f"📝 <b>Note:</b> {text}", styles['Note'])

def warning_box(text):
    return Paragraph(f"⚠️ <b>Important:</b> {text}", styles['Warning'])

def build_pdf():
    doc = SimpleDocTemplate(
        OUTPUT_PATH, pagesize=A4,
        topMargin=25*mm, bottomMargin=25*mm,
        leftMargin=20*mm, rightMargin=20*mm,
        title="Deploying React App to GitHub Pages",
        author="Gunalakshme",
    )

    story = []

    # ── Title Page ─────────────────────────────────────
    story.append(Spacer(1, 60))
    story.append(Paragraph("Deploying a React (Vite) App<br/>to GitHub Pages", styles['DocTitle']))
    story.append(Paragraph("Complete Step-by-Step Guide", styles['DocSubtitle']))
    story.append(hr())
    story.append(Spacer(1, 10))

    meta_data = [
        ["Project", "Arrear Predictor App"],
        ["Author", "Gunalakshme"],
        ["Date", "June 1, 2026"],
        ["Live URL", "https://gunalakshme.github.io/arrear-predictor-app/"],
    ]
    for label, val in meta_data:
        story.append(Paragraph(f"<b>{label}:</b> {val}", styles['Body']))

    story.append(Spacer(1, 20))

    # ── Table of Contents ──────────────────────────────
    story.append(Paragraph("Table of Contents", styles['H2']))
    toc_items = [
        "1. Overview",
        "2. Prerequisites",
        "3. Step 1: Configure Vite for GitHub Pages",
        "4. Step 2: Create GitHub Actions Workflow",
        "5. Step 3: Update .gitignore",
        "6. Step 4: Create a GitHub Repository",
        "7. Step 5: Install and Authenticate GitHub CLI",
        "8. Step 6: Initialize Git and Push Code",
        "9. Step 7: Enable GitHub Pages",
        "10. Step 8: Verify Deployment",
        "11. Step 9: Integrate Firebase Realtime Database",
        "12. Step 10: Set Up Firebase Realtime Database",
        "13. Updating Your App",
        "14. Troubleshooting",
    ]
    for item in toc_items:
        story.append(Paragraph(item, styles['BulletItem']))
    
    story.append(PageBreak())

    # ── 1. Overview ────────────────────────────────────
    story.append(Paragraph("1. Overview", styles['H1']))
    story.append(Paragraph(
        "This guide walks through the complete process of deploying a <b>React application</b> "
        "(built with <b>Vite</b>) to <b>GitHub Pages</b> — a free static site hosting service "
        "provided by GitHub. Once deployed, your app will be accessible to anyone on the internet "
        "via a public URL.", styles['Body']
    ))
    story.append(spacer(6))
    story.append(Paragraph("How It Works", styles['H3']))
    story.append(code_block(
        "Your Code → Push to GitHub → GitHub Actions (auto-build) → GitHub Pages (hosting) → Live URL"
    ))
    story.append(Paragraph(
        "<b>GitHub Actions</b> automatically builds your app every time you push code, and "
        "<b>GitHub Pages</b> serves the built files as a static website.", styles['Body']
    ))

    story.append(hr())

    # ── 2. Prerequisites ──────────────────────────────
    story.append(Paragraph("2. Prerequisites", styles['H1']))
    story.append(Paragraph("Before starting, ensure you have:", styles['Body']))
    prereqs = [
        "<b>Node.js</b> (v18 or later) — check with: node --version",
        "<b>npm</b> — check with: npm --version",
        "<b>Git</b> — check with: git --version",
        "A <b>GitHub account</b> at github.com",
        "A working <b>Vite + React</b> project that runs locally with npm run dev",
        "<b>Homebrew</b> (macOS) — check with: brew --version",
    ]
    for p in prereqs:
        story.append(Paragraph(f"• {p}", styles['BulletItem']))

    story.append(hr())

    # ── Step 1: Configure Vite ─────────────────────────
    story.append(Paragraph("Step 1: Configure Vite for GitHub Pages", styles['H1']))
    story.append(Paragraph("Why This Is Needed", styles['H2']))
    story.append(Paragraph(
        "GitHub Pages serves your app from a subpath (e.g., https://username.github.io/repo-name/), "
        "not from the root (/). By default, Vite assumes your app is served from /, which would "
        "cause all asset paths (CSS, JS, images) to break. Setting the <b>base</b> option fixes this.",
        styles['Body']
    ))
    story.append(spacer(4))
    story.append(Paragraph("What To Do", styles['H2']))
    story.append(Paragraph(
        "Open the file <font face='Courier' color='#d63384'>vite.config.js</font> in your project root and add the <font face='Courier' color='#d63384'>base</font> property:",
        styles['Body']
    ))
    story.append(code_block(
        "import { defineConfig } from 'vite'\n"
        "import react from '@vitejs/plugin-react'\n"
        "\n"
        "export default defineConfig({\n"
        "  plugins: [react()],\n"
        "  base: '/arrear-predictor-app/',\n"
        "})"
    ))
    story.append(make_table(
        ["Property", "Value", "Purpose"],
        [["base", "'/arrear-predictor-app/'", "Must match your GitHub repository name exactly, wrapped in / slashes"]],
        col_widths=[60, 140, 270]
    ))
    story.append(spacer(4))
    story.append(warning_box(
        "The <b>base</b> value MUST match your GitHub repository name. "
        "If your repo is named <font face='Courier'>my-cool-app</font>, then set "
        "<font face='Courier'>base: '/my-cool-app/'</font>."
    ))

    story.append(hr())

    # ── Step 2: GitHub Actions Workflow ─────────────────
    story.append(Paragraph("Step 2: Create GitHub Actions Workflow", styles['H1']))
    story.append(Paragraph("Why This Is Needed", styles['H2']))
    story.append(Paragraph(
        "GitHub Actions is a CI/CD (Continuous Integration / Continuous Deployment) service built into GitHub. "
        "We create a <b>workflow file</b> that tells GitHub to automatically build and deploy your app "
        "whenever you push code to the main branch.", styles['Body']
    ))
    story.append(spacer(4))
    story.append(Paragraph("What To Do", styles['H2']))
    story.append(Paragraph(
        "Create the following directory structure and file in your project:",
        styles['Body']
    ))
    story.append(code_block(
        ".github/\n"
        "  workflows/\n"
        "    deploy.yml"
    ))
    story.append(Paragraph(
        "Create the file <font face='Courier' color='#d63384'>.github/workflows/deploy.yml</font> with this content:",
        styles['Body']
    ))
    story.append(code_block(
        "name: Deploy to GitHub Pages\n"
        "\n"
        "on:\n"
        "  push:\n"
        "    branches: ['main']\n"
        "  workflow_dispatch:\n"
        "\n"
        "permissions:\n"
        "  contents: read\n"
        "  pages: write\n"
        "  id-token: write\n"
        "\n"
        "concurrency:\n"
        "  group: 'pages'\n"
        "  cancel-in-progress: false\n"
        "\n"
        "jobs:\n"
        "  build:\n"
        "    runs-on: ubuntu-latest\n"
        "    steps:\n"
        "      - uses: actions/checkout@v4\n"
        "      - uses: actions/setup-node@v4\n"
        "        with:\n"
        "          node-version: 20\n"
        "          cache: 'npm'\n"
        "      - run: npm ci\n"
        "      - run: npm run build\n"
        "      - uses: actions/configure-pages@v5\n"
        "      - uses: actions/upload-pages-artifact@v3\n"
        "        with:\n"
        "          path: './dist'\n"
        "\n"
        "  deploy:\n"
        "    environment:\n"
        "      name: github-pages\n"
        "    runs-on: ubuntu-latest\n"
        "    needs: build\n"
        "    steps:\n"
        "      - uses: actions/deploy-pages@v4"
    ))
    story.append(spacer(4))
    story.append(Paragraph("Workflow Breakdown", styles['H3']))
    story.append(make_table(
        ["Section", "Purpose"],
        [
            ["on: push: branches: ['main']", "Triggers the workflow on every push to main"],
            ["workflow_dispatch", "Allows manual triggering from GitHub UI"],
            ["permissions", "Grants permission to read code and write to Pages"],
            ["concurrency", "Prevents multiple simultaneous deployments"],
            ["Build Job", "Checks out code, installs Node.js, runs npm ci and npm run build"],
            ["Deploy Job", "Takes the built ./dist folder and deploys to GitHub Pages"],
        ],
        col_widths=[170, 300]
    ))

    story.append(hr())

    # ── Step 3: .gitignore ─────────────────────────────
    story.append(Paragraph("Step 3: Update .gitignore", styles['H1']))
    story.append(Paragraph("Why This Is Needed", styles['H2']))
    story.append(Paragraph(
        "The .gitignore file tells Git which files and folders to exclude from the repository. "
        "We don't want to push unnecessary files like node_modules, build outputs, or local-only files.",
        styles['Body']
    ))
    story.append(spacer(4))
    story.append(Paragraph("Key Exclusions", styles['H3']))
    story.append(make_table(
        ["Excluded", "Reason"],
        [
            ["node_modules", "Dependencies are installed from package.json during build — can be 100s of MBs"],
            ["dist", "Build output is generated by GitHub Actions — we don't commit it"],
            [".DS_Store", "macOS system files that are not needed"],
            ["venv-pdf", "Python virtual environment not needed for the web app"],
        ],
        col_widths=[120, 350]
    ))

    story.append(hr())

    # ── Step 4: Create GitHub Repo ─────────────────────
    story.append(Paragraph("Step 4: Create a GitHub Repository", styles['H1']))
    story.append(Paragraph("What To Do", styles['H2']))
    story.append(Paragraph("1. Go to <b>github.com/new</b> in your browser", styles['Body']))
    story.append(Paragraph("2. Fill in the details:", styles['Body']))
    story.append(Paragraph("• <b>Repository name:</b> arrear-predictor-app (must match the base in vite.config.js)", styles['BulletItem']))
    story.append(Paragraph("• <b>Description:</b> (optional) Arrear Predictor App", styles['BulletItem']))
    story.append(Paragraph("• <b>Visibility:</b> Select <b>Public</b> (required for free GitHub Pages)", styles['BulletItem']))
    story.append(spacer(4))
    story.append(Paragraph("3. <b>DO NOT</b> check any of these boxes:", styles['Body']))
    story.append(Paragraph("• ❌ Add a README file", styles['BulletItem']))
    story.append(Paragraph("• ❌ Add .gitignore", styles['BulletItem']))
    story.append(Paragraph("• ❌ Choose a license", styles['BulletItem']))
    story.append(spacer(4))
    story.append(Paragraph("4. Click <b>Create repository</b>", styles['Body']))
    story.append(spacer(6))
    story.append(note_box(
        "GitHub Pages is free only for <b>public</b> repositories on the free plan. "
        "Private repos require GitHub Pro."
    ))
    story.append(warning_box(
        "Do NOT add a README or .gitignore on GitHub — we already have them locally. "
        "Adding them would create conflicts when pushing."
    ))

    story.append(hr())

    # ── Step 5: GitHub CLI ─────────────────────────────
    story.append(Paragraph("Step 5: Install and Authenticate GitHub CLI", styles['H1']))
    story.append(Paragraph("Why This Is Needed", styles['H2']))
    story.append(Paragraph(
        "To push code from your computer to GitHub, Git needs to authenticate with your GitHub account. "
        "The <b>GitHub CLI (gh)</b> is the easiest way to set this up on macOS.",
        styles['Body']
    ))
    story.append(spacer(6))

    story.append(Paragraph("5a. Install GitHub CLI", styles['H2']))
    story.append(code_block("brew install gh"))

    story.append(Paragraph("5b. Authenticate with GitHub", styles['H2']))
    story.append(code_block("gh auth login"))
    story.append(Paragraph("When prompted, select:", styles['Body']))
    story.append(Paragraph("1. <b>Where do you use GitHub?</b> → GitHub.com", styles['BulletItem']))
    story.append(Paragraph("2. <b>Preferred protocol?</b> → HTTPS", styles['BulletItem']))
    story.append(Paragraph("3. <b>Authenticate Git with credentials?</b> → Yes", styles['BulletItem']))
    story.append(Paragraph("4. <b>How to authenticate?</b> → Login with a web browser", styles['BulletItem']))
    story.append(spacer(4))
    story.append(Paragraph(
        "The CLI will display a <b>one-time code</b>. Press Enter to open your browser, "
        "paste the code, and click Authorize.", styles['Body']
    ))
    story.append(spacer(4))
    story.append(Paragraph("Expected success message:", styles['Body']))
    story.append(code_block(
        "✓ Authentication complete.\n"
        "✓ Configured git protocol\n"
        "✓ Logged in as Gunalakshme"
    ))

    story.append(hr())

    # ── Step 6: Git Init and Push ──────────────────────
    story.append(Paragraph("Step 6: Initialize Git and Push Code", styles['H1']))
    story.append(Paragraph("What To Do", styles['H2']))
    story.append(Paragraph("Run the following commands in your terminal, one by one:", styles['Body']))
    story.append(code_block(
        "# Navigate to your project directory\n"
        "cd /path/to/your/arrear-predictor-app\n"
        "\n"
        "# Initialize a new Git repository\n"
        "git init\n"
        "\n"
        "# Add all files to staging\n"
        "git add .\n"
        "\n"
        "# Create the first commit\n"
        "git commit -m \"Initial commit: Arrear Predictor App\"\n"
        "\n"
        "# Rename the branch to 'main'\n"
        "git branch -M main\n"
        "\n"
        "# Connect local repo to GitHub repo\n"
        "git remote add origin https://github.com/YOUR_USERNAME/arrear-predictor-app.git\n"
        "\n"
        "# Push the code to GitHub\n"
        "git push -u origin main"
    ))
    story.append(spacer(6))
    story.append(Paragraph("Command Breakdown", styles['H3']))
    story.append(make_table(
        ["Command", "What It Does"],
        [
            ["git init", "Creates a .git folder, turning your project into a Git repository"],
            ["git add .", "Stages all files (respecting .gitignore) for the next commit"],
            ["git commit -m \"...\"", "Saves a snapshot of staged files with a descriptive message"],
            ["git branch -M main", "Renames the default branch from master to main"],
            ["git remote add origin <URL>", "Links your local repo to the GitHub repo"],
            ["git push -u origin main", "Uploads code to GitHub; sets main as default push target"],
        ],
        col_widths=[170, 300]
    ))
    story.append(spacer(6))
    story.append(Paragraph("Expected output:", styles['Body']))
    story.append(code_block(
        "To https://github.com/Gunalakshme/arrear-predictor-app.git\n"
        " * [new branch]      main -> main\n"
        "branch 'main' set up to track 'origin/main'."
    ))

    story.append(hr())

    # ── Step 7: Enable GitHub Pages ────────────────────
    story.append(Paragraph("Step 7: Enable GitHub Pages", styles['H1']))

    story.append(Paragraph("Option A: Using GitHub CLI (Faster)", styles['H2']))
    story.append(code_block(
        "gh api repos/YOUR_USERNAME/arrear-predictor-app/pages \\\n"
        "  -X POST -f build_type=workflow"
    ))

    story.append(Paragraph("Option B: Using GitHub Website (Manual)", styles['H2']))
    story.append(Paragraph("1. Go to your repository on GitHub", styles['Body']))
    story.append(Paragraph("2. Click the <b>Settings</b> tab (gear icon)", styles['Body']))
    story.append(Paragraph("3. In the left sidebar, click <b>Pages</b>", styles['Body']))
    story.append(Paragraph("4. Under Build and deployment → Source, select <b>GitHub Actions</b>", styles['Body']))
    story.append(Paragraph("5. Click <b>Save</b>", styles['Body']))

    story.append(hr())

    # ── Step 8: Verify ─────────────────────────────────
    story.append(Paragraph("Step 8: Verify Deployment", styles['H1']))
    story.append(Paragraph("Check Workflow Status", styles['H2']))

    story.append(Paragraph("Using CLI:", styles['H3']))
    story.append(code_block("gh run list --repo YOUR_USERNAME/arrear-predictor-app --limit 3"))

    story.append(Paragraph("Using GitHub Website:", styles['H3']))
    story.append(Paragraph("1. Go to your repo → click the <b>Actions</b> tab", styles['Body']))
    story.append(Paragraph("2. You should see a workflow run named \"Deploy to GitHub Pages\"", styles['Body']))
    story.append(Paragraph("3. Click on it to see the progress", styles['Body']))
    story.append(spacer(6))

    story.append(Paragraph("Expected Results", styles['H3']))
    story.append(code_block(
        "✓ build  (23s) — Installs dependencies and builds the app\n"
        "✓ deploy (20s) — Deploys the built files to GitHub Pages"
    ))

    story.append(spacer(6))
    story.append(Paragraph("Access Your Live App", styles['H2']))
    story.append(Paragraph(
        "Once both jobs show ✓, your app is live at:", styles['Body']
    ))
    story.append(code_block("https://YOUR_USERNAME.github.io/arrear-predictor-app/"))
    story.append(note_box(
        "It may take 1-2 minutes after deployment for the URL to become active for the first time."
    ))

    story.append(hr())

    # ── Step 9: Integrate Firebase Realtime Database ─────
    story.append(Paragraph("Step 9: Integrate Firebase Realtime Database", styles['H1']))
    story.append(Paragraph("Why This Is Needed", styles['H2']))
    story.append(Paragraph(
        "By default, the application stores data locally in the browser's <b>localStorage</b>. "
        "This data is sandboxed per device/browser. To enable cross-device synchronization "
        "(e.g., data entered on a phone appearing on a computer), we migrate the data storage to "
        "<b>Firebase Realtime Database</b>.", styles['Body']
    ))
    story.append(spacer(4))
    story.append(Paragraph("What To Do", styles['H2']))
    story.append(Paragraph("1. Install Firebase SDK in the project root:", styles['Body']))
    story.append(code_block("npm install firebase"))
    story.append(Paragraph(
        "2. Create the configuration module <font face='Courier' color='#d63384'>src/firebase.js</font> with these helper functions:",
        styles['Body']
    ))
    story.append(code_block(
        "import { initializeApp } from 'firebase/app';\n"
        "import { getDatabase, ref, set, get, onValue, remove } from 'firebase/database';\n"
        "\n"
        "const firebaseConfig = {\n"
        "  apiKey: 'YOUR_API_KEY',\n"
        "  authDomain: 'YOUR_PROJECT.firebaseapp.com',\n"
        "  databaseURL: 'https://YOUR_PROJECT-default-rtdb.firebaseio.com',\n"
        "  projectId: 'YOUR_PROJECT',\n"
        "  storageBucket: 'YOUR_PROJECT.firebasestorage.app',\n"
        "  messagingSenderId: 'YOUR_SENDER_ID',\n"
        "  appId: 'YOUR_APP_ID'\n"
        "};\n"
        "\n"
        "const app = initializeApp(firebaseConfig);\n"
        "const db = getDatabase(app);\n"
        "\n"
        "export const dbWrite = async (path, data) => set(ref(db, path), data);\n"
        "export const dbListen = (path, callback, fallback) => {\n"
        "  return onValue(ref(db, path), (snap) => callback(snap.exists() ? snap.val() : fallback));\n"
        "};"
    ))
    story.append(Paragraph(
        "3. Refactor state management in <font face='Courier' color='#d63384'>src/ArrearPredictor.jsx</font>:",
        styles['Body']
    ))
    story.append(Paragraph(
        "• Import <font face='Courier'>dbWrite</font> and <font face='Courier'>dbListen</font> from <font face='Courier'>./firebase</font>.<br/>"
        "• Setup <font face='Courier'>useEffect</font> hooks to listen to database paths (<font face='Courier'>/users</font>, <font face='Courier'>/subjects</font>, <font face='Courier'>/studentDb</font>, <font face='Courier'>/reg</font>) in real-time.<br/>"
        "• Add a loading screen state until the initial connection is established.<br/>"
        "• Setup a debounced write helper to prevent overloading the database during user interactions.",
        styles['BulletItem']
    ))

    story.append(hr())
    story.append(PageBreak())

    # ── Step 10: Set Up Firebase Database ───────────────
    story.append(Paragraph("Step 10: Set Up Firebase Realtime Database", styles['H1']))
    story.append(Paragraph("What To Do in Firebase Console", styles['H2']))
    story.append(Paragraph("1. Create your project:", styles['Body']))
    story.append(Paragraph("• Go to <b>console.firebase.google.com</b> and click <b>Create a project</b>.", styles['BulletItem']))
    story.append(Paragraph("• Name the project <b>arrear-predictor</b>, and click continue.", styles['BulletItem']))
    story.append(Paragraph("• Register a Web App by clicking the <b>Web tag (&lt;/&gt;)</b> on the homepage to generate your <b>firebaseConfig</b> object.", styles['BulletItem']))
    
    story.append(Paragraph("2. Initialize Realtime Database:", styles['Body']))
    story.append(Paragraph("• In the left sidebar, click <b>Build</b> → <b>Realtime Database</b>.", styles['BulletItem']))
    story.append(Paragraph("• Click the <b>Create Database</b> button.", styles['BulletItem']))
    story.append(Paragraph("• <b>Database Options:</b> Choose a region (e.g., United States) and click <b>Next</b>.", styles['BulletItem']))
    story.append(Paragraph("• <b>Security Rules:</b> Select <b>Start in test mode</b> (this allows read/write access for development) and click <b>Enable</b>.", styles['BulletItem']))
    
    story.append(spacer(4))
    story.append(note_box(
        "If you do not see the \"Start in test mode\" options or the \"Enable\" button, "
        "zoom out your browser (using <b>Cmd + -</b> or <b>Ctrl + -</b>) to reveal "
        "the scrollable bottom section of the Firebase setup modal."
    ))

    story.append(Paragraph("3. Link Database to App Config:", styles['Body']))
    story.append(Paragraph(
        "Verify your database URL on the dashboard header (e.g., <font face='Courier'>https://your-project-default-rtdb.firebaseio.com/</font>) "
        "and copy it into your <font face='Courier'>src/firebase.js</font> under the <font face='Courier'>databaseURL</font> field.", styles['Body']
    ))

    story.append(hr())
    story.append(PageBreak())

    # ── Updating Your App ──────────────────────────────
    story.append(Paragraph("Updating Your App", styles['H1']))
    story.append(Paragraph(
        "Whenever you make changes to your app, deploy the update with just 3 commands:",
        styles['Body']
    ))
    story.append(code_block(
        "# Stage all changes\n"
        "git add .\n"
        "\n"
        "# Commit with a descriptive message\n"
        "git commit -m \"Describe what you changed\"\n"
        "\n"
        "# Push to GitHub (auto-deploys in ~1 minute)\n"
        "git push"
    ))
    story.append(Paragraph(
        "The GitHub Actions workflow will automatically rebuild and redeploy your app.",
        styles['Body']
    ))

    story.append(hr())

    # ── Troubleshooting ────────────────────────────────
    story.append(Paragraph("Troubleshooting", styles['H1']))
    story.append(Paragraph("Common Issues and Solutions", styles['H2']))
    story.append(make_table(
        ["Problem", "Solution"],
        [
            ["404 error on the live URL", "Check that base in vite.config.js matches your repo name exactly"],
            ["Blank page loads", "Open browser DevTools (F12) → Console tab. Look for asset loading errors"],
            ["Workflow fails at Install", "Make sure package-lock.json is committed (not in .gitignore)"],
            ["Workflow fails at Build", "Run npm run build locally first to check for build errors"],
            ["Permission denied on push", "Re-run gh auth login to re-authenticate"],
            ["Repository not found on push", "Verify the repo exists and the remote URL is correct"],
        ],
        col_widths=[160, 310]
    ))
    story.append(spacer(10))
    story.append(Paragraph("Useful Commands", styles['H3']))
    story.append(code_block(
        "# Check your Git remote URL\n"
        "git remote -v\n"
        "\n"
        "# Check GitHub authentication status\n"
        "gh auth status\n"
        "\n"
        "# Manually trigger a deployment\n"
        "gh workflow run deploy.yml\n"
        "\n"
        "# View recent workflow runs\n"
        "gh run list --repo YOUR_USERNAME/arrear-predictor-app"
    ))

    story.append(hr())
    story.append(Spacer(1, 20))
    story.append(Paragraph(
        "<i>Guide generated on June 1, 2026</i>", 
        ParagraphStyle('Footer', parent=styles['Body'], alignment=TA_CENTER, textColor=GRAY)
    ))

    # ── Build ──────────────────────────────────────────
    doc.build(story)
    print(f"✅ PDF generated successfully: {OUTPUT_PATH}")

if __name__ == "__main__":
    build_pdf()
