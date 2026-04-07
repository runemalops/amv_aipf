import { create } from 'zustand';
import { persist } from 'zustand/middleware';
import type { Project } from '@/api/types';

interface ProjectsState {
  projects: Project[];
  filteredProjects: Project[];
  filter: string;
  loading: boolean;
  error: string | null;
  setProjects: (projects: Project[]) => void;
  setFilter: (filter: string) => void;
  setLoading: (loading: boolean) => void;
  setError: (error: string | null) => void;
}

export const useProjectsStore = create<ProjectsState>()(
  persist(
    (set, get) => ({
      projects: [],
      filteredProjects: [],
      filter: 'all',
      loading: false,
      error: null,

      setProjects: (projects) => {
        const filter = get().filter;
        set({
          projects,
          filteredProjects: filter === 'all' 
            ? projects 
            : projects.filter(p => p.technologies.some(t => t.toLowerCase().includes(filter.toLowerCase()))),
        });
      },

      setFilter: (filter) => {
        const { projects } = get();
        set({
          filter,
          filteredProjects: filter === 'all'
            ? projects
            : projects.filter(p => 
                p.technologies.some(t => t.toLowerCase().includes(filter.toLowerCase()))
              ),
        });
      },

      setLoading: (loading) => set({ loading }),
      setError: (error) => set({ error }),
    }),
    { name: 'projects-storage' }
  )
);
