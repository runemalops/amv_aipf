import { useEffect, useState } from 'react';
import { Card, CardBody } from '@/components/ui';
import { Badge } from '@/components/ui';
import { Button } from '@/components/ui';
import { Skeleton } from '@/components/ui';
import type { Project } from '@/api/types';

interface ProjectsGridProps {
  initialProjects?: Project[];
  showFilters?: boolean;
  onProjectClick?: (project: Project) => void;
}

export function ProjectsGrid({ 
  initialProjects, 
  showFilters = true,
  onProjectClick 
}: ProjectsGridProps) {
  const [projects, setProjects] = useState<Project[]>(initialProjects || []);
  const [loading, setLoading] = useState(!initialProjects);
  const [error, setError] = useState<string | null>(null);
  const [activeFilter, setActiveFilter] = useState('all');
  const [filters, setFilters] = useState<string[]>(['all']);

  useEffect(() => {
    if (initialProjects) {
      const allTechs = new Set<string>();
      initialProjects.forEach(p => {
        p.technologies.forEach(t => allTechs.add(t.trim()));
      });
      setFilters(['all', ...Array.from(allTechs).sort()]);
      return;
    }

    const fetchProjects = async () => {
      try {
        const response = await fetch('/api/projects');
        if (!response.ok) throw new Error('Failed to fetch projects');
        const data = await response.json();
        setProjects(data);
        
        const allTechs = new Set<string>();
        data.forEach((p: Project) => {
          p.technologies.forEach((t: string) => allTechs.add(t.trim()));
        });
        setFilters(['all', ...Array.from(allTechs).sort()]);
      } catch (err) {
        setError(err instanceof Error ? err.message : 'Unknown error');
      } finally {
        setLoading(false);
      }
    };

    fetchProjects();
  }, [initialProjects]);

  const filteredProjects = activeFilter === 'all'
    ? projects
    : projects.filter(p => 
        p.technologies.some(t => t.toLowerCase().includes(activeFilter.toLowerCase()))
      );

  if (loading) {
    return (
      <div className="projects-grid">
        {[1, 2, 3].map(i => (
          <Card key={i} className="project-card-skeleton">
            <Skeleton height={200} />
            <div className="p-3">
              <Skeleton width="80%" height={24} />
              <Skeleton width="100%" className="mt-2" />
              <Skeleton width="60%" className="mt-2" />
            </div>
          </Card>
        ))}
      </div>
    );
  }

  if (error) {
    return (
      <div className="alert alert-danger" role="alert">
        Error loading projects: {error}
      </div>
    );
  }

  return (
    <div className="projects-section">
      {showFilters && filters.length > 1 && (
        <div className="projects-filters mb-4">
          <div className="filter-buttons">
            {filters.map(filter => (
              <button
                key={filter}
                className={`filter-btn ${activeFilter === filter ? 'active' : ''}`}
                onClick={() => setActiveFilter(filter)}
              >
                {filter === 'all' ? 'All' : filter}
              </button>
            ))}
          </div>
        </div>
      )}

      {filteredProjects.length === 0 ? (
        <div className="text-center py-5">
          <p className="text-muted">No projects found.</p>
        </div>
      ) : (
        <div className="projects-grid">
          {filteredProjects.map(project => (
            <Card key={project.id} hover className="project-card" padding="none">
              {project.image && (
                <div className="project-image-wrapper">
                  <img
                    src={project.image}
                    alt={project.title}
                    className="project-image"
                    loading="lazy"
                  />
                </div>
              )}
              <CardBody className="project-content">
                <h3 className="project-title">{project.title}</h3>
                <p className="project-description">{project.description}</p>
                
                <div className="project-technologies mb-3">
                  {project.technologies.slice(0, 4).map((tech, index) => (
                    <Badge key={index} variant="secondary">{tech}</Badge>
                  ))}
                  {project.technologies.length > 4 && (
                    <Badge variant="light">+{project.technologies.length - 4}</Badge>
                  )}
                </div>

                <div className="project-links">
                  {project.demo && (
                    <Button
                      variant="primary"
                      size="sm"
                      onClick={() => window.open(project.demo!, '_blank')}
                    >
                      Demo
                    </Button>
                  )}
                  {project.git_url && (
                    <Button
                      variant="outline"
                      size="sm"
                      onClick={() => window.open(project.git_url!, '_blank')}
                    >
                      GitHub
                    </Button>
                  )}
                  {onProjectClick && (
                    <Button
                      variant="ghost"
                      size="sm"
                      onClick={() => onProjectClick(project)}
                    >
                      Details
                    </Button>
                  )}
                </div>
              </CardBody>
            </Card>
          ))}
        </div>
      )}
    </div>
  );
}
