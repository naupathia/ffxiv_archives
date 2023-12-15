import Image from "next/image";
import Search from "./ui/search";

export default function Home() {
  return (
    <main className="flex min-h-screen flex-col justify-between p-24">
      <div className="relative flex place-items-center before:absolute before:h-[300px] before:w-[480px] before:-translate-x-1/2 before:rounded-full before:bg-gradient-radial before:from-white before:to-transparent before:blur-2xl before:content-[''] after:absolute after:-z-20 after:h-[180px] after:w-[240px] after:translate-x-1/3 after:bg-gradient-conic after:from-sky-200 after:via-blue-200 after:blur-2xl after:content-[''] before:dark:bg-gradient-to-br before:dark:from-transparent before:dark:to-blue-700 before:dark:opacity-10 after:dark:from-sky-900 after:dark:via-[#0141ff] after:dark:opacity-40 before:lg:h-[360px] z-[-1]">
        <div className="w-full">
          <div className="flex w-full items-center justify-between">
            <h1 className={`text-2xl`}>FFXIV Lore</h1>
          </div>
          <div className="mt-4 flex items-center justify-between gap-2 md:mt-8">
            <Search placeholder="Search..." />
          </div>
          {/*  <Suspense key={query + currentPage} fallback={<InvoicesTableSkeleton />}>
        <Table query={query} currentPage={currentPage} />
      </Suspense> */}
          <div className="mt-5 flex w-full justify-center">
            {/* <Pagination totalPages={totalPages} /> */}
          </div>
        </div>
      </div>
    </main>
  );
}
