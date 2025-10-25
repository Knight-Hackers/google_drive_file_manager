import "./App.css";

function Navbar() {
  return (
    <header className="nav">
      <div className="wrap">
        <a className="brand" href="/">YourBrand</a>
        <nav className="links">
          <a href="#features">Features</a>
          <a href="#showcase">Showcase</a>
          <a href="/login/google" className="btn ghost">Sign in</a>
          <a href="#get-started" className="btn">Get started</a>
        </nav>
      </div>
    </header>
  );
}

function Hero() {
  return (
    <section className="hero">
      <div className="wrap grid">
        <div className="hero-text">
          <h1>Build a clean React homepage fast</h1>
          <p className="muted">
            Vite for instant dev, FastAPI for secure backend. Ship a modern UI with
            simple components and no heavy dependencies.
          </p>
          <div className="actions">
            <a className="btn" href="#get-started">Get started</a>
            <a className="btn ghost" href="/login/google">Sign in with Google</a>
          </div>
          <p className="note">Cookie sessions. No tokens stored in the browser.</p>
        </div>
        <div className="hero-art">
          <div className="device">
            <div className="bar" />
            <div className="screen">
              <div className="dots" />
              <div className="lines">
                <span /><span /><span /><span />
              </div>
            </div>
          </div>
        </div>
      </div>
    </section>
  );
}

function Features() {
  const items = [
    { title: "Secure auth", desc: "Google OAuth handled on the backend with cookies." },
    { title: "Fast dev", desc: "Vite HMR and a small, friendly codebase." },
    { title: "Clean design", desc: "Responsive layout, sharp typography, accessible UI." },
    { title: "Easy data", desc: "Call /api routes with credentials included." },
    { title: "Production ready", desc: "Static build served by FastAPI." },
    { title: "Composable", desc: "Add sections without changing the core styles." },
  ];
  return (
    <section id="features" className="features">
      <div className="wrap">
        <h2>Why this starter</h2>
        <div className="cards">
          {items.map((it) => (
            <article key={it.title} className="card">
              <h3>{it.title}</h3>
              <p className="muted">{it.desc}</p>
            </article>
          ))}
        </div>
      </div>
    </section>
  );
}

function Showcase() {
  return (
    <section id="showcase" className="showcase">
      <div className="wrap grid">
        <div>
          <h2>Show your product</h2>
          <p className="muted">
            Drop a screenshot, animation, or a quick demo here. The panel on the right
            is a flexible placeholder styled to look like a window.
          </p>
          <ul className="bullets">
            <li>Instant page load</li>
            <li>Responsive by default</li>
            <li>Minimal CSS with utility classes</li>
          </ul>
        </div>
        <div className="panel">
          <div className="panel-head">
            <span className="dot" />
            <span className="dot" />
            <span className="dot" />
          </div>
          <div className="panel-body">
            <div className="skeleton" />
          </div>
        </div>
      </div>
    </section>
  );
}

function CTA() {
  return (
    <section id="get-started" className="cta">
      <div className="wrap center">
        <h2>Ready to launch</h2>
        <p className="muted">
          Connect your API routes and deploy. Replace copy and colors to match your brand.
        </p>
        <div className="actions">
          <a className="btn" href="/login/google">Sign in</a>
          <a className="btn ghost" href="#features">See features</a>
        </div>
      </div>
    </section>
  );
}

function Footer() {
  return (
    <footer className="footer">
      <div className="wrap foot">
        <p>© {new Date().getFullYear()} YourBrand</p>
        <nav className="foot-links">
          <a href="#">Privacy</a>
          <a href="#">Terms</a>
          <a href="#">Contact</a>
        </nav>
      </div>
    </footer>
  );
}

export default function App() {
  return (
    <div className="page">
      <Navbar />
      <main>
        <Hero />
        <Features />
        <Showcase />
        <CTA />
      </main>
      <Footer />
    </div>
  );
}
