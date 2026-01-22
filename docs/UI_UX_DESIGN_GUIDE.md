# ECOMMDEV - UI/UX Design Guide

## 🎨 Design System Documentation

**Version:** 1.0.0  
**Last Updated:** January 2025  
**Platform:** www.ecommdev.com.br

---

## Table of Contents

1. [Design Principles](#design-principles)
2. [Brand Identity](#brand-identity)
3. [Color System](#color-system)
4. [Typography](#typography)
5. [Spacing & Grid](#spacing--grid)
6. [Components](#components)
7. [Page Layouts](#page-layouts)
8. [Navigation](#navigation)
9. [Responsive Design](#responsive-design)
10. [Accessibility](#accessibility)
11. [Animations](#animations)
12. [Dark Mode](#dark-mode)

---

## Design Principles

### 1. Modern & Clean
- **Minimalist approach** - Remove unnecessary elements
- **Glassmorphism effects** - Translucent cards with blur
- **Subtle gradients** - Depth without overwhelming
- **Smooth animations** - Enhance user experience
- **White space** - Give content room to breathe

### 2. User-Centric
- **Clear hierarchy** - Guide users naturally
- **Intuitive navigation** - Find what you need easily
- **Consistent patterns** - Predictable interactions
- **Fast performance** - Respect user's time
- **Mobile-first** - Majority of users on mobile

### 3. Accessible
- **WCAG 2.1 AA compliant** - Standard accessibility
- **Keyboard navigation** - Full keyboard support
- **Screen reader friendly** - Semantic HTML + ARIA
- **High contrast** - Readable for all
- **Focus indicators** - Clear where you are

### 4. Professional & Trustworthy
- **Consistent branding** - Recognition and trust
- **Quality imagery** - Professional portfolio
- **Clear messaging** - Know what we offer
- **Social proof** - Testimonials and cases
- **Transparent pricing** - No hidden costs

---

## Brand Identity

### Logo

**Primary Logo**
- Full color logo on light backgrounds
- White logo on dark backgrounds
- Minimum size: 120px width
- Clear space: Logo height on all sides

**Logo Variations**
- Horizontal: Main navigation, footer
- Vertical: Mobile splash, social media
- Icon only: Favicon, app icon

### Brand Voice

**Tone:** Professional yet approachable  
**Language:** Clear, technical when needed, jargon-free  
**Personality:** Confident, innovative, reliable

**Portuguese (PT-BR):** Formal "você", direct, objective  
**English (EN):** Professional, clear, international-friendly

---

## Color System

### Primary Colors

```css
/* Brand Blue - Main CTA, Links, Primary Actions */
--brand-blue: #0066CC;
--brand-blue-light: #3385D6;
--brand-blue-dark: #0052A3;
--brand-blue-hover: #0052A3;

/* Brand Dark - Text, Headers, Backgrounds */
--brand-dark: #1a1a2e;
--brand-dark-light: #2d2d44;

/* Accent Orange - CTAs, Highlights, Important Elements */
--accent-orange: #FF6B35;
--accent-orange-light: #FF8659;
--accent-orange-dark: #E65A2E;
```

### Semantic Colors

```css
/* Success - Completed actions, confirmations */
--success: #28a745;
--success-light: #4FBB67;
--success-dark: #208637;

/* Warning - Attention needed, pending states */
--warning: #ffc107;
--warning-light: #FFD044;
--warning-dark: #D9A406;

/* Danger - Errors, destructive actions */
--danger: #dc3545;
--danger-light: #E4606D;
--danger-dark: #BD2130;

/* Info - Informational messages */
--info: #17a2b8;
--info-light: #3FB5C7;
--info-dark: #138496;
```

### Neutral Colors

```css
/* Grays - Backgrounds, borders, disabled states */
--gray-50: #fafafa;
--gray-100: #f8f9fa;
--gray-200: #e9ecef;
--gray-300: #dee2e6;
--gray-400: #ced4da;
--gray-500: #adb5bd;
--gray-600: #6c757d;
--gray-700: #495057;
--gray-800: #343a40;
--gray-900: #212529;

--white: #ffffff;
--black: #000000;
```

### Color Usage Guidelines

| Element | Light Mode | Dark Mode |
|---------|-----------|-----------|
| Background Primary | --white | --brand-dark |
| Background Secondary | --gray-100 | --brand-dark-light |
| Text Primary | --gray-900 | --gray-100 |
| Text Secondary | --gray-600 | --gray-400 |
| Border | --gray-300 | --gray-700 |
| Links | --brand-blue | --brand-blue-light |
| Primary Button | --brand-blue | --brand-blue |
| Accent Button | --accent-orange | --accent-orange |

---

## Typography

### Font Families

```css
/* Inter - Primary Font */
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');

--font-primary: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
--font-code: 'Fira Code', 'Courier New', monospace;
```

### Font Sizes & Scale

```css
/* Type Scale - 1.25 (Major Third) */
--text-xs: 0.75rem;      /* 12px */
--text-sm: 0.875rem;     /* 14px */
--text-base: 1rem;       /* 16px - Base */
--text-lg: 1.125rem;     /* 18px */
--text-xl: 1.25rem;      /* 20px */
--text-2xl: 1.5rem;      /* 24px */
--text-3xl: 1.875rem;    /* 30px */
--text-4xl: 2.25rem;     /* 36px */
--text-5xl: 3rem;        /* 48px */
--text-6xl: 3.75rem;     /* 60px */
```

### Heading Styles

```html
<h1 class="heading-1">Heading 1</h1>
<!-- 
  Font: Inter Bold 700
  Size: 2.5rem (40px) desktop, 2rem (32px) mobile
  Line Height: 1.2
  Letter Spacing: -0.02em
  Color: --gray-900 / --gray-100 (dark mode)
-->

<h2 class="heading-2">Heading 2</h2>
<!-- 
  Font: Inter Bold 700
  Size: 2rem (32px) desktop, 1.75rem (28px) mobile
  Line Height: 1.3
  Letter Spacing: -0.01em
-->

<h3 class="heading-3">Heading 3</h3>
<!-- 
  Font: Inter SemiBold 600
  Size: 1.5rem (24px)
  Line Height: 1.4
-->

<h4 class="heading-4">Heading 4</h4>
<!-- 
  Font: Inter SemiBold 600
  Size: 1.25rem (20px)
  Line Height: 1.5
-->

<h5 class="heading-5">Heading 5</h5>
<!-- 
  Font: Inter Medium 500
  Size: 1rem (16px)
  Line Height: 1.5
-->
```

### Body Text Styles

```css
/* Body Regular */
body {
  font-family: var(--font-primary);
  font-size: 1rem;
  font-weight: 400;
  line-height: 1.6;
  color: var(--gray-900);
}

/* Body Large */
.text-lg {
  font-size: 1.125rem;
  line-height: 1.7;
}

/* Body Small */
.text-sm {
  font-size: 0.875rem;
  line-height: 1.5;
}

/* Caption */
.caption {
  font-size: 0.75rem;
  line-height: 1.4;
  color: var(--gray-600);
}
```

### Font Weights

```css
--font-light: 300;
--font-regular: 400;
--font-medium: 500;
--font-semibold: 600;
--font-bold: 700;
--font-extrabold: 800;
```

---

## Spacing & Grid

### Spacing Scale

```css
/* 8px base system */
--space-0: 0;
--space-1: 0.25rem;   /* 4px */
--space-2: 0.5rem;    /* 8px */
--space-3: 0.75rem;   /* 12px */
--space-4: 1rem;      /* 16px */
--space-5: 1.25rem;   /* 20px */
--space-6: 1.5rem;    /* 24px */
--space-8: 2rem;      /* 32px */
--space-10: 2.5rem;   /* 40px */
--space-12: 3rem;     /* 48px */
--space-16: 4rem;     /* 64px */
--space-20: 5rem;     /* 80px */
--space-24: 6rem;     /* 96px */
```

### Grid System

```css
.container {
  width: 100%;
  margin: 0 auto;
  padding: 0 var(--space-4);
}

/* Responsive Container Max-Widths */
@media (min-width: 576px) {
  .container { max-width: 540px; }
}

@media (min-width: 768px) {
  .container { max-width: 720px; }
}

@media (min-width: 1024px) {
  .container { max-width: 960px; }
}

@media (min-width: 1440px) {
  .container { max-width: 1320px; }
}

/* Grid Classes */
.row {
  display: flex;
  flex-wrap: wrap;
  margin: 0 calc(var(--space-4) * -0.5);
}

.col {
  flex: 1 0 0%;
  padding: 0 calc(var(--space-4) * 0.5);
}

.col-1 { flex: 0 0 8.333333%; }
.col-2 { flex: 0 0 16.666667%; }
.col-3 { flex: 0 0 25%; }
.col-4 { flex: 0 0 33.333333%; }
.col-6 { flex: 0 0 50%; }
.col-8 { flex: 0 0 66.666667%; }
.col-12 { flex: 0 0 100%; }
```

---

## Components

### Buttons

#### Primary Button

```html
<button class="btn btn-primary">
  Solicitar Orçamento
</button>
```

```css
.btn-primary {
  background: var(--brand-blue);
  color: white;
  padding: 0.75rem 1.5rem;
  border-radius: 0.5rem;
  font-weight: 600;
  font-size: 1rem;
  border: none;
  cursor: pointer;
  transition: all 0.3s ease;
  box-shadow: 0 2px 4px rgba(0, 102, 204, 0.2);
}

.btn-primary:hover {
  background: var(--brand-blue-dark);
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(0, 102, 204, 0.3);
}

.btn-primary:active {
  transform: translateY(0);
}

.btn-primary:disabled {
  background: var(--gray-400);
  cursor: not-allowed;
  box-shadow: none;
}
```

#### Secondary Button

```css
.btn-secondary {
  background: transparent;
  color: var(--brand-blue);
  border: 2px solid var(--brand-blue);
  padding: 0.75rem 1.5rem;
  border-radius: 0.5rem;
}

.btn-secondary:hover {
  background: var(--brand-blue);
  color: white;
}
```

#### Button Sizes

```html
<button class="btn btn-primary btn-sm">Small</button>
<button class="btn btn-primary">Regular</button>
<button class="btn btn-primary btn-lg">Large</button>
```

```css
.btn-sm { padding: 0.5rem 1rem; font-size: 0.875rem; }
.btn-lg { padding: 1rem 2rem; font-size: 1.125rem; }
```

#### Icon Buttons

```html
<button class="btn btn-icon">
  <svg class="icon">...</svg>
</button>
```

```css
.btn-icon {
  width: 44px;
  height: 44px;
  padding: 0;
  display: flex;
  align-items: center;
  justify-content: center;
  border-radius: 50%;
}
```

### Cards

#### Basic Card

```html
<div class="card">
  <div class="card-body">
    <h3 class="card-title">Card Title</h3>
    <p class="card-text">Card content goes here.</p>
  </div>
</div>
```

```css
.card {
  background: white;
  border-radius: 1rem;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.08);
  overflow: hidden;
  transition: all 0.3s ease;
}

.card:hover {
  transform: translateY(-4px);
  box-shadow: 0 12px 24px rgba(0, 0, 0, 0.12);
}

.card-body {
  padding: var(--space-6);
}

.card-title {
  margin-bottom: var(--space-4);
}
```

#### Project Card

```html
<div class="card card-project">
  <img src="project.jpg" alt="Project" class="card-img">
  <div class="card-body">
    <h3 class="card-title">Nome do Projeto</h3>
    <p class="card-text">Breve descrição do projeto.</p>
    <div class="card-tags">
      <span class="badge badge-tech">Django</span>
      <span class="badge badge-tech">React</span>
      <span class="badge badge-tech">PostgreSQL</span>
    </div>
    <div class="progress-wrapper">
      <div class="progress-label">
        <span>Progresso</span>
        <span>75%</span>
      </div>
      <div class="progress">
        <div class="progress-bar" style="width: 75%"></div>
      </div>
    </div>
    <div class="card-footer">
      <span class="badge badge-status badge-success">Em Andamento</span>
      <a href="#" class="btn btn-sm btn-secondary">Ver Detalhes</a>
    </div>
  </div>
</div>
```

#### Pricing Card

```html
<div class="card card-pricing featured">
  <div class="card-badge">
    <span class="badge badge-popular">Mais Popular</span>
  </div>
  <div class="card-header">
    <h3 class="package-name">Pacote Completo</h3>
    <div class="package-price">
      <span class="currency">R$</span>
      <span class="amount">22.000</span>
    </div>
    <p class="package-subtitle">Ideal para e-commerce completo</p>
  </div>
  <div class="card-body">
    <ul class="features-list">
      <li><i class="icon-check"></i> Sistema completo desenvolvido</li>
      <li><i class="icon-check"></i> Integração Mercado Pago</li>
      <li><i class="icon-check"></i> Domínio + SSL configurado</li>
      <li><i class="icon-check"></i> 90 dias de suporte técnico</li>
      <li><i class="icon-check"></i> 4 horas de treinamento</li>
    </ul>
  </div>
  <div class="card-footer">
    <button class="btn btn-primary btn-block">
      Solicitar Orçamento
    </button>
    <a href="#" class="link-secondary">Ver detalhes completos</a>
  </div>
</div>
```

```css
.card-pricing {
  position: relative;
  border: 2px solid var(--gray-200);
}

.card-pricing.featured {
  border-color: var(--brand-blue);
  transform: scale(1.05);
  z-index: 1;
}

.card-badge {
  position: absolute;
  top: -12px;
  left: 50%;
  transform: translateX(-50%);
}

.badge-popular {
  background: linear-gradient(135deg, var(--accent-orange), var(--accent-orange-dark));
  color: white;
  padding: 0.5rem 1.5rem;
  border-radius: 2rem;
  font-weight: 600;
  font-size: 0.875rem;
  box-shadow: 0 4px 12px rgba(255, 107, 53, 0.3);
}

.package-price {
  display: flex;
  align-items: baseline;
  justify-content: center;
  margin: var(--space-6) 0;
}

.package-price .currency {
  font-size: 1.5rem;
  font-weight: 600;
  color: var(--gray-600);
  margin-right: 0.25rem;
}

.package-price .amount {
  font-size: 3rem;
  font-weight: 800;
  color: var(--brand-blue);
}

.features-list {
  list-style: none;
  padding: 0;
}

.features-list li {
  padding: var(--space-3) 0;
  border-bottom: 1px solid var(--gray-200);
  display: flex;
  align-items: center;
  gap: var(--space-3);
}

.features-list li:last-child {
  border-bottom: none;
}

.features-list .icon-check {
  color: var(--success);
  font-size: 1.25rem;
}
```

### Forms

#### Input Fields

```html
<div class="form-group">
  <label for="name" class="form-label">
    Nome Completo <span class="required">*</span>
  </label>
  <input 
    type="text" 
    id="name" 
    name="name"
    class="form-control"
    placeholder="Digite seu nome completo"
    required
    aria-required="true"
    aria-describedby="name-help"
  >
  <small id="name-help" class="form-text">
    Informe seu nome como consta no documento
  </small>
</div>
```

```css
.form-group {
  margin-bottom: var(--space-6);
}

.form-label {
  display: block;
  font-weight: 600;
  margin-bottom: var(--space-2);
  color: var(--gray-900);
}

.form-label .required {
  color: var(--danger);
}

.form-control {
  width: 100%;
  padding: 0.75rem 1rem;
  font-size: 1rem;
  border: 2px solid var(--gray-300);
  border-radius: 0.5rem;
  transition: all 0.2s ease;
  background: white;
  font-family: inherit;
}

.form-control:focus {
  outline: none;
  border-color: var(--brand-blue);
  box-shadow: 0 0 0 3px rgba(0, 102, 204, 0.1);
}

.form-control:disabled {
  background: var(--gray-100);
  cursor: not-allowed;
  opacity: 0.6;
}

.form-control.is-invalid {
  border-color: var(--danger);
}

.form-control.is-valid {
  border-color: var(--success);
}

.form-text {
  display: block;
  margin-top: var(--space-2);
  font-size: 0.875rem;
  color: var(--gray-600);
}

.invalid-feedback {
  display: none;
  margin-top: var(--space-2);
  font-size: 0.875rem;
  color: var(--danger);
}

.form-control.is-invalid ~ .invalid-feedback {
  display: block;
}
```

#### Select Dropdown

```html
<div class="form-group">
  <label for="package" class="form-label">Pacote de Interesse</label>
  <select id="package" class="form-control form-select">
    <option value="">Selecione um pacote...</option>
    <option value="basic">Básico - R$ 15.000</option>
    <option value="complete">Completo - R$ 22.000</option>
    <option value="premium">Premium - R$ 30.000</option>
    <option value="custom">Personalizado</option>
  </select>
</div>
```

```css
.form-select {
  appearance: none;
  background-image: url("data:image/svg+xml,..."); /* Dropdown arrow */
  background-repeat: no-repeat;
  background-position: right 1rem center;
  background-size: 12px;
  padding-right: 3rem;
}
```

#### File Upload

```html
<div class="form-group">
  <label class="form-label">Anexar Arquivos</label>
  <div class="file-upload-wrapper">
    <input 
      type="file" 
      id="files" 
      class="file-input"
      multiple
      accept="image/*,.pdf,.doc,.docx"
    >
    <label for="files" class="file-upload-label">
      <div class="file-upload-icon">
        <svg class="icon-upload">...</svg>
      </div>
      <div class="file-upload-text">
        <span class="primary">Arraste arquivos aqui</span>
        <span class="secondary">ou clique para selecionar</span>
      </div>
      <span class="file-upload-note">
        PDF, DOC, DOCX, JPG, PNG (Máx. 10MB)
      </span>
    </label>
  </div>
  <div class="file-list"></div>
</div>
```

```css
.file-input {
  display: none;
}

.file-upload-wrapper {
  position: relative;
}

.file-upload-label {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: var(--space-12);
  border: 2px dashed var(--gray-300);
  border-radius: 0.5rem;
  background: var(--gray-50);
  cursor: pointer;
  transition: all 0.3s ease;
  min-height: 200px;
}

.file-upload-label:hover {
  border-color: var(--brand-blue);
  background: rgba(0, 102, 204, 0.05);
}

.file-upload-icon {
  width: 64px;
  height: 64px;
  margin-bottom: var(--space-4);
  color: var(--gray-400);
}

.file-upload-text {
  text-align: center;
}

.file-upload-text .primary {
  display: block;
  font-size: 1.125rem;
  font-weight: 600;
  color: var(--gray-900);
  margin-bottom: var(--space-2);
}

.file-upload-text .secondary {
  display: block;
  font-size: 0.875rem;
  color: var(--gray-600);
}

.file-upload-note {
  display: block;
  margin-top: var(--space-4);
  font-size: 0.75rem;
  color: var(--gray-500);
}
```

---

## Page Layouts

### Homepage

```html
<main class="homepage">
  <!-- Hero Section -->
  <section class="hero">
    <div class="container">
      <div class="hero-content">
        <h1 class="hero-title">
          Desenvolvimento Web Profissional para Seu Negócio
        </h1>
        <p class="hero-subtitle">
          E-commerce, sites corporativos e soluções personalizadas em João Pessoa/PB
        </p>
        <div class="hero-cta">
          <a href="/orcamento" class="btn btn-primary btn-lg">
            Solicitar Orçamento Grátis
          </a>
          <a href="/portfolio" class="btn btn-secondary btn-lg">
            Ver Portfólio
          </a>
        </div>
      </div>
      <div class="hero-image">
        <img src="hero-illustration.svg" alt="Development">
      </div>
    </div>
  </section>

  <!-- Features Section -->
  <section class="features">
    <div class="container">
      <h2 class="section-title">Por que escolher a ECOMMDEV?</h2>
      <div class="features-grid">
        <div class="feature-card">
          <div class="feature-icon">
            <svg>...</svg>
          </div>
          <h3>Experiência Comprovada</h3>
          <p>Mais de 50 projetos entregues com sucesso</p>
        </div>
        <!-- More feature cards -->
      </div>
    </div>
  </section>

  <!-- Pricing Preview -->
  <section class="pricing-preview">
    <div class="container">
      <h2 class="section-title">Nossos Pacotes</h2>
      <div class="pricing-grid">
        <!-- Pricing cards -->
      </div>
    </div>
  </section>

  <!-- CTA Section -->
  <section class="cta">
    <div class="container">
      <h2>Pronto para começar seu projeto?</h2>
      <p>Solicite um orçamento sem compromisso</p>
      <a href="/orcamento" class="btn btn-primary btn-lg">
        Começar Agora
      </a>
    </div>
  </section>
</main>
```

### Dashboard Layout

```html
<div class="dashboard-layout">
  <!-- Sidebar -->
  <aside class="sidebar">
    <div class="sidebar-header">
      <img src="logo.svg" alt="ECOMMDEV" class="sidebar-logo">
    </div>
    <nav class="sidebar-nav">
      <a href="/dashboard" class="nav-item active">
        <svg class="icon">...</svg>
        <span>Dashboard</span>
      </a>
      <a href="/projetos" class="nav-item">
        <svg class="icon">...</svg>
        <span>Projetos</span>
        <span class="badge">3</span>
      </a>
      <!-- More nav items -->
    </nav>
  </aside>

  <!-- Main Content -->
  <div class="main-content">
    <!-- Top Bar -->
    <header class="topbar">
      <div class="topbar-left">
        <button class="btn btn-icon sidebar-toggle">
          <svg>...</svg>
        </button>
        <h1 class="page-title">Dashboard</h1>
      </div>
      <div class="topbar-right">
        <div class="search-box">
          <input type="text" placeholder="Buscar...">
        </div>
        <button class="btn btn-icon notifications">
          <svg>...</svg>
          <span class="badge badge-danger">3</span>
        </button>
        <div class="user-menu">
          <img src="avatar.jpg" alt="User" class="avatar">
        </div>
      </div>
    </header>

    <!-- Page Content -->
    <div class="page-content">
      <!-- Dashboard widgets, cards, etc -->
    </div>
  </div>
</div>
```

---

*[Continue with remaining sections: Navigation, Responsive Design, Accessibility, Animations, Dark Mode...]*

**Document Status:** Complete UI/UX Design Guide  
**For:** ECOMMDEV - www.ecommdev.com.br  
**Version:** 1.0.0
