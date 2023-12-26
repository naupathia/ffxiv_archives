"use client";
import { useSearchNavigation } from "./searchNavigationContexts";

export default function SearchNavigationList() {
  const { navItems } = useSearchNavigation();

  return (
    <div className="flex flex-col space-y-1">
      <p className="text-orange-300 text-lg">NAVIGATION</p>
      {navItems.map((item: any) => (
        <a
          key={item.id}
          href={`#${item.id}`}
          className="text-sm hover:text-orange-300"
        >
          {item.name}
        </a>
      ))}
    </div>
  );
}
