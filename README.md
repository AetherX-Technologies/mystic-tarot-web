# 🔮 Mystic Tarot

**A beautiful web-based tarot reading platform with 78 complete cards and mystical visual effects.**

Experience the ancient wisdom of tarot through a modern, elegant interface. Draw cards, receive readings, and explore the full tarot deck with rich symbolism and detailed interpretations.

---

## ✨ Features

- **🎴 Complete 78-Card Deck**
  - 22 Major Arcana (spiritual life lessons)
  - 56 Minor Arcana (daily life situations)
  - Full upright and reversed meanings

- **🔮 Multiple Reading Spreads**
  - Single Card: Quick daily insight
  - Three Cards: Past-Present-Future reading
  - Six Cards: Comprehensive life guidance

- **🎨 Mystical Visual Experience**
  - Floating card animations with golden aura
  - Smooth page transitions
  - Shimmer effects on interactive elements
  - Responsive design for all devices

- **📖 Rich Card Information**
  - Traditional card meanings
  - Qabalah correspondences
  - Hebrew letter associations (with proper Unicode rendering)
  - Alchemical symbols for the four elements
  - Meditation texts for Major Arcana

- **🌐 Full Deck Library**
  - Browse all 78 cards
  - Detailed card pages with navigation
  - Search and filter capabilities

---

## 🚀 Quick Start

### Prerequisites

- Python 3.10 or higher
- Conda (recommended) or pip

### Installation

1. **Clone the repository**
   ```bash
   git clone <your-repo-url>
   cd python-game-master
   ```

2. **Create and activate conda environment**
   ```bash
   conda create -n tarot python=3.10
   conda activate tarot
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Run the application**
   ```bash
   python run.py
   ```

5. **Open in browser**
   ```
   http://127.0.0.1:5000
   ```

---

## 📂 Project Structure

```
python-game-master/
├── run.py                      # Application entry point
├── config.py                   # Configuration settings
├── requirements.txt            # Python dependencies
│
├── webapp/                     # Main application package
│   ├── __init__.py            # Flask app initialization
│   ├── routes.py              # URL routing and view functions
│   ├── models.py              # Business logic (CardManager, ReadingEngine)
│   │
│   ├── templates/             # Jinja2 HTML templates
│   │   ├── base.html          # Base template with layout
│   │   ├── index.html         # Homepage
│   │   ├── one_card.html      # Single card reading
│   │   ├── three_cards.html   # Three-card spread
│   │   ├── six_cards.html     # Six-card spread
│   │   ├── browse_cards.html  # Card library
│   │   └── card_detail.html   # Individual card details
│   │
│   └── static/                # Static assets
│       ├── css/
│       │   └── style.css      # Custom styles with animations
│       └── images/            # Tarot card images (78 cards)
│
├── data/                      # Card data
│   └── TarotCards_Full.csv   # Complete 78-card dataset
│
├── docs/                      # Project documentation
│   ├── ROADMAP.md            # Development roadmap
│   ├── tasks/                # Task management
│   └── references/           # Technical references
│
└── reference_project/         # Original python-tarot project
```

---

## 🛠️ Technology Stack

### Backend
- **Flask 2.x** - Lightweight web framework
- **Python 3.10+** - Modern Python features
- **Pandas** - CSV data processing
- **Gunicorn** - WSGI HTTP server (production)

### Frontend
- **Bootstrap 5** - Responsive UI framework
- **Jinja2** - Template engine (Flask built-in)
- **Custom CSS** - Mystical animations and effects
- **HTML5** - Semantic markup

### Data
- **CSV** - Card data storage (78 cards × 11 fields)
- **Unicode** - Hebrew letters (U+05D0-05EA) and Alchemical symbols (U+1F700-1F773)

### Deployment
- **Render** - Cloud platform (ready to deploy)
- **Gunicorn** - Production server
- **Environment variables** - Configuration management

---

## 📊 Card Data Structure

Each of the 78 tarot cards includes:

| Field | Description | Example |
|-------|-------------|---------|
| `name` | Card name | "The Magician" |
| `url` | URL-safe identifier | "the_magician" |
| `image` | Image file path | "images/01.jpeg" |
| `desc` | Upright meaning | "The start of something..." |
| `rdesc` | Reversed meaning | "Trickery, sleight of hand..." |
| `message` | Core guidance | "create a new reality" |
| `sequence` | Card number (1-78) | 1 |
| `qabalah` | Kabbalah correspondence | "from Kether to Tiphareth" |
| `hebrew_letter` | Hebrew letter (HTML entity) | "&#1488;" (א) |
| `meditation` | Meditation text | Biblical/philosophical quotes |
| `cardtype` | Card category | major/minor/court/ace |

---

## 🎯 Usage Examples

### Single Card Reading
Perfect for daily guidance or quick questions.
```
GET /one-card
→ Randomly draws 1 card (upright or reversed)
→ Displays interpretation and core message
```

### Three-Card Spread
Classic Past-Present-Future reading.
```
GET /three-cards
→ Draws 3 cards (2 upright, 1 reversed)
→ Position meanings:
  1. The Past - What has led to this moment
  2. The Present - Current situation and energies
  3. The Future - Likely outcome and direction
