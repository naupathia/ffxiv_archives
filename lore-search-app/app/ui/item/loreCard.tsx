"use client";

import { Panel, PanelHeaderTemplateOptions } from "primereact/panel";
import { useState } from "react";
import LoreBody from "./loreBody";
import { convertToTitleCase } from "@/app/lib/functions";
import { ToggleButton } from "primereact/togglebutton";

export default function LoreCard({
  lore,
  toggleable,
}: {
  lore: LoreEntry;
  toggleable: boolean;
}) {
  const [collapsed, setCollapsed] = useState(false);
  const headerText = lore.title
    ? lore.title
    : convertToTitleCase(lore.datatype.name);
  const typeText = lore.title ? lore.datatype.name.toUpperCase() : "";
  const [showJP, setShowJP] = useState(false);

  const hasJpText = lore.text_jp != null && lore.text_jp != '';

  const headerTemplate = function (options: PanelHeaderTemplateOptions) {
    const className = `${options.className} flex align-items-center gap-2 lg:pt-6 lg:pb-6`;
    const titleClassName = `text-lg lg:text-2xl`;

    return (
      <div className={className}>
        <div className="flex flex-col md:flex-row md:flex-1 items-baseline md:gap-2 grow">
          <h1 className={titleClassName}>
            {toggleable ? (
              <a
                className="p-panel-header-link"
                href={`/item/${lore._id}`}
                target="_blank"
              >
                {headerText}
              </a>
            ) : (
              <>{headerText}</>
            )}
          </h1>
          <span className="text-xs md:text-sm">{typeText}</span>
        </div>
        <ToggleButton
          onLabel="JP"
          offLabel="EN"
          checked={showJP}
          onChange={(e) => setShowJP(!showJP)}
          disabled={!hasJpText}
          className="text-xs p-1"
        />
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
      <LoreBody lore={lore} showJP={showJP} />
    </Panel>
  );
}
