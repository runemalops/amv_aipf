interface NavbarProps {
  brand?: string;
  links?: Array<{ label: string; href: string }>;
  currentPath?: string;
  language?: 'en' | 'es';
  onLanguageChange?: (lang: 'en' | 'es') => void;
  onMenuToggle?: () => void;
  menuOpen?: boolean;
}

export function Navbar({
  brand = 'Portfolio',
  links = [],
  currentPath = '/',
  language = 'en',
  onLanguageChange,
  onMenuToggle,
  menuOpen = false,
}: NavbarProps) {
  return (
    <nav className="navbar navbar-expand-lg navbar-light bg-light">
      <div className="container">
        <a className="navbar-brand" href="/">
          {brand}
        </a>
        
        <button
          className="navbar-toggler"
          type="button"
          onClick={onMenuToggle}
          aria-expanded={menuOpen}
          aria-label="Toggle navigation"
        >
          <span className="navbar-toggler-icon" />
        </button>

        <div className={`collapse navbar-collapse ${menuOpen ? 'show' : ''}`}>
          <ul className="navbar-nav ms-auto">
            {links.map((link) => (
              <li key={link.href} className="nav-item">
                <a
                  className={`nav-link ${currentPath === link.href ? 'active' : ''}`}
                  href={link.href}
                >
                  {link.label}
                </a>
              </li>
            ))}
          </ul>

          {onLanguageChange && (
            <div className="navbar-language ms-3">
              <select
                className="form-select form-select-sm"
                value={language}
                onChange={(e) => onLanguageChange(e.target.value as 'en' | 'es')}
                aria-label="Select language"
              >
                <option value="en">EN</option>
                <option value="es">ES</option>
              </select>
            </div>
          )}
        </div>
      </div>
    </nav>
  );
}
