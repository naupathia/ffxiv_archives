"use client";

import { PrimeReactProvider } from 'primereact/api';

export default function PrimeReactProviders({ children }: { children: React.ReactNode }) {
    return (
        <PrimeReactProvider>
            {children}
        </PrimeReactProvider>
    );
}