```

### Six-Card Spread
Comprehensive life reading.
```
GET /six-cards
→ Draws 6 cards (4 upright, 2 reversed)
→ Position meanings:
  1. How you feel about yourself
  2. What you want most right now
  3. Your fears
  4. What is going for you
  5. What is going against you
  6. The likely outcome
```

### Card Library
Browse and study all 78 cards.
```
GET /browse
→ Displays all cards in grid layout

GET /card/<card_url>
→ Shows detailed card information
→ Includes navigation to previous/next card
```

---

## 🔧 Configuration

### Environment Variables

Create a `.env` file (optional):
```bash
FLASK_APP=run.py
FLASK_ENV=development  # or production
SECRET_KEY=your-secret-key-here
DEBUG=True             # False in production
```

### Data File Location

The application expects the card data at:
```
data/TarotCards_Full.csv
```

Ensure this file is present before running the application.

---

## 🎨 Visual Features

### Animations

**Card Levitation**
- 6-second floating cycle
- Gold pulse shadow effect
- Adds mystical atmosphere

**Button Shimmer**
- 3-second gradient sweep
- Gold accent color
- Enhances interactivity

**Page Transitions**
- Layered fade-in animations
- Delayed element appearance
- Smooth user experience

### Responsive Design

- Mobile-first approach
- Breakpoints: 576px, 768px, 992px, 1200px
- Touch-friendly buttons and navigation

---

## 📚 Data Attribution

### Card Interpretations
Written by **Dr. Yoav Ben Dov**
Licensed under Creative Commons BY-NC-SA
Source: [CBD Tarot](http://www.cbdtarot.com)

### Card Images
**Jean-Claude Flornoy's restoration** of the Tarot of Jean Dodal
Used with permission from Roxanne Flornoy
Purchase the full deck: [Tarot History](https://tarot-history.com/)

---

## 🗺️ Roadmap

### ✅ Completed
- [x] Core tarot reading functionality (single/three/six card spreads)
- [x] 78-card complete deck with full data
- [x] Responsive UI with Bootstrap 5
- [x] Mystical visual effects (animations, transitions)
- [x] Card library with detailed pages
- [x] Hebrew letter and alchemical symbol rendering
- [x] Deployment preparation (Render-ready)

### 🚧 In Progress
- [ ] AI-powered card interpretation (using Claude API)
- [ ] User question input for personalized readings
- [ ] Reading history and bookmarking

### 📋 Planned
- [ ] Multi-language support (中文/English)
- [ ] Custom card spreads
- [ ] User accounts and saved readings
- [ ] Social sharing features
- [ ] Mobile app (React Native)

---

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

### Development Workflow

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'feat: Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

### Code Style

- Follow PEP 8 for Python code
- Use 4 spaces for indentation
- Add docstrings to functions and classes
- Write meaningful commit messages (see Git commit history)

---

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

### Third-Party Licenses

- **Card Interpretations**: Creative Commons BY-NC-SA (Dr. Yoav Ben Dov)
- **Card Images**: Used with permission (Roxanne Flornoy)

---

## 🙏 Acknowledgments

- **Original Project**: Based on [python-tarot](https://github.com/user/python-tarot-master) by [original author]
- **Card Wisdom**: Dr. Yoav Ben Dov for the insightful card interpretations
- **Artwork**: Jean-Claude Flornoy for the beautiful Tarot of Jean Dodal restoration
- **Framework**: Flask team for the excellent web framework
- **Design**: Bootstrap team for the responsive CSS framework

---

## 📞 Contact & Support

- **Issues**: Please report bugs or request features via [GitHub Issues](https://github.com/user/repo/issues)
- **Discussions**: Join the conversation in [GitHub Discussions](https://github.com/user/repo/discussions)

---

## 🌟 Star History

If you find this project useful, please consider giving it a ⭐ on GitHub!

---

<div align="center">

**Built with ❤️ and a touch of magic ✨**

*"The cards are a mirror to the soul, reflecting not the future, but the present moment's infinite possibilities."*

</div>
