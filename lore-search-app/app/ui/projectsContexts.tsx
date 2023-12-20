"use client";

import {
  Dispatch,
  createContext,
  useContext,
  useReducer,
  useState,
} from "react";

const CurrentProjectContext = createContext({});
const ProjectsContext = createContext<Project[]>([]);
const ProjectsDispatchContext = createContext<Dispatch<any>>(
  (() => undefined) as Dispatch<any>
);

export default function ProjectsProvider({ children }: { children: any }) {
  const [projects, dispatch] = useReducer(projectsReducer, initialProjects);
  const [currentProject, setCurrentProject] = useState(JSON.parse(sessionStorage.selectedProject));
  return (
    <CurrentProjectContext.Provider value={{currentProject, setCurrentProject}}>
      <ProjectsContext.Provider value={projects}>
        <ProjectsDispatchContext.Provider value={dispatch}>
          {children}
        </ProjectsDispatchContext.Provider>
      </ProjectsContext.Provider>
    </CurrentProjectContext.Provider>
  );
}

export function useCurrentProject() {
    return useContext(CurrentProjectContext);
  }
  
export function useProjects() {
  return useContext(ProjectsContext);
}

export function useProjectsDispatch() {
  return useContext(ProjectsDispatchContext);
}

export function projectsReducer(projects: Project[], action: any) {
  switch (action.type) {
    case "add": {
      const results = [
        ...projects,
        {
          id: crypto.randomUUID(),
          name: action.name,
        },
      ];
      sessionStorage.setItem("projects", JSON.stringify(results));
      return results;
    }
    case "delete": {
      const results = projects.filter((t: Project) => t.id !== action.id);
      sessionStorage.setItem("projects", JSON.stringify(results));
      return results;
    }
    default: {
      throw Error("Unknown action: " + action.type);
    }
  }
}

export function containsProject(projects: Project[], name: string) {
  return projects.some((x) => x.name === name);
}

const initialProjects: Project[] = JSON.parse(sessionStorage.projects) ?? [];
