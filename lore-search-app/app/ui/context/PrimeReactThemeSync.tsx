"use client"
import { useEffect, useContext } from "react";
import { useTheme } from "next-themes";
import { PrimeReactContext } from "primereact/api";

// Separate component to access PrimeReactContext **inside** PrimeReactProvider
export default function ThemeSync({ children }: { children: React.ReactNode }) {
    const { theme } = useTheme(); // Get theme from next-themes
    const { changeTheme } = useContext(PrimeReactContext);


    useEffect(() => {
        if (!theme || !changeTheme) return; // Avoid SSR issues

        const linkId = "theme-link";
        const newTheme = theme === "dark" ? "lara-dark-blue" : "lara-light-blue";
        const currentTheme = newTheme === "lara-dark-blue" ? "lara-light-blue" : "lara-dark-blue";
        console.log("🚀 ~ useEffect ~ newTheme:", newTheme)

        changeTheme(currentTheme, newTheme, linkId, () => {
            const existingLinks = document.querySelectorAll(`link[id="${linkId}"]`);
            if (existingLinks.length > 1) {
                document.head.removeChild(existingLinks[0]); // Remove old theme link
            }
        });
    }, [theme, changeTheme]);


    return <>{children}</>;
}
