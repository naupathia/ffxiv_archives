import React from "react";
import { useDroppable } from "@dnd-kit/core";

export default function Droppable({ children }: { children: React.ReactNode }) {
  const { isOver, setNodeRef } = useDroppable({
    id: "droppable",
  });
  const style = {
    color: isOver ? "blue" : undefined,
  };

  return (
    <div ref={setNodeRef} style={style}>
      {children}
    </div>
  );
}
