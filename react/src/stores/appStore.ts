import { create } from 'zustand';
import { persist } from 'zustand/middleware';

interface AppState {
  language: 'en' | 'es';
  theme: 'light' | 'dark';
  mobileMenuOpen: boolean;
  setLanguage: (lang: 'en' | 'es') => void;
  toggleTheme: () => void;
  toggleMobileMenu: () => void;
  closeMobileMenu: () => void;
}

export const useAppStore = create<AppState>()(
  persist(
    (set) => ({
      language: 'en',
      theme: 'light',
      mobileMenuOpen: false,

      setLanguage: (language) => set({ language }),
      toggleTheme: () => set((state) => ({ 
        theme: state.theme === 'light' ? 'dark' : 'light' 
      })),
      toggleMobileMenu: () => set((state) => ({ 
        mobileMenuOpen: !state.mobileMenuOpen 
      })),
      closeMobileMenu: () => set({ mobileMenuOpen: false }),
    }),
    { name: 'app-storage' }
  )
);
