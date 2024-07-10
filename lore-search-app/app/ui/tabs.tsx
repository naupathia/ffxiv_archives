import Link from "next/link";
import { useState } from "react";


export default function Tabs(){
    const [currentTab, setCurrentTab] = useState(null)

    return (
        <div>
            
          <div className="tab-header bg-blue-500/10">
            <Link className="tab basis-1" href="" target="none">
              SEARCH
            </Link>
            <Link className="tab basis-1" href="" target="none" onck>
              BOOKMARKS
            </Link>
          </div>
        </div>
    ).
}