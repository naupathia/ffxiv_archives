
export default function Layout({ children }: { children: React.ReactNode }) {
  return (
    <div>
      <main className="min-h-screen min-w-full">
        {children}
      </main>
    </div>
  );
}
