import { Panel, PanelHeaderTemplateOptions } from "primereact/panel";
import { useState } from "react";
import LoreBody from "./loreBody";
import Link from "next/link";

export default function LoreCard({
  text,
  lore,
  toggleable,
}: {
  text: string;
  lore: LoreEntry;
  toggleable: boolean;
}) {
  const [collapsed, setCollapsed] = useState(false);

  const headerTemplate = function (options: PanelHeaderTemplateOptions) {
    const className = `${options.className} flex align-items-center justify-content-between pt-8 pb-8`;
    const titleClassName = `${options.titleClassName} text-xl`

    return (
      <div className={className}>
        <div className="flex items-baseline gap-2">
          <h1 className={titleClassName}><Link href={`/item/${lore._id}`} target="_blank">{lore.title}</Link></h1>
          <span className="text-sm">{lore.datatype.name.toUpperCase()}</span>
        </div>
        {options.togglerElement}
      </div>
    );
  };

  return (
    <Panel
      headerTemplate={headerTemplate}
      toggleable={toggleable}
      collapsed={collapsed}
      onToggle={(e) => setCollapsed(e.value)}
    >
      <LoreBody text={text} lore={lore} />
    </Panel>
  );
}
