import Link from "next/link";

export default function Tabs() {
  // const [currentTab, setCurrentTab] = useState(null)

  return (
    <div>
      <div className="tab-header bg-blue-500/10">
        <Link className="tab basis-1" href="" target="none">
          SEARCH
        </Link>
        <Link className="tab basis-1" href="" target="none">
          BOOKMARKS
        </Link>
      </div>
    </div>
  );
}
