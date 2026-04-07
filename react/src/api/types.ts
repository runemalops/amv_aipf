export interface Project {
  id: number;
  title: string;
  description: string;
  technologies: string[];
  link: string | null;
  demo: string | null;
  git_url: string | null;
  featured: boolean;
  image?: string;
}

export interface BlogPost {
  id: number;
  title: string;
  excerpt: string;
  content: string;
  image: string | null;
  date: string;
  author: string;
  category: string | null;
}

export interface Experience {
  title: string;
  company: string;
  period: string;
  location: string;
  responsibilities: string[];
  technologies: string[];
}

export interface Education {
  degree: string;
  school: string;
  year: string;
}

export interface Skill {
  name: string;
  icon: string;
  category?: string;
}

export interface Interest {
  name: string;
}

export interface SocialLink {
  platform: string;
  url: string;
  icon: string;
}

export interface ContactFormData {
  name: string;
  email: string;
  subject: string;
  message: string;
}

export interface SiteConfig {
  site_title: string;
  site_subtitle: string;
  hero_title: string;
  hero_cta_text: string;
  hero_cta_link: string;
  hero_cta_secondary_text: string;
  hero_cta_secondary_link: string;
}